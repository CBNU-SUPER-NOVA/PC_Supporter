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

    # 명령어 실행
    result = subprocess.run(command, shell=True, check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


def send_to_gpt(prompt):
    """
    GPT-3.5-turbo API에 메시지를 보내고 응답을 반환합니다.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please output the result as a code:\n{prompt}"}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content


def main():
    """
    메인 함수로, 사용자가 입력한 명령어를 실행하고 결과를 GPT에 전달합니다.
    """
    command = input("Enter a command to execute: ")

    # 운영체제에 따른 명령어 조정
    if platform.system() == "Windows":
        if command == "ls":
            command = "dir"
        elif command == "pwd":
            command = "cd"

    # 명령어 실행 결과 가져오기
    command_result = run_command(command)
    print(f"Command Result:\n{command_result}")

    # GPT로 보낼 프롬프트 작성
    prompt = f"The command '{command}' was executed and returned the following result: {command_result}"

    # GPT에 데이터 전달
    response = send_to_gpt(prompt)

    # 응답 출력
    print("\nResponse from GPT:")
    print(response)


if __name__ == "__main__":
    main()
