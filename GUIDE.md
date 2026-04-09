# Vue 3 + TypeScript 入门指南

## 一、项目目录结构

```
vue3-starter/
├── index.html                  # 网页入口（Vite 以此为起点）
├── package.json                # 项目描述：依赖、脚本命令
├── vite.config.ts              # Vite 构建工具配置
├── tsconfig.json               # TypeScript 主配置
├── tsconfig.node.json          # TypeScript 针对 Node/Vite 的配置
├── node_modules/               # npm 安装的依赖包（不要手动改）
├── frontend/
│   ├── main.ts                 # JS/TS 入口：创建 Vue 应用
│   ├── App.vue                 # 根组件（第一个 Vue 组件）
│   ├── vite-env.d.ts           # 告诉 TS 什么是 .vue 文件
│   └── components/
│       └── TodoList.vue        # 子组件
```

---

## 二、每个文件是干什么的

### 1. `index.html` — 网页入口

浏览器加载的第一个文件。它只有两个关键点：

```html
<div id="app"></div>                          <!-- Vue 挂载点 -->
<script type="module" src="/frontend/main.ts"></script>  <!-- 加载 TS 入口 -->
```

- `<div id="app">` 是一个空容器，Vue 会把整个应用渲染到里面
- `type="module"` 表示用 ES Module 方式加载脚本
- Vite 开发服务器会自动处理 `.ts` 文件，你不需要手动编译

### 2. `package.json` — 项目描述

```jsonc
{
  "name": "vue3-starter",       // 项目名
  "version": "1.0.0",           // 版本号
  "private": true,              // 不发布到 npm

  // ========= 最重要的部分：脚本命令 =========
  "scripts": {
    "dev": "vite",              // npm run dev → 启动开发服务器
    "build": "vite build",      // npm run build → 打包到 dist/
    "preview": "vite preview"   // npm run preview → 预览打包结果
  },

  // ========= 依赖 =========
  "dependencies": {             // 运行时依赖（会打包进最终产物）
    "vue": "^3.5.0"
  },
  "devDependencies": {          // 开发时依赖（仅开发环境用）
    "@vitejs/plugin-vue": "^5.2.0",  // Vite 的 Vue 插件
    "typescript": "^5.7.0",          // TypeScript 编译器
    "vite": "^6.0.0",                // 构建工具
    "vue-tsc": "^2.2.0"              // Vue 的 TS 类型检查
  }
}
```

**dependencies vs devDependencies：**
- `dependencies`：用户运行时需要（如 Vue 本身）
- `devDependencies`：只有开发者才需要（编译器、打包工具等）

### 3. `vite.config.ts` — 构建工具配置

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],   // 注册 Vue 插件，让 Vite 能处理 .vue 文件
})
```

**Vite 是什么？** 一个超快的开发服务器 + 构建工具。它做的事情：
- 开发时：按需编译，改了代码浏览器瞬间热更新
- 打包时：把 TS、Vue、CSS 编译成浏览器能直接运行的 JS/CSS

### 4. `tsconfig.json` — TypeScript 配置

```jsonc
{
  "compilerOptions": {
    "target": "ES2020",           // 编译成哪个 JS 版本
    "module": "ESNext",           // 使用最新模块系统
    "moduleResolution": "bundler",// 模块解析策略（Vite 场景用 bundler）
    "strict": true,               // 开启所有严格检查（推荐！）
    "lib": ["ES2020", "DOM"],     // 可用的类型库（DOM = 浏览器 API）
    "noEmit": true,               // 不输出文件（Vite 负责编译）
    "paths": {
      "@/*": ["./frontend/*"]          // 路径别名：import xx from '@/components/Foo'
    }
  },
  "include": ["frontend/**/*.ts", "frontend/**/*.vue"]  // 哪些文件参与 TS 检查
}
```

### 5. `tsconfig.node.json` — Vite 配置的 TS 环境

`tsconfig.json` 通过 `references` 引用它，专门给 `vite.config.ts` 提供类型检查。

### 6. `frontend/main.ts` — 应用入口

```ts
import { createApp } from 'vue'   // 从 Vue 库导入 createApp 函数
import App from './App.vue'        // 导入根组件

createApp(App).mount('#app')       // 创建应用 → 挂载到 index.html 的 #app
```

**执行流程：** `index.html` → 加载 `main.ts` → 创建 Vue 应用 → 渲染 `App.vue`

### 7. `frontend/vite-env.d.ts` — 类型声明

```ts
declare module '*.vue' { ... }
```

因为 TypeScript 默认不认识 `.vue` 文件，这个文件告诉 TS："`.vue` 文件导出的是一个 Vue 组件"。

---

## 三、.vue 文件（单文件组件 SFC）

这是 Vue 的核心概念。每个 `.vue` 文件由三部分组成：

```
┌─────────────────────────┐
│  <template>             │  ← HTML 模板（页面结构）
│    <div>...</div>       │
│  </template>            │
├─────────────────────────┤
│  <script setup lang="ts">│ ← TS 逻辑（数据、方法）
│    const count = ref(0) │
│  </script>              │
├─────────────────────────┤
│  <style scoped>         │  ← CSS 样式（scoped = 只作用于此组件）
│    h1 { color: red; }   │
│  </style>               │
└─────────────────────────┘
```

**`<script setup>` 是什么？**
- Vue 3 的语法糖，比传统的 `export default { ... }` 更简洁
- 里面声明的变量、函数自动可在 `<template>` 中使用
- 推荐所有新代码都用 `<script setup>`

---

## 四、Vue 3 核心 API 速查

### 响应式数据

```ts
import { ref, reactive } from 'vue'

// ref：用于基本类型（string, number, boolean）
const count = ref(0)
count.value++          // JS 中用 .value 读写
// 模板中直接用 {{ count }}，不需要 .value

// reactive：用于对象
const user = reactive({ name: 'Tom', age: 20 })
user.name = 'Jerry'    // 直接读写属性
```

### 计算属性

```ts
import { computed } from 'vue'

const count = ref(5)
const doubled = computed(() => count.value * 2)  // 依赖变化时自动重算
```

### 模板指令

| 指令 | 作用 | 示例 |
|------|------|------|
| `v-if` / `v-else` | 条件渲染（DOM 会移除） | `<p v-if="show">可见</p>` |
| `v-show` | 条件显示（CSS display 切换） | `<p v-show="show">可见</p>` |
| `v-for` | 循环渲染列表 | `<li v-for="item in list" :key="item.id">` |
| `v-model` | 双向绑定 | `<input v-model="name" />` |
| `v-bind` (缩写 `:`) | 绑定属性 | `<img :src="url" />` |
| `v-on` (缩写 `@`) | 绑定事件 | `<button @click="fn">` |

### 生命周期

```ts
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  console.log('组件挂载完成，可以操作 DOM')
})

onUnmounted(() => {
  console.log('组件卸载，清理定时器等')
})
```

### 父子组件通信

```ts
// 子组件：接收父组件传来的数据
const props = defineProps<{
  title: string
  count: number
}>()

// 子组件：向父组件发送事件
const emit = defineEmits<{
  (e: 'update', value: string): void
}>()
emit('update', '新值')
```

```html
<!-- 父组件使用子组件 -->
<ChildComponent title="Hello" :count="5" @update="handleUpdate" />
```

---

## 五、如何启动

```bash
# 1. 进入项目目录
cd vue3-starter

# 2. 安装依赖（只需要第一次，已经装过了可跳过）
npm install

# 3. 启动开发服务器
npm run dev
```

启动后会看到类似输出：

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

打开浏览器访问 `http://localhost:5173/` 即可看到页面。

**其他命令：**

| 命令 | 作用 |
|------|------|
| `npm run dev` | 启动开发服务器（支持热更新） |
| `npm run build` | 打包到 `dist/` 目录（用于部署） |
| `npm run preview` | 本地预览打包后的效果 |

---

## 六、开发流程

```
1. 修改 .vue 文件 → 保存 → 浏览器自动刷新（热更新）
2. 新建组件 → 在父组件中 import → 使用
3. 出错了 → 看浏览器控制台（F12）或终端的错误提示
```

**新建组件的步骤：**

```
1. 在 frontend/components/ 下创建 XxxView.vue
2. 写好 <template> <script setup> <style scoped>
3. 在需要用的父组件中：import XxxView from './components/XxxView.vue'
4. 在父组件模板中直接写：<XxxView />
```

---

## 七、下一步学习建议

1. **改改现有代码** — 修改 `App.vue` 中的数据，体验响应式更新
2. **新建组件** — 在 `components/` 下创建自己的组件
3. **学 Vue Router** — 多页面路由：`npm install vue-router`
4. **学 Pinia** — 全局状态管理：`npm install pinia`
5. **官方文档** — https://cn.vuejs.org/ （中文，写得很好）
