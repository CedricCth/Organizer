/**
 * Composition root for the Todos feature.
 *
 * LAYER: adapters
 * This is the ONLY place where concrete impls (SupabaseTodoRepository) are
 * wired into use cases. Server actions, server components, and route handlers
 * call this to get a ready-to-use module.
 */

import { createServerSupabaseClient } from '@/shared/infrastructure/supabase/serverClient'
import { makeCreateTodo } from '../application/createTodo'
import { makeListTodos } from '../application/listTodos'
import { makeToggleTodo } from '../application/toggleTodo'
import { makeSupabaseTodoRepository } from './SupabaseTodoRepository'

/**
 * Build the Todos module with real Supabase-backed dependencies.
 * Call once per request — the Supabase server client is per-request.
 */
export function makeTodosModule() {
  const supabase = createServerSupabaseClient()
  const todos = makeSupabaseTodoRepository(supabase)
  return {
    createTodo: makeCreateTodo({ todos }),
    listTodos: makeListTodos({ todos }),
    toggleTodo: makeToggleTodo({ todos }),
  }
}

export type TodosModule = ReturnType<typeof makeTodosModule>
