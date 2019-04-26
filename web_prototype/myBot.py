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

bot = ChatBot(
    'Bot',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///web.db',
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
    "./tests.json"
)
globResponse = ''
globInput = ''
bad = []
result = []
for statement in bot.storage.filter():
    if statement.in_response_to:
        result.append([statement.in_response_to, statement.text])


def export_json():    
    file_path='./result.json'
    import json
    export = {'conversations': result}
    with open(file_path, 'w+') as jsonfile:
        json.dump(export, jsonfile, ensure_ascii=False)

    file_path='./bad.json'
    import json
    export = {'conversations': bad}
    with open(file_path, 'w+') as jsonfile:
        json.dump(export, jsonfile, ensure_ascii=False)


    for i in bad:
       for j in result :
            if j==i:
                result.remove(j)

    file_path='./tests.json'
    import json
    export = {'conversations': result}
    with open(file_path, 'w+') as jsonfile:
        json.dump(export, jsonfile, ensure_ascii=False)