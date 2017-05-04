# !/usr/bin/python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

logging.basicConfig(level=logging.INFO)

chatbot = ChatBot("myBot", storage_adapter='chatterbot.storage.SQLAlchemyDatabaseAdapter',database="chatterbot-database",drop_create=True)
chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train('./test.corpus.json')

# 开始对话
while True:
    print(chatbot.get_response(input(">")))