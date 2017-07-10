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
        msg += u"Por favor indica una clave usando el comando /key seguido de una palabra."
        print(msg)
        audio_file = self._tts.synthesize(msg)
        self.state = DialogState.KEY_PROMPT

        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg,
        )
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def key_received(self, bot, update, keys):
        u"""Método recibido cuando me llega un /key"""
        if self.state != DialogState.KEY_PROMPT:
            print("add an error handle here")
            return

        key = " ".join(keys).strip()

        if key == '':
            msg = "Tu clave es vacía. Por favor, ingresa /key seguido de la clave esperada"
            audio_file = self._tts.synthesize(msg)
            bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

            return

        self.key = key
        self.state = DialogState.READY

        msg = u"Gracias. Tu clave fue guardada exitosamente."\
              u" Usa el comando /pregun para ver si estás bien"

        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

    def take_notice(self, bot, update, time):
        """/pregun recibido"""
        if self.state == DialogState.BEGIN or self.state == DialogState.KEY_PROMPT:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=u"Setea una clave primero si no lo hiciste o esperá a"\
                     u" que te pregunte la primera vez"
            )
            return
        elif self.state != DialogState.READY:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=u"Hay un pedido en espera. Debe finalizar dicho pedido"\
                     u" para realizar otro"
            )
            return

        # Validador
        try:
            secs = time[0]

            self._launch_ask(secs, bot, update)
        except ValueError:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Necesito un tiempo con valor numerico para saber en"\
                     " cuanto tiempo preguntarte"
            )
        except Exception, e:
            print(e)

    def _launch_ask(self, secs, bot, update):
        t = threading.Thread(target=self.ask, args=(secs, bot, update))
        t.start()
        self.state = DialogState.ON_HOLD


    def ask(self, secs, bot, update):
        u"""Método llamado cuando se pregunta si está bien."""
        h, r = divmod(secs, 3600)
        m, r = divmod(r, 60)
        s = r

        msg = "Te preguntaremos en {} horas, {} minutos y {} segundos cómo estás".format(
            h,
            m,
            s
        )
        audio_file = self._tts.synthesize(msg)
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)

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
        wav_file = utils.save_to_wav(bot, update)
        print("Archivo guardado en {}".format(wav_file.name))

        if self.state == DialogState.WAITING_ANSWER:
            self._process_password_answer(bot, update, wav_file)
        elif self.state == DialogState.READY:
            self._process_request(bot, update, wav_file)
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="No estaba esperando ningún audio"\
                     " por el momento, pero gracias por hablarme!"
            )
            return

    def _process_password_answer(self, bot, update, wav_file):
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

    def _process_request(self, bot, update, wav_file):
        try:
            time = utils.recognize_time(self._stt, wav_file)

            if time:
                self._launch_ask(time, bot, update)
            else:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text="No entendimos tu pedido. Puedes mandar un audio o "\
                         " bien utilizar /pregun <secs> para hacer un"\
                         " pedido."
                )

        except WatsonException as e:
            print(e)
