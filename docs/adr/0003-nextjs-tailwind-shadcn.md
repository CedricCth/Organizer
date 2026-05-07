# ADR-003 — Frontend: Next.js 15 + Tailwind v4 + shadcn/ui

**Date:** 2026-05-07
**Status:** Accepted

## Context

Need a frontend framework that:
- supports PWA cleanly,
- has excellent server-side auth handling (so we don't ship sessions to the client),
- is well-documented and understood by Claude Code (so future implementation work is high-quality),
- gives us a "cute" customizable look without huge component libraries.

## Options considered

1. **Next.js 15 (App Router) + Tailwind v4 + shadcn/ui** — current React mainstream. Server Components + Server Actions handle auth elegantly.
2. **Remix / React Router v7** — also good for forms-heavy apps. Smaller ecosystem in 2026, fewer deployment integrations.
3. **SvelteKit + Tailwind** — beautiful DX, smaller bundles, but smaller community and fewer Supabase examples.
4. **Plain Vite + React + Tailwind** — simplest, but we'd hand-roll routing, SSR, server-side auth, etc.

## Decision

**Next.js 15 (App Router) + TypeScript + Tailwind v4 + shadcn/ui + lucide-react icons.**

## Why

- Vercel makes deployment a single `git push`.
- Server Components let auth checks happen server-side — no flash of unauthenticated content.
- Tailwind v4's perf improvements and CSS-first config are a real upgrade.
- shadcn/ui ships components into our repo (rather than as a black-box library), which means we can theme everything to feel warm, soft, and couples-y without fighting library defaults.
- Best-documented stack for Claude Code, which directly helps you ship faster in later sessions.

## Trade-offs accepted

- Next.js has more concepts to learn (Server vs Client Components, Server Actions, etc.) than a plain SPA — but the payoff is real and Claude Code handles them well.
- Vercel lock-in is mild — we can self-host Next.js elsewhere if needed.

## Revisit when

- Bundle size or perf becomes a real problem (it won't for this app).
- We have a strong reason to prefer a different framework.
