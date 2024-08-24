# utils/code_handler.py
# 이 모듈은 추출된 코드를 처리하고 실행 결과를 관리하는 기능을 제공합니다.

from .code_extractor import extract_code
from .code_executor import execute_code

def handle_code_blocks(code_blocks):
    """
    주어진 코드 블록들을 처리하고, 실행 가능한 형태로 변환합니다.
    :param code_blocks: 코드 블록 딕셔너리 리스트
    :return: 실행 가능한 코드 블록 리스트
    """
    executable_blocks = []
    for block in code_blocks:
        if block['type'] in ['python', 'bash']:
            executable_blocks.append(block)
    return executable_blocks