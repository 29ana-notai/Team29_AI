import torch
import numpy as np
from app.config.stt_config import STTConfig
import logging
import io
from pydub import AudioSegment, effects

logger = logging.getLogger(__name__)

class STTModel:
    def __init__(self, gpu_memory_fraction=0.3):
        self.model = None
        self.use_faster_whisper = STTConfig.USE_FASTER_WHISPER
        self.device = None
        self.compute_type = None
        self.gpu_memory_fraction = gpu_memory_fraction

    def get_compute_type(self):
        if self.device == "cuda":
            return "float16"
        return "int8" if self.use_faster_whisper else "float32"

    def initialize_model(self):
        if self.model is None:
            try:
                import torch
                if torch.cuda.is_available():
                    self.device = "cuda"
                    torch.cuda.set_per_process_memory_fraction(self.gpu_memory_fraction)
                else:
                    self.device = "cpu"
                self.compute_type = self.get_compute_type()
                
                if self.use_faster_whisper:
                    self.model = self.initialize_faster_whisper()
                else:
                    self.model = self.initialize_whisper()
                
            except Exception as e:
                logger.error(f"STTModel 초기화 중 오류 발생: {str(e)}", exc_info=True)
                raise

    def initialize_faster_whisper(self):
        from faster_whisper import WhisperModel
        model = WhisperModel(STTConfig.MODEL_SIZE, device=self.device, compute_type=self.compute_type)
        logger.info(f"STTModel 초기화 완료 (faster_whisper 사용, device: {self.device}, compute_type: {self.compute_type})")
        return model

    def initialize_whisper(self):
        import whisper
        model = whisper.load_model(STTConfig.MODEL_SIZE).to(self.device)
        logger.info(f"STTModel 초기화 완료 (원본 whisper 사용, device: {self.device}, compute_type: {self.compute_type})")
        return model

    def preprocess_audio(self, audio_data):
        audio = AudioSegment.from_file(audio_data, format="mp3")
        audio = effects.normalize(audio)
        audio = audio.set_frame_rate(STTConfig.SAMPLE_RATE)
        audio = audio.set_channels(1)
        
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        return wav_data.read()

    def transcribe(self, audio_data):
        try:
            preprocessed_audio = self.preprocess_audio(audio_data)
            
            if self.use_faster_whisper:
                result = self._transcribe_faster_whisper(preprocessed_audio)
            else:
                result = self.transcribe_whisper(preprocessed_audio)

            words_with_timestamps = self.normalize_timestamps(result['words'], result['audio_length'])

            return {
                "text": result['full_text'].strip(),
                "words": words_with_timestamps,
                "language": result['language'],
                "language_probability": result['language_probability'],
                "audio_length": result['audio_length']
            }
        except Exception as e:
            logger.error(f"음성 변환 중 오류 발생: {str(e)}", exc_info=True)
            raise

    def _transcribe_faster_whisper(self, preprocessed_audio):
        segments, info = self.model.transcribe(preprocessed_audio, beam_size=STTConfig.BEAM_SIZE, word_timestamps=STTConfig.WORD_TIMESTAMPS)
        full_text = " ".join(segment.text for segment in segments)
        words = [
            {"word": word.word, "start": word.start, "end": word.end}
            for segment in segments
            for word in segment.words
        ]
        return {
            'full_text': full_text,
            'words': words,
            'language': info.language,
            'language_probability': info.language_probability,
            'audio_length': info.duration
        }

    def transcribe_whisper(self, preprocessed_audio):
        audio_array = np.frombuffer(preprocessed_audio, dtype=np.int16).astype(np.float32) / STTConfig.AUDIO_NORMALIZATION_FACTOR
        audio_array = torch.from_numpy(audio_array).to(self.device)
        
        result = self.model.transcribe(audio_array, language="ko")
        words = [{"word": segment["text"], "start": segment["start"], "end": segment["end"]}
            for segment in result["segments"]]
        return {
            'full_text': result["text"],
            'words': words,
            'language': result["language"],
            'language_probability': 1.0,
            'audio_length': len(audio_array) / STTConfig.SAMPLE_RATE
        }

    def normalize_timestamps(self, words, audio_length):
        def normalize_time(time):
            return min(time * audio_length / words[-1]['end'], audio_length)

        return [
            {"word": item["word"], "start": normalize_time(item["start"]), "end": normalize_time(item["end"])}
            for item in words
        ]
