# code_pipeline.py
import os
import json

def get_home_directory():
    """
    사용자 홈 디렉토리 경로를 반환
    """
    return os.path.expanduser("~")

def save_pipeline_to_file(pipeline, filename):
    """
    파이프라인 데이터를 사용자 홈 디렉토리에 파일로 저장
    """
    home_directory = get_home_directory()
    file_path = os.path.join(home_directory, filename)

    with open(file_path, 'w') as f:
        json.dump(pipeline, f)

def load_pipeline_from_file(filename):
    """
    사용자 홈 디렉토리에서 파일을 로드
    """
    home_directory = get_home_directory()
    file_path = os.path.join(home_directory, filename)

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    

def create_pipeline(blocks):
    """
    여러 코드 블록을 받아 파이프라인을 생성

    :param blocks: 블록화된 코드 딕셔너리들의 리스트
    :return: 코드 블록의 파이프라인 리스트
    """
    pipeline = []  # 파이프라인 리스트 초기화
    for block in blocks:
        pipeline.append(block)
    return pipeline