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
import re  

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

# a list of stepwords and common used words for this chatbot. These words are removed from every sentence
# before we take the response. With this way we try to increase the confidence value in every response
# It's a way to solve the problem of chatterbot library due to the use of Greek language
delete_list = [" ο ", " η ", " το "," την "," τη "," τον "," τα ", " για "," τις "," τι "," να "," τη ", " ειναι "," σε ", " του ","Σε ", "Τι ",
" πρεπει ", " καποιος ", " καποια ", " καποιο ", " κατι ", " στο ", " στη ", " στην ", " στα ", " στους "," στον ", " οι "," θελω ", 
 " ηθελα ", " μεταπτυχιακου"," μεταπτυχιακο"," μεταπτυχιακο ", " με ", " και "]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getResponse",methods=['GET'])
def get_bot_response():
    global globResponse
    global globInput
    userText = request.args.get('msg')
    userText1 = ' ' + userText # problem with  " ποιο " or  "ποιο " , space sensitive at the beggining of every sentence

    # remove from user input the words that exist in array delete_list
    i=0;
    while i<len(delete_list):
        userText1 = re.sub(str(delete_list[i]), " ", userText1)
        i += 1

    globInput = userText1
    getResp = bot.get_response(userText1)
    conf=getResp.confidence
    print(conf)
    if conf > 0.35 :
        globResponse =  str(getResp)
    else :
        globResponse = 'Δεν καταλαβαίνω, θέλετε να ρωτήσετε κάτι άλλο ?'
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

@app.route("/userFeedback",methods=['GET','POST'])
def user_feed():
    userText1 = str(request.args.get('userText'))
    botText1 =  str(request.args.get('botText'))
    userFeed1 =  str(request.args.get('userFeed'))
    user.append([userText1, botText1,userFeed1])
    if request.method == 'POST':
        return 'ok'
    else:
        return 'problem'


if __name__ == "__main__":
    app.run()


export_json()
bot.storage.drop()
