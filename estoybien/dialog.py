#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
from tempfile import NamedTemporaryFile
from pydub import AudioSegment


class Dialog(object):
    u"""Clase que implementa el diálogo con una persona."""

    def __init__(self, user):
        u"""Constructor.

        Parámetros
        ----------

        user: telegram.ext.User
            Usuario con el que estamos dialogando
        """
        self.user = user

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        name = self.user.name

        msg = u"Hola {}, soy el chatbot de EstoyBien".format(name)

        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def text_received(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def voice_received(self, bot, update):
        wav_file = self._save_to_wav(bot, update)

        print("Archivo guardado en {}".format(wav_file.name))

        bot.send_message(chat_id=update.message.chat_id, text="Recibí audio")

    def _save_to_wav(self, bot, update):
        """Salva update de audio en un .wav."""
        file_id = update.message.voice.file_id
        ext = update.message.voice.mime_type.split("/")[-1]
        temp_file = NamedTemporaryFile(suffix=".{}".format(ext), delete=False)
        wav_file = NamedTemporaryFile(suffix=".wav", delete=False)

        # Primero la guardo en el formato que venga
        voice_file = bot.get_file(file_id)
        voice_file.download(temp_file.name)
        # Luego la convierto a .wav
        AudioSegment.from_file(temp_file.name).export(wav_file, format="wav")

        return wav_file
