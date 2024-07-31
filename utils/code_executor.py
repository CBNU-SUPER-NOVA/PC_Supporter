# utils/code_executor.py
# 이 모듈은 추출된 코드를 로컬 환경에서 실행하는 기능을 제공합니다.

import subprocess
import sys
import io


def execute_code(code):
    """
    추출된 코드를 로컬 환경에서 실행합니다.
    """
    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        exec(code, {'__builtins__': __builtins__, 'subprocess': subprocess})

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return output
    except Exception as e:
        return f"코드 실행 중 오류 발생:\n{e}"
