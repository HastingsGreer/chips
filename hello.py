from flask import Flask, flash, request, jsonify
from flask_cors import CORS

import random
import pickle

import datetime
import copy
app = Flask(__name__)

CORS(app)
app.config['DEBUG'] = False 

users = {}

pokergames = {}

seenIPS = set()


@app.route('/joingame')
def joingame(): 
    gameId = request.args.get('gameId')
    user = request.cookies.get('user')
    if not user in users:
        return "Steve dies at the end of Wonder Woman"
    if(users[user]["gameId"] == gameId):
        return "alreadydid"
    users[user]["gameId"] = gameId
    
    if not gameId in pokergames:
        pokergames[gameId] = [{ 
	         "money" : {user: int(request.args.get('initialMoney'))},
		 "actor" : user,
		 "pot" : 0,
		 "initialMoney" : int(request.args.get('initialMoney'))
	}]
	
    else:
        game = pokergames[gameId]
	
        oldstate = copy.deepcopy(game[-1])

        oldstate["money"][user] = oldstate["initialMoney"]
	oldstate["actor"] = user
	game.append(oldstate)
    return ""


@app.route('/getstate')
def getstate():
    print(users)
    print(pokergames)
    user = request.cookies.get('user')
    if not user in users:
       new = True
       user = str(random.random())
       money = 1000 if request.access_route[0] not in seenIPS else 0
       users[user] = {"gameId":0}
    seenIPS.add(request.access_route[0])
    if random.random() > .96:
        print("saved")
        """
        pickle.dump(users, open("users.pickle", "wb"))
        pickle.dump(prices, open("prices.pickle", "wb"))
        pickle.dump(histories, open("histories.pickle", "wb"))
        pickle.dump(seenIPS, open("seenIPS.pickle", "wb"))"""
    if(users[user]["gameId"] in pokergames):
        response = app.make_response(jsonify(pokergames[users[user]["gameId"]]))
    else:
        response = app.make_response(jsonify([]))
    response.set_cookie("user", value = user, expires = datetime.datetime(9999, 1, 1))
    return response

@app.route('/bet')
def bet():
    user = request.cookies.get('user')
    if not user in users:
        return "derp"

    game = pokergames[users[user]["gameId"]]
    oldstate = copy.deepcopy(game[-1])
    amount = int(request.args.get("amount"))
    
    if amount > oldstate["money"][user]:
        return "too poor"
    
    oldstate["money"][user] -= amount
    oldstate["pot"] += amount
    oldstate["actor"] = user
    game.append(oldstate)
    return "went well"

@app.route('/takepot')
def takepot():
    user = request.cookies.get('user')
    if not user in users:
        return "derp"
    
    game = pokergames[users[user]["gameId"]]
    oldstate = copy.deepcopy(game[-1])
    
    oldstate["money"][user] += oldstate["pot"]
    oldstate["pot"] = 0
    oldstate["actor"] = user
    

    game.append(oldstate)
    return "went well"




if __name__ == '__main__':

    app.run(host = "0.0.0.0", port = 6790)

