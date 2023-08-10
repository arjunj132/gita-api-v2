from flask import Flask,jsonify,render_template
import requests
import os
import random, datetime
from flask_cors import CORS

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


@app.route("/shlokaoftheday")
def shlokday():
    return jsonify([getshlokaforday()[0], getshlokaforday()[1]])

@app.route("/<chap>/<shlok>")
def getshlok(chap, shlok):
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
    
    headers = {
        'accept': 'application/json',
    }

    params = {
        'access_token': response.json()["access_token"],
    }
    response = requests.get('https://bhagavadgita.io/api/v1/chapters/' + chap + '/verses/' + shlok, params=params, headers=headers)

    return jsonify(
        {
            "script": response.json()["transliteration"],
            "meaning": response.json()["meaning"]
        }
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
    
    headers = {
        'accept': 'application/json',
    }

    params = {
        'access_token': response.json()["access_token"],
        'language': 'hi',
    }
    response = requests.get('https://bhagavadgita.io/api/v1/chapters/' + chap + '/verses/' + shlok, params=params, headers=headers)

    return jsonify(
        {
            "script": response.json()["text"],
            "meaning": response.json()["meaning"]
        }
    )


def filterList(number, list1):
    containing = [s for s in list1 if number in s]
    return containing[0]

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
