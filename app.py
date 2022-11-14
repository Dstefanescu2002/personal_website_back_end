from flask import Flask, request
# from urllib.request import Request, urlopen
# import json
# from random import *
from daniel_bot import DanielBot
import os

app = Flask(__name__)
db = DanielBot()

@app.route("/")
def main_route():
    return "<p><b>Usage:</b><br />&emsp;POST:  /daniel_bot/  => Get a response to a question</p>"

# @app.route("/pokemon", methods = ['GET'])
# def pokemon():
#     random_num = randint(1, 1000)
#     req = Request(
#         url='https://pokeapi.co/api/v2/pokemon/random_num/', 
#         headers={'User-Agent': 'Mozilla/5.0'}
#     )
#     content= urlopen(req).read()
#     json_content = json.loads(content)
#     return f"You are: {json_content['name']}"

@app.route("/daniel_bot", methods = ['POST'])
def daniel_bot():
    question = request.form.get('question', False)
    if not question:
        return 'I cannot answer that question. Please try again!'
    return db.get_response(question)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)