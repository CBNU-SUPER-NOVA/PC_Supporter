# utils/code_extractor.py
# 이 모듈은 주어진 텍스트에서 코드 블록을 추출하는 기능을 제공합니다.

import re


def extract_code(text):
    """
    주어진 텍스트에서 마크다운 코드 블록을 제거하고, 언어별로 코드 블록을 분리합니다.
    빈 코드 블록도 'text' 항목으로 추가합니다.
    """
    # 마크다운 코드 블록 패턴 정의
    code_block_pattern = re.compile(r'```(\w*)\n(.*?)\n```', re.DOTALL)
    # 코드 블록을 저장할 리스트
    blocks = []

    # 코드 블록을 추출하고, 텍스트와 코드 블록의 위치를 기록
    last_pos = 0
    for match in code_block_pattern.finditer(text):
        start, end = match.span()
        language = match.group(1).strip().lower()
        code = match.group(2).strip()

        # 텍스트와 코드 블록의 위치를 기반으로 순서를 유지
        if last_pos < start:
            # 빈 코드 블록이 아닌 일반 텍스트 추가
            blocks.append(('text', text[last_pos:start].strip()))

        # 빈 코드 블록 처리
        if not code:
            blocks.append(('text', ''))
        else:
            # 언어를 'bash'로 통합
            if language in {'zsh', 'shell', 'cmd'}:
                language = 'bash'
            blocks.append((language, code))

        last_pos = end

    # 마지막 텍스트 추가
    if last_pos < len(text):
        blocks.append(('text', text[last_pos:].strip()))

    # 빈 항목 제거
    return [(block_type, content) for block_type, content in blocks if content]


print(extract_code(text))
