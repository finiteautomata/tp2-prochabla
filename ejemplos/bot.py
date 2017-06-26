#! coding: utf-8
"""Bot de ejemplo que contesta 'hola mundo'"""
import os
from telegram.ext import Updater, CommandHandler
from telegram import Bot


token = os.environ['TELEGRAM_TOKEN']


def start(bot, update):
    """Handler para el comando /start."""
    print("Recibí info")
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo")


if __name__ == '__main__':

    bot = Bot(token=token)

    print("Retrieving data")
    print(bot.get_me())

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
