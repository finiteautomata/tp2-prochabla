#! coding: utf-8
"""Clase para el ChatBot de EstoyBien."""
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
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
        self._bot = Bot(token=token)
        self._updater = Updater(token=token)
        print("Inicializando bot...")
        print(self._bot.get_me())

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
        import ipdb; ipdb.set_trace()
        bot.send_message(chat_id=update.message.chat_id, text="Hola! Soy el Chat de EstoyBien")

    def _text_received(self, bot, update):
        """Handler para mensajes."""
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def _voice_received(self, bot, update):
        """Handler para mensajes recibidos de voz."""
        wav_file = self._save_to_wav(update)

        print("Archivo guardado en {}".format(wav_file.name))

        bot.send_message(chat_id=update.message.chat_id, text="Recibí audio")

    def _save_to_wav(self, update):
        """Salva update de audio en un .wav."""
        file_id = update.message.voice.file_id
        ext = update.message.voice.mime_type.split("/")[-1]
        temp_file = NamedTemporaryFile(suffix=".{}".format(ext), delete=False)
        wav_file = NamedTemporaryFile(suffix=".wav", delete=False)

        # Primero la guardo en el formato que venga
        voice_file = self._bot.get_file(file_id)
        voice_file.download(temp_file.name)
        # Luego la convierto a .wav
        AudioSegment.from_file(temp_file.name).export(wav_file, format="wav")

        return wav_file
