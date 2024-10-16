import os
import sys


def resource_path(relative_path):
    """PyInstaller 패키징 후에도 리소스 파일 경로를 찾을 수 있도록 함"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
