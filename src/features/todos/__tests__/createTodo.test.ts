/**
 * Unit test for the createTodo use case.
 *
 * LAYER: tests
 * Demonstrates the payoff of DI: this test exercises real domain rules through
 * the real use case, but with a hand-rolled in-memory repository — no Supabase,
 * no Next.js, no network. Runs in milliseconds.
 */

import { describe, expect, it, vi } from 'vitest'
import { coupleId, userId } from '@/shared/domain/ids'
import { makeCreateTodo } from '../application/createTodo'
import type { CreateTodoData, TodoRepository, UpdateTodoPatch } from '../application/TodoRepository'
import { TodoValidationError, type Todo } from '../domain/Todo'

/** Tiny in-memory fake. Reusable across use case tests. */
function makeFakeRepo(): TodoRepository & { items: Todo[] } {
  const items: Todo[] = []
  return {
    items,
    async listForCouple() { return items },
    async findById(id) { return items.find(t => t.id === id) ?? null },
    async create(input: CreateTodoData) {
      const todo: Todo = {
        ...input,
        id: `fake-${items.length + 1}` as Todo['id'],
        createdAt: new Date('2026-05-07T12:00:00Z'),
      }
      items.push(todo)
      return todo
    },
    async update(id, patch: UpdateTodoPatch) {
      const idx = items.findIndex(t => t.id === id)
      if (idx === -1) throw new Error('not found')
      const merged: Todo = {
        ...items[idx],
        ...(patch.title !== undefined ? { title: patch.title } : {}),
        ...(patch.notes !== undefined ? { notes: patch.notes } : {}),
        ...(patch.assignee !== undefined ? { assignee: patch.assignee } : {}),
        ...(patch.status !== undefined ? { status: patch.status } : {}),
        ...(patch.dueDate !== undefined ? { dueDate: patch.dueDate } : {}),
      }
      items[idx] = merged
      return merged
    },
    async remove(id) {
      const idx = items.findIndex(t => t.id === id)
      if (idx !== -1) items.splice(idx, 1)
    },
  }
}

const A_COUPLE = coupleId('couple-1')
const A_USER = userId('user-1')

describe('createTodo', () => {
  it('rejects empty / whitespace-only titles via the domain rule', async () => {
    const repo = makeFakeRepo()
    const createTodo = makeCreateTodo({ todos: repo })

    await expect(
      createTodo({ coupleId: A_COUPLE, createdBy: A_USER, title: '   ' }),
    ).rejects.toBeInstanceOf(TodoValidationError)

    expect(repo.items).toHaveLength(0)
  })

  it('rejects titles longer than 200 chars', async () => {
    const repo = makeFakeRepo()
    const createTodo = makeCreateTodo({ todos: repo })

    await expect(
      createTodo({ coupleId: A_COUPLE, createdBy: A_USER, title: 'x'.repeat(201) }),
    ).rejects.toBeInstanceOf(TodoValidationError)
  })

  it('trims the title before persisting', async () => {
    const repo = makeFakeRepo()
    const createTodo = makeCreateTodo({ todos: repo })

    const todo = await createTodo({
      coupleId: A_COUPLE,
      createdBy: A_USER,
      title: '   buy oat milk   ',
    })

    expect(todo.title).toBe('buy oat milk')
    expect(repo.items[0]?.title).toBe('buy oat milk')
  })

  it('defaults assignee to "either" and status to "open"', async () => {
    const repo = makeFakeRepo()
    const createTodo = makeCreateTodo({ todos: repo })

    const todo = await createTodo({
      coupleId: A_COUPLE,
      createdBy: A_USER,
      title: 'water plants',
    })

    expect(todo.assignee).toBe('either')
    expect(todo.status).toBe('open')
  })

  it('passes through optional fields when provided', async () => {
    const repo = makeFakeRepo()
    const createSpy = vi.spyOn(repo, 'create')
    const createTodo = makeCreateTodo({ todos: repo })

    const due = new Date('2026-05-10T18:00:00Z')
    await createTodo({
      coupleId: A_COUPLE,
      createdBy: A_USER,
      title: 'pick up package',
      notes: 'building B reception',
      assignee: 'me',
      dueDate: due,
    })

    expect(createSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        notes: 'building B reception',
        assignee: 'me',
        dueDate: due,
      }),
    )
  })
})
