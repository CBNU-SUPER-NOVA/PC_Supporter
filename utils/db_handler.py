import sqlite3
import os
from cryptography.fernet import Fernet

def get_key_path():
    return os.path.join(os.path.dirname(__file__), "encryption.key")

def generate_encryption_key():
    key = Fernet.generate_key()
    with open(get_key_path(), "wb") as key_file:
        key_file.write(key)
    print("새로운 암호화 키가 생성되었습니다.")

def load_encryption_key():
    key_path = get_key_path()
    if not os.path.exists(key_path):
        print("encryption.key 파일이 없습니다. 새 키를 생성합니다.")
        generate_encryption_key()

    with open(key_path, "rb") as key_file:
        return key_file.read()

encryption_key = load_encryption_key()
cipher = Fernet(encryption_key)

def init_db():

    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    # 모델 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            encrypted_api_key TEXT NOT NULL
        )
    ''')

    try:
        cursor.execute("ALTER TABLE conversations ADD COLUMN model_name TEXT DEFAULT 'GPT'")
        print("model_name 열이 추가되었습니다.")
    except sqlite3.OperationalError:
        print("model_name 열이 이미 존재합니다.")

    # 대화 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model_name TEXT DEFAULT 'GPT',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 메시지 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            sender_type TEXT CHECK(sender_type IN ('ai', 'user')),
            content_type TEXT CHECK(content_type IN ('text', 'python', 'zsh', 'shell', 'bash')),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        )
    ''')

    # 코드 블록 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            code_type TEXT,
            code_data TEXT,
            order_num INTEGER,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        )
    ''')

    # 프롬프트 설정 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompt_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT
        )
    ''')

    # 기본 대화 설정 (최초 실행 시)
    cursor.execute('''
        INSERT OR IGNORE INTO conversations (id, name, model_name)
        VALUES (1, 'MyConversation', 'GPT')
    ''')

    conn.commit()
    conn.close()

def insert_prompt(prompt):
    """
    프롬프트를 prompt_settings 테이블에 저장
    """
    try:
        conn = sqlite3.connect('PC_Supporter.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO prompt_settings (prompt) 
            VALUES (?)
        ''', (prompt,))

        conn.commit()
        print("프롬프트가 저장되었습니다.")
    except sqlite3.Error as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()

def view_prompt_settings():
    """
    prompt_settings 테이블의 모든 프롬프트 조회
    """
    try:
        conn = sqlite3.connect('PC_Supporter.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM prompt_settings')
        rows = cursor.fetchall()

        if rows:
            print("프롬프트 설정 데이터:")
            for row in rows:
                print(row)
        else:
            print("prompt_settings 테이블에 데이터가 없습니다.")
    except sqlite3.Error as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()

# 테스트: 프롬프트 조회
view_prompt_settings()

def get_all_prompts():
    """
    저장된 모든 프롬프트를 가져오기
    """
    try:
        conn = sqlite3.connect('PC_Supporter.db')
        cursor = conn.cursor()

        cursor.execute('SELECT prompt FROM prompt_settings')
        prompts = cursor.fetchall()

        return [prompt[0] for prompt in prompts] if prompts else []
    except sqlite3.Error as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()

def save_api_key(model_name, api_key):
    """API 키를 암호화하여 저장하거나 업데이트"""
    encrypted_key = cipher.encrypt(api_key.encode())  # API 키 암호화
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    # 기존 키가 있는지 확인 후 업데이트 또는 삽입
    cursor.execute('''
        INSERT INTO models (model_name, encrypted_api_key)
        VALUES (?, ?)
        ON CONFLICT(model_name) DO UPDATE SET encrypted_api_key = excluded.encrypted_api_key
    ''', (model_name, encrypted_key))

    conn.commit()
    conn.close()


def load_api_key(model_name):
    """
    저장된 API 키를 복호화하여 반환
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT encrypted_api_key FROM models WHERE model_name = ?
    ''', (model_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return cipher.decrypt(result[0]).decode()
    return None

def create_conversation(name, model_name='GPT'):
    """
    새로운 대화를 생성하고, 모든 프롬프트를 초기 메시지로 추가
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    try:
        # 대화 생성
        cursor.execute('''
            INSERT INTO conversations (name, model_name)
            VALUES (?, ?)
        ''', (name, model_name))
        conversation_id = cursor.lastrowid

        # 모든 프롬프트 불러오기
        prompts = get_all_prompts()

        # 각 프롬프트를 해당 대화의 초기 메시지로 저장
        for prompt in prompts:
            cursor.execute('''
                INSERT INTO messages (conversation_id, sender_type, content_type, content)
                VALUES (?, 'system', 'text', ?)
            ''', (conversation_id, prompt))

        conn.commit()
        print(f"대화 '{name}'가 생성되었습니다. (ID: {conversation_id})")
        return conversation_id
    except sqlite3.Error as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()


def get_conversation_model(conversation_id):
    """
    특정 대화에 사용된 모델 이름을 반환
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT model_name FROM conversations WHERE id = ?
    ''', (conversation_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 'GPT'

def save_prompt_setting(prompt):
    """
    prompt_settings 테이블에 프롬프트를 저장하는 함수
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO prompt_settings (prompt) VALUES (?)
    ''', (prompt,))

    conn.commit()
    conn.close()

def load_prompt_setting():
    """
    저장된 프롬프트 설정을 불러오기
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('SELECT prompt FROM prompt_settings ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None



def save_message_to_db(conversation_id, sender_type, content_type, content):
    """
    메시지를 데이터베이스에 저장
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO messages (conversation_id, sender_type, content_type, content)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, sender_type, content_type, content))

    conn.commit()
    conn.close()


def save_code_to_db(conversation_id, code_type, code_data, order_num):
    """
    코드 블록을 데이터베이스에 저장
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO code_blocks (conversation_id, code_type, code_data, order_num)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, code_type, code_data, order_num))

    conn.commit()
    conn.close()


def get_conversation_names():
    """
    데이터베이스에서 대화 목록의 이름을 가져오는 함수
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM conversations")
    conversation_names = cursor.fetchall()
    conn.close()
    return conversation_names


def get_messages(conversation_id):
    """
    특정 대화에 속한 모든 메시지를 조회하여 반환
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT sender_type, content_type, content, created_at 
        FROM messages 
        WHERE conversation_id = ? 
        ORDER BY created_at
    ''', (conversation_id,))
    messages = cursor.fetchall()

    conn.close()
    return messages


def get_code_blocks(conversation_id):
    """
    특정 대화에 속한 모든 코드 블록을 조회하여 반환
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, code_type, code_data, order_num 
        FROM code_blocks 
        WHERE conversation_id = ? 
        ORDER BY order_num
    ''', (conversation_id,))
    code_blocks = cursor.fetchall()

    conn.close()
    return code_blocks


def update_code_order(id, new_order_num):
    """
    특정 코드 블록의 순서를 업데이트
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE code_blocks
        SET order_num = ?
        WHERE id = ?
    ''', (new_order_num, id))

    conn.commit()
    conn.close()


def delete_code_from_db(id):
    """
    특정 코드 블록을 데이터베이스에서 삭제
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM code_blocks
        WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

# 코드 블럭 text 내용 변경


def update_code_data(id, code_data):
    """
    특정 코드 블록의 코드 데이터를 업데이트
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE code_blocks
        SET code_data = ?
        WHERE id = ?
    ''', (code_data, id))

    conn.commit()
    conn.close()

def update_conversation_name(id, new_name):
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE conversations
        SET name = ?
        WHERE id = ?
    ''', (new_name, id))

    conn.commit()
    conn.close()


def delete_conversation_and_related_data(conversation_id):
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM messages
        WHERE conversation_id = ?
    ''', (conversation_id, ))
    
    cursor.execute('''
        DELETE FROM code_blocks
        WHERE conversation_id = ?
    ''', (conversation_id, ))
    
    cursor.execute('''
        DELETE FROM conversations
        WHERE id = ?
    ''', (conversation_id, ))
    
    conn.commit()
    conn.close()