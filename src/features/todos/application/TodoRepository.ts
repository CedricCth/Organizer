/**
 * TodoRepository — the interface the application layer depends on.
 *
 * LAYER: application
 * RULE: this interface is DEFINED here in application/. It is IMPLEMENTED in
 * adapters/ (SupabaseTodoRepository.ts) and in tests (a fake repo). That's
 * Dependency Inversion: the inner layer owns the contract, outer layers obey.
 */

import type { CoupleId, TodoId, UserId } from '@/shared/domain/ids'
import type { Todo, TodoAssignee, TodoStatus } from '../domain/Todo'

/** Input for creating a Todo — domain has already cleaned/validated title and notes. */
export interface CreateTodoData {
  coupleId: CoupleId
  createdBy: UserId
  title: string
  notes: string | null
  assignee: TodoAssignee
  status: TodoStatus
  dueDate: Date | null
}

/** Patch type for update — only the mutable fields. */
export type UpdateTodoPatch = Partial<{
  title: string
  notes: string | null
  assignee: TodoAssignee
  status: TodoStatus
  dueDate: Date | null
}>

export interface TodoRepository {
  listForCouple(coupleId: CoupleId): Promise<Todo[]>
  findById(id: TodoId): Promise<Todo | null>
  create(data: CreateTodoData): Promise<Todo>
  update(id: TodoId, patch: UpdateTodoPatch): Promise<Todo>
  remove(id: TodoId): Promise<void>
}
