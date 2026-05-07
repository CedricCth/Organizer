/**
 * Server actions — the HTTP boundary for the Todos feature.
 *
 * LAYER: adapters / delivery boundary
 * RULE: server actions are THIN. They (1) parse input with Zod, (2) get the
 * authenticated context, (3) call a use case via the composition root,
 * (4) revalidate the cache. Domain logic does NOT live here.
 */

'use server'

import { revalidatePath } from 'next/cache'
import { coupleId as makeCoupleId, todoId as makeTodoId, userId as makeUserId } from '@/shared/domain/ids'
import { getAuthContext } from '@/features/auth/adapters/composition' // TODO: implement when auth feature is built
import { CreateTodoSchema, ToggleTodoSchema } from './schema'
import { makeTodosModule } from './composition'

export async function createTodoAction(formData: FormData) {
  const parsed = CreateTodoSchema.parse(Object.fromEntries(formData))

  // getAuthContext returns { userId, coupleId } verified server-side from the session.
  // Until auth is implemented, this throws — that's fine, it'll wire up cleanly later.
  const { userId, coupleId } = await getAuthContext()

  const { createTodo } = makeTodosModule()
  const todo = await createTodo({
    coupleId: makeCoupleId(coupleId),
    createdBy: makeUserId(userId),
    title: parsed.title,
    notes: parsed.notes ?? null,
    assignee: parsed.assignee,
    dueDate: parsed.dueDate ?? null,
  })

  revalidatePath('/todos')
  return todo
}

export async function toggleTodoAction(formData: FormData) {
  const parsed = ToggleTodoSchema.parse(Object.fromEntries(formData))
  await getAuthContext() // ensures the request is authed; RLS does the rest

  const { toggleTodo } = makeTodosModule()
  const todo = await toggleTodo(makeTodoId(parsed.id))

  revalidatePath('/todos')
  return todo
}
