<!-- 纯前端版本：数据存在浏览器内存，刷新即丢失，无网络请求 -->

<template>
  <h2>待办事项（本地版本）</h2>
  <p class="hint">数据存在浏览器内存中，刷新页面会丢失，无网络请求</p>

  <form @submit.prevent="addTodo">
    <input v-model="newTodo" placeholder="添加新待办..." />
    <button type="submit">添加</button>
  </form>

  <ul class="todo-list">
    <li v-for="todo in todos" :key="todo.id" :class="{ done: todo.done }">
      <input type="checkbox" v-model="todo.done" />
      <span>{{ todo.text }}</span>
      <button class="del" @click="removeTodo(todo.id)">✕</button>
    </li>
  </ul>

  <p class="summary">共 {{ todos.length }} 项，已完成 {{ doneCount }} 项</p>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Todo {
  id: number
  text: string
  done: boolean
}

let nextId = 0
const newTodo = ref('')
const todos = ref<Todo[]>([])

function addTodo() {
  const text = newTodo.value.trim()
  if (!text) return
  todos.value.push({ id: nextId++, text, done: false })
  newTodo.value = ''
}

function removeTodo(id: number) {
  todos.value = todos.value.filter(t => t.id !== id)
}

const doneCount = computed(() => todos.value.filter(t => t.done).length)
</script>

<style scoped>
.hint { color: #999; font-size: 13px; margin-top: 0; }

form { display: flex; gap: 8px; margin-bottom: 12px; }
form input { flex: 1; }

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
</style>
