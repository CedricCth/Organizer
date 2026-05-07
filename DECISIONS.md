# Architectural Decisions

> The "why" behind major technical choices for the Couples App. New decisions are appended chronologically. Each ADR (Architectural Decision Record) lists context, alternatives considered, the decision, and trade-offs accepted.
>
> If a future request implies changing one of these decisions, write a new ADR superseding the old one — don't silently change direction.

---

## ADR template

```
## ADR-XXX — <short title>
**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded by ADR-YYY

### Context
What's the situation? What constraints are real?

### Options considered
1. Option A — pros / cons
2. Option B — pros / cons
3. Option C — pros / cons

### Decision
What we picked and the one-sentence reason.

### Trade-offs accepted
What we are knowingly giving up.

### Revisit when
Conditions that should make us reconsider.
```

---

## ADR-001 — App type: Progressive Web App (PWA)
**Date:** 2026-05-07
**Status:** Accepted

### Context
Stef is on Android. Partner is on iOS. Stef does not have a Mac, which is required for iOS App Store publishing. The goal is the fastest possible path to a working app both partners can use, with no app-store gatekeepers and no recurring fees.

### Options considered
1. **PWA (Progressive Web App)** — built as a website, installable to home screen on iOS Safari and Android Chrome. Works on desktop too. No stores. Free.
2. **React Native + Expo** — single codebase, native iOS + Android. Excellent DX. But: iOS App Store still requires a Mac for final build/submit (or paid EAS Build at $99+/year), plus $99/year Apple Developer fee.
3. **Flutter** — same store-publishing problem as React Native, plus a new language to learn (Dart) and a smaller backend ecosystem.
4. **Fully native (Swift + Kotlin)** — best polish per platform, but two codebases. Massive overkill for an MVP.

### Decision
**PWA.** Built as a Next.js web app, with a manifest + service worker so it can be added to the home screen and behave like a native app.

### Trade-offs accepted
- iOS only allows PWA installation from Safari (not Chrome on iOS).
- iOS push notifications work but require installing the PWA first, and lag native apps on a few minor features.
- No native widgets or deep OS integrations.
- The "Add to Home Screen" step is one extra friction point compared to App Store install.

### Why this is right *for now*
Zero gatekeepers, zero fees, both partners can use it the day it ships. If we later want native presence, we can wrap the PWA in **Capacitor** without rewriting — most logic stays as-is.

### Revisit when
- We want App Store / Play Store presence for credibility or distribution.
- iOS PWA limitations start blocking a feature we genuinely need.

---

## ADR-002 — Backend: Supabase
**Date:** 2026-05-07
**Status:** Accepted

### Context
We need: user auth, a database for shared todos, real-time sync ("when partner adds a todo, I see it"), strict data isolation between couples, and we want minimal ops work for an MVP.

### Options considered
1. **Supabase** — Postgres + Auth + Realtime + Storage as a managed service. Open source. Generous free tier. Row-Level Security policies enforce data isolation in the database itself.
2. **Firebase** — Google's BaaS. Mature, scales well, easy auth. Firestore is NoSQL.
3. **Custom Node.js + Postgres backend** — full control, hosted on Railway/Fly/Render. Maximum flexibility.
4. **Appwrite / PocketBase / Convex** — newer alternatives. Smaller ecosystems, less Claude-Code documentation, more risk for a couple-of-users app.

### Decision
**Supabase.**

### Why
- **Relational data fits the domain.** Couples ↔ users ↔ todos is a graph of foreign keys. SQL is the right shape; Firestore's NoSQL would force us into denormalization gymnastics.
- **Row-Level Security is the perfect privacy primitive.** We write one policy like `auth.uid() IN (couple.user_a, couple.user_b)` and the database itself refuses to return another couple's data — even if we have a bug in app code. Firebase has security rules but they're harder to test and reason about for relational data.
- **Realtime is built-in.** Postgres changes stream over websockets; the client `useEffect`s to a channel. No extra service to run.
- **Open source escape hatch.** If Supabase the company ever goes away or changes pricing, we can self-host the same software. Firebase has no such option.
- **Auth is included** with secure-by-default cookie sessions, email confirmation, password reset — nothing to build from scratch.

### Trade-offs accepted
- Less mature mobile SDK than Firebase (not relevant for a PWA).
- Realtime can lag under extreme load — irrelevant at our scale.
- We are tied to Postgres flavor of SQL.

### Revisit when
- We want to scale to thousands of couples and need very specific infra control.
- We need a feature Supabase doesn't support (very unlikely for this app's scope).

---

## ADR-003 — Frontend: Next.js 15 + Tailwind v4 + shadcn/ui
**Date:** 2026-05-07
**Status:** Accepted

### Context
Need a frontend framework that:
- supports PWA cleanly,
- has excellent server-side auth handling (so we don't ship sessions to the client),
- is well-documented and understood by Claude Code (so future implementation work is high-quality),
- gives us a "cute" customizable look without huge component libraries.

### Options considered
1. **Next.js 15 (App Router) + Tailwind v4 + shadcn/ui** — current React mainstream. Server Components + Server Actions handle auth elegantly.
2. **Remix / React Router v7** — also good for forms-heavy apps. Smaller ecosystem in 2026, fewer deployment integrations.
3. **SvelteKit + Tailwind** — beautiful DX, smaller bundles, but smaller community and fewer Supabase examples.
4. **Plain Vite + React + Tailwind** — simplest, but we'd hand-roll routing, SSR, server-side auth, etc.

### Decision
**Next.js 15 (App Router) + TypeScript + Tailwind v4 + shadcn/ui + lucide-react icons.**

### Why
- Vercel makes deployment a single `git push`.
- Server Components let auth checks happen server-side — no flash of unauthenticated content.
- Tailwind v4's perf improvements and CSS-first config are a real upgrade.
- shadcn/ui ships components into our repo (rather than as a black-box library), which means we can theme everything to feel warm, soft, and couples-y without fighting library defaults.
- Best-documented stack for Claude Code, which directly helps you ship faster in later sessions.

### Trade-offs accepted
- Next.js has more concepts to learn (Server vs Client Components, Server Actions, etc.) than a plain SPA — but the payoff is real and Claude Code handles them well.
- Vercel lock-in is mild — we can self-host Next.js elsewhere if needed.

### Revisit when
- Bundle size or perf becomes a real problem (it won't for this app).
- We have a strong reason to prefer a different framework.

---

## ADR-004 — Hosting: Vercel (frontend) + Supabase Cloud (backend)
**Date:** 2026-05-07
**Status:** Accepted

### Context
Want HTTPS, a custom domain, edge performance, and zero ops. Want it free or near-free for personal use.

### Options considered
1. **Vercel + Supabase Cloud** — zero-config, free tiers cover this app's usage, automatic HTTPS, preview deployments per branch.
2. **Self-hosted on a VPS (Hetzner / DigitalOcean)** — cheaper at scale, full control, but real ops work (TLS, deploys, backups, monitoring).
3. **Cloudflare Pages + Workers + D1** — very fast, but D1 is SQLite-flavored and lacks Supabase's auth/realtime out of the box.
4. **Netlify + Supabase Cloud** — similar to Vercel but Vercel has tighter Next.js integration.

### Decision
**Vercel for the Next.js app, Supabase Cloud for the backend.**

### Trade-offs accepted
- Mild vendor coupling to Vercel's Next.js deployment model.
- Free tier limits exist but won't bite for a 2-person personal app.

### Revisit when
- Free tier limits are hit consistently.
- We want everything on one provider for simplicity.

---

## ADR-005 — MVP scope: Auth + Shared Todos only
**Date:** 2026-05-07
**Status:** Accepted

### Context
The user explicitly asked for a lean MVP. The risk of feature-complete v1 is shipping nothing for months while polishing things that turn out not to matter.

### Options considered
1. **Lean MVP** — auth + couple pairing + shared todos. Ship in weeks.
2. **Feature-complete v1** — also includes recurring tasks, activity feed, notifications, categories. Ship in months.

### Decision
**Lean MVP.** Recurring tasks and activity feed move to v1.1, notifications and categories to v2. See `FEATURES.md` for the full milestone split.

### Trade-offs accepted
- v1.0 will feel basic — that's fine; the goal is to learn what we actually use.
- Recurring tasks are listed as a household must-have ("weekly cleaning, shopping"), so v1.1 needs to follow MVP quickly.

### Revisit when
- MVP is shipped and we know what we actually reach for daily.

---

## ADR-006 — Architecture: Pragmatic Clean Architecture + C4 + functional DI
**Date:** 2026-05-07
**Status:** Accepted

### Context
Stef explicitly asked for "best practice and most extensible," with SOLID (especially Open/Closed) and dependency injection treated as first-class concerns. The app will grow over time (MVP → v1.1 → v2 → maybe). Future Claude Code sessions will implement features semi-independently, and we want them to be unable to silently violate the architectural intent.

We need:
1. A **visualization** of the architecture so the structure can be grasped at a glance.
2. A **code organization** that enforces SOLID and is genuinely extensible.
3. A **DI mechanism** that makes use cases testable without ceremony.

### Options considered

#### Visualization
1. **C4 (Context / Container / Component) + sequence diagrams**, all in Mermaid in markdown. Modern de-facto standard since Simon Brown's work in the late 2010s, still the recommended approach in 2026.
2. **Full classical UML 2.x** (class, sequence, state, deployment). Comprehensive but heavy; class diagrams don't map cleanly to modern TypeScript + Server Components.
3. **Ad-hoc box-and-arrow diagrams** with no formal model. Quick but doesn't scale and gets stale.

#### Code organization
1. **Pragmatic Clean Architecture** — four layers (domain / application / adapters / infrastructure) with the dependency rule pointing inward. Adapted thoughtfully for Next.js Server Components and Supabase.
2. **Strict / textbook Clean Architecture** — same layers, with extra ceremony (presenters, DTOs at every boundary, Server Components forbidden from calling use cases directly). Most disciplined, most files.
3. **Layered modular monolith** — feature folders with repository + service layers but no strict domain/application split. Faster to write, less extensible long-term.

#### DI mechanism
1. **Manual functional DI** — factory functions take a `Deps` object; a composition root wires real impls. No runtime library.
2. **Lightweight DI container** (e.g. `tsyringe`) — decorator-based auto-wiring. Reduces boilerplate at scale but adds a runtime dep and learning curve.
3. **Class-based manual DI** — same idea as #1 but with classes and constructor injection. More OO ceremony.

### Decision
- **Visualization: C4 (Levels 1–3) + sequence diagrams for tricky flows (signup, couple pairing, todo + realtime fan-out), all in Mermaid in `ARCHITECTURE.md`.**
- **Code organization: Pragmatic Clean Architecture** with the four-layer split documented in `ARCHITECTURE.md`. Each feature lives in `src/features/<feature>/` with `domain/`, `application/`, `adapters/`, `ui/` subfolders.
- **DI: manual functional DI**, factory functions with explicit `Deps` types, assembled in a per-feature `adapters/composition.ts`.

### Why this combination
- C4 + Mermaid is plain-text in the repo — diagrams version-control with the code, render in GitHub and most editors, and don't require special tooling.
- Pragmatic clean architecture protects the things that benefit from protection (domain rules, business logic) without imposing ceremony on the things that don't (Server Components calling a use case is fine; we're not introducing presenters just to satisfy a doctrine).
- Functional DI is idiomatic in modern TypeScript, equally testable, and skips a runtime DI library we don't need at our scale.

### Trade-offs accepted
- More files than a "throw it all in `app/`" Next.js layout. The four-layer split adds folders per feature.
- Future Claude Code sessions need to internalize the dependency-direction rule. We mitigate this with explicit rules in `CLAUDE.md` and a worked code example in `src/features/todos/`.
- We are not maximally swappable: while domain and application are framework-free, the adapter layer is plainly tied to Supabase. We've decided that's acceptable — the protection that matters is on the inner layers.

### Revisit when
- The four-layer split feels heavy for the actual size of features being added (then we relax toward layered modular).
- We outgrow manual DI (then we consider `tsyringe` or similar).
- A new diagramming tool offers something materially better than C4 + Mermaid.
