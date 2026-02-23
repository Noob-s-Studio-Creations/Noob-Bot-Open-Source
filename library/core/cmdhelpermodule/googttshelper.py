import tempfile
import os

from gtts import gTTS
from gtts.lang import tts_langs
from langdetect import detect, DetectorFactory, lang_detect_exception

from library.core.helpmodule.randomtextcreator import GetRandomText
import botconfig as config

DetectorFactory.seed = 0

SUPPORTED_LANGS = tts_langs()

def TTSNow(text: str):
    try:
        detected_lang = detect(text)
    except lang_detect_exception.LangDetectException:
        detected_lang = "en"

    if detected_lang not in SUPPORTED_LANGS:
        detected_lang = "en"

    base_temp = os.path.join(
        tempfile.gettempdir(),
        config.BotOwnerTeam,
        config.AppName,
        "temporary",
        "tts"
    )
    os.makedirs(
        base_temp,
        exist_ok=True
    )

    file_name = f"tmp_{GetRandomText()}.mp3"
    file_path = os.path.join(
        base_temp,
        file_name
    )

    tts = gTTS(
        text=text,
        lang=detected_lang,
        slow=False
    )
    tts.save(file_path)

    return file_path, detected_lang