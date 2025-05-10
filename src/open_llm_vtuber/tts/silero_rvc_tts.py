import sys
import os

from ruaccent import RUAccent
from silero_tts.silero_tts import SileroTTS
from loguru import logger
from .tts_interface import TTSInterface

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class TTSEngine(TTSInterface):
    def __init__(self, model_id="v3_1_ru", language="ru", speaker="baya", device='cpu'):
        self.tts = SileroTTS(model_id=model_id, language=language, speaker=speaker, sample_rate=48000, device=device)
        if language == "ru":
            self.accentizer = RUAccent()
            self.accentizer.load(omograph_model_size='turbo', use_dictionary=True)

    def generate_audio(self, text, file_name_no_ext=None):
        """
        Generate speech audio file using TTS.
        text: str
            the text to speak
        file_name_no_ext: str
            name of the file without extension


        Returns:
        str: the path to the generated audio file

        """
        file_name = self.generate_cache_file_name(file_name_no_ext, "wav")

        try:
            if not self.accentizer == None:
                text = self.accentizer.process_all(text)
            self.tts.tts(text, file_name)
        except Exception as e:
            logger.critical(f"\nError: silero-rvc-tts unable to generate audio: {e}")
            return None

        return file_name


# en-US-AvaMultilingualNeural
# en-US-EmmaMultilingualNeural
# en-US-JennyNeural
