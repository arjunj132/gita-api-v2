from flask import Flask,jsonify,render_template
import requests
import os
import random, datetime
from flask_cors import CORS
import pprint
import google.generativeai as palm

app = Flask(__name__)
CORS(app)

def getshlokaforday():
    x = datetime.datetime.today().strftime("%Y:%m:%d")
    random.seed(x)
    shlokas = [
        "0",
        "47",
        "72",
        "43",
        "42",
        "29",
        "47",
        "30",
        "28",
        "34",
        "42",
        "55",
        "20",
        "35",
        "27",
        "20",
        "24",
        "28",
        "78",
    ]
    r_int = random.randint(1, 18)
    r1_int = random.randint(1, int(shlokas[r_int]))
    return [r_int, r1_int]


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/tests/search-basic/<q>")
def aipalm(q):
    palm.configure(api_key=os.environ["PALM_API"])
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)
    prompt = f"""
A user is searching this up:

{q}

Give a overview of this. No not provide information on any sensitive or dangerous content.
"""

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=1,
        # The maximum length of the response
        max_output_tokens=10000,
    )

    print(completion.result)
    return "hi"


@app.route("/shlokaoftheday")
def shlokday():
    return jsonify([getshlokaforday()[0], getshlokaforday()[1]])

@app.route("/<chap>/<shlok>")
def getshlok(chap, shlok):
    url = "https://bhagavad-gita3.p.rapidapi.com/v2/chapters/" + chap + "/verses/" + shlok + "/"

    headers = {
        "X-RapidAPI-Key": os.environ["RAPID_API"],
        "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return jsonify(
        {
            "script": response.json()["transliteration"],
            "meaning": response.json()["translations"][2]["description"]
        }
    )

@app.route("/android/<chap>/<shlok>")
def getshlokand(chap, shlok):
    url = "https://bhagavad-gita3.p.rapidapi.com/v2/chapters/" + chap + "/verses/" + shlok + "/"

    headers = {
        "X-RapidAPI-Key": os.environ["RAPID_API"],
        "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return jsonify(
        [
            response.json()["transliteration"],
            response.json()["translations"][2]["description"]
        ]
    )

@app.route('/getaccesstoken')
def accesstoken():
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = {
        'client_id': os.environ['client_id'],
        'client_secret': os.environ['client_secret'],
        'grant_type': 'client_credentials',
        'scope': 'verse chapter',
    }

    response = requests.post('https://bhagavadgita.io/auth/oauth/token', headers=headers, data=data)

    return response.json()


#hindi text

@app.route("/hindi/<chap>/<shlok>")
def gethindishlok(chap, shlok):
    url = "https://bhagavad-gita3.p.rapidapi.com/v2/chapters/" + chap + "/verses/" + shlok + "/"

    headers = {
        "X-RapidAPI-Key": os.environ["RAPID_API"],
        "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    return jsonify(
        {
            "script": response.json()["text"],
            "meaning": response.json()["translations"][6]["description"]
        }
    )


def filterList(number, list1):
    containing = [s for s in list1 if number in s]
    return containing[0]


@app.route("/testing/<chap>/<shlok>")
def test_purohit(chap, shlok):
    response = requests.get('https://bhagavadgitaapi.in/slok/' + chap + '/' + shlok)
    resultjson = {
        "script": response.json()["transliteration"],
        "meaning": response.json()["purohit"]["et"],
        "chapter": chap,
        "shloka": shlok
    }
    return jsonify(resultjson)


@app.route("/GitaTeluguAPIproxy/<lang>/<chap>/<shloka>")
def gettelugushlok(lang, chap, shloka):
    headers = {
        'accept': 'application/json',
    }

    response = requests.get('https://gita-api.vercel.app/' + lang + '/verse/' + chap + '/' + shloka, headers=headers)
    meaning = response.json()["translation"] 
    return jsonify(
        {
            "script": filterList(shloka, response.json()["verse"]) if type(response.json()["verse"]) == list else response.json()["verse"],
            "meaning": meaning + " (This meaning is for multiple shlokas)" if type(response.json()["verse"]) == list else meaning
        }
    )