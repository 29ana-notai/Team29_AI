from app.util.preprocessing import preprocess_lecture_content
from app.client.llm_client import LLMAPIClient
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def generate_summary_and_problem(lecture_material: str, stt_result: str, user_text: str) -> Dict[str, str]:
    client = LLMAPIClient()
    try:
        summary = client.summarize(lecture_material, stt_result, user_text)
        problem = client.generate_problem(lecture_material, stt_result, user_text, summary)
        
        return {
            "summary": summary,
            "problem": problem
        }
    except Exception as e:
        logger.error(f"GPT API 호출 중 오류 발생: {str(e)}")
        raise RuntimeError(f"GPT API 호출 중 오류 발생"
)