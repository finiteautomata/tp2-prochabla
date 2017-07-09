#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
import utils
import time
import threading
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
        self.event = threading.Event()
        self.current_question = 0
        self.state = 0

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        name = self.user.name
        msg = u"Hola {}, soy el chatbot de EstoyBien ¡Espero poder ayudarte! Por favor indica una clave.".format(name)
        audio_file = self._tts.synthesize(msg)
        self.state = 1

        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def key_received(self, bot, update, keys):
        u"""Método recibido cuando me llega un /key"""
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
        """/pregun recibido"""
        if self.state != 2:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Setea una clave primero si no lo hiciste o esperá a que te pregunte la primera vez antes de pedirme una pregunta de nuevo"
            )
            return

        # Validador
        try:
            int(time[0])
        except ValueError:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Necesito un tiempo con valor numerico para saber en cuanto tiempo preguntarte"
            )
            return

        self.state = 3
        try:
            t = threading.Thread(target=self.ask, args=(time[0], bot, update))
            t.start()
        except Exception, e:
            print(e)


    def ask(self, secs, bot, update):
        u"""Método llamado cuando se pregunta si está bien."""
        time.sleep(float(secs))
        msg = u"¿Te encuentras bien?"
        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

        self.state = 4

        self.event.clear()
        t = threading.Thread(target=self.wait_five, args=(self.current_question,))
        t.start()
        self.event.wait()
        if self.state != 2:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Estamos llamando a la policía ya mismo. Cuando terminen de comer la pizza seguro ya van a comprar un helado y después seguro estan en camino para ayudarte... ponele"
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Gracias por confirmarmos que estás bien"
            )
            self.current_question += 1
            print(self.current_question)
        return

    def wait_five(self, current):
        print("estoy en wait")
        time.sleep(60)
        if current == self.current_question:
            print("wait activo")
            self.event.set()
        else:
            print("wait no activo")
            print(current)
            print(self.current_question)
        return

    def text_received(self, bot, update):
        u"""Acción a realizar al recibir un texto."""
        bot.send_message(
            chat_id=update.message.chat_id,
            text=update.message.text
        )

    def voice_received(self, bot, update):
        u"""Acción a realizar al recibir un archivo de voz."""

        if self.state == 4:
            wav_file = utils.save_to_wav(bot, update)
            print("Archivo guardado en {}".format(wav_file.name))
            try:
                stt_results = self._stt.recognize(
                    wav_file,
                    keywords=[self.key],
                    keywords_threshold=0.5
                )
                print(stt_results)
                alternatives = stt_results["results"][0]["alternatives"]

                if alternatives[0]["transcript"].rstrip() == self.key:
                    self.event.set()
                    self.state = 2
                else:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text="No reconocimos tu clave, por favor mandala de nuevo"
                    )

            except WatsonException as e:
                print(e)
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="No estaba esperando ningún audio por el momento, pero gracias por hablarme!"
            )
            return

