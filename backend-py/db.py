"""数据库层：用 SQLite 存储 Todo，就是一个文件（todos.db）"""
import sqlite3

DATABASE = 'todos.db'


def get_db(db_path=None):
    """获取数据库连接"""
    conn = sqlite3.connect(db_path or DATABASE)
    conn.row_factory = sqlite3.Row  # 让查询结果可以用字段名访问
    return conn


def init_db(db_path=None):
    """建表（如果不存在的话）"""
    conn = get_db(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            text  TEXT    NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def row_to_dict(row):
    """把数据库行转成字典，done 从 0/1 转成 bool"""
    return {
        'id': row['id'],
        'text': row['text'],
        'done': bool(row['done']),
    }


# ========== CRUD 函数 ==========

def get_all(db_path=None):
    """查全部"""
    conn = get_db(db_path)
    rows = conn.execute('SELECT * FROM todos ORDER BY id DESC').fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_by_id(todo_id, db_path=None):
    """查单个"""
    conn = get_db(db_path)
    row = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    conn.close()
    return row_to_dict(row) if row else None


def create(text, done=False, db_path=None):
    """新增"""
    conn = get_db(db_path)
    cursor = conn.execute(
        'INSERT INTO todos (text, done) VALUES (?, ?)',
        (text, 1 if done else 0),
    )
    new_id = cursor.lastrowid
    conn.commit()
    row = conn.execute('SELECT * FROM todos WHERE id = ?', (new_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def update(todo_id, text=None, done=None, db_path=None):
    """更新"""
    existing = get_by_id(todo_id, db_path)
    if not existing:
        return None
    text = text if text is not None else existing['text']
    done = done if done is not None else existing['done']
    conn = get_db(db_path)
    conn.execute(
        'UPDATE todos SET text = ?, done = ? WHERE id = ?',
        (text, 1 if done else 0, todo_id),
    )
    conn.commit()
    conn.close()
    return {'id': todo_id, 'text': text, 'done': done}


def delete(todo_id, db_path=None):
    """删除"""
    conn = get_db(db_path)
    cursor = conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
