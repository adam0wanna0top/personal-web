# Vue 3 + TypeScript 入门实战

一个帮助初学者理解**前后端如何通信**的教学项目。包含一个 Vue 3 前端和两个功能完全等价的后端（TypeScript / Python），让你在对比中学习。

## 功能一览

| 功能 | 说明 | 涉及知识点 |
|------|------|-----------|
| 计数器 + 双向绑定 | 输入名字、加减计数 | `ref`、`computed`、`v-model`、`v-if`、`v-for` |
| 本地待办事项 | 纯前端，数据存在内存 | 组件化、响应式数组操作 |
| API 待办事项 | 通过 `fetch()` 调用后端 CRUD | REST API、JSON、`onMounted` |
| 后端切换 | 下拉框一键切换 TS / Python 后端 | 同一套 API，不同实现 |
| 实时监控面板 | WebSocket 推送 CPU / 内存 / 请求日志 | WebSocket、断线重连、实时数据流 |

## 技术栈

```
前端：Vue 3.5 + TypeScript 5.7 + Vite 6
TS 后端：Express 4 + better-sqlite3 + ws（WebSocket）
Python 后端：Flask 3.1 + flask-sock + psutil
数据库：SQLite（零配置，数据存为本地文件）
```

## 项目结构

```
vue3-starter/
├── index.html                     # 入口 HTML
├── package.json                   # 前端依赖
├── vite.config.ts                 # Vite 配置
├── tsconfig.json                  # TypeScript 配置
│
├── frontend/                      # 前端源码
│   ├── main.ts                    # 应用入口，挂载 Vue 实例
│   ├── App.vue                    # 根组件（计数器 + 概念列表）
│   └── components/
│       ├── TodoList.vue           # 待办事项（纯前端版，无网络请求）
│       ├── TodoListApi.vue        # 待办事项（API 版，连接后端）
│       └── Monitor.vue            # 系统监控面板（WebSocket 实时数据）
│
├── backend-ts/                    # TypeScript 后端
│   ├── package.json               # ESM 模式，tsx 运行
│   ├── tsconfig.json
│   └── src/
│       ├── index.ts               # Express 路由 + WebSocket 服务
│       └── db.ts                  # SQLite 数据库 CRUD 操作
│
└── backend-py/                    # Python 后端
    ├── requirements.txt           # Flask 等依赖
    ├── app.py                     # Flask 路由 + WebSocket 服务
    └── db.py                      # SQLite 数据库 CRUD 操作
```

## 快速开始

### 前端

```bash
npm install
npm run dev
# 打开 http://localhost:5173
```

### TypeScript 后端

```bash
cd backend-ts
npm install
npm run dev
# 启动在 http://localhost:3001
# WebSocket 监控：ws://localhost:3001/ws
```

### Python 后端

```bash
cd backend-py

# 创建虚拟环境（只需一次）
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动
python app.py
# 启动在 http://localhost:3002
# WebSocket 监控：ws://localhost:3002/ws
```

> 两个后端可以同时启动，前端通过下拉框自由切换。

## API 接口

两个后端实现完全相同的 RESTful API：

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| `GET` | `/api/todos` | 获取所有待办 | — | `[{id, text, done}]` |
| `GET` | `/api/todos/:id` | 获取单个 | — | `{id, text, done}` |
| `POST` | `/api/todos` | 新建待办 | `{text, done?}` | `{id, text, done}` (201) |
| `PUT` | `/api/todos/:id` | 更新待办 | `{text?, done?}` | `{id, text, done}` |
| `DELETE` | `/api/todos/:id` | 删除待办 | — | `{success: true}` |

监控相关：

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/health` | 系统指标（内存、CPU、运行时间） |
| `GET` | `/api/stats` | 请求统计和最近日志 |
| WebSocket | `/ws` | 实时推送（`init` / `health` / `log`） |

### 数据库表结构

```sql
CREATE TABLE todos (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0   -- SQLite 用 0/1 表示布尔值
);
```

## 核心知识点

### 前后端通信的两种方式

本项目同时演示了两种通信方式，方便对比学习：

**REST（HTTP 请求）** — TodoListApi 组件使用

```
浏览器                               服务器
  │  GET /api/todos  ──────────→    │
  │  ←───── [{...}, {...}]  ──────  │
  │  POST /api/todos ──────────→    │
  │  ←───── {id: 1, ...}  ────────  │
```

- 前端主动发请求，后端被动响应
- 适合 CRUD 操作（增删改查）
- 代码中的 `fetch()` 就是浏览器内置的 HTTP 请求工具

**WebSocket（长连接）** — Monitor 组件使用

```
浏览器                               服务器
  │  ──── 建立连接 ────────────→    │
  │  ←──── init (初始数据)  ──────  │
  │  ←──── health (每5秒)  ───────  │
  │  ←──── log (有请求时)  ────────  │
  │  ←──── health (每5秒)  ───────  │
  │  ...                            │
```

- 一次连接，后端可以**主动推送**数据
- 适合实时场景（监控、聊天、通知）
- 断线后自动重连（Monitor.vue 中实现了 3 秒重连）

### CORS（跨域资源共享）

前端跑在 `localhost:5173`，后端跑在 `localhost:3001` / `3002`，端口不同就是"跨域"。两个后端都配置了 CORS 允许前端访问：

```typescript
// TS 后端 (index.ts)
app.use(cors({ origin: 'http://localhost:5173' }))
```

```python
# Python 后端 (app.py)
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
```

### 两个后端为什么 API 完全一样？

这是故意设计的——同一套 API 用两种语言实现，方便你：

1. 选择自己熟悉的语言阅读后端代码
2. 对比 TypeScript 和 Python 的语法差异
3. 理解 API 是一种**契约**，与实现语言无关

## 常见问题

**Q: 启动前端后页面空白或报错？**

确认已经运行 `npm install` 安装依赖。

**Q: API 版待办事项显示"无法连接后端"？**

需要先启动至少一个后端（TS 或 Python），前端才能拿到数据。

**Q: Python 后端启动报错 `ModuleNotFoundError`？**

确保已激活虚拟环境并安装依赖：

```bash
cd backend-py
source venv/bin/activate
pip install -r requirements.txt
```

**Q: 切换后端后数据不一样？**

两个后端各自使用独立的 `todos.db` 文件，数据互不共享。

**Q: 监控面板显示"离线"？**

对应的后端未启动。启动后前端会自动重连（3 秒后）。

## 学习路线建议

1. 先读 `src/App.vue`，理解 Vue 3 基础语法
2. 读 `src/components/TodoList.vue`，理解纯前端组件
3. 读 `src/components/TodoListApi.vue`，理解如何调用后端 API
4. 选一个后端（TS 或 Python），跟踪一个完整的 CRUD 请求流程
5. 读 `src/components/Monitor.vue`，理解 WebSocket 实时通信
6. 尝试自己添加功能（如：编辑待办文本、添加优先级、搜索过滤）
