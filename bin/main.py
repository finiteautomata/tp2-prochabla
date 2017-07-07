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

    bot = estoybien.ChatBot(
        telegram_token=config.get('TELEGRAM', 'app_token'),
        tts_user=config.get('WATSON', 'tts_user'),
        tts_pass=config.get('WATSON', 'tts_pass'),
        stt_user=config.get('WATSON', 'stt_user'),
        stt_pass=config.get('WATSON', 'stt_pass'),
    )

    bot.start()
