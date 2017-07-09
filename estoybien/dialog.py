#! coding: utf-8
u"""Clase que implementa el diálogo con una persona."""
import utils
import time
import threading
import enum
from watson_developer_cloud import WatsonException


class DialogState(enum.Enum):
    u"""Enum para estado de Diálogo."""

    BEGIN = 0
    KEY_PROMPT = 1
    READY = 2
    ON_HOLD = 3
    WAITING_ANSWER = 4


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
        self.state = DialogState.BEGIN

    def start(self, bot, update):
        u"""Comienza la conversación con el usuario.

        Este método es llamado cuando el usuario ejecuta /start
        """
        msg = u"Hola {}, soy el chatbot de EstoyBien ¡Espero poder ayudarte! "
        msg = msg.format(self.user.first_name)
        msg += u"Por favor indica una clave usando el comando /key."
        print(msg)
        audio_file = self._tts.synthesize(msg)
        self.state = DialogState.KEY_PROMPT

        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def key_received(self, bot, update, keys):
        u"""Método recibido cuando me llega un /key"""
        if self.state != DialogState.KEY_PROMPT:
            print("add an error handle here")
            return

        key = " ".join(keys)

        self.key = key

        self.state = DialogState.READY

        msg = u"Gracias. Tu clave fue guardada exitosamente."\
              u" Usa el comando /pregun para ver si estás bien"

        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def take_notice(self, bot, update, time):
        """/pregun recibido"""
        if self.state != DialogState.READY:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=u"Setea una clave primero si no lo hiciste o esperá a"\
                     u" que te pregunte la primera vez antes de pedirme una"\
                     u" pregunta de nuevo"
            )
            return

        # Validador
        try:
            int(time[0])
        except ValueError:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Necesito un tiempo con valor numerico para saber en"\
                     " cuanto tiempo preguntarte"
            )
            return

        self.state = DialogState.ON_HOLD
        try:
            t = threading.Thread(target=self.ask, args=(time[0], bot, update))
            t.start()
        except Exception, e:
            print(e)

    def ask(self, secs, bot, update):
        u"""Método llamado cuando se pregunta si está bien."""
        time.sleep(float(secs))
        msg = u"Hola {} ¿Te encuentras bien? Por favor dinos tu clave"

        msg = msg.format(self.user.first_name)

        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

        self.state = DialogState.WAITING_ANSWER

        self.event.clear()
        t = threading.Thread(
            target=self.wait_five,
            args=(self.current_question,))
        t.start()
        self.event.wait()
        if self.state != DialogState.READY:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Estamos llamando a la policía ya mismo."\
                     " Cuando terminen de comer la pizza"\
                     " y de comer un helado"\
                     " seguro estan en camino para ayudarte."
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
        u"""Función que espera para disparar alerta."""
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
        if self.state == DialogState.WAITING_ANSWER:
            wav_file = utils.save_to_wav(bot, update)
            print("Archivo guardado en {}".format(wav_file.name))
            try:
                stt_results = self._stt.recognize(
                    wav_file,
                    keywords=[self.key],
                    keywords_threshold=0.5
                )
                print(stt_results)

                if self.key in stt_results['results'][0]['keywords_result']:
                    self.event.set()
                    self.state = DialogState.READY
                else:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text="No reconocimos tu clave, por favor"\
                             " mandala de nuevo"
                    )

            except WatsonException as e:
                print(e)
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="No estaba esperando ningún audio"\
                     " por el momento, pero gracias por hablarme!"
            )
            return
