from utils.code_blocker import block_code
from utils.code_pipeline import create_pipeline
from utils.code_executor import execute_pipeline, validate_path

# 예제 코드 블록 생성
block_1 = block_code("Print Hello", "Prints 'Hello, World!'", "print('Hello, World!')")
block_2 = block_code("Print Bye", "Prints 'Goodbye, World!'", "print('Goodbye, World!')")

# 파이프라인 생성
pipeline = create_pipeline([block_1, block_2])

# 파이프라인 실행
execute_pipeline(pipeline)

# 로컬 경로 확인 예시
path = "/some/path/to/validate"
is_valid = validate_path(path)
print(f"Path '{path}' is valid: {is_valid}")