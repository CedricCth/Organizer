# CLAUDE.md — Couples App

> **Read this first.** This file orients any Claude session — Cowork, Claude Code, or any other — before touching this project.

---

## Project snapshot

A **Progressive Web App** for couples and married partners to share household todos, weekly chores, and stay aligned without nagging each other. Mobile-first. Cute, calm, secure.

- **Owner:** Stef
- **Audience:** two paired partners, that's it
- **MVP focus:** auth + couple pairing + shared todos
- **Status as of 2026-05-07:** planning complete; implementation has not started

---

## Always reference these files

When implementing or discussing **any feature**, always start by reading the file(s) below that apply:

- **[`FEATURES.md`](./FEATURES.md)** — the source of truth for **what's in scope**, what's MVP vs later, and what's out of scope. If a request is ambiguous about scope, check here first. If a feature isn't listed, it isn't approved.
- **[`BACKLOG.md`](./BACKLOG.md)** — the source of truth for **what we're building next, in what order**. Epics are prioritized (P0/P1/P2/P3) with sizes, dependencies, and Definitions of Done. Pull from the top; don't cherry-pick.
- **[`TECH_STACK.md`](./TECH_STACK.md)** — the source of truth for **what tools, libraries, and versions** to use. Do not introduce new tools without updating this file via an ADR.
- **[`ARCHITECTURE.md`](./ARCHITECTURE.md)** — the source of truth for **how the code is structured**: layer rules, the dependency direction, C4 diagrams, sequence diagrams, the DI pattern. Read before writing code.
- **[`DECISIONS.md`](./DECISIONS.md)** — the **why** behind major technical and architectural choices. Read before challenging or changing a major decision. Add a new ADR if the decision is changing.
- **[`WORKFLOW.md`](./WORKFLOW.md)** — **how Stef and Claude work together** on this project: the process for adding features, making decisions, structuring sessions.

If you're about to implement, plan, or recommend something on this project, you should have read at least `FEATURES.md`, `TECH_STACK.md`, and `ARCHITECTURE.md` for the relevant area before responding.

---

## Hard rules

1. **Do not invent features.** If a feature isn't in `FEATURES.md`, stop and ask Stef before implementing it. Add it to `FEATURES.md` if approved.
2. **Do not swap tech.** If a request implies a tool, library, or service that isn't in `TECH_STACK.md`, raise it as a candidate ADR in `DECISIONS.md` and propose it to Stef before adopting.
3. **Do not violate the architecture.** See § Architecture rules below — these are non-negotiable.
4. **Update the docs in the same change.** When a feature ships, update its line in `FEATURES.md`. When a decision is made, write the ADR. Code changes that don't update the relevant doc are incomplete.
5. **Security is first-class.** This app stores relationship data. Default to: HTTPS, Row-Level Security on every user-data table, httpOnly+Secure cookies, strong password requirements, no PII in logs, no third-party analytics. See `TECH_STACK.md` § Security baseline.
6. **Cute and calm.** The visual and tonal feel should be warm, soft, friendly — never corporate or aggressive. Copy should feel like a kind partner, not a productivity tool.
7. **Ask, don't assume.** Smaller change, not bigger. When in doubt, surface the question instead of guessing.

---

## Architecture rules

> **These rules are not suggestions.** They exist so the codebase stays SOLID, extensible, and testable. Read `ARCHITECTURE.md` for the full picture; the rules below are the must-follow summary. If a rule and a request conflict, surface the conflict — do not silently break a rule.

### The architecture in one paragraph

We use **Pragmatic Clean Architecture**. Code is organized by feature in `src/features/<feature>/`, with four layers: `domain/` (pure TypeScript, no framework imports), `application/` (use cases + repository interfaces), `adapters/` (Supabase repositories, Zod schemas, server actions, composition root), and `ui/` (React components). **Dependencies always point inward**: outer layers import from inner layers, never the reverse. We use **functional DI** — factory functions with explicit `Deps` types, assembled at a per-feature composition root. There is no DI container.

### Rules Claude Code MUST follow

**R1. The dependency direction is inviolable.**
- `domain/` may not import from `application/`, `adapters/`, `ui/`, `app/`, `next/*`, `@supabase/*`, `react`, or `zod`.
- `application/` may not import from `adapters/`, `ui/`, `app/`, `next/*`, `@supabase/*`, or any specific repository implementation. It may import from this feature's `domain/` and from `src/shared/domain/`.
- `adapters/` may import from this feature's `domain/`, `application/`, plus `next/*`, `@supabase/*`, `zod`, and shared infrastructure.
- `app/` (Next.js routes) imports feature UI components and calls server actions — it never imports directly from `domain/`.

If you find yourself wanting to break R1, **stop and ask**. The most common temptation: "just import Supabase here in the use case for one quick query." No. Add a method to the repository interface and implement it in the adapter.

**R2. Every feature lives in `src/features/<feature>/`** with the four subfolders (`domain/`, `application/`, `adapters/`, `ui/`) and a `__tests__/` folder. No exceptions. New top-level folders need an ADR.

**R3. Repository interfaces are defined in `application/`, implemented in `adapters/`.** Never define a repository interface inside `adapters/` — the dependency would point the wrong way.

**R4. Use cases are factory functions with explicit `Deps`.**
```ts
export interface CreateXDeps { repo: XRepository; clock?: Clock }
export function makeCreateX({ repo, clock = systemClock }: CreateXDeps) {
  return async function createX(input: CreateXInput) { /* ... */ }
}
```
Don't create top-level singletons. Don't reach into module-scope state. Pass dependencies in.

**R5. Server actions are thin.** A server action in `adapters/actions.ts` does three things: parse input with Zod, call a use case via the composition root, and return / revalidate. Domain logic does not live in server actions.

**R6. Validation has two layers.** Zod validates **input shape** at the adapter boundary. Domain validation (length, business rules, invariants) lives in the use case or domain layer. Don't conflate them.

**R7. Tests for use cases use fake repositories, not real Supabase.** Unit tests must not touch the database. The DI pattern exists specifically to make this trivial.

**R8. RLS is required, not optional.** Every Supabase migration that creates a user-data table must enable Row-Level Security and define policies in the same migration. A table without RLS is a bug.

**R9. Adding a feature follows the order in `ARCHITECTURE.md` § Adding a new feature**: domain → application → adapters → delivery → docs. Don't start from the UI and work inward.

**R10. When unsure where something belongs, the question is "what does this depend on?"** If it depends on Supabase, it's an adapter. If it depends only on domain types, it's application. If it depends on nothing framework-y, it's domain.

**R11. Every use case requires at least one unit test using a fake repository.** A new use case in `application/` is incomplete without a corresponding test in `__tests__/` that exercises it through a fake repo (no Supabase, no network). The pattern is shown in `src/features/todos/__tests__/createTodo.test.ts`.

### The canonical worked example

When in doubt about how a feature should be structured, **look at `src/features/todos/`**. That folder is the reference implementation of every rule above:

- `domain/Todo.ts` — pure entity, value types, validation rules
- `application/TodoRepository.ts` — interface defined here
- `application/createTodo.ts` — factory-function use case with explicit `Deps`
- `adapters/SupabaseTodoRepository.ts` — implements the interface
- `adapters/composition.ts` — composition root
- `adapters/actions.ts` — thin server action
- `__tests__/createTodo.test.ts` — unit test using a fake repo

A new feature should mirror this folder structure. The `src/features/todos/README.md` walks through the file order for a new reader.

### Visual reference

The architecture is also rendered as diagrams in [`./diagrams/`](./diagrams/):
- `1_context.png` / `2_container.png` / `3_component.png` — C4 levels 1–3 (the third one *is* the Clean Architecture diagram)
- `4_seq_signup.png` / `5_seq_pairing.png` / `6_seq_todo.png` — sequence diagrams for the trickier flows

Re-render with `python3 diagrams/render.py` after non-trivial architecture changes.

### Before writing any non-trivial code

Quick mental checklist:
- [ ] Have I read `ARCHITECTURE.md` for this feature area?
- [ ] Have I read the relevant entry in `FEATURES.md`?
- [ ] Do I know which layer this code belongs in?
- [ ] If I'm adding a new dependency, is it allowed by the dependency rule?
- [ ] Will this be testable without spinning up Supabase?
- [ ] Have I looked at how `src/features/todos/` solves the same shape of problem?

---

## Quick context — the stack (one screen)

- **Web app, PWA** (installable on iOS Safari and Android Chrome via Add to Home Screen)
- **Frontend:** Next.js 15 (App Router) + TypeScript + React 19 + Tailwind v4 + shadcn/ui + lucide-react
- **Backend:** Supabase (Postgres + Auth + Realtime), Row-Level Security enforced
- **Hosting:** Vercel (frontend) + Supabase Cloud (backend)
- **Forms:** React Hook Form + Zod
- **Tests:** Vitest + Playwright
- **Package manager:** pnpm

Full detail and rationale in `TECH_STACK.md` and `DECISIONS.md`.

---

## Repo layout (target)

See `TECH_STACK.md` § Repository layout. Once the repo is bootstrapped, this section can be made authoritative.

---

## How to start any session

1. Read this file.
2. Skim `FEATURES.md`, `TECH_STACK.md`, `ARCHITECTURE.md`, and `DECISIONS.md` for context relevant to the request.
3. If the request involves writing or changing code, also open `src/features/todos/` — that's the canonical pattern to mirror.
4. Confirm the scope of the task with Stef before writing code or making non-trivial recommendations.
5. Plan before coding (use a TodoList for any non-trivial change).
6. Update relevant docs as part of the change.

---

## Notes for Claude Code sessions specifically

- Honor the rules above without prompting.
- Prefer small, reviewable changes. One feature per branch.
- Mirror `src/features/todos/` when adding any new feature — same four subfolders, same file shapes, same DI pattern.
- Always run `pnpm typecheck` and the relevant tests before declaring a task done.
- A new use case is not "done" until R11 is satisfied (unit test using a fake repo).
- When generating SQL migrations for Supabase, place them under `supabase/migrations/` and ensure RLS is enabled on every new user-data table.
- If a change alters the architecture (new layer, new boundary, new repository interface), update `ARCHITECTURE.md` *and* re-render the diagrams (`python3 diagrams/render.py`).
- Never store secrets in the repo. All env vars go in Vercel + Supabase config.
