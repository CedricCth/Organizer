/**
 * Todo — domain entity and pure rules.
 *
 * LAYER: domain
 * RULE: this file MUST NOT import from `next`, `@supabase/*`, `react`, `zod`,
 * or any I/O lib. If you find yourself wanting to, you're in the wrong layer.
 */

import type { CoupleId, TodoId, UserId } from '@/shared/domain/ids'

export type TodoStatus = 'open' | 'done'
export type TodoAssignee = 'me' | 'partner' | 'either'

export interface Todo {
  readonly id: TodoId
  readonly coupleId: CoupleId
  readonly title: string
  readonly notes: string | null
  readonly assignee: TodoAssignee
  readonly status: TodoStatus
  readonly dueDate: Date | null
  readonly createdAt: Date
  readonly createdBy: UserId
}

// ----- Pure domain rules -----

export const TITLE_MIN = 1
export const TITLE_MAX = 200
export const NOTES_MAX = 2000

export class TodoValidationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'TodoValidationError'
  }
}

/** Trim and validate a title. Returns the cleaned title. Throws TodoValidationError if invalid. */
export function validateTitle(raw: string): string {
  const trimmed = raw.trim()
  if (trimmed.length < TITLE_MIN) {
    throw new TodoValidationError('Title cannot be empty')
  }
  if (trimmed.length > TITLE_MAX) {
    throw new TodoValidationError(`Title must be at most ${TITLE_MAX} characters`)
  }
  return trimmed
}

/** Validate notes (optional). Returns the trimmed notes or null. */
export function validateNotes(raw: string | null | undefined): string | null {
  if (raw == null) return null
  const trimmed = raw.trim()
  if (trimmed.length === 0) return null
  if (trimmed.length > NOTES_MAX) {
    throw new TodoValidationError(`Notes must be at most ${NOTES_MAX} characters`)
  }
  return trimmed
}

/** Toggle status — pure. Returns a new Todo with status flipped. */
export function toggleStatus(todo: Todo): Todo {
  return { ...todo, status: todo.status === 'open' ? 'done' : 'open' }
}

/** Mark done — pure. */
export function markDone(todo: Todo): Todo {
  return { ...todo, status: 'done' }
}

/** Mark open — pure. */
export function markOpen(todo: Todo): Todo {
  return { ...todo, status: 'open' }
}
