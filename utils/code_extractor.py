# utils/code_extractor.py
# 이 모듈은 주어진 텍스트에서 코드 블록을 추출하는 기능을 제공합니다.

import re
import json


def extract_code(text):
    """
    주어진 텍스트에서 모든 코드 블록과 일반 텍스트를 추출합니다.
    코드 블록은 ```python, ```zsh, ```cmd, ```shell, ```bash 또는 ```로 감싸져 있다고 가정합니다.
    반환된 리스트는 각 블록의 타입과 내용을 포함합니다.
    """
    code_blocks = []

    # 코드 블록과 일반 텍스트를 모두 추출할 수 있는 정규 표현식
    pattern = r'```(python|zsh|cmd|shell|bash)?\n(.*?)```|([^`]+)'

    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        if match[0]:  # 코드 블록일 때
            code_type = match[0]
            if code_type in {"zsh", "cmd", "shell"}:
                code_type = "bash"
            elif not code_type:  # 타입이 없을 경우
                code_type = "text"
            code_data = match[1].strip()
            code_blocks.append({"type": code_type, "data": code_data})
        elif match[2].strip():  # 일반 텍스트일 때
            code_blocks.append({"type": "text", "data": match[2].strip()})

    return code_blocks
