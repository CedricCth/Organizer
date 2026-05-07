# ADR-006 — Architecture: Pragmatic Clean Architecture + C4 + functional DI

**Date:** 2026-05-07
**Status:** Accepted

## Context

Stef explicitly asked for "best practice and most extensible," with SOLID (especially Open/Closed) and dependency injection treated as first-class concerns. The app will grow over time (MVP → v1.1 → v2 → maybe). Future Claude Code sessions will implement features semi-independently, and we want them to be unable to silently violate the architectural intent.

We need:
1. A **visualization** of the architecture so the structure can be grasped at a glance.
2. A **code organization** that enforces SOLID and is genuinely extensible.
3. A **DI mechanism** that makes use cases testable without ceremony.

## Options considered

### Visualization

1. **C4 (Context / Container / Component) + sequence diagrams**, all in Mermaid in markdown. Modern de-facto standard since Simon Brown's work in the late 2010s, still the recommended approach in 2026.
2. **Full classical UML 2.x** (class, sequence, state, deployment). Comprehensive but heavy; class diagrams don't map cleanly to modern TypeScript + Server Components.
3. **Ad-hoc box-and-arrow diagrams** with no formal model. Quick but doesn't scale and gets stale.

### Code organization

1. **Pragmatic Clean Architecture** — four layers (domain / application / adapters / infrastructure) with the dependency rule pointing inward. Adapted thoughtfully for Next.js Server Components and Supabase.
2. **Strict / textbook Clean Architecture** — same layers, with extra ceremony (presenters, DTOs at every boundary, Server Components forbidden from calling use cases directly). Most disciplined, most files.
3. **Layered modular monolith** — feature folders with repository + service layers but no strict domain/application split. Faster to write, less extensible long-term.

### DI mechanism

1. **Manual functional DI** — factory functions take a `Deps` object; a composition root wires real impls. No runtime library.
2. **Lightweight DI container** (e.g. `tsyringe`) — decorator-based auto-wiring. Reduces boilerplate at scale but adds a runtime dep and learning curve.
3. **Class-based manual DI** — same idea as #1 but with classes and constructor injection. More OO ceremony.

## Decision

- **Visualization: C4 (Levels 1–3) + sequence diagrams for tricky flows (signup, couple pairing, todo + realtime fan-out), all in Mermaid in [`../ARCHITECTURE.md`](../ARCHITECTURE.md).**
- **Code organization: Pragmatic Clean Architecture** with the four-layer split documented in [`../ARCHITECTURE.md`](../ARCHITECTURE.md). Each feature lives in `src/features/<feature>/` with `domain/`, `application/`, `adapters/`, `ui/` subfolders.
- **DI: manual functional DI**, factory functions with explicit `Deps` types, assembled in a per-feature `adapters/composition.ts`.

## Why this combination

- C4 + Mermaid is plain-text in the repo — diagrams version-control with the code, render in GitHub and most editors, and don't require special tooling.
- Pragmatic clean architecture protects the things that benefit from protection (domain rules, business logic) without imposing ceremony on the things that don't (Server Components calling a use case is fine; we're not introducing presenters just to satisfy a doctrine).
- Functional DI is idiomatic in modern TypeScript, equally testable, and skips a runtime DI library we don't need at our scale.

## Trade-offs accepted

- More files than a "throw it all in `app/`" Next.js layout. The four-layer split adds folders per feature.
- Future Claude Code sessions need to internalize the dependency-direction rule. We mitigate this with explicit rules in [`../../CLAUDE.md`](../../CLAUDE.md) and a worked code example in `src/features/todos/`.
- We are not maximally swappable: while domain and application are framework-free, the adapter layer is plainly tied to Supabase. We've decided that's acceptable — the protection that matters is on the inner layers.

## Revisit when

- The four-layer split feels heavy for the actual size of features being added (then we relax toward layered modular).
- We outgrow manual DI (then we consider `tsyringe` or similar).
- A new diagramming tool offers something materially better than C4 + Mermaid.
