from flask import Flask,jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "GitaAPI - powered by BhagavadGita.io"

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

    return response.json()


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

    return response.json()
