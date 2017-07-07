#! coding:utf-8
u"""Módulo de servicios TTS."""
from watson_developer_cloud import SpeechToTextV1


class STT(object):
    """Wrapper nuestro del IBM Bluemix."""

    def __init__(self, username, password):
        u"""Constructor.

        Parámetros
        ----------

        username: string

            Token para el
        password: string

        """
        self._stt = SpeechToTextV1(username=username, password=password)

    def recognize(self, audio_file, alternatives=1):
        u"""Aplica ASR al audio_file"""
        return self._stt.recognize(
            audio_file,
            content_type="audio/wav",
            model="es-ES_BroadbandModel",
            max_alternatives=str(alternatives),
            continuous="true")
