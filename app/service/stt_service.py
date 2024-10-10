import io
import logging
from app.model.stt_model import STTModel

logger = logging.getLogger(__name__)

def initialize_stt_model(gpu_memory_fraction=0.3):
    logger.info(f"STT 모델을 GPU 메모리 비율 {gpu_memory_fraction}로 초기화합니다")
    stt_model = STTModel(gpu_memory_fraction=gpu_memory_fraction)
    stt_model.initialize_model()
    logger.info("STT 모델 초기화가 완료되었습니다")
    return stt_model

def transcribe_audio(audio_data, stt_model):
    try:
        audio_stream = io.BytesIO(audio_data)
        audio_stream.seek(0)
        result = stt_model.transcribe(audio_stream)
        return result
    except Exception as e:
        logger.error(f"오디오 변환 중 오류 발생: {str(e)}", exc_info=True)
        raise
