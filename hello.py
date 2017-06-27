from flask import Flask, flash, request, jsonify
from flask_cors import CORS

import random
import pickle

import datetime

app = Flask(__name__)

CORS(app)
app.config['DEBUG'] = False 

users = {}

pokergames = {}

seenIPS = set()

def log(meme):
    if not meme in histories:
        histories[meme] = []
    histories[meme].append( {"time":datetime.datetime.utcnow(), "price":prices[meme]})
    
    entry = {"meme": meme, "price": prices[meme]}
    if len(transactions) and transactions[-1]["meme"] == meme:
        transactions[-1] = entry
    else:
        transactions.append(entry)

@app.route('/joinGame')
def joinGame() 
         gameId = request.args.get('gameId')
         if not gameId in games:
             games[gameId] = [{"users" : [
         game = games[gameId]
         
         self.state = states[0]
@app.route('/')
def getstate():
    user = request.cookies.get('user')
    if not user in users:
       new = True
       user = str(random.random())
       money = 1000 if request.access_route[0] not in seenIPS else 0
       users[user] = {"game":0}
    seenIPS.add(request.access_route[0])
    if random.random() > .96:
       print("saved")"""
       pickle.dump(users, open("users.pickle", "wb"))
       pickle.dump(prices, open("prices.pickle", "wb"))
       pickle.dump(histories, open("histories.pickle", "wb"))
       pickle.dump(seenIPS, open("seenIPS.pickle", "wb"))"""
    response = app.make_response(jsonify(pokergames[users[user]]))
    response.set_cookie("user", value = user, expires = datetime.datetime(9999, 1, 1))
    return response

@app.route('/bet')
def buy():
    user = request.cookies.get('user')
    if not user in users:
        return "derp"
    meme = request.args.get("meme")
    if not meme in prices:
       prices[meme] = 0
    if not meme in users[user]["stocks"]:
       users[user]["stocks"][meme] = 0
    if users[user]["money"] > prices[meme]:
       users[user]["money"] -= prices[meme]
       users[user]["stocks"][meme] += 1
       prices[meme] += 1
    log(meme)
    return ""

@app.route('/sell')
def sell():
    user = request.cookies.get('user')
    if not user in users:
        return "derp"
    meme = request.args.get("meme")
    if not( meme in users[user]["stocks"] ) or users[user]["stocks"][meme] == 0 :
       return "you don't have that"
    if not( meme in prices):
       prices[meme] = 12
    prices[meme] -= 1
    users[user]["money"] += prices[meme]
    users[user]["stocks"][meme] -= 1
    log(meme)
    return ""




@app.route('/stocks')
def stocks():
    return jsonify(prices)

@app.route('/history')
def history():
    meme = request.args.get("meme")
    if not meme in histories:
       return jsonify([])
    return jsonify(histories[meme])

@app.route('/recent')
def recent():   
    return jsonify(transactions[-100:])


if __name__ == '__main__':

    app.run(host = "0.0.0.0", port = 6790)

