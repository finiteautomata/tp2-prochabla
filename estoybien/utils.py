#! coding: utf-8
u"""Módulo para utilidades varias de estoybien."""
from tempfile import NamedTemporaryFile
from pydub import AudioSegment


def save_to_wav(bot, update):
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

    # "Actualizo"
    wav_file.seek(0)

    return wav_file
