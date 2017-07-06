# coding=utf-8
"""Ejemplo de TTS muy simple."""
import ConfigParser
from watson_developer_cloud import TextToSpeechV1
from pydub.playback import play
from pydub import AudioSegment

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config/development.conf")

tts = TextToSpeechV1(
    username=config.get('WATSON_KEYS', 'username'),
    password=config.get('WATSON_KEYS', 'password')
)

w = tts.synthesize("Hola a todos", voice="es-LA_SofiaVoice", accept="audio/wav")

play(AudioSegment(data=w))
