# 05-Python后端开发指南

# Python 后端开发指南
## 技术栈
- Flask 3.1 + flask-sock（WebSocket）+ psutil（系统监控）
- SQLite3 标准库（无 ORM，直接写 SQL）
- 函数式风格
## 项目结构
```plaintext
backend-py/
├── app.py               # Flask 路由 + WebSocket 服务
├── db.py                # SQLite 数据库 CRUD 操作
├── requirements.txt     # 依赖清单
└── venv/                # 虚拟环境

```

## 启动方式
```bash
cd backend-py
python3 -m venv venv                    # 创建虚拟环境（只需一次）
source venv/bin/activate                # 激活虚拟环境
pip install -r requirements.txt         # 安装依赖（只需一次）
python app.py                           # http://localhost:3002

```

## app.py — 路由 + WebSocket
### 初始化
```python
app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
sock = Sock(app)
init_db()

```

### 请求日志
使用 Flask 的 `@app.after_request` 钩子记录每个请求：
```python
@app.after_request
def log_request(response):
    global total_requests
    total_requests += 1
    log = {'method': request.method, 'path': request.path, ...}
    broadcast({'type': 'log', 'log': log, 'totalRequests': total_requests})
    return response

```

### WebSocket 实现
使用 flask-sock 库，装饰器风格：
```python
@sock.route('/ws')
def ws_connection(ws):
    ws_clients.append(ws)
    ws.send(json.dumps({type: 'init', health, stats}))
    try:
        while True:
            ws.receive()  # 保持连接
    finally:
        ws_clients.remove(ws)

```

### 系统监控
使用 psutil 获取系统信息：
```python
import psutil

mem = psutil.virtual_memory()    # 内存信息
psutil.cpu_count()               # CPU 核心数
psutil.cpu_percent(interval=0)   # CPU 负载

```

### 后台推送线程
```python
def push_health():
    while True:
        time.sleep(5)
        if ws_clients:
            broadcast({'type': 'health', 'health': get_health_data()})

threading.Thread(target=push_health, daemon=True).start()

```

## db.py — 数据库层
使用 Python 标准库 sqlite3：
```python
import sqlite3

def get_db():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row   # 让查询结果可用字段名访问
    return conn

```

### CRUD 函数

<lark-table rows="6" cols="3" header-row="true" column-widths="244,244,244">

  <lark-tr>
    <lark-td>
      函数
    </lark-td>
    <lark-td>
      SQL
    </lark-td>
    <lark-td>
      说明
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `get_all()`
    </lark-td>
    <lark-td>
      `SELECT * FROM todos ORDER BY id DESC`
    </lark-td>
    <lark-td>
      查全部，转字典列表
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `get_by_id(id)`
    </lark-td>
    <lark-td>
      `SELECT * FROM todos WHERE id = ?`
    </lark-td>
    <lark-td>
      查单个，不存在返回 None
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `create(text, done)`
    </lark-td>
    <lark-td>
      `INSERT INTO todos (text, done) VALUES (?, ?)`
    </lark-td>
    <lark-td>
      新增
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `update(id, text, done)`
    </lark-td>
    <lark-td>
      `UPDATE todos SET text=?, done=? WHERE id=?`
    </lark-td>
    <lark-td>
      更新，支持部分更新
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `delete(id)`
    </lark-td>
    <lark-td>
      `DELETE FROM todos WHERE id = ?`
    </lark-td>
    <lark-td>
      删除
    </lark-td>
  </lark-tr>
</lark-table>

### 类型转换辅助
```python
def row_to_dict(row):
    return {
        'id': row['id'],
        'text': row['text'],
        'done': bool(row['done']),   # 0/1 → False/True
    }

```

## 依赖清单
```plaintext
flask>=3.1
flask-cors>=5.0
flask-sock>=0.7
psutil>=6.0

```

## 测试
Python 后端使用 pytest 进行单元测试。
### 测试框架
- **pytest** — Python 标准测试框架（`pytest>=8.0.0`）
- 每个测试使用独立的临时数据库（`tmp_path` fixture），互不影响
### 测试文件
```plaintext
backend-py/test_db.py    # 数据库 CRUD 单元测试（83 行）

```

### 测试内容
- CRUD 全流程测试（创建、查询、更新、删除）
- 边界情况（查不到、更新不存在的记录）
- 部分更新（只改 done 不改 text）
### db.py 可测试性改进
所有数据库函数现在支持可选的 `db_path` 参数，便于测试时使用临时数据库：
```python
# 生产环境正常调用
get_all()
create('Buy milk')

# 测试环境使用临时数据库
get_all(db_path='/tmp/test.db')
create('Buy milk', db_path='/tmp/test.db')

```

### 运行测试
```bash
cd backend-py
python -m pytest test_db.py -v

```

### CI 集成
PR 到 master 时自动运行语法检查和测试：
```bash
python -m py_compile app.py
python -m py_compile db.py
python -m pytest test_db.py -v

```

## 依赖清单
```plaintext
flask>=3.1
flask-cors>=5.0
flask-sock>=0.7
psutil>=7.0
pytest>=8.0    # 测试框架

```


