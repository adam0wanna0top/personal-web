# 开发策略

本文档描述项目的分支管理、CI/CD 流水线、版本发布和紧急修复流程。

---

## 一、分支模型

```
master ──────────────────────────────────── 生产分支（永远稳定可部署）
  │
  ├── develop ───────────────────────────── 开发集成分支
  │     │
  │     ├── feature/add-search             功能分支
  │     ├── feature/user-auth
  │     └── feature/dark-mode
  │
  ├── release/v1.1.0 ───────────────────── 发布准备分支
  │
  └── hotfix/fix-crash ──────────────────── 紧急修复分支
```

### 五种分支规则

| 分支 | 命名规范 | 从哪拉出 | 合并到 | 生命周期 |
|------|---------|---------|--------|---------|
| `master` | — | — | — | 永久 |
| `develop` | — | master | — | 永久 |
| `feature/*` | `feature/简短描述` | develop | develop (通过 PR) | 开发完即删 |
| `release/*` | `release/v1.x.0` | develop | master + develop | 发布完即删 |
| `hotfix/*` | `hotfix/简短描述` | master | master + develop | 修复完即删 |

---

## 二、日常工作流

### 开发新功能（feature 分支）

```bash
# 1. 从 develop 拉出功能分支
git checkout develop
git pull origin develop
git checkout -b feature/add-search

# 2. 开发，定期提交和推送
git add .
git commit -m "feat: add search input component"
git push -u origin feature/add-search

# 3. 在 GitHub 上创建 Pull Request → develop
#    CI 自动检查（编译 + 类型检查），通过后人工 Review

# 4. 合并后删除分支
git checkout develop
git pull origin develop
git branch -d feature/add-search
git push origin --delete feature/add-search
```

### 定期发布（release 分支）

当 develop 上积累了足够的功能，准备发布新版本：

```bash
# 1. 从 develop 拉出 release 分支
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# 2. 在 release 分支上只做：
#    - Bug 修复
#    - 更新 package.json 中的版本号
#    - 更新 CHANGELOG
#    不加新功能！

git add .
git commit -m "chore: bump version to 1.1.0"

# 3. 测试通过后，合并到 master（打 tag）和 develop
git checkout master
git merge release/v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0: 搜索功能、暗色模式"

git checkout develop
git merge release/v1.1.0

git push origin master --tags
git push origin develop

# 4. 删除 release 分支
git branch -d release/v1.1.0
git push origin --delete release/v1.1.0
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
git checkout master
git merge hotfix/fix-crash
git tag -a v1.0.1 -m "Hotfix v1.0.1: crash on empty list"

# 4. 同步到 develop
git checkout develop
git merge hotfix/fix-crash

git push origin master --tags
git push origin develop

# 5. 删除 hotfix 分支
git branch -d hotfix/fix-crash
git push origin --delete hotfix/fix-crash
```

---

## 三、CI 流水线（GitHub Actions）

### PR 检查（`.github/workflows/ci.yml`）

每次 PR 到 `develop` 或 `master` 时自动运行：

| 检查项 | 命令 | 作用 |
|-------|------|------|
| 前端编译 | `npm install && npm run build` | 确保前端代码能编译通过 |
| TS 后端类型检查 | `cd backend-ts && npm install && npx tsc --noEmit` | 确保 TypeScript 无类型错误 |
| Python 语法检查 | `cd backend-py && python -m py_compile app.py db.py` | 确保 Python 代码无语法错误 |

任何一步失败，PR 不可合并。

### 自动发布（`.github/workflows/release.yml`）

当 master 上推送 `v*` tag 时自动触发：

1. 编译前端（`npm run build`）
2. 打包 `dist/` 为 zip
3. 创建 GitHub Release 页面，附带编译产物

---

## 四、版本号规范（语义化版本 SemVer）

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

## 五、Commit 消息规范

所有 commit 消息使用以下前缀：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: add search filter` |
| `fix:` | Bug 修复 | `fix: prevent crash on empty input` |
| `docs:` | 文档更新 | `docs: update README` |
| `refactor:` | 代码重构 | `refactor: extract API helper` |
| `style:` | 代码格式 | `style: fix indentation` |
| `chore:` | 杂项 | `chore: update dependencies` |

---

## 六、GitHub 仓库保护设置

在 GitHub 仓库 **Settings → Branches → Branch protection rules** 中配置：

**`master` 分支保护：**
- ✅ Require a pull request before merging
- ✅ Require approvals（至少 1 人 Review）
- ✅ Require status checks to pass（CI 必须通过）
- ✅ Require branches to be up to date before merging

**`develop` 分支保护：**
- ✅ Require a pull request before merging
- ✅ Require status checks to pass

---

## 七、速查表

| 场景 | 命令 |
|------|------|
| 开始新功能 | `git checkout develop && git pull && git checkout -b feature/xxx` |
| 提交代码 | `git add . && git commit -m "feat: xxx"` |
| 推送分支 | `git push -u origin feature/xxx` |
| 准备发布 | `git checkout develop && git checkout -b release/v1.x.0` |
| 打 tag | `git tag -a v1.x.0 -m "Release v1.x.0"` |
| 推送 tag | `git push origin master --tags` |
| 紧急修复 | `git checkout master && git checkout -b hotfix/xxx` |
| 删除已合并分支 | `git branch -d xxx && git push origin --delete xxx` |
