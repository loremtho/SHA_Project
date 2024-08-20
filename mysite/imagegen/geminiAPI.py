import google.generativeai as genai
import os

# 'YOUR_ACTUAL_API_KEY'를 실제 API 키로 바꿉니다.
os.environ["GOOGLE_API_KEY"] = "AIzaSyCOb-lP30R-se-MbkMXOiHFDYWcaArQFC0"

# 이제 genai 라이브러리를 구성합니다.
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

#구글 ai 모델 설정 => text 전용 제일 빠른 모델
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 한글 텍스트를 영어로 번역하는 함수
def translate_to_english(input_text):
    prompt = f"Translate this text from Korean to English: {input_text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# 영어 텍스트를 한글로 번역하는 함수
def translate_to_korean(input_text):
    prompt = f"Translate this text from English to Korean: {input_text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# 영어 텍스트를 Stable Diffusion 프롬프트로 변환하는 함수
def transform_to_stable_diffusion_prompt(english_text, negative_text=None):

    # 긍정적 프롬프트 생성
    prompt = f"Create a detailed art prompt for Stable Diffusion: {english_text}"
    response = model.generate_content(prompt)
    positive_prompt = response.text.strip()

    negative_prompt = ""
    if negative_text:
        # 부정적 프롬프트 생성
        neg_prompt = f"Create a negative prompt to avoid certain elements in Stable Diffusion: {negative_text}"
        neg_response = model.generate_content(neg_prompt)
        negative_prompt = neg_response.text.strip()
        
    formatted_prompt = f"### Positive Prompt:\n{positive_prompt}\n"
    if negative_prompt:
        formatted_prompt += f"\n### Negative Prompt:\n{negative_prompt}\n"

    print('포맷된 프롬프트' + formatted_prompt)
    return formatted_prompt