# Architecture Decision Records

> The **why** behind major technical and architectural choices for the Couples App. Each ADR captures one decision: the context, the options considered, what we picked, and what we accepted in trade. Once written, ADRs are **never edited** — if a decision changes, write a new ADR that supersedes the old one and mark the old one's status accordingly. The history is the value.

## Index

| # | Title | Status |
|---|---|---|
| [0001](./0001-pwa-app-type.md) | App type: Progressive Web App (PWA) | Accepted |
| [0002](./0002-supabase-backend.md) | Backend: Supabase | Accepted |
| [0003](./0003-nextjs-tailwind-shadcn.md) | Frontend: Next.js 15 + Tailwind v4 + shadcn/ui | Accepted |
| [0004](./0004-vercel-hosting.md) | Hosting: Vercel (frontend) + Supabase Cloud (backend) | Accepted |
| [0005](./0005-mvp-scope.md) | MVP scope: Auth + Shared Todos only | Accepted |
| [0006](./0006-clean-architecture.md) | Architecture: Pragmatic Clean Architecture + C4 + functional DI | Accepted |
| [0007](./0007-docker-local-dev.md) | Docker for local development | Accepted |

## Conventions

- **Filename:** `NNNN-short-slug.md`, four-digit zero-padded number, lowercase kebab-case slug.
- **Numbering:** strictly sequential. The next ADR is `0008-…`. Numbers are never reused.
- **Status values:** `Proposed` · `Accepted` · `Deprecated` · `Superseded by ADR-NNNN`.
- **Never rewrite a past ADR.** If a decision changes, write a new ADR that says "Supersedes ADR-NNNN" and update the older ADR's status to "Superseded by ADR-MMMM". Keep the trail.
- **Length:** roughly one page. If it's longer, you probably have a system design doc, not an ADR.

## Template

Copy this skeleton when adding a new ADR:

```markdown
# ADR-NNNN — <short title>

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded by ADR-MMMM

## Context

What's the situation? What constraints are real?

## Options considered

1. Option A — pros / cons
2. Option B — pros / cons
3. Option C — pros / cons

## Decision

What we picked and the one-sentence reason.

## Trade-offs accepted

What we are knowingly giving up.

## Revisit when

Conditions that should make us reconsider.
```

## When to write a new ADR

- We're choosing between technologies, libraries, or services and the choice will be hard to undo.
- We're locking in a pattern that future Claude sessions will be expected to follow.
- We're saying "no" to a tempting option for a reason future-us will want to remember.

If you're not sure whether something needs an ADR — write it. Cheap insurance.
