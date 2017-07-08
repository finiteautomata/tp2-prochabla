#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
from . import utils
from watson_developer_cloud import WatsonException


class Dialog(object):
    u"""Clase que implementa el diálogo con una persona."""

    def __init__(self, user, tts, stt):
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
        self._stt = stt

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        name = self.user.name
        msg = u"Hola {}, soy el chatbot de EstoyBien ¡Espero poder ayudarte!"
        msg = msg.format(name)

        audio_file = self._tts.synthesize(msg)

        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def text_received(self, bot, update):
        u"""Acción a realizar al recibir un texto."""
        bot.send_message(
            chat_id=update.message.chat_id,
            text=update.message.text
        )

    def voice_received(self, bot, update):
        u"""Acción a realizar al recibir un archivo de voz."""
        wav_file = utils.save_to_wav(bot, update)

        print("Archivo guardado en {}".format(wav_file.name))

        try:
            stt_results = self._stt.recognize(
                wav_file,
                keywords=["bien", "mal", "estoy"],
                keywords_threshold=0.5
            )

            print(stt_results)
            alternatives = stt_results["results"][0]["alternatives"]

            bot.send_message(
                chat_id=update.message.chat_id,
                text=alternatives[0]["transcript"]
            )
        except WatsonException as e:
            print(e)
