import os
import openai
import google.generativeai as genai
import platform
import requests
from utils.db_handler import load_api_key  # API 키를 불러오는 함수

# 모델 이름에 따라 API 키 로드, 없으면 None 처리
openai_api_key = None or load_api_key('GPT')
gemini_api_key = None or load_api_key('Gemini')
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
    system_message = f"{default_prompt}\nThe user is using a {os_info} operating system. If the request involves providing code, respond with Python code. If the request involves commands, respond with Zsh commands." if default_prompt else f"The user is using a {os_info} operating system. If the request involves providing code, respond with Python code. If the request involves commands, respond with Zsh commands."


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
        system_message = f"{default_prompt}\nThe user is using a {os_info} operating system. If the request involves providing code, respond with Python code. If the request involves commands, respond with Zsh commands." if default_prompt else f"The user is using a {os_info} operating system. If the request involves providing code, respond with Python code. If the request involves commands, respond with Zsh commands."

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
    if (use_api == "Gemini"):
        return send_to_gemini(prompt)
    else:
        return send_to_gpt(prompt)


import openai

def validate_openai_api_key(api_key):
    try:
        # OpenAI API 키 설정
        openai.api_key = api_key
        
        # API 키 유효성 검사를 위한 간단한 모델 호출
        openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Ping"}],
        )
        return True  # 성공적으로 호출되면 API 키가 유효
    except openai.APIStatusError:
        return False  # 인증 실패 시 False 반환
    except Exception as e:
        print(f"OpenAI API 확인 중 오류 발생: {e}")
        return False  # 기타 오류 처리

    
def validate_gemini_api_key(api_key):
    try:
        # Google Gemini API의 URL
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"

        # 요청에 사용될 데이터
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "Give me five subcategories of jazz?"}]
                }
            ]
        }

        # 헤더 설정
        headers = {
            "Content-Type": "application/json"
        }

        # POST 요청 보내기
        response = requests.post(url, json=data, headers=headers)

        # 상태 코드 확인
        if response.status_code == 200:
            return True  # API 키가 유효하면 True 반환
        else:
            print(f"응답 코드: {response.status_code}, 응답 내용: {response.text}")
            return False

    except Exception as e:
        print(f"Gemini API 확인 중 오류 발생: {e}")
        return False