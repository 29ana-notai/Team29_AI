def preprocess_lecture_content(lecture_material, stt_result, user_text):
    material_length = len(lecture_material.split())
    stt_length = len(stt_result.split())
    user_length = len(user_text.split())

    min_length = 10
    
    if material_length < min_length:
        lecture_material += "\n[Note: Insufficient lecture material content.]"
    if stt_length < min_length:
        stt_result += "\n[Note: Insufficient speech recognition result.]"
    if user_length < min_length:
        user_text += "\n[Note: Insufficient user input.]"
    if lecture_material.lower().strip() in ["표지", "목차", "제목"]:
        lecture_material = "[Note: The lecture material is a cover page or table of contents.]"
        
    return lecture_material, stt_result, user_text
