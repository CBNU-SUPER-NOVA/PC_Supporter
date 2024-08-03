import os
from dotenv import load_dotenv
import openai

load_dotenv()

# 환경변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# openai 모듈에 API 키 설정
openai.api_key = api_key


def send_to_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5
    )
    return response.choices[0].message.content


prompt = "What is your name?"

response = send_to_gpt(prompt)

print(response)
