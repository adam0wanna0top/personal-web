import { describe, it, expect, beforeEach, afterAll } from 'vitest'
import { createTodoDb } from '../db.js'

describe('todoDb', () => {
  const db = createTodoDb(':memory:')

  afterAll(() => {
    db.close()
  })

  beforeEach(() => {
    // 清空表数据
    const todos = db.getAll()
    for (const t of todos) {
      db.remove(t.id)
    }
  })

  it('creates a todo', () => {
    const todo = db.create('Buy milk')
    expect(todo).toEqual({ id: expect.any(Number), text: 'Buy milk', done: false })
  })

  it('creates a todo with done=true', () => {
    const todo = db.create('Done task', true)
    expect(todo.done).toBe(true)
  })

  it('gets all todos', () => {
    db.create('Task 1')
    db.create('Task 2')
    const todos = db.getAll()
    expect(todos).toHaveLength(2)
    // ORDER BY id DESC
    expect(todos[0].text).toBe('Task 2')
  })

  it('gets todo by id', () => {
    const created = db.create('Find me')
    const found = db.getById(created.id)
    expect(found).toEqual(created)
  })

  it('returns undefined for non-existent id', () => {
    expect(db.getById(99999)).toBeUndefined()
  })

  it('updates a todo', () => {
    const created = db.create('Original')
    const updated = db.update(created.id, { text: 'Updated', done: true })
    expect(updated).toEqual({ id: created.id, text: 'Updated', done: true })
  })

  it('partial update preserves fields', () => {
    const created = db.create('Keep text')
    db.update(created.id, { done: true })
    const found = db.getById(created.id)
    expect(found?.text).toBe('Keep text')
    expect(found?.done).toBe(true)
  })

  it('update returns undefined for non-existent id', () => {
    expect(db.update(99999, { text: 'Nope' })).toBeUndefined()
  })

  it('deletes a todo', () => {
    const created = db.create('Delete me')
    expect(db.remove(created.id)).toBe(true)
    expect(db.getById(created.id)).toBeUndefined()
  })

  it('remove returns false for non-existent id', () => {
    expect(db.remove(99999)).toBe(false)
  })
})
