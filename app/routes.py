from flask import Blueprint, request, jsonify
from app.task.celery_tasks import process_llm, process_stt
from app import celery
import logging

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__, url_prefix='/api/ai')

def get_task_info(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'result': None
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'result': None
        }
        logger.error(f"작업 실패: {str(task.info)}")
    else:
        response = {
            'state': task.state,
            'result': task.result
        }
    return response

@api.route('/stt', methods=['POST'])
def stt_endpoint():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "오디오 파일이 제공되지 않았습니다"}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({"error": "선택된 파일이 없습니다"}), 400
        
        if not audio_file.filename.lower().endswith('.mp3'):
            return jsonify({"error": "MP3 파일만 지원됩니다"}), 400
        
        audio_data = audio_file.read()
        task = process_stt.delay(audio_data)
        return jsonify({"taskId": task.id, "taskType": "stt"}), 202
    except Exception as e:
        logger.error(f"STT 엔드포인트 오류: {str(e)}", exc_info=True)
        return jsonify({"error": "서버 내부 오류가 발생했습니다"}), 500

@api.route('/llm', methods=['POST'])
def llm_endpoint():
    data = request.json
    if not data:
        return jsonify({"error": "JSON 데이터가 제공되지 않았습니다"}), 400
 
    lecture_material = data.get('ocrText', '')
    stt_result = data.get('stt', '')
    user_text = data.get('keyboardNote', '')
    task = process_llm.delay(lecture_material, stt_result, user_text)
    return jsonify({"taskId": task.id, "taskType": "llm"}), 202

@api.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    response = get_task_info(task_id)
    return jsonify(response)

@api.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": f"오류가 발생했습니다: {str(e)}"}), 500
