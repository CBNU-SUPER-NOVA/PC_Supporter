import sqlite3

def init_db():
    """
    데이터베이스를 초기화하고 필요한 테이블을 생성
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()
    
    # 대화 메타데이터 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 메시지 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            sender_type TEXT CHECK(sender_type IN ('ai', 'user')),
            content_type TEXT CHECK(content_type IN ('text', 'code')),
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

    conn.commit()
    conn.close()

def create_conversation(name):
    """
    새로운 대화를 생성하고, 생성된 대화의 ID를 반환
    """
    conn = sqlite3.connect('PC_Supporter.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO conversations (name)
        VALUES (?)
    ''', (name,))

    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    
    return conversation_id

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
