# utils/code_handler.py
# 이 모듈은 추출된 코드를 처리하고 실행 결과를 관리하는 기능을 제공합니다.

from .code_extractor import extract_code
from .code_executor import execute_code


def handle_code(text):
    code = extract_code(text)
    if code:
        print("추출된 코드:")
        print(code)
        result = execute_code(code)
        print("실행 결과:")
        print(result)
    else:
        print("코드를 추출할 수 없습니다.")
