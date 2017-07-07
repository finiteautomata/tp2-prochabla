#! coding:utf-8
u"""Módulo de servicios TTS."""
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from watson_developer_cloud import TextToSpeechV1


class TTS(object):
    """Wrapper nuestro del IBM Bluemix."""

    def __init__(self, username, password):
        u"""Constructor.

        Parámetros
        ----------

        username: string

            Token para el
        password: string

        """
        self._tts_service = TextToSpeechV1(
            username=username,
            password=password
        )

    def synthesize(self, message):
        u"""Sintetiza un mensaje.

        Devuelve un archivo abierto con el audio sintetizado
        """
        temp_file = NamedTemporaryFile(suffix=".wav", delete=False)
        raw_audio = self._tts_service.synthesize(
            message,
            voice="es-LA_SofiaVoice",
            accept="audio/wav"
        )

        AudioSegment(data=raw_audio).export(temp_file, format="wav")

        # Hago seek 0 para que actualice los cambios... (está bien?)
        temp_file.seek(0)

        return temp_file