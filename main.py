from utils.code_handler import handle_code
from utils.code_executor import validate_path
from utils.code_blocker import block_code
from utils.code_pipeline import create_pipeline, save_pipeline_to_file

def main():
 # 테스트용 코드 블록
    extracted_codes = [
        {
            "name": "Test Block 1",
            "description": "This is a test code block 1",
            "code": "print('Hello from Block 1')"
        },
        {
            "name": "Test Block 2",
            "description": "This is a test code block 2",
            "code": "print('Hello from Block 2')"
        }
    ]

    # extracted_codes = [
    #     {"name": "Code Block 1", "description": "First code block", "path": "/path/to/your/code1.py"},
    #     {"name": "Code Block 2", "description": "Second code block", "path": "/path/to/your/code2.py"},
    #     # 추가적인 코드 블록들...
    # ]

    # # 유효한 코드 블록만 필터링
    # valid_code_blocks = []
    # for code in extracted_codes:
    #     if validate_path(code["path"]):
    #         with open(code["path"], "r") as file:
    #             code_content = file.read()
    #             valid_code_blocks.append(block_code(code["name"], code["description"], code_content))
    #     else:
    #         print(f"Invalid path: {code['path']}")

     # 블록화된 코드 블록들을 파이프라인으로 생성
    valid_code_blocks = []
    for code in extracted_codes:
        valid_code_blocks.append(block_code(code["name"], code["description"], code["code"]))
    
    # 파이프라인 생성
    pipeline = create_pipeline(valid_code_blocks)

    # 파이프라인을 파일로 저장
    save_pipeline_to_file(pipeline)

if __name__ == "__main__":
    main()