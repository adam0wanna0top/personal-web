// 数据库层：用 SQLite 存储 Todo，操作就是一个文件（todos.db）
import Database from 'better-sqlite3'

// 打开（或创建）数据库文件
const db = new Database('todos.db')

// 建表（如果不存在的话）
db.exec(`
  CREATE TABLE IF NOT EXISTS todos (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    text  TEXT    NOT NULL,
    done  INTEGER NOT NULL DEFAULT 0
  )
`)

// 导出 CRUD 函数供路由使用
export const todoDb = {
  // 查全部
  getAll() {
    return db.prepare('SELECT * FROM todos ORDER BY id DESC').all()
      .map((row: any) => ({ ...row, done: Boolean(row.done) }))
  },

  // 查单个
  getById(id: number) {
    const row = db.prepare('SELECT * FROM todos WHERE id = ?').get(id) as any
    return row ? { ...row, done: Boolean(row.done) } : undefined
  },

  // 新增
  create(text: string, done = false) {
    const result = db.prepare('INSERT INTO todos (text, done) VALUES (?, ?)').run(text, done ? 1 : 0)
    return { id: Number(result.lastInsertRowid), text, done }
  },

  // 更新
  update(id: number, updates: { text?: string; done?: boolean }) {
    const existing = this.getById(id)
    if (!existing) return undefined
    const text = updates.text ?? existing.text
    const done = updates.done ?? existing.done
    db.prepare('UPDATE todos SET text = ?, done = ? WHERE id = ?').run(text, done ? 1 : 0, id)
    return { id, text, done }
  },

  // 删除
  remove(id: number) {
    return db.prepare('DELETE FROM todos WHERE id = ?').run(id).changes > 0
  },
}
