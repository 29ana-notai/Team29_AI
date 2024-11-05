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
Please provide a detailed summary of the above content. Format your response as follows:
- Create an appropriate title for the content and wrap it in h3 tags
- Use br tags for line breaks
- Use hr tags for section separations
- Wrap important keywords, concepts, and key points in <b> tags

Include these sections:
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
Please generate questions based on the above content. Format your response as follows:
- Create an appropriate title for the questions and wrap it in h3 tags
- Use br tags for line breaks
- Use hr tags between major sections
- Wrap important keywords, concepts, and key points in <b> tags

Generate the following questions:
1. 3 multiple-choice questions (4 options each)
   - Each question should cover key concepts and measure understanding, not just memorization.
2. 3 short-answer questions
   - These should verify understanding of core terms or concepts.
3. 2 essay questions
   - One to assess conceptual understanding
   - Another to evaluate application skills and critical thinking
4. 1 additional question related to the user input text
   - This should consider the user's interests or points of inquiry.

For each question, include:
- The question itself
- Answer options (for multiple choice)
- Correct answer
- Brief explanation
- Learning objective being assessed

Please provide the response in Korean.
"""
    return prompt