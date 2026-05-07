# ADR-002 — Backend: Supabase

**Date:** 2026-05-07
**Status:** Accepted

## Context

We need: user auth, a database for shared todos, real-time sync ("when partner adds a todo, I see it"), strict data isolation between couples, and we want minimal ops work for an MVP.

## Options considered

1. **Supabase** — Postgres + Auth + Realtime + Storage as a managed service. Open source. Generous free tier. Row-Level Security policies enforce data isolation in the database itself.
2. **Firebase** — Google's BaaS. Mature, scales well, easy auth. Firestore is NoSQL.
3. **Custom Node.js + Postgres backend** — full control, hosted on Railway/Fly/Render. Maximum flexibility.
4. **Appwrite / PocketBase / Convex** — newer alternatives. Smaller ecosystems, less Claude-Code documentation, more risk for a couple-of-users app.

## Decision

**Supabase.**

## Why

- **Relational data fits the domain.** Couples ↔ users ↔ todos is a graph of foreign keys. SQL is the right shape; Firestore's NoSQL would force us into denormalization gymnastics.
- **Row-Level Security is the perfect privacy primitive.** We write one policy like `auth.uid() IN (couple.user_a, couple.user_b)` and the database itself refuses to return another couple's data — even if we have a bug in app code. Firebase has security rules but they're harder to test and reason about for relational data.
- **Realtime is built-in.** Postgres changes stream over websockets; the client `useEffect`s to a channel. No extra service to run.
- **Open source escape hatch.** If Supabase the company ever goes away or changes pricing, we can self-host the same software. Firebase has no such option.
- **Auth is included** with secure-by-default cookie sessions, email confirmation, password reset — nothing to build from scratch.

## Trade-offs accepted

- Less mature mobile SDK than Firebase (not relevant for a PWA).
- Realtime can lag under extreme load — irrelevant at our scale.
- We are tied to Postgres flavor of SQL.

## Revisit when

- We want to scale to thousands of couples and need very specific infra control.
- We need a feature Supabase doesn't support (very unlikely for this app's scope).
