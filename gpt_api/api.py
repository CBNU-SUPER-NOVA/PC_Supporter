import os
import subprocess
from dotenv import load_dotenv
import openai
import platform

# 환경변수에서 API 키 가져오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# openai 모듈에 API 키 설정
openai.api_key = api_key

def run_command(command):
    """
    터미널 명령어를 실행하고, 그 결과를 반환합니다.
    """
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

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
    return response.choices[0].message['content']

def main():
    """
    메인 함수로, 사용자가 입력한 명령어를 실행하고 결과를 GPT에 전달합니다.
    """
    # 기본 프롬프트 설정 (필요할 경우 외부에서 가져올 수도 있음)
    default_prompt = "Please note that this assistant understands different operating systems such as Windows, macOS, and Linux."

    while True:
        user_input = input("Enter a command or message ('exit' to quit): ")

        # 종료 조건
        if user_input.lower() == 'exit':
            break

        # 사용자 입력 처리
        response = send_to_gpt(user_input, default_prompt)

        # 응답 출력
        print("\nResponse from GPT:")
        print(response)

if __name__ == "__main__":
    main()
