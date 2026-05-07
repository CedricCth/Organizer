/**
 * createTodo — application use case.
 *
 * LAYER: application
 * Pattern: factory function `makeCreateTodo(deps)` returns the use case.
 * Dependencies are passed in (DI), never imported as concrete impls.
 */

import type { CoupleId, UserId } from '@/shared/domain/ids'
import type { Todo, TodoAssignee } from '../domain/Todo'
import { validateNotes, validateTitle } from '../domain/Todo'
import type { TodoRepository } from './TodoRepository'

export interface CreateTodoDeps {
  todos: TodoRepository
}

export interface CreateTodoInput {
  coupleId: CoupleId
  createdBy: UserId
  title: string
  notes?: string | null
  assignee?: TodoAssignee
  dueDate?: Date | null
}

export function makeCreateTodo({ todos }: CreateTodoDeps) {
  return async function createTodo(input: CreateTodoInput): Promise<Todo> {
    // Domain-layer validation. Throws TodoValidationError on bad input.
    const title = validateTitle(input.title)
    const notes = validateNotes(input.notes)

    return todos.create({
      coupleId: input.coupleId,
      createdBy: input.createdBy,
      title,
      notes,
      assignee: input.assignee ?? 'either',
      status: 'open',
      dueDate: input.dueDate ?? null,
    })
  }
}

export type CreateTodo = ReturnType<typeof makeCreateTodo>
