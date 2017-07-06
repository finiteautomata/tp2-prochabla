#! coding:utf-8
"""Bot de ejemplo que contesta 'hola mundo'"""
import sys
import os
import ConfigParser
sys.path.append(os.path.abspath("."))
import estoybien

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config/development.conf")


if __name__ == '__main__':

    bot = estoybien.ChatBot(config.get('TELEGRAM', 'app_token'))

    bot.start()
