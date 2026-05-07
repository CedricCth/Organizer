/**
 * Supabase server client — placeholder.
 *
 * LAYER: shared/infrastructure
 * Wires the Supabase client to Next.js server context (cookies for session).
 * Will be filled in when auth feature is bootstrapped. Stub kept here so the
 * rest of the skeleton type-checks against a real symbol.
 *
 * When implementing:
 *   - Use `@supabase/ssr` createServerClient
 *   - Read cookies via `next/headers`
 *   - Return a per-request SupabaseClient
 */

import type { SupabaseClient } from '@supabase/supabase-js'

export function createServerSupabaseClient(): SupabaseClient {
  throw new Error(
    'createServerSupabaseClient: not yet implemented. ' +
    'Wire up @supabase/ssr with next/headers cookies when auth feature lands.',
  )
}
