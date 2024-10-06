import requests
import json
from app.config.app_config import Config
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ServerClient:
    def __init__(self):
        self.base_url = Config.SPRING_SERVER_URL

    def send_llm_result(self, task_id: str, summary: str, problem: str) -> Optional[Dict]:
        endpoint = f"{self.base_url}/api/ai/llm/callback"
        
        payload = {
            "taskId": task_id,
            "summary": summary,
            "problem": problem
        }

        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"서버에 LLM 결과를 전송하는 중 오류가 발생했습니다: {e}")
            return None

    def send_stt_result(self, task_id: str, stt_result: Dict) -> Optional[Dict]:
        endpoint = f"{self.base_url}/api/ai/stt/callback"
        
        payload = {
            "taskId": task_id,
            "text": stt_result["text"],
            "words": stt_result["words"],
            "language": stt_result["language"],
            "languageProbability": stt_result["language_probability"]
        }

        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"서버에 STT 결과를 전송하는 중 오류가 발생했습니다: {e}")
            return None