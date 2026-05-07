/**
 * SupabaseTodoRepository — concrete TodoRepository backed by Supabase.
 *
 * LAYER: adapters
 * RULE: this file imports `@supabase/supabase-js` (allowed in adapters).
 * `application/` and `domain/` must never do this.
 *
 * Skeleton — actual SQL is annotated as TODO and will be implemented when
 * the migrations land. The shape is correct so types check end-to-end.
 */

import type { SupabaseClient } from '@supabase/supabase-js'
import { coupleId as makeCoupleId, todoId as makeTodoId, userId as makeUserId } from '@/shared/domain/ids'
import type { CoupleId, TodoId } from '@/shared/domain/ids'
import type { Todo } from '../domain/Todo'
import type { CreateTodoData, TodoRepository, UpdateTodoPatch } from '../application/TodoRepository'

/** Database row shape, matching the `todos` table. */
interface TodoRow {
  id: string
  couple_id: string
  title: string
  notes: string | null
  assignee: 'me' | 'partner' | 'either'
  status: 'open' | 'done'
  due_date: string | null
  created_at: string
  created_by: string
}

function rowToDomain(row: TodoRow): Todo {
  return {
    id: makeTodoId(row.id),
    coupleId: makeCoupleId(row.couple_id),
    title: row.title,
    notes: row.notes,
    assignee: row.assignee,
    status: row.status,
    dueDate: row.due_date ? new Date(row.due_date) : null,
    createdAt: new Date(row.created_at),
    createdBy: makeUserId(row.created_by),
  }
}

export function makeSupabaseTodoRepository(supabase: SupabaseClient): TodoRepository {
  return {
    async listForCouple(coupleId: CoupleId): Promise<Todo[]> {
      // RLS ensures we only get this couple's rows even without explicit filter,
      // but we still pass it explicitly for clarity.
      const { data, error } = await supabase
        .from('todos')
        .select('*')
        .eq('couple_id', coupleId)
        .order('created_at', { ascending: false })
      if (error) throw error
      return (data as TodoRow[]).map(rowToDomain)
    },

    async findById(id: TodoId): Promise<Todo | null> {
      const { data, error } = await supabase
        .from('todos')
        .select('*')
        .eq('id', id)
        .maybeSingle()
      if (error) throw error
      return data ? rowToDomain(data as TodoRow) : null
    },

    async create(input: CreateTodoData): Promise<Todo> {
      const { data, error } = await supabase
        .from('todos')
        .insert({
          couple_id: input.coupleId,
          created_by: input.createdBy,
          title: input.title,
          notes: input.notes,
          assignee: input.assignee,
          status: input.status,
          due_date: input.dueDate?.toISOString() ?? null,
        })
        .select('*')
        .single()
      if (error) throw error
      return rowToDomain(data as TodoRow)
    },

    async update(id: TodoId, patch: UpdateTodoPatch): Promise<Todo> {
      const dbPatch: Record<string, unknown> = {}
      if (patch.title !== undefined) dbPatch.title = patch.title
      if (patch.notes !== undefined) dbPatch.notes = patch.notes
      if (patch.assignee !== undefined) dbPatch.assignee = patch.assignee
      if (patch.status !== undefined) dbPatch.status = patch.status
      if (patch.dueDate !== undefined) dbPatch.due_date = patch.dueDate?.toISOString() ?? null

      const { data, error } = await supabase
        .from('todos')
        .update(dbPatch)
        .eq('id', id)
        .select('*')
        .single()
      if (error) throw error
      return rowToDomain(data as TodoRow)
    },

    async remove(id: TodoId): Promise<void> {
      const { error } = await supabase.from('todos').delete().eq('id', id)
      if (error) throw error
    },
  }
}
