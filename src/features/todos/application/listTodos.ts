/**
 * listTodos — application use case.
 *
 * LAYER: application
 * Trivially small on purpose. A use case is allowed to be a thin pass-through
 * when there is no domain logic to apply. Don't invent rules for the sake of it.
 */

import type { CoupleId } from '@/shared/domain/ids'
import type { Todo } from '../domain/Todo'
import type { TodoRepository } from './TodoRepository'

export interface ListTodosDeps {
  todos: TodoRepository
}

export function makeListTodos({ todos }: ListTodosDeps) {
  return async function listTodos(coupleId: CoupleId): Promise<Todo[]> {
    return todos.listForCouple(coupleId)
  }
}

export type ListTodos = ReturnType<typeof makeListTodos>
