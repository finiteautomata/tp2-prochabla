#! coding: utf-8
"""Bot de ejemplo que contesta 'hola mundo'"""
import os
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot


token = os.environ['TELEGRAM_TOKEN']
received_path = os.path.abspath(os.path.join(".", "recibidos"))


def start(bot, update):
    """Handler para el comando /start."""
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo")


def echo(bot, update):
    """Handler para mensajes."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def voice_received(bot, update):
    """Handler para mensajes recibidos de voz."""
    file_id = update.message.voice.file_id
    ext = update.message.voice.mime_type.split("/")[-1]
    file_path = os.path.join(received_path, file_id + "." + ext)

    voice_file = bot.get_file(file_id)
    voice_file.download(file_path)
    print("File saved to {}".format(file_path))

    bot.send_message(chat_id=update.message.chat_id, text="Recibí audio")

if __name__ == '__main__':

    bot = Bot(token=token)

    print("Retrieving data")
    print(bot.get_me())

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text, echo)
    voice_handler = MessageHandler(Filters.voice, voice_received)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(voice_handler)

    updater.start_polling()
