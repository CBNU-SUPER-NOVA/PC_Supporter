# utils/code_extractor.py
# 이 모듈은 주어진 텍스트에서 코드 블록을 추출하는 기능을 제공합니다.

import re

# TODO: 코드 블록이 여러 개일 경우 처리


def extract_code(text):
    """
    주어진 텍스트에서 코드 블록을 추출합니다.
    코드 블록은 ```python 또는 ```로 감싸져 있다고 가정합니다.
    """
    code_match = re.search(r'```(?:python)?\n(.*?)```', text, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    return None
