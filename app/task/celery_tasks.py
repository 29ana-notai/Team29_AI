from app import celery
from app.service.llm_service import generate_summary_and_problem
from app.service.stt_service import transcribe_audio
from app.client.server_client import ServerClient
import traceback
import logging
from typing import Dict
logger = logging.getLogger(__name__)
server_client = ServerClient()

@celery.task(bind=True)
def process_stt(self, audio_data):
    self.update_state(state='PROCESSING')
    try:
        result = transcribe_audio(audio_data)
        server_client.send_stt_result(self.request.id, result)
        return result
    except Exception as e:
        error_info = {
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'traceback': traceback.format_exc()
        }
        self.update_state(state='FAILURE', meta=error_info)
        raise

@celery.task(bind=True)
def process_llm(self, lecture_material: str, stt_result: str, user_text: str) -> Dict:
    self.update_state(state='PROCESSING')
    try:
        result = generate_summary_and_problem(lecture_material, stt_result, user_text)
        server_client.send_llm_result(self.request.id, result['summary'], result['problem'])
        return result
    except Exception as e:
        error_info = {
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'traceback': traceback.format_exc()
        }
        self.update_state(state='FAILURE', meta=error_info)
        raise
