#! /usr/bin/python3
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.storage import StorageAdapter
from chatterbot.storage import SQLStorageAdapter
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_first_response
from chatterbot.response_selection import get_most_frequent_response
from flask import Flask, render_template, request
import requests
from myBot import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getResponse",methods=['GET'])
def get_bot_response():
    global globResponse
    global globInput
    userText = request.args.get('msg')
    globInput = userText
    getResp = bot.get_response(userText)
    conf=getResp.confidence
    if conf > 0.80 :
        globResponse =  str(getResp)
    else :
        globResponse = 'ΔΕΝ ΚΑΤΑΛΑΒΑΙΝΩ, ΘΕΛΕΙΣ ΝΑ ΡΩΤΗΣΕΙΣ ΚΑΤΙ ΑΛΛΟ'
    result.append([globInput, globResponse])
    return globResponse

@app.route("/badResponse",methods=['GET','POST'])
def get_bad():
	userText1 = str(request.args.get('userText'))
	botText1 =  str(request.args.get('botText'))
	bad.append([userText1, botText1])
	if request.method == 'POST':
	    return 'ok'
	else:
	    return 'problem'


if __name__ == "__main__":
    app.run()


export_json()
bot.storage.drop()
