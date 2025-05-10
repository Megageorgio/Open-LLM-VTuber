import sys
import os
import base64
from speechify import Speechify
from loguru import logger
from .tts_interface import TTSInterface

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


class TTSEngine(TTSInterface):
    temp_audio_file = "temp"
    file_extension = "wav"
    new_audio_dir = "cache"

    def __init__(self, api_key, voice, pitch=None, rate=None, emotions=None):
        self.client = Speechify(token=api_key)
        self.voice = voice
        self.pitch = pitch
        self.rate = rate
        self.emotions = emotions

        if not os.path.exists(self.new_audio_dir):
            os.makedirs(self.new_audio_dir)

    def _prepare_text(self, text, emotion):
        emotion_map = {'fear': 'terrified', 'anger': 'angry', 'disgust': 'angry', 'sadness': 'sad', 'joy': 'cheerful', 'neutral': 'calm', 'surprise': 'surprised'}
        
        result_emotion = emotion_map.get(emotion, None)
        
        if self.emotions and result_emotion:
            text = f'<speechify:style emotion="{result_emotion}">' + text + '</speechify:style>'
            
        if self.pitch and self.rate and (self.pitch != "medium" or self.rate != "medium"):
            text = f'<prosody pitch="{self.pitch}" rate="{self.rate}">' + text + '</prosody>'
            
        return '<speak>' + text + '</speak>'

    def generate_audio(self, text, file_name_no_ext=None, emotion=None):
        result = self.client.tts.audio.speech(
            input=self._prepare_text(text, emotion),
            voice_id=self.voice,
            model="simba-multilingual",
            audio_format="wav"
        )
        file_name = self.generate_cache_file_name(file_name_no_ext, self.file_extension)

        with open(file_name, "wb") as f:
            f.write(base64.b64decode(result.audio_data))
            
        return file_name