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

First, analyze if the provided content is sufficient for creating a comprehensive summary:
1. Check if the lecture material contains clear learning objectives and main topics
2. Verify if the STT result provides additional context or examples
3. Evaluate if the content is detailed enough for meaningful analysis

If the content is insufficient, please provide:
- Which specific aspects of the content are missing
- What kind of additional information would be needed

If the content is sufficient, please provide a detailed summary in Korean. Format your response as follows:

<h3>적절한 제목</h3>
<br>
<hr>
1. 핵심 주제 및 개요<br>
- 주제의 전반적인 맥락과 배경을 포함하여 설명
- 해당 주제가 다루는 핵심 영역을 구체적으로 서술
<br>
2. 주요 개념 (5-7개 항목)<br>
- 각 개념의 정의를 명확하게 서술
- 실제 적용 예시나 사례를 포함
<br>
3. 상세 내용<br>
각 주요 개념별로:
- 개념의 세부 구성 요소 설명
- 실제 활용 방법과 예시
<br>
4. 중요성 및 관련성<br>
- 실무/학문적 측면에서의 중요성
- 다른 주제나 분야와의 연관성
<br>
5. 결론<br>
- 핵심 내용의 종합적 정리
<br>
6. 사용자 입력 관련성<br>
- 사용자의 관심사/질문과의 구체적 연관성
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

First, evaluate if the provided content contains enough detail for meaningful questions:
1. Check if key concepts are clearly defined
2. Verify if there are sufficient examples and applications
3. Confirm if the content depth allows for various question types

If the content is insufficient, please specify what additional information would be needed.

If the content is sufficient, please generate questions in Korean. Format your response as follows:

<h3>평가 문항</h3>
<br>
<hr>
<b>객관식 문항 (3문제)</b><br>
1. [문제 내용]<br>
   ① [구체적인 보기 내용]<br>
   ② [구체적인 보기 내용]<br>
   ③ [구체적인 보기 내용]<br>
   ④ [구체적인 보기 내용]<br>
   - 정답: [정답 선택지]<br>
   - 설명: [정답에 대한 자세한 설명과 오답 선택지를 고른 경우의 문제점]<br>
<br>
<hr>
<b>주관식 문항 (3문제)</b><br>
1. [문제 내용]<br>
   - 정답: [예상되는 정답의 핵심 내용]<br>
   - 설명: [정답에 대한 부연 설명]<br>
<br>
<hr>
<b>서술형 문항 (2문제)</b><br>
1. [개념 이해를 확인하는 문제]<br>
   - 예시답안: [구체적인 답안 내용]<br>
   - 설명: [답안에 대한 부연 설명]<br>
<br>
<hr>
<b>사용자 맞춤 문항 (1문제)</b><br>
[사용자 입력 내용과 연계된 문제]<br>
- 예시답안: [예상되는 답안 내용]<br>
- 설명: [답안에 대한 부연 설명]<br>
"""
    return prompt