import io
import logging
from app.model.stt_model import STTModel

logger = logging.getLogger(__name__)
stt_model = STTModel()

def transcribe_audio(audio_data):
    try:
        audio_stream = io.BytesIO(audio_data)
        audio_stream.seek(0)
        result = stt_model.transcribe(audio_stream)
        return result
    except Exception as e:
        logger.error(f"오디오 변환 중 오류 발생: {str(e)}", exc_info=True)
        raise
