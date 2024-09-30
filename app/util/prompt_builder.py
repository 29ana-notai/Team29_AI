def build_summary_prompt(lecture_material, stt_result, user_text):
    context = f"""Lecture Material:
{lecture_material}
Lecture Recording STT Result:
{stt_result}
User Input Text:
{user_text}
"""
    prompt = f"""The following is the lecture material, lecture recording STT result, and user input text:
{context}
Based on the above content, please provide a detailed summary according to the following structure:
1. Core topic and overview (2-3 sentences)
2. Key concepts (5-7 bullet points)
3. Detailed content (2-3 sub-bullet points for each key concept)
4. Relevance and importance (2-3 sentences)
5. Conclusion or summary (1-2 sentences)
6. Relevance to user input text (1-2 sentences)

Please provide the response in Korean.
"""
    return prompt

def build_problem_prompt(lecture_material, stt_result, user_text, summary):
    context = f"""Lecture Material:
{lecture_material}
Lecture Recording STT Result:
{stt_result}
User Input Text:
{user_text}
Summary:
{summary}
"""
    prompt = f"""The following is the lecture material, lecture recording STT result, user input text, and content summary:
{context}
Based on the above content, please generate questions in the following format:
1. 3 multiple-choice questions (4 options each)
   - Each question should cover key concepts and measure understanding, not just memorization.
2. 3 short-answer questions
   - These should verify understanding of core terms or concepts.
3. 2 essay questions
   - One to assess conceptual understanding
   - Another to evaluate application skills and critical thinking
4. 1 additional question related to the user input text
   - This should consider the user's interests or points of inquiry.
Please provide answers and brief explanations for each question.
Also, briefly explain what learning objective each question is assessing.
Please provide the response in Korean.
"""
    return prompt
