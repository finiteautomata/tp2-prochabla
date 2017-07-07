#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
from tempfile import NamedTemporaryFile
from pydub import AudioSegment


class Dialog(object):
    u"""Clase que implementa el diálogo con una persona."""

    def __init__(self, user, tts):
        u"""Constructor.

        Parámetros
        ----------

        user: telegram.ext.User
            Usuario con el que estamos dialogando
        tts: TextToSpeech service
            Objeto usado para sintetizar habla
        """
        self.user = user
        self._tts = tts

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        name = self.user.name
        msg = u"Hola {}, soy el chatbot de EstoyBien ¡Espero poder ayudarte!".format(name)
        audio_file = self._tts.synthesize(msg)

        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def text_received(self, bot, update):
        u"""Acción a realizar al recibir un texto."""
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def voice_received(self, bot, update):
        u"""Acción a realizar al recibir un archivo de voz."""
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
