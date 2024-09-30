from openai import OpenAI
from ..config import Config
from app.util.preprocessing import preprocess_lecture_content
from app.util.prompt_builder import build_summary_prompt, build_problem_prompt
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class LLMAPIClient:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def process(self, lecture_material: str, stt_result: str, user_text: str, task_type: str, summary: Optional[str] = None) -> str:
        try:
            processed_material, processed_stt, processed_user_text = preprocess_lecture_content(
                lecture_material, stt_result, user_text
            )
            if task_type == "summarize":
                prompt = build_summary_prompt(processed_material, processed_stt, processed_user_text)
            elif task_type == "problem":
                prompt = build_problem_prompt(processed_material, processed_stt, processed_user_text, summary)
            else:
                raise ValueError(f"알 수 없는 작업 유형: {task_type}")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in summarizing educational content and generating questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"LLM API 처리 중 오류 발생: {str(e)}")
            raise

    def summarize(self, lecture_material: str, stt_result: str, user_text: str) -> str:
        return self.process(lecture_material, stt_result, user_text, "summarize")

    def generate_problem(self, lecture_material: str, stt_result: str, user_text: str, summary: str) -> str:
        return self.process(lecture_material, stt_result, user_text, "problem", summary)