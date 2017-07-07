#! coding: utf-8
"""Clase para el ChatBot de EstoyBien."""
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot
from .tts import TTS
from .dialog import Dialog


class ChatBot(object):
    """Clase para el ChatBot de EstoyBien."""

    def __init__(self, telegram_token, tts_user, tts_pass):
        u"""Constructor.

        Parámetros
        ----------

        token: string

            Token para el Telegram Chatbot
        """
        self._bot = Bot(token=telegram_token)
        self._updater = Updater(token=telegram_token)
        self._tts = TTS(
            username=tts_user,
            password=tts_pass,
        )

        print("Inicializando bot...")
        print(self._bot.get_me())

        self._dialogs = {}

    def start(self):
        u"""Arranca el chatbot."""
        dispatcher = self._updater.dispatcher

        start_handler = CommandHandler('start', self._start_received)
        echo_handler = MessageHandler(Filters.text, self._text_received)
        voice_handler = MessageHandler(Filters.voice, self._voice_received)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(voice_handler)

        self._updater.start_polling()

        print("Chatbot corriendo")

    def _start_received(self, bot, update):
        """Handler de start"""
        user = update.effective_user

        dialog = self.get_dialog(user)

        dialog.start(bot, update)

    def _text_received(self, bot, update):
        """Handler para mensajes."""
        user = update.effective_user

        dialog = self.get_dialog(user)

        dialog.text_received(bot, update)

    def _voice_received(self, bot, update):
        """Handler para mensajes recibidos de voz."""
        user = update.effective_user

        dialog = self.get_dialog(user)

        dialog.voice_received(bot, update)

    def get_dialog(self, user):
        """Devuelve Dialog del usuario.

        Si no existe, lo crea
        """
        if user not in self._dialogs:
            self._dialogs[user] = Dialog(user, self._tts)

        return self._dialogs[user]
