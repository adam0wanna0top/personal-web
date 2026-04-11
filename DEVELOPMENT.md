# 开发策略

本文档描述项目的分支管理、CI/CD 流水线、版本发布和紧急修复流程。

---

## 一、分支模型

个人项目采用简化的分支策略，不使用 develop 分支，所有功能通过 PR 直接合入 master。

```
master ──────────────────────────────────── 生产分支（永远稳定可部署）
  │
  ├── feature/add-search                   功能分支
  ├── feature/user-auth
  └── feature/dark-mode

  ├── hotfix/fix-crash ──────────────────── 紧急修复分支
```

### 三种分支规则

| 分支 | 命名规范 | 从哪拉出 | 合并到 | 生命周期 |
|------|---------|---------|--------|---------|
| `master` | — | — | — | 永久 |
| `feature/*` | `feature/简短描述` | master | master (通过 PR) | 开发完即删 |
| `hotfix/*` | `hotfix/简短描述` | master | master | 修复完即删 |

---

## 二、日常工作流

### 开发新功能（feature 分支）

```bash
# 1. 从 master 拉出功能分支
git checkout master
git pull origin master
git checkout -b feature/add-search

# 2. 开发，定期提交和推送
git add .
git commit -m "feat: add search input component"
git push -u origin feature/add-search

# 3. 在 GitHub 上创建 Pull Request → master
#    CI 自动检查（编译 + 类型检查 + 测试），通过后合并

# 4. 合并后删除分支
git checkout master
git pull origin master
git branch -d feature/add-search
git push origin --delete feature/add-search
```

### 发布新版本

当 master 上积累了足够的功能，准备发布新版本：

```bash
# 1. 确保 master 是最新的
git checkout master
git pull origin master

# 2. 更新版本号
#    编辑 package.json 中的 version 字段

# 3. 打 tag 并推送（自动触发 Release 工作流）
git tag -a v1.1.0 -m "Release v1.1.0: 搜索功能、暗色模式"
git push origin master --tags

# 4. GitHub Actions 会自动：
#    - 编译前端
#    - 打包 dist/
#    - 创建 GitHub Release 页面，附带编译产物
```

### 紧急修复（hotfix 分支）

线上发现 bug，需要紧急修复：

```bash
# 1. 从 master 拉出 hotfix 分支
git checkout master
git pull origin master
git checkout -b hotfix/fix-crash

# 2. 修复并测试
git add .
git commit -m "fix: prevent crash on empty todo list"
git push -u origin hotfix/fix-crash

# 3. 创建 PR 合并到 master，CI 通过后合并

# 4. 合并后删除分支
git checkout master
git pull origin master
git branch -d hotfix/fix-crash
git push origin --delete hotfix/fix-crash

# 5. 如果需要紧急发布，打 patch tag
git tag -a v1.0.1 -m "Hotfix v1.0.1: crash on empty list"
git push origin master --tags
```

---

## 三、CI 流水线（GitHub Actions）

### PR 检查（`.github/workflows/ci.yml`）

每次 PR 到 `master` 时自动运行，三个 Job 并行：

| Job | 检查项 | 作用 |
|-----|-------|------|
| **frontend** | `npm run build` + `vue-tsc --noEmit` + `npm test` | 前端编译、类型检查、单元测试 |
| **backend-ts** | `tsc --noEmit` + `npm test` | TS 后端类型检查、单元测试 |
| **backend-py** | `py_compile` + `pytest` | Python 语法检查、单元测试 |

任何一步失败，PR 不可合并。

### 自动发布（`.github/workflows/release.yml`）

当 master 上推送 `v*` tag 时自动触发：

1. 编译前端（`npm run build`）
2. 打包 `dist/` 为 zip
3. 创建 GitHub Release 页面，附带编译产物

---

## 四、测试框架

| 组件 | 框架 | 测试文件位置 |
|------|------|------------|
| 前端 | Vitest + Vue Test Utils | `frontend/__tests__/*.test.ts` |
| TS 后端 | Vitest | `backend-ts/src/__tests__/*.test.ts` |
| Python 后端 | pytest | `backend-py/test_*.py` |

### 运行测试

```bash
# 前端
npm test

# TS 后端
cd backend-ts && npm test

# Python 后端
cd backend-py && python -m pytest test_db.py -v
```

---

## 五、版本号规范（语义化版本 SemVer）

```
v1.2.3
│ │ │
│ │ └── Patch: bug 修复（向下兼容）
│ └──── Minor: 新功能（向下兼容）
└────── Major: 破坏性变更
```

示例：
- `v1.0.0` → 首个正式版本
- `v1.1.0` → 新增搜索功能
- `v1.1.1` → 修复搜索框输入 bug
- `v2.0.0` → 重构 API，不兼容旧版

---

## 六、Commit 消息规范

所有 commit 消息使用以下前缀：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: add search filter` |
| `fix:` | Bug 修复 | `fix: prevent crash on empty input` |
| `docs:` | 文档更新 | `docs: update README` |
| `refactor:` | 代码重构 | `refactor: extract API helper` |
| `style:` | 代码格式 | `style: fix indentation` |
| `chore:` | 杂项 | `chore: update dependencies` |
| `test:` | 测试 | `test: add db unit tests` |

---

## 七、GitHub 仓库保护设置

在 GitHub 仓库 **Settings → Branches → Branch protection rules** 中配置：

**`master` 分支保护：**
- ✅ Require a pull request before merging
- ✅ Require status checks to pass → 勾选 frontend / backend-ts / backend-py
- ✅ Require branches to be up to date before merging

---

## 八、速查表

| 场景 | 命令 |
|------|------|
| 开始新功能 | `git checkout master && git pull && git checkout -b feature/xxx` |
| 提交代码 | `git add . && git commit -m "feat: xxx"` |
| 推送分支 | `git push -u origin feature/xxx` |
| 发布版本 | `git tag -a v1.x.0 -m "Release v1.x.0" && git push origin master --tags` |
| 紧急修复 | `git checkout master && git checkout -b hotfix/xxx` |
| 删除已合并分支 | `git branch -d xxx && git push origin --delete xxx` |
| 运行前端测试 | `npm test` |
| 运行 TS 后端测试 | `cd backend-ts && npm test` |
| 运行 Python 测试 | `cd backend-py && python -m pytest -v` |
