from app import celery
from app import celery
from app.service.llm_service import generate_summary_and_problem
from app.service.stt_service import transcribe_audio, initialize_stt_model
from app.client.server_client import ServerClient
import traceback
import logging
from typing import Dict
from celery.signals import worker_process_init

logger = logging.getLogger(__name__)
server_client = ServerClient()
stt_model = None

@worker_process_init.connect
def configure_worker(**kwargs):
    global stt_model
    stt_model = initialize_stt_model(gpu_memory_fraction=0.3)

@celery.task(bind=True)
def process_stt(self, audio_data):
    global stt_model
    self.update_state(state='PROCESSING')
    try:
        if stt_model is None:
            stt_model = initialize_stt_model(gpu_memory_fraction=0.3)
        result = transcribe_audio(audio_data, stt_model)
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
