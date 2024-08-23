# utils/code_pipeline.py
import os
import datetime

def create_pipeline(blocks):
    """
    여러 코드 블록을 받아 파이프라인을 생성

    :param blocks : 블록화된 코드 딕셔너리들의 리스트
    :return : 코드 블록의 파이프라인 리스트
    """
    pipeline = []  # 여기서 pipeline 리스트를 초기화
    for block in blocks:
        pipeline.append(block)
    return pipeline

def save_pipeline_to_file(pipeline):
    """
    파이프라인을 파일로 저장. 파일 이름은 현재 날짜와 시간으로 구성

    :param pipleline : 파이프라인 리스트
    """
    # 파이프라인을 저장할 디렉토리 경로
    directory = 'pipelines'

    # # 디렉토리가 존재하지 않으면 생성
    # if not os.path.exists(directory):
    #     try:
    #         os.makedirs(directory)
    #     except Exception as e:
    #         print(f"Error creating directory {directory}: {e}")
    #         return
        
    # # 디렉토리 생성 확인
    # if not os.path.exists(directory):
    #     print(f"Directory does not exist after creation attempt: {directory}")
    #     return

    # 현재 날짜와 시간으로 파일 이름 생성
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"pipeline_{timestamp}.txt"
    file_path = os.path.join('pipelines', file_name)

    with open(file_path, "w") as file:
        for block in pipeline:
            file.write(f"# {block['name']} : {block['description']}\n")
            file.write(block['code'])
            file.write("\n\n")

    print(f"Pipeline saved to {file_path}")
