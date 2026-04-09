<!-- 监控面板：通过 WebSocket 实时接收后端推送的监控数据 -->
<!-- 对比轮询：不用定时去问后端，后端有新数据会主动推过来 -->

<template>
  <h2>系统监控面板（WebSocket）</h2>

  <!-- 服务状态卡片 -->
  <div class="cards">
    <div v-for="s in services" :key="s.name" class="card">
      <span class="dot" :class="s.online ? 'green' : 'red'"></span>
      <div>
        <strong>{{ s.name }}</strong>
        <span class="port">:{{ s.port }}</span>
      </div>
      <div v-if="s.online" class="info">
        运行 {{ formatUptime(s.uptime) }}
      </div>
      <div v-else class="info offline">离线</div>
    </div>
  </div>

  <!-- 系统资源 -->
  <div class="resources" v-if="tsHealth || pyHealth">
    <div class="bar-group">
      <label>内存使用：{{ (tsHealth || pyHealth)?.memory.percent }}%</label>
      <div class="bar">
        <div class="bar-fill mem" :style="{ width: (tsHealth || pyHealth)?.memory.percent + '%' }"></div>
      </div>
      <span class="bar-text">{{ (tsHealth || pyHealth)?.memory.used }} / {{ (tsHealth || pyHealth)?.memory.total }} MB</span>
    </div>
    <div class="bar-group">
      <label>CPU 负载：{{ (tsHealth || pyHealth)?.cpu.load }}</label>
      <div class="bar">
        <div class="bar-fill cpu" :style="{ width: Math.min((tsHealth || pyHealth)?.cpu.load || 0, 100) + '%' }"></div>
      </div>
      <span class="bar-text">{{ (tsHealth || pyHealth)?.cpu.cores }} 核心</span>
    </div>
  </div>

  <!-- 请求日志 -->
  <h3>API 请求日志 <span class="ws-badge">实时</span></h3>
  <div class="tabs">
    <button :class="{ active: logTab === 'ts' }" @click="logTab = 'ts'">TypeScript :3001</button>
    <button :class="{ active: logTab === 'py' }" @click="logTab = 'py'">Python :3002</button>
  </div>
  <p class="log-summary">共 {{ (logTab === 'ts' ? tsStats : pyStats)?.totalRequests || 0 }} 次请求</p>
  <table class="log-table" v-if="currentLogs.length">
    <thead>
      <tr><th>方法</th><th>路径</th><th>状态码</th><th>时间</th></tr>
    </thead>
    <tbody>
      <tr v-for="(log, i) in currentLogs" :key="i">
        <td><span class="method" :class="log.method.toLowerCase()">{{ log.method }}</span></td>
        <td>{{ log.path }}</td>
        <td><span :class="statusClass(log.status)">{{ log.status }}</span></td>
        <td>{{ log.time }}</td>
      </tr>
    </tbody>
  </table>
  <p v-else class="no-logs">暂无请求记录</p>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ========== 类型 ==========
interface HealthInfo {
  status: string
  uptime: number
  memory: { total: number; used: number; percent: number }
  cpu: { model: string; cores: number; load: number }
}
interface LogEntry { method: string; path: string; status: number; time: string }
interface StatsInfo { totalRequests: number; recentLogs: LogEntry[] }
interface Service {
  name: string
  port: number
  wsUrl: string
  online: boolean
  uptime: number
}

// ========== 状态 ==========
const services = ref<Service[]>([
  { name: 'TS 后端 (Express)', port: 3001, wsUrl: 'ws://localhost:3001/ws', online: false, uptime: 0 },
  { name: 'Python 后端 (Flask)', port: 3002, wsUrl: 'ws://localhost:3002/ws', online: false, uptime: 0 },
])

const tsHealth = ref<HealthInfo | null>(null)
const pyHealth = ref<HealthInfo | null>(null)
const tsStats = ref<StatsInfo>({ totalRequests: 0, recentLogs: [] })
const pyStats = ref<StatsInfo>({ totalRequests: 0, recentLogs: [] })
const logTab = ref<'ts' | 'py'>('ts')

const currentLogs = computed(() => (logTab.value === 'ts' ? tsStats.value : pyStats.value)?.recentLogs || [])

// ========== WebSocket 连接 ==========

// 为每个后端建立 WebSocket 连接
function connectWebSocket(service: Service) {
  const ws = new WebSocket(service.wsUrl)

  ws.onopen = () => {
    service.online = true
    console.log(`WebSocket 已连接：${service.name}`)
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    const isTs = service.port === 3001

    switch (data.type) {
      // 初始连接时，后端一次性发送当前所有数据
      case 'init':
        if (isTs) {
          tsHealth.value = data.health
          tsStats.value = data.stats
        } else {
          pyHealth.value = data.health
          pyStats.value = data.stats
        }
        service.uptime = data.health.uptime
        break

      // 后端每 5 秒推送一次系统资源
      case 'health':
        if (isTs) tsHealth.value = data.health
        else pyHealth.value = data.health
        service.uptime = data.health.uptime
        break

      // 每当有 API 请求发生，后端立刻推送一条日志
      case 'log':
        if (isTs) {
          tsStats.value.totalRequests = data.totalRequests
          tsStats.value.recentLogs.unshift(data.log)
          if (tsStats.value.recentLogs.length > 20) tsStats.value.recentLogs.length = 20
        } else {
          pyStats.value.totalRequests = data.totalRequests
          pyStats.value.recentLogs.unshift(data.log)
          if (pyStats.value.recentLogs.length > 20) pyStats.value.recentLogs.length = 20
        }
        break
    }
  }

  ws.onclose = () => {
    service.online = false
    // 断线后 3 秒自动重连
    setTimeout(() => connectWebSocket(service), 3000)
  }

  ws.onerror = () => ws.close()

  return ws
}

let sockets: WebSocket[] = []

// ========== 工具函数 ==========
function formatUptime(seconds: number) {
  if (seconds < 60) return `${seconds}秒`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}分${seconds % 60}秒`
  return `${Math.floor(seconds / 3600)}时${Math.floor((seconds % 3600) / 60)}分`
}

function statusClass(code: number) {
  if (code < 300) return 'status-ok'
  if (code < 400) return 'status-warn'
  return 'status-err'
}

onMounted(() => {
  // 对比之前的轮询方式：
  // 旧：setInterval(() => fetch('/api/health'), 5000)  → 每 5 秒发 HTTP 请求
  // 新：new WebSocket('ws://...')                       → 一次连接，后端主动推
  sockets = services.value.map(s => connectWebSocket(s))
})

onUnmounted(() => {
  sockets.forEach(ws => ws.close())
})
</script>

<style scoped>
h2 { color: #35495e; }
h3 { color: #35495e; margin-top: 20px; }

.ws-badge {
  font-size: 11px;
  background: #9b59b6;
  color: #fff;
  padding: 2px 6px;
  border-radius: 3px;
  vertical-align: middle;
}

.cards {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}
.card {
  flex: 1;
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot.green { background: #27ae60; box-shadow: 0 0 6px #27ae60; }
.dot.red { background: #e74c3c; box-shadow: 0 0 6px #e74c3c; }
.port { color: #888; font-size: 13px; }
.info { font-size: 13px; color: #666; margin-left: auto; }
.info.offline { color: #e74c3c; }

.resources { margin-bottom: 16px; }
.bar-group { margin: 8px 0; }
.bar-group label { font-size: 14px; color: #333; }
.bar {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  margin: 4px 0;
  overflow: hidden;
}
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.bar-fill.mem { background: linear-gradient(90deg, #42b883, #f39c12); }
.bar-fill.cpu { background: linear-gradient(90deg, #3498db, #9b59b6); }
.bar-text { font-size: 12px; color: #888; }

.tabs { display: flex; gap: 8px; margin-bottom: 8px; }
.tabs button {
  padding: 4px 12px;
  font-size: 13px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}
.tabs button.active { background: #42b883; color: #fff; border-color: #42b883; }
.log-summary { font-size: 13px; color: #888; margin: 4px 0 8px; }

.log-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.log-table th {
  text-align: left;
  padding: 6px 8px;
  background: #f5f5f5;
  border-bottom: 2px solid #ddd;
}
.log-table td {
  padding: 5px 8px;
  border-bottom: 1px solid #eee;
}
.method {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: bold;
  color: #fff;
}
.method.get { background: #27ae60; }
.method.post { background: #f39c12; }
.method.put { background: #3498db; }
.method.delete { background: #e74c3c; }
.method.options { background: #888; }

.status-ok { color: #27ae60; }
.status-warn { color: #f39c12; }
.status-err { color: #e74c3c; }
.no-logs { color: #888; font-size: 13px; }
</style>
