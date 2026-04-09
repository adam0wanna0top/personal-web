<!-- 子组件：演示前端如何通过 fetch() 与后端 API 通信 -->

<template>
  <h2>待办事项（API 版本）</h2>

  <!-- 后端选择器：切换 TS / Python 后端 -->
  <div class="backend-selector">
    <label>后端：</label>
    <select v-model="apiBase" @change="loadTodos">
      <option value="http://localhost:3001/api">TypeScript (Express) :3001</option>
      <option value="http://localhost:3002/api">Python (Flask) :3002</option>
    </select>
    <span class="status" :class="msgType">{{ msg }}</span>
  </div>

  <!-- 表单提交 -->
  <form @submit.prevent="addTodo">
    <input v-model="newTodo" placeholder="添加新待办..." :disabled="loading" />
    <button type="submit" :disabled="loading">{{ loading ? '...' : '添加' }}</button>
  </form>

  <!-- 列表 -->
  <ul class="todo-list" v-if="!loading">
    <li v-for="todo in todos" :key="todo.id" :class="{ done: todo.done }">
      <input type="checkbox" v-model="todo.done" @change="toggleTodo(todo)" />
      <span>{{ todo.text }}</span>
      <button class="del" @click="removeTodo(todo.id)">✕</button>
    </li>
  </ul>
  <p v-else class="loading">加载中...</p>

  <p class="summary">共 {{ todos.length }} 项，已完成 {{ doneCount }} 项</p>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// ========== 类型定义 ==========
interface Todo {
  id: number
  text: string
  done: boolean
}

// ========== 状态 ==========
const apiBase = ref('http://localhost:3001/api')  // API 地址，可切换
const newTodo = ref('')
const todos = ref<Todo[]>([])
const loading = ref(false)
const msg = ref('')
const msgType = ref('')

// 显示提示信息（3秒后消失）
function showMsg(text: string, type: string) {
  msg.value = text
  msgType.value = type
  setTimeout(() => { msg.value = '' }, 3000)
}

// ========== API 调用（fetch） ==========

// 加载全部
async function loadTodos() {
  loading.value = true
  try {
    // fetch(地址) → 发 GET 请求 → 拿到响应 → 解析 JSON
    const res = await fetch(`${apiBase.value}/todos`)
    todos.value = await res.json()
    showMsg('已连接', 'success')
  } catch {
    showMsg('无法连接后端', 'error')
  } finally {
    loading.value = false
  }
}

// 添加
async function addTodo() {
  const text = newTodo.value.trim()
  if (!text) return
  try {
    // POST 请求：method + headers + body
    const res = await fetch(`${apiBase.value}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    const todo: Todo = await res.json()
    todos.value.unshift(todo)
    newTodo.value = ''
  } catch {
    showMsg('添加失败', 'error')
  }
}

// 切换完成状态
async function toggleTodo(todo: Todo) {
  try {
    // PUT 请求：更新数据
    await fetch(`${apiBase.value}/todos/${todo.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: todo.done }),
    })
  } catch {
    todo.done = !todo.done  // 失败时回滚
    showMsg('更新失败', 'error')
  }
}

// 删除
async function removeTodo(id: number) {
  try {
    // DELETE 请求
    await fetch(`${apiBase.value}/todos/${id}`, { method: 'DELETE' })
    todos.value = todos.value.filter(t => t.id !== id)
  } catch {
    showMsg('删除失败', 'error')
  }
}

// 计算属性
const doneCount = computed(() => todos.value.filter(t => t.done).length)

// 组件挂载时自动加载数据
onMounted(loadTodos)
</script>

<style scoped>
form { display: flex; gap: 8px; margin-bottom: 12px; }
form input { flex: 1; }

.backend-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}
.backend-selector select {
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
.status { margin-left: auto; font-size: 12px; }
.status.success { color: #27ae60; }
.status.error { color: #e74c3c; }

.todo-list { list-style: none; padding: 0; }
.todo-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
}
.todo-list li.done span { text-decoration: line-through; color: #999; }

.del {
  background: #e74c3c;
  padding: 2px 8px;
  font-size: 12px;
}
.del:hover { background: #c0392b; }

.summary { color: #888; font-size: 14px; }
.loading { color: #888; text-align: center; padding: 20px; }
</style>
