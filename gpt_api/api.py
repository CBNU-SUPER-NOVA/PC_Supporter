import os
import openai
import google.generativeai as genai
import platform
from dotenv import load_dotenv

# 환경변수에서 API 키 가져오기
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# OpenAI와 Gemini API 설정
openai.api_key = openai_api_key
genai.configure(api_key=gemini_api_key)


def send_to_gpt(user_input, default_prompt=""):
    """
    GPT-3.5-turbo API에 메시지를 보내고 응답을 반환합니다.
    """
    # 운영체제 정보 확인
    os_info = platform.system()

    # 시스템 메시지: 기본 프롬프트 및 운영체제 정보 포함
    system_message = f"{default_prompt}\nThe user is using a {os_info} operating system." if default_prompt else f"The user is using a {os_info} operating system."

    # GPT에 전달할 메시지 구조
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]

    # GPT API 호출
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content


def send_to_gemini(prompt, default_prompt=""):
    """
    Gemini API를 사용하여 텍스트를 생성하고 응답을 반환합니다.
    """
    try:
        # 운영체제 정보 확인
        os_info = platform.system()

        # 기본 프롬프트와 시스템 정보 포함
        system_message = f"{default_prompt}\nThe user is using a {os_info} operating system." if default_prompt else f"The user is using a {os_info} operating system."
        combined_prompt = f"{system_message}\n{prompt}"

        # 생성 모델 설정
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # 텍스트 생성
        response = model.generate_content(combined_prompt)

        # 응답 결과 반환
        return response.text
    except Exception as e:
        print(f"Gemini API 요청 중 오류 발생: {e}")
        return f"Gemini API 요청 중 오류 발생: {e}"


def send_to_llm(prompt, use_api):
    if (use_api == "GEMINI"):
        return send_to_gemini(prompt)
    else:
        return send_to_gpt(prompt)
