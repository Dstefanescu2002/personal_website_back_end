from flask import Flask
from urllib.request import Request, urlopen
import json
from random import *

app = Flask(__name__)

@app.route("/")
def main_route():
    return "<p><b>Usage:</b><br />&emsp;/happy-phrase/: Get a random happy phrase</p>"

@app.route("/pokemon")
def pokemon():
    random_num = randint(1, 1000)
    req = Request(
        url='https://pokeapi.co/api/v2/pokemon/random_num/', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    content= urlopen(req).read()
    json_content = json.loads(content)
    return f"You are: {json_content['name']}"