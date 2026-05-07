/**
 * Zod schemas — input validation at the adapter (HTTP) boundary.
 *
 * LAYER: adapters
 * Note: Zod handles SHAPE / TYPE validation. Domain rules (length limits,
 * business invariants) live in the domain layer (Todo.ts validateTitle).
 * Don't duplicate them here — let the use case re-validate.
 */

import { z } from 'zod'
import { TITLE_MAX, NOTES_MAX } from '../domain/Todo'

export const CreateTodoSchema = z.object({
  title: z.string().min(1).max(TITLE_MAX),
  notes: z.string().max(NOTES_MAX).optional().nullable(),
  assignee: z.enum(['me', 'partner', 'either']).default('either'),
  dueDate: z.coerce.date().optional().nullable(),
})

export type CreateTodoFormInput = z.infer<typeof CreateTodoSchema>

export const ToggleTodoSchema = z.object({
  id: z.string().uuid(),
})
export type ToggleTodoFormInput = z.infer<typeof ToggleTodoSchema>
