/**
 * toggleTodo — application use case.
 *
 * LAYER: application
 * Demonstrates: read-modify-write through the repository, with the actual
 * status transition delegated to a pure domain function (`toggleStatus`).
 */

import type { TodoId } from '@/shared/domain/ids'
import type { Todo } from '../domain/Todo'
import { toggleStatus } from '../domain/Todo'
import type { TodoRepository } from './TodoRepository'

export interface ToggleTodoDeps {
  todos: TodoRepository
}

export class TodoNotFoundError extends Error {
  constructor(id: TodoId) {
    super(`Todo not found: ${id}`)
    this.name = 'TodoNotFoundError'
  }
}

export function makeToggleTodo({ todos }: ToggleTodoDeps) {
  return async function toggleTodo(id: TodoId): Promise<Todo> {
    const current = await todos.findById(id)
    if (!current) throw new TodoNotFoundError(id)

    const next = toggleStatus(current)
    return todos.update(id, { status: next.status })
  }
}

export type ToggleTodo = ReturnType<typeof makeToggleTodo>
