// Express 服务器 + WebSocket：API 路由 + 实时推送监控数据
import express from 'express'
import cors from 'cors'
import os from 'os'
import http from 'http'
import { WebSocketServer, WebSocket } from 'ws'
import { todoDb } from './db.js'

const app = express()
const PORT = 3001
const startTime = Date.now()

// ========== 请求日志 & 计数 ==========
interface LogEntry { method: string; path: string; status: number; time: string }
const requestLogs: LogEntry[] = []
let totalRequests = 0

app.use(cors({ origin: 'http://localhost:5173' }))
app.use(express.json())

// 记录每个请求的中间件
app.use((req, res, next) => {
  totalRequests++
  res.on('finish', () => {
    const log: LogEntry = {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      time: new Date().toLocaleTimeString(),
    }
    requestLogs.unshift(log)
    if (requestLogs.length > 50) requestLogs.length = 50

    // 有新请求时，立刻通过 WebSocket 推送给所有监控客户端
    broadcast({ type: 'log', log, totalRequests })
  })
  next()
})

// ========== Todo API 路由 ==========

app.get('/api/todos', (_req, res) => {
  res.json(todoDb.getAll())
})

app.get('/api/todos/:id', (req, res) => {
  const todo = todoDb.getById(Number(req.params.id))
  if (!todo) return res.status(404).json({ error: '未找到' })
  res.json(todo)
})

app.post('/api/todos', (req, res) => {
  const { text } = req.body
  if (!text?.trim()) return res.status(400).json({ error: '内容不能为空' })
  const todo = todoDb.create(text.trim(), req.body.done)
  res.status(201).json(todo)
})

app.put('/api/todos/:id', (req, res) => {
  const todo = todoDb.update(Number(req.params.id), req.body)
  if (!todo) return res.status(404).json({ error: '未找到' })
  res.json(todo)
})

app.delete('/api/todos/:id', (req, res) => {
  if (!todoDb.remove(Number(req.params.id))) {
    return res.status(404).json({ error: '未找到' })
  }
  res.json({ success: true })
})

// ========== 监控 HTTP API（保留，用于初始加载）==========

function getHealthData() {
  const totalMem = os.totalmem()
  const freeMem = os.freemem()
  return {
    status: 'ok',
    uptime: Math.floor((Date.now() - startTime) / 1000),
    memory: {
      total: Math.round(totalMem / 1024 / 1024),
      used: Math.round((totalMem - freeMem) / 1024 / 1024),
      percent: Math.round((1 - freeMem / totalMem) * 100),
    },
    cpu: {
      model: os.cpus()[0]?.model ?? 'unknown',
      cores: os.cpus().length,
      load: Math.round(os.loadavg()[0] * 100) / 100,
    },
  }
}

app.get('/api/health', (_req, res) => res.json(getHealthData()))
app.get('/api/stats', (_req, res) => res.json({ totalRequests, recentLogs: requestLogs.slice(0, 20) }))

// ========== WebSocket：实时推送监控数据 ==========

const server = http.createServer(app)
const wss = new WebSocketServer({ server, path: '/ws' })

// 广播消息给所有连接的客户端
function broadcast(data: object) {
  const msg = JSON.stringify(data)
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg)
    }
  })
}

wss.on('connection', (ws) => {
  console.log('监控客户端已连接 (WebSocket)')

  // 连接时先发一次当前状态
  ws.send(JSON.stringify({
    type: 'init',
    health: getHealthData(),
    stats: { totalRequests, recentLogs: requestLogs.slice(0, 20) },
  }))

  ws.on('close', () => console.log('监控客户端已断开'))
})

// 每 5 秒推送一次系统资源数据
setInterval(() => {
  if (wss.clients.size > 0) {
    broadcast({ type: 'health', health: getHealthData() })
  }
}, 5000)

// 启动
server.listen(PORT, () => {
  console.log(`TypeScript 后端已启动 → http://localhost:${PORT}`)
  console.log(`WebSocket 监控 → ws://localhost:${PORT}/ws`)
})
