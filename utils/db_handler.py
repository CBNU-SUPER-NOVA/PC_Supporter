# utils/db_handler.py
import sqlite3

def init_db():
    """
    데이터베이스를 초기화하고 필요한 테이블을 생성
    """
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    
    # 대화 메타데이터 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 코드 블록 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            code TEXT,
            language TEXT,
            order_num INTEGER,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        )
    ''')

    conn.commit()
    conn.close()

def create_conversation(name):
    """
    새로운 대화를 생성하고, 생성된 대화의 ID를 반환
    """
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO conversations (name)
        VALUES (?)
    ''', (name,))

    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    
    return conversation_id

def save_code_to_db(conversation_id, code, language, order_num):
    """
    코드 블록을 데이터베이스에 저장
    """
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO code_blocks (conversation_id, code, language, order_num)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, code, language, order_num))
    
    conn.commit()
    conn.close()

def update_code_order(id, new_order_num):
    """
    특정 코드 블록의 순서를 업데이트
    """
    conn = sqlite3.connect('workflow.db')
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
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM code_blocks
        WHERE id = ?
    ''', (id,))
    
    conn.commit()
    conn.close()

def get_conversations():
    """
    모든 대화를 조회하여 반환
    """
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, created_at FROM conversations')
    conversations = cursor.fetchall()
    
    conn.close()
    return conversations

def get_code_blocks(conversation_id):
    """
    특정 대화에 속한 모든 코드 블록을 조회하여 반환
    """
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, code, language, order_num 
        FROM code_blocks 
        WHERE conversation_id = ? 
        ORDER BY order_num
    ''', (conversation_id,))
    code_blocks = cursor.fetchall()
    
    conn.close()
    return code_blocks

# def query_db():
#     conn = sqlite3.connect('workflow.db')
#     cursor = conn.cursor()

#     # conversations 테이블 조회
#     cursor.execute('SELECT * FROM conversations')
#     conversations = cursor.fetchall()
#     print("Conversations:")
#     for row in conversations:
#         print(row)

#     # code_blocks 테이블 조회
#     cursor.execute('SELECT * FROM code_blocks')
#     code_blocks = cursor.fetchall()
#     print("\nCode Blocks:")
#     for row in code_blocks:
#         print(row)

#     conn.close()

# if __name__ == "__main__":
#     query_db()