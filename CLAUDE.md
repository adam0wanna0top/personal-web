# CLAUDE.md — Vue 3 Starter 项目上下文

## 项目概述

Vue 3 + TypeScript 入门教学项目，包含前端和两个后端（TS/Python），帮助初学者理解前后端通信。

## 技术栈

| 层级 | 技术 | 端口 |
|------|------|------|
| 前端 | Vue 3 + TypeScript + Vite 6 | 5173 |
| TS 后端 | Express + better-sqlite3 + ws | 3001 |
| Python 后端 | Flask + flask-sock + psutil | 3002 |
| 数据库 | SQLite（零配置） | — |

## 启动命令

```bash
npm run dev                                          # 前端
cd backend-ts && npm run dev                         # TS 后端
cd backend-py && source venv/bin/activate && python app.py  # Python 后端
```

## API 快速参考

两个后端实现完全一致的 RESTful API：

```
GET    /api/todos       → 获取所有待办
POST   /api/todos       → 创建 { text, done }
PUT    /api/todos/:id   → 更新 { text?, done? }
DELETE /api/todos/:id   → 删除
GET    /api/health      → 系统指标
GET    /api/stats       → 请求统计
WS     /ws              → 实时推送（init/health/log）
```

## 代码风格

- 前端：`<script setup lang="ts">`、`<style scoped>`、ref/reactive
- TS 后端：ESM（`"type": "module"`），tsx 运行
- Python 后端：函数式，无 ORM，直接写 SQL

## 项目知识库

详细文档位于 `docs/` 目录，CLAUDE.md 只保留精简摘要。

| 文档 | 查阅场景 |
|------|---------|
| 01-项目概览 | 项目定位、功能、技术栈 |
| 02-架构设计 | 系统架构、通信方式、数据流 |
| 03-前端开发指南 | Vue 组件、开发模式 |
| 04-TS后端开发指南 | TS 后端路由、数据库操作 |
| 05-Python后端开发指南 | Python 后端路由、数据库操作 |
| 06-API参考手册 | API 变更、新增接口 |
| 07-开发环境与调试 | 环境搭建、常见问题 |
| 08-初学者教程 | 概念解释、入门指导 |
| 09-变更记录 | 版本历史 |

何时查阅：新功能开发 → 02 + 对应指南；改 API → 06；调试 → 07

更新文档：开发完成后执行 `/sync-docs`
