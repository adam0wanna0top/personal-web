# 06-API参考手册

# API 参考手册
两个后端（TS :3001 / Python :3002）实现完全相同的 API。
## Todo CRUD 接口
### GET /api/todos
获取所有待办事项。
响应：
```json
[
  {"id": 1, "text": "学习 Vue 3", "done": false},
  {"id": 2, "text": "写后端 API", "done": true}
]

```

### GET /api/todos/:id
获取单个待办事项。
成功响应 (200)：
```json
{"id": 1, "text": "学习 Vue 3", "done": false}

```

未找到 (404)：
```json
{"error": "未找到"}

```

### POST /api/todos
创建新待办事项。
请求体：
```json
{"text": "新待办内容", "done": false}

```

成功响应 (201)：
```json
{"id": 3, "text": "新待办内容", "done": false}

```

参数校验失败 (400)：
```json
{"error": "内容不能为空"}

```

### PUT /api/todos/:id
更新待办事项（支持部分更新）。
请求体：
```json
{"text": "修改后的内容"}

```

或：
```json
{"done": true}

```

或同时更新：
```json
{"text": "修改后的内容", "done": true}

```

成功响应：
```json
{"id": 1, "text": "修改后的内容", "done": true}

```

### DELETE /api/todos/:id
删除待办事项。
成功响应：
```json
{"success": true}

```

## 监控接口
### GET /api/health
获取系统健康指标。
响应：
```json
{
  "status": "ok",
  "uptime": 120,
  "memory": {
    "total": 16384,
    "used": 8192,
    "percent": 50
  },
  "cpu": {
    "model": "Apple M1",
    "cores": 8,
    "load": 2.5
  }
}

```

### GET /api/stats
获取请求统计和最近日志。
响应：
```json
{
  "totalRequests": 42,
  "recentLogs": [
    {"method": "GET", "path": "/api/todos", "status": 200, "time": "14:30:25"}
  ]
}

```

## WebSocket /ws
实时推送监控数据，连接后自动接收三类消息：
### init（连接时立即发送）
```json
{
  "type": "init",
  "health": { ... },
  "stats": { "totalRequests": 10, "recentLogs": [...] }
}

```

### health（每 5 秒推送）
```json
{
  "type": "health",
  "health": { "status": "ok", "uptime": 125, "memory": {...}, "cpu": {...} }
}

```

### log（有 API 请求时立即推送）
```json
{
  "type": "log",
  "log": {"method": "POST", "path": "/api/todos", "status": 201, "time": "14:30:25"},
  "totalRequests": 11
}

```

## 状态码汇总

<lark-table rows="5" cols="3" header-row="true" column-widths="244,244,244">

  <lark-tr>
    <lark-td>
      状态码
    </lark-td>
    <lark-td>
      含义
    </lark-td>
    <lark-td>
      触发场景
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      200
    </lark-td>
    <lark-td>
      成功
    </lark-td>
    <lark-td>
      GET / PUT 成功
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      201
    </lark-td>
    <lark-td>
      创建成功
    </lark-td>
    <lark-td>
      POST 创建新资源
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      400
    </lark-td>
    <lark-td>
      请求错误
    </lark-td>
    <lark-td>
      text 为空
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      404
    </lark-td>
    <lark-td>
      未找到
    </lark-td>
    <lark-td>
      id 不存在
    </lark-td>
  </lark-tr>
</lark-table>


