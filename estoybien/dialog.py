#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
import utils
import time
import threading

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
        self.state = 0

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        name = self.user.name
        msg = u"Hola {}, soy el chatbot de EstoyBien ¡Espero poder ayudarte! Por favor indica una clave.".format(name)
        audio_file = self._tts.synthesize(msg)
        self.state = 1 #TODO: usar enum

        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def key_received(self, bot, update, keys):
        if self.state < 1:
            print("add an error handle here")
            return
        
        key = " ".join(keys)

        self.key = key

        self.state = 2

        msg = u"Gracias. Tu clave fue guardada exitosamente. Avisame si querés que te pregunte si estás bien."
        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)
    

    def take_notice(self, bot, update, time):
        
        if self.state < 2:
            print("proper error handle soon")
            return
        
        try:
            int(time[0])
        except ValueError:
            print("another proper error handling soon")
            return

        try:
            t = threading.Thread(target=self.ask, args=(time[0], bot, update))
            t.start()
        except Exception, e:
            print(e)
        

    def ask(self, secs, bot, update):
        time.sleep(float(secs))
        msg = u"Te encuentras bien?"
        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

        print("pregunta enviada. Lo que seguiria es cambiar a un proximo estado indicando que quiero y espero un audio con la clave y algo que chequee si respondo en x tiempo")
        return

    def text_received(self, bot, update):
        u"""Acción a realizar al recibir un texto."""
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def voice_received(self, bot, update):
        u"""Acción a realizar al recibir un archivo de voz."""
        wav_file = utils.save_to_wav(bot, update)

        print("Archivo guardado en {}".format(wav_file.name))

        stt_results = self._stt.recognize(wav_file)
        alternatives = stt_results["results"][0]["alternatives"]

        bot.send_message(chat_id=update.message.chat_id, text=alternatives[0]["transcript"])
