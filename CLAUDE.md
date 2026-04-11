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

## 飞书知识库集成

本项目使用飞书知识库作为详细文档中心，CLAUDE.md 只保留精简摘要，详细内容在知识库中。

**知识库信息：**
- Space ID: `7627434554577013717`
- Root Node: `CkKVwTsC8iFejqkehrYcrxZEn9b`

**知识库文档索引（查询时使用对应 doc_id）：**

| 文档 | doc_id | 查询场景 |
|------|--------|---------|
| 01-项目概览 | `SwjwdffWho9BXwxC790cRROjne8` | 了解项目定位、功能、技术栈 |
| 02-架构设计 | `O7LAd3rPDoqxxVxnlmhczSV3nod` | 理解系统架构、通信方式、数据流 |
| 03-前端开发指南 | `UC8Md3fNeoMSv1xtCYZcDPbNnbc` | 编辑 Vue 组件、查组件模式 |
| 04-TS后端开发指南 | `CJx9drLfUoaCVExq2JkcHAgVnBg` | 修改 TS 后端、查路由/数据库操作 |
| 05-Python后端开发指南 | `GdZidl9HhoBLYxxRbZTcVwabnYb` | 修改 Python 后端 |
| 06-API参考手册 | `RYQcdASkXo8fw7xgguucLc7gnNb` | 涉及 API 变更、新增接口 |
| 07-开发环境与调试 | `JY8Hd9To3ozjpLx9oUncvWfPnqb` | 环境搭建、常见问题排查 |
| 08-初学者教程 | `Kqzxd61xVoSjJCxyskQcGyA5nQg` | 需要向初学者解释概念 |
| 09-变更记录 | `TLfsd3EGlowgT7x2JqbcMokCnve` | 查版本历史 |

**查询命令：**
```bash
# 读取文档内容
lark-cli docs +fetch --doc <doc_id> --format pretty

# 搜索文档
lark-cli docs +search --query "搜索关键词" --format pretty
```

**何时主动查询知识库：**
- 开始新功能开发 → 查 02-架构设计 + 对应开发指南
- 修改 API → 查 06-API参考手册
- 调试问题 → 查 07-开发环境与调试
- 向用户解释概念 → 查 08-初学者教程

## 知识库自动同步

PR 合并到 master 后，GitHub Actions (`wiki-sync.yml`) 自动触发知识库同步：
1. 检测变更文件 → 映射到对应文档
2. Claude Code 分析变更 → 生成文档内容
3. lark-cli 更新飞书知识库

手动触发：GitHub Actions → Wiki Sync → Run workflow
