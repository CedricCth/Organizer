# Tech Stack — Couples App

> Source of truth for **what we are building it with**. Always read this before pulling in a new library, framework, or service. If a request implies tech that isn't here, raise it as an ADR in `DECISIONS.md` first.
> Last reviewed: 2026-05-07

---

## At a glance

| Layer | Choice | Notes |
|---|---|---|
| App type | Progressive Web App (PWA) | Installable on iOS + Android via "Add to Home Screen" |
| Frontend framework | **Next.js 15** (App Router) | React Server Components + client islands |
| Language | **TypeScript** (strict mode) | Non-negotiable |
| UI library | **React 19** | Bundled with Next 15 |
| Styling | **Tailwind CSS v4** | Utility-first, fast |
| Component library | **shadcn/ui** | Copy-paste components, fully customizable, cute by default |
| Icons | **lucide-react** | Pairs with shadcn |
| Forms | **React Hook Form** + **Zod** | Schema-first validation, shared between client and server |
| Auth | **Supabase Auth** | Email/password, secure session cookies |
| Database | **Postgres** (via Supabase) | Relational, with Row-Level Security |
| Realtime | **Supabase Realtime** | Postgres changes streamed via websockets |
| Hosting (frontend) | **Vercel** | Zero-config Next.js, free tier sufficient for personal use |
| Backend services | **Supabase Cloud** | Hosted Postgres + Auth + Realtime + Storage |
| Package manager | **pnpm** | Fast, disk-efficient |
| Lint / Format | **ESLint** + **Prettier** | Standard configs |
| Testing | **Vitest** (unit) + **Playwright** (e2e) | |
| PWA tooling | **next-pwa** (or built-in Next.js PWA support if mature enough at install time) | Service worker + manifest |
| Web push | **web-push** library + Supabase function | iOS 16.4+, Android, Desktop |

---

## Why this stack (short version)

- **Next.js 15 + React 19 + TypeScript** is the most-used, most-documented, and most Claude-Code-friendly web stack as of mid-2026. App Router with Server Components keeps the bundle small and the auth secure (server-side session checks).
- **Tailwind v4 + shadcn/ui + lucide** gives us a fast path to a custom, cute look without fighting a heavy component library. shadcn components live in our own repo, so we can theme them to feel warm.
- **Supabase** gives us auth + Postgres + realtime + storage in one. Row-Level Security means "Couple A cannot see Couple B's todos" is enforced in the database, not just in app code — a much stronger guarantee.
- **Vercel + Supabase Cloud** means zero infra work. Push to GitHub, it's live on HTTPS with a real domain.

The full case for each major choice (with alternatives considered) lives in `DECISIONS.md`.

---

## Repository layout (target)

This layout follows Pragmatic Clean Architecture (see `ARCHITECTURE.md`). Each feature is self-contained under `src/features/<feature>/` with the four-layer split.

```
couples-app/
├── app/                                # Next.js App Router (delivery layer — thin)
│   ├── (auth)/{login,signup,reset}/page.tsx
│   ├── (app)/{todos,couple,settings}/page.tsx
│   ├── api/                            # route handlers if needed
│   ├── layout.tsx
│   └── manifest.webmanifest
│
├── src/
│   ├── features/                       # one folder per feature; never import across features' internals
│   │   ├── auth/
│   │   │   ├── domain/                 # User, Email value object, AuthErrors — pure TS
│   │   │   ├── application/            # signUp.ts, signIn.ts, UserRepository.ts (interface)
│   │   │   ├── adapters/               # SupabaseUserRepository.ts, actions.ts, schema.ts, composition.ts
│   │   │   ├── ui/                     # SignUpForm.tsx, LoginForm.tsx
│   │   │   └── __tests__/
│   │   ├── couple/
│   │   │   └── ... (same shape)
│   │   └── todos/
│   │       └── ... (same shape)
│   │
│   └── shared/
│       ├── domain/                     # cross-feature primitives (UserId, CoupleId, branded types)
│       ├── infrastructure/
│       │   ├── supabase/{browserClient,serverClient}.ts
│       │   └── env.ts                  # typed env vars (Zod-validated)
│       └── ui/                         # cross-feature UI helpers
│
├── components/
│   └── ui/                             # shadcn/ui primitives (button, input, dialog, ...)
│
├── supabase/
│   └── migrations/                     # SQL migrations, RLS enabled on every user-data table
│
├── public/
│   └── icons/                          # PWA icons (192, 512, maskable, apple-touch)
│
├── tests/
│   ├── unit/                           # cross-feature unit suites (per-feature tests live alongside code)
│   └── e2e/                            # Playwright
│
├── CLAUDE.md
├── ARCHITECTURE.md
├── FEATURES.md
├── TECH_STACK.md
├── DECISIONS.md
├── WORKFLOW.md
└── package.json
```

The dependency rule (`infrastructure → adapters → application → domain`, always inward) is documented in `ARCHITECTURE.md` and codified in `CLAUDE.md` § Architecture rules.

---

## PWA specifics

- `manifest.webmanifest` with name, icons (192, 512, maskable), theme color, `display: "standalone"`.
- Service worker for offline shell (cache static assets, fall back to "you're offline" page for data routes).
- Install prompt UX: gentle banner on second visit, never blocking.
- iOS notes:
  - Push notifications work on iOS 16.4+, but only after the user installs the PWA to their home screen and grants permission.
  - Status bar styling via `apple-mobile-web-app-status-bar-style`.
  - Apple touch icon set explicitly.

---

## Security baseline (must-haves)

- **Transport:** HTTPS everywhere, HSTS preload.
- **Sessions:** httpOnly + Secure + SameSite=Lax cookies. No tokens in localStorage.
- **Auth:** Supabase email/password with strong-password rule (min 12 chars), email confirmation required.
- **DB authorization:** Row-Level Security enabled on every user-data table. Tested via Supabase test fixtures.
- **CSP:** Strict Content-Security-Policy header — no inline scripts.
- **Rate limiting:** at the Supabase / Vercel edge for `/auth/*` and signup.
- **Input validation:** Zod schemas on every form, mirrored on server actions.
- **PII in logs:** none. Hash or redact emails in logs.
- **Dependencies:** Renovate bot or `pnpm audit` weekly.
- **Secrets:** all in Vercel env vars and Supabase project secrets — nothing committed.

---

## What we will NOT add without an ADR

- Any new state management library (we'll use React + Supabase + Zustand only if absolutely needed).
- Any new CSS / styling system besides Tailwind.
- Any analytics or tracking SDK.
- Any AI / LLM integration that sends couple data anywhere.
- A different database or ORM.
- A different auth provider.

---

## Versions to verify at install time

These were current at planning time (2026-05-07). Re-check with `pnpm outdated` or each package's docs at the moment of bootstrapping the repo, since this stack moves quickly:

- Next.js 15.x
- React 19.x
- Tailwind CSS v4.x
- TypeScript 5.x
- Supabase JS v2.x

Pin major versions in `package.json` and rely on Renovate / Dependabot for minor bumps.
