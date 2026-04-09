# CLAUDE.md — Vue 3 Starter 项目上下文

## 项目概述

Vue 3 + TypeScript 入门教学项目，包含前端和两个后端（TS/Python），目的是帮助初学者理解前后端如何通信。

## 技术栈

- **前端**：Vue 3 + TypeScript + Vite 6（端口 5173）
- **TS 后端**：Express + better-sqlite3（端口 3001）
- **Python 后端**：Flask + SQLite（端口 3002）
- **数据库**：SQLite（零配置，文件型数据库）

## 常用命令

```bash
# 前端
npm run dev              # http://localhost:5173

# TS 后端
cd backend-ts && npm run dev   # http://localhost:3001

# Python 后端（需先建虚拟环境）
cd backend-py && source venv/bin/activate && python app.py  # http://localhost:3002
```

## 项目结构

```
├── src/                          # 前端
│   ├── main.ts
│   ├── App.vue
│   └── components/
│       └── TodoList.vue          # 用 fetch() 调后端 API，可切换 TS/Python 后端
├── backend-ts/                   # TypeScript 后端（Express + SQLite）
│   └── src/
│       ├── index.ts              # 路由定义
│       └── db.ts                 # 数据库操作
└── backend-py/                   # Python 后端（Flask + SQLite）
    ├── app.py                    # 路由定义
    ├── db.py                     # 数据库操作
    └── requirements.txt
```

## API（两个后端完全一致）

```
GET    /api/todos       → 获取所有待办
POST   /api/todos       → 创建 { text, done }
PUT    /api/todos/:id   → 更新 { text?, done? }
DELETE /api/todos/:id   → 删除
```

## 代码风格

- 前端：`<script setup lang="ts">`、`<style scoped>`、ref/reactive
- TS 后端：ESM（`"type": "module"`），tsx 运行
- Python 后端：函数式，无 ORM，直接写 SQL

## 教学文档

`GUIDE.md` 包含完整入门指南：目录结构说明、配置文件解释、Vue 3 API 速查、启动方法。
