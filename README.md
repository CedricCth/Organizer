# Couples App

A small, private Progressive Web App for partners to share household todos, weekly chores, and stay aligned without nagging each other. Mobile-first. Cute, calm, secure.

## Status

Planning is done; bootstrap is in progress (see Jira `CA-26` for the live state). The MVP is auth + couple pairing + a shared todo list. Everything beyond that is intentionally out of scope until v1.0 ships.

## Where to look

- **[`CLAUDE.md`](./CLAUDE.md)** — read first if you're a Claude session. The hard rules, architecture summary, and pointers into the planning docs.
- **[`docs/`](./docs/)** — the planning docs:
  - [`docs/FEATURES.md`](./docs/FEATURES.md) — what's in scope for MVP, v1.1, v2, and what's out of scope.
  - [`docs/BACKLOG.md`](./docs/BACKLOG.md) — prioritized epics; pull from the top.
  - [`docs/TECH_STACK.md`](./docs/TECH_STACK.md) — the stack and the security baseline.
  - [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — Pragmatic Clean Architecture, layer rules, C4 + sequence diagrams.
  - [`docs/WORKFLOW.md`](./docs/WORKFLOW.md) — how Stef and Claude work together on this project.
  - [`docs/adr/`](./docs/adr/) — Architecture Decision Records (the *why* behind every major choice).
- **[`diagrams/`](./diagrams/)** — rendered C4 + sequence diagrams referenced from `docs/ARCHITECTURE.md`.

## Stack

Next.js 15 (App Router) · React 19 · TypeScript · Tailwind v4 · shadcn/ui · Supabase (Postgres + Auth + Realtime) · Vercel · pnpm. Full detail and rationale in `docs/TECH_STACK.md` and `docs/adr/`.

## Quickstart

The repo will run locally once bootstrap (epic `EPIC-01`) is complete. Until then, the runnable code is the reference implementation in `src/features/todos/`. See `CLAUDE.md` for the always-current entry point.
