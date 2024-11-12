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
       if not stt_result or not isinstance(stt_result, dict):
           logger.error("stt_result가 없거나 딕셔너리 형식이 아닙니다.")
           return None
       
       if "text" not in stt_result or "words" not in stt_result:
           logger.error("stt_result에 필수 키(text 또는 words)가 없습니다.")
           return None

       endpoint = f"{self.base_url}/api/ai/stt/callback"
       
       payload = {
           "taskId": task_id,
           "text": stt_result["text"].replace('\n', ' ').strip(),  
           "words": stt_result["words"]
       }
       
       headers = {
           "Content-Type": "application/json"
       }
       
       try:
           response = requests.post(endpoint, json=payload, headers=headers)
           
           if response.status_code == 200:
               return {"success": True}
               
           response.raise_for_status()
           
       except requests.RequestException as e:
           logger.error(f"서버에 STT 결과를 전송하는 중 오류가 발생했습니다: {e}")
           return None