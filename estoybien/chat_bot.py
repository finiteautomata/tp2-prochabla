#! coding: utf-8
"""Clase para el ChatBot de EstoyBien."""
import os
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot

class ChatBot(object):
    """Clase para el ChatBot de EstoyBien."""

    def __init__(self, token):
        u"""Constructor.

        Parámetros
        ----------

        token: string

            Token para el Telegram Chatbot
        """
        self._bot = Bot(token)

        print("Inicializando bot...")
        print(self._bot.get_me())

    def start(self):
        u"""Arranca el chatbot."""
        print("Chatbot corriendo")
