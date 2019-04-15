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


# Create a new instance of a ChatBot
# The chatbot we create has a read_only attribute to avoid training on time
# We strore the new data (inout - response) in a json file
# Every time we restart the ChatBot we retrain it we the new data
# With this method we avoid unnecessary work load and we specify better the training set we  want

bot = ChatBot(
    'Bot',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbot.db',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'response_selection_method': get_most_frequent_response,
            'threshold': 0.90
         }
    ]
)

# Set the trainer
trainer = ChatterBotCorpusTrainer(bot)

# Train the chat bot from a json file
trainer.train(
    "./final.json"
)

# Create an array to store bad answers (we define bad answers the one that the user indicates)
bad = [] 

# Create an array to store the previous training set as well as the new one
result = []
for statement in bot.storage.filter():
    if statement.in_response_to:
        result.append([statement.in_response_to, statement.text])


while True:
    try:
        print('ΕΙΜΑΙ ΤΟ ChatBot ΡΩΤΗΣΤΕ ΜΕ ΓΙΑ ΤΟ ΜΕΤΑΠΤΥΧΙΑΚΟ')
        user_input = input()
        print('ΑΠΑΝΤΗΣΗ :')
        bot_response = bot.get_response(user_input)
        print(str(bot_response))
        print('useful or not , if not press n')
        user_opinion = input()
        # We store the new respnses good or bad
        result.append([user_input, str(bot_response)])
        if user_opinion == 'n':
            print('thanks for feedback')
            # We store the bad respnses 
            bad.append([user_input, str(bot_response)])
            if user_opinion != 'n':
                break
            continue
    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

# Export the new training set with good and bad responses
file_path='./final.json'
import json
export = {'conversations': result}
with open(file_path, 'w+') as jsonfile:
    json.dump(export, jsonfile, ensure_ascii=False)


# Export the bad responses
file_path='./bad.json'
import json
export = {'conversations': bad}
with open(file_path, 'w+') as jsonfile:
    json.dump(export, jsonfile, ensure_ascii=False)







# Export the final result responses 
# Basically this will be the raining set that the bot will be trained next time
# For confirmation purposes the final.json and bad.json  are left to ckeck the result
# The code below can also be in a seperate python file to avoid wasting time 
for i in bad:
   for j in result :
        if j==i:
            result.remove(j)

file_path='./result.json'
import json
export = {'conversations': result}
with open(file_path, 'w+') as jsonfile:
    json.dump(export, jsonfile, ensure_ascii=False)





#delete database when programm ends
bot.storage.drop()
