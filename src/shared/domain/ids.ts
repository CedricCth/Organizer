/**
 * Branded ID types — cross-feature primitives.
 *
 * These live in `src/shared/domain/` because they're used by multiple features
 * (a Todo references a CoupleId, the Couple feature owns the CoupleId concept,
 * and we don't want to create a feature-to-feature import).
 *
 * Branded types catch the bug where you accidentally pass a UserId where a
 * CoupleId was expected — they're nominally typed at compile time, even though
 * at runtime they're just strings.
 */

declare const __brand: unique symbol

export type Branded<T, B> = T & { readonly [__brand]: B }

export type UserId = Branded<string, 'UserId'>
export type CoupleId = Branded<string, 'CoupleId'>
export type TodoId = Branded<string, 'TodoId'>
export type InviteCode = Branded<string, 'InviteCode'>

// Constructors — the only sanctioned way to mint a branded id.
// Validation lives here so it can't be bypassed by casting.
export function userId(raw: string): UserId {
  if (!raw) throw new Error('UserId cannot be empty')
  return raw as UserId
}
export function coupleId(raw: string): CoupleId {
  if (!raw) throw new Error('CoupleId cannot be empty')
  return raw as CoupleId
}
export function todoId(raw: string): TodoId {
  if (!raw) throw new Error('TodoId cannot be empty')
  return raw as TodoId
}
