<!-- 根组件：Vue 单文件组件 (SFC) = <template> + <script> + <style> -->

<template>
  <div class="app">
    <h1>{{ title }}</h1>

    <!-- v-model 双向绑定 -->
    <input v-model="name" placeholder="输入你的名字" />

    <!-- 条件渲染 v-if -->
    <p v-if="name">你好，<strong>{{ name }}</strong>！欢迎学习 Vue 3</p>
    <p v-else>请在上方输入你的名字 👆</p>

    <hr />

    <!-- 列表渲染 v-for -->
    <h2>Vue 3 核心概念</h2>
    <ul>
      <li v-for="item in concepts" :key="item.name">
        <strong>{{ item.name }}</strong>：{{ item.desc }}
      </li>
    </ul>

    <hr />

    <!-- 事件绑定 @click + 计算属性 -->
    <h2>计数器示例</h2>
    <p>当前计数：<strong>{{ count }}</strong>（{{ parity }}）</p>
    <div class="btn-group">
      <button @click="count--">-1</button>
      <button @click="count++">+1</button>
      <button @click="count = 0">重置</button>
    </div>

    <hr />

    <!-- 子组件：纯前端版本 vs API 版本 -->
    <TodoList />

    <hr />

    <TodoListApi />

    <hr />

    <Monitor />
  </div>
</template>

<script setup lang="ts">
// <script setup> 是 Vue 3 的语法糖，自动暴露变量到模板

import { ref, computed } from 'vue'
import TodoList from './components/TodoList.vue'
import TodoListApi from './components/TodoListApi.vue'
import Monitor from './components/Monitor.vue'

// ref：创建响应式数据（基本类型用 ref，对象用 reactive）
const title = ref('Vue 3 + TypeScript 入门')
const name = ref('')
const count = ref(0)

// computed：计算属性，依赖变化时自动更新
const parity = computed(() => (count.value % 2 === 0 ? '偶数' : '奇数'))

// 数据列表
const concepts = ref([
  { name: 'ref / reactive', desc: '声明响应式数据' },
  { name: 'computed', desc: '计算属性，自动缓存' },
  { name: 'v-if / v-show', desc: '条件渲染' },
  { name: 'v-for', desc: '列表渲染，必须加 :key' },
  { name: 'v-model', desc: '双向数据绑定' },
  { name: '@event', desc: '事件绑定（如 @click）' },
  { name: 'props / emit', desc: '父子组件通信' },
  { name: '生命周期', desc: 'onMounted, onUnmounted 等' },
])
</script>

<style scoped>
/* scoped = 样式只作用于当前组件 */
.app {
  max-width: 640px;
  margin: 40px auto;
  font-family: system-ui, sans-serif;
  padding: 0 20px;
}

h1 { color: #42b883; }
h2 { color: #35495e; margin-top: 16px; }

input {
  width: 100%;
  padding: 8px 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
}
input:focus { outline: none; border-color: #42b883; }

.btn-group { display: flex; gap: 8px; }

button {
  padding: 6px 16px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  background: #42b883;
  color: #fff;
  cursor: pointer;
}
button:hover { background: #369e6f; }

ul { padding-left: 20px; }
li { margin: 6px 0; line-height: 1.6; }

hr { border: none; border-top: 1px solid #eee; margin: 24px 0; }
</style>
