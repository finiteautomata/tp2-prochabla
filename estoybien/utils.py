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

quantity_keywords = {
    "una": 1,
    "un": 1,
    "dos": 2,
    "tres": 4,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "quince": 15,
    "veinte": 20,
    "treinta": 30,
    "cuarenta": 40,
    "cuarenta y cinco": 45,
    "cincuenta": 50,
    "sesenta": 60
}

time_keywords = {
    "segundo": 1,
    "segundos": 1,
    "minuto": 60,
    "minutos": 60,
    "hora": 3600,
    "horas": 3600,
}


def recognize_time(stt, wav_file):
    u"""Dado un STT object y un wav_file, devuelve si encontró un tiempo.

    Devuelve
    --------
        tiempo: int
            Cantidad en segundos spotteada en el wav
    """
    global quantity_keywords, time_keywords

    keywords = ",".join(quantity_keywords.keys() + time_keywords.keys())

    stt_results = stt.recognize(
        wav_file,
        keywords=keywords,
        keywords_threshold=0.5
    )

    spotted_keywords = stt_results['results'][0]['keywords_result'].keys()
    try:
        quantity = next(t for t in spotted_keywords if t in quantity_keywords)
        time_measure = next(t for t in spotted_keywords if t in time_keywords)

        return quantity_keywords[quantity] * time_keywords[time_measure]
    except StopIteration:
        return None
