# Backlog — Couples App

> The prioritized list of **epics** (feature-sized chunks of work) that turn the plan in `FEATURES.md` into shippable software. Pull from the top.
> Last updated: 2026-05-07

---

## How this backlog works

This is the strategic doc — **what** we plan to build, **in what order**, with rough effort and the dependencies between epics. The tactical, day-to-day breakdown lives in the **TodoList** (in this Cowork session, and later in GitHub Issues / Linear if we move there).

Workflow, like a real engineering team would do it:

1. **Refinement.** Before we start an epic, we re-read it here, sanity-check scope, break it into tasks in the TodoList. If new info changes the size, we update this file.
2. **Pull from the top.** Always work the highest-priority unblocked epic. Don't cherry-pick a P2 because it's fun.
3. **One epic at a time.** Finish before starting the next. Half-done epics are technical debt.
4. **Definition of Done is non-negotiable.** Each epic has a DoD checklist. Not done until DoD is green — including doc updates.
5. **Update on ship.** When an epic completes: mark the line `✅ shipped <date>`, update `FEATURES.md`, move to "Recently shipped" at the bottom of this file.
6. **Add new ideas to `FEATURES.md` first**, then promote to the backlog only when scoped. Backlog = scoped work, not raw wishes.

---

## Legend

**Priority**

| Tag | Meaning |
|---|---|
| **P0** | MVP critical path — must ship to have an app at all |
| **P1** | First post-MVP wave (v1.1) — landed soon after launch |
| **P2** | v2 delight features — once the app is loved and used daily |
| **P3** | "Maybe / dreaming" — listed so we don't forget; no commitment yet |

**Size** (T-shirt + day range — pace-agnostic, calendar days at the rate we're actually working)

| Size | Days | Means |
|---|---|---|
| **S** | ~1–2d | Single sitting, low risk, well understood |
| **M** | ~3–4d | A few sittings, some unknowns, one feature folder |
| **L** | ~5–7d | New feature folder + DB + UI + tests, real surface area |
| **XL** | ~8–10d | Big — multiple new layers/integrations, or canonical reference work |

**Status**

| Status | Meaning |
|---|---|
| **Backlog** | Scoped, not started |
| **Refining** | Being broken into tasks |
| **In progress** | Actively being implemented |
| **Blocked** | Waiting on a dependency or a decision |
| **Done** | Shipped (move to "Recently shipped" at the bottom) |

---

## Currently in progress

_Nothing yet._

---

## P0 — MVP (must ship to have an app)

These seven epics deliver the MVP scope from `FEATURES.md` § MVP — v1.0. Order matters: each unlocks the next. Total rough estimate **~28–37 days** of focused work.

### EPIC-01 — Project Bootstrap & Tooling
- **Priority:** P0 · **Size:** M (~3d) · **Status:** Backlog
- **Depends on:** — (this is the start)
- **Milestone:** MVP
- **Why:** There is no running Next.js app yet. We have an architectural skeleton (`src/features/todos/`) but no `package.json`, no app router, no shadcn setup, no CI. Nothing else can start until this exists.
- **Scope:**
  - Initialize the repo with **pnpm + Next.js 15 (App Router) + TypeScript strict + React 19**.
  - Wire **Tailwind v4**, **shadcn/ui**, **lucide-react**.
  - Set up **ESLint + Prettier**, **Vitest** (unit), **Playwright** (e2e).
  - Confirm the four-layer folder skeleton (`src/features/`, `src/shared/`, `app/`, `components/ui/`, `supabase/migrations/`) and that the existing `src/features/todos/` skeleton compiles inside the new project.
  - A simple `/health` page that renders with shadcn primitives — proof of life.
  - First commit pushed to GitHub; first deploy live on Vercel with HTTPS.
- **Definition of Done:**
  - [ ] `pnpm typecheck`, `pnpm lint`, `pnpm test`, `pnpm build` all pass locally.
  - [ ] `/health` page is live on a Vercel preview URL.
  - [ ] `TECH_STACK.md` updated with any version pins discovered during install.

### EPIC-02 — Supabase Project & Auth Wiring
- **Priority:** P0 · **Size:** M (~3d) · **Status:** Backlog
- **Depends on:** EPIC-01
- **Milestone:** MVP
- **Why:** Everything user-facing depends on having a configured Supabase project and a typed, validated env. Locking this down once means feature epics never have to fight infra.
- **Scope:**
  - Create the Supabase project (Cloud); record project URL + anon/service keys.
  - **Zod-validated env loader** in `src/shared/infrastructure/env.ts`.
  - **Server + browser Supabase clients** (the server one already stubbed out — wire to real env, plus a browser client).
  - First migration in `supabase/migrations/`: `profiles` table (display_name, avatar_url, fk to `auth.users`) **with RLS enabled and policies**.
  - Server-side `getCurrentUser()` helper in `shared/infrastructure/`.
  - Local Supabase dev workflow documented in CLAUDE.md notes (or a short `supabase/README.md`).
- **Definition of Done:**
  - [ ] Local dev hits Supabase Cloud successfully.
  - [ ] `profiles` migration applies cleanly; RLS policy unit-tested with two fake users.
  - [ ] Vercel env vars set; preview build connects to Supabase.

### EPIC-03 — Auth & Account
- **Priority:** P0 · **Size:** L (~5d) · **Status:** Backlog
- **Depends on:** EPIC-02
- **Milestone:** MVP · **FEATURES.md ref:** § MVP / Auth & Account
- **Why:** Sign-up, sign-in, sign-out, password reset, basic profile. First real feature to mirror the canonical `todos/` shape — sets the precedent for everything after.
- **Scope:**
  - `src/features/auth/` with full four-layer split (mirrors `todos/`).
  - **Domain:** `User`, `Email` value object, `AuthErrors` (InvalidEmail, WeakPassword, EmailTaken, etc.).
  - **Application:** `signUp`, `signIn`, `signOut`, `requestPasswordReset` — factory functions with explicit `Deps`. `UserRepository` interface in this layer.
  - **Adapters:** `SupabaseUserRepository`, `schema.ts` (Zod), `actions.ts` (server actions), `composition.ts`.
  - **UI:** `SignUpForm`, `LoginForm`, `ResetForm`, basic profile edit (display name + optional avatar). Built on shadcn primitives, warm/calm tone.
  - **Pages:** `/signup`, `/login`, `/reset`, `/onboarding`, `/settings/profile`.
  - Strong-password rule (min 12 chars, complexity not over-strict).
  - Email confirmation flow, secure httpOnly + Secure session cookies.
  - **Tests:** unit tests per use case using **fake repos** (R11), Playwright e2e for the signup happy path.
- **Definition of Done:**
  - [ ] User can sign up, confirm email, log in, log out, reset password from the live preview.
  - [ ] R11 satisfied: each use case has a unit test that doesn't touch Supabase.
  - [ ] e2e: signup → confirm → login → logout green.
  - [ ] `FEATURES.md` Auth lines marked `✅ shipped <date>`.

### EPIC-04 — Couple Pairing
- **Priority:** P0 · **Size:** L (~5d) · **Status:** Backlog
- **Depends on:** EPIC-03
- **Milestone:** MVP · **FEATURES.md ref:** § MVP / Couple Pairing
- **Why:** The "couple" boundary is the foundation of every privacy guarantee. Without it, todos can't be scoped to a couple — and RLS can't isolate data.
- **Scope:**
  - `src/features/couple/` — full four-layer split.
  - **Domain:** `Couple`, `Invite`, errors `AlreadyPairedError`, `ExpiredInviteError`, `UnknownInviteError`.
  - **Application:** `createInvite`, `redeemInvite`, `leaveCouple`. `CoupleRepository` interface.
  - **Adapters:** `SupabaseCoupleRepository`, schema, actions, composition.
  - **DB migrations:** `couples` (user_a, user_b, paired_at), `couple_invites` (code, inviter, expires_at). RLS on both. Unique constraint enforcing one-couple-per-user. Transactional redeem (insert couple + delete invite atomically).
  - **UI:** generate-invite page (shows code + share button), redeem-invite page, leave-couple confirm dialog.
  - **Pages:** `/couple` (lands here when unpaired or paired).
  - Invite expiry (e.g. 24h) and code format that's friendly to share verbally (e.g. `MOON-RIVER-42`).
  - **Tests:** unit + e2e for full pair → leave flow.
- **Definition of Done:**
  - [ ] Two test users pair via invite code on the live preview.
  - [ ] RLS verified: user from a different couple cannot read either party's couple row.
  - [ ] Cannot be in two couples (DB constraint + use case invariant).
  - [ ] FEATURES.md Couple Pairing lines updated.

### EPIC-05 — Shared Todos (canonical feature)
- **Priority:** P0 · **Size:** XL (~8–10d) · **Status:** Backlog
- **Depends on:** EPIC-04
- **Milestone:** MVP · **FEATURES.md ref:** § MVP / Shared Todo List
- **Why:** The core value of the app. Also the **canonical reference** for all future features — it has to fully embody the architecture so future Claude Code sessions can mirror it.
- **Scope:**
  - Promote the existing `src/features/todos/` skeleton to a complete, working feature.
  - **Domain:** finish `Todo` entity, `Title` value object, `AssigneeKind` (`me` / `partner` / `either`), validation rules (title 1–200 chars trimmed), pure status transitions.
  - **Application:** `createTodo`, `listTodos`, `toggleTodo`, `editTodo`, `deleteTodo`. Round out `TodoRepository`.
  - **Adapters:** finish `SupabaseTodoRepository`, schema, actions, composition.
  - **DB migration:** `todos` table (id, couple_id, title, notes, due_date, assignee_kind, assignee_user_id, done_at, created_at, updated_at) with RLS scoped to the couple.
  - **UI:** `TodoList`, `TodoForm`, `TodoItem` with **optimistic updates**, sort by created/due/status. shadcn-based, warm visual tone.
  - **Realtime:** Supabase channel subscription so the partner sees inserts/updates/deletes within ~1s.
  - **Pages:** `/todos`.
  - **Tests:** unit per use case (fake repo), e2e for the full CRUD + realtime fan-out flow (two browser contexts).
  - Update `src/features/todos/README.md` so it accurately describes the now-complete feature.
- **Definition of Done:**
  - [ ] Two paired users can add, edit, complete, delete todos and see each other's changes within 1s on the live preview.
  - [ ] All five use cases have unit tests with a fake repo.
  - [ ] Sort by created / due / status works.
  - [ ] FEATURES.md Shared Todo List lines updated.
  - [ ] `src/features/todos/README.md` is accurate as the canonical reference.

### EPIC-06 — PWA Shell & Install
- **Priority:** P0 · **Size:** M (~3d) · **Status:** Backlog
- **Depends on:** EPIC-01 (technically) but best landed after EPIC-05 so the "installable app" actually does something.
- **Milestone:** MVP · **TECH_STACK.md ref:** § PWA specifics
- **Why:** The PWA part of "Progressive Web App" — without this we are just a website. Stef is on Android, partner on iOS — both must be able to install via Add to Home Screen.
- **Scope:**
  - `manifest.webmanifest` (name, icons 192 / 512 / maskable, theme color, `display: standalone`).
  - PWA icons in `public/icons/`.
  - Service worker for offline shell (cache static assets, fall back to "you're offline" for data routes).
  - Apple touch icon + status-bar style.
  - Gentle install-prompt banner on second visit (no nag).
  - Tested on iOS Safari and Android Chrome via Add to Home Screen.
- **Definition of Done:**
  - [ ] App installs to home screen on iOS and Android with custom icon.
  - [ ] Installed app opens in standalone mode (no browser chrome).
  - [ ] Offline shell loads when network is off.

### EPIC-07 — Security Hardening Baseline
- **Priority:** P0 · **Size:** M (~2–3d) · **Status:** Backlog
- **Depends on:** EPIC-05 (so RLS tests cover real tables)
- **Milestone:** MVP · **TECH_STACK.md ref:** § Security baseline
- **Why:** This app stores relationship data. The security baseline in `TECH_STACK.md` is non-negotiable; this epic makes it true rather than aspirational.
- **Scope:**
  - HSTS preload header.
  - Strict CSP (no inline scripts).
  - Rate limiting on `/auth/*` (Vercel edge or Supabase).
  - PII redaction in server logs.
  - **RLS test fixtures** verifying Couple A truly cannot read Couple B's data across `profiles`, `couples`, `couple_invites`, `todos`.
  - Renovate (or Dependabot) configured; weekly `pnpm audit`.
  - **Account deletion** flow (deletes profile + couple + todos atomically; respects FK cascades).
- **Definition of Done:**
  - [ ] CSP, HSTS verified via observatory scan or equivalent.
  - [ ] Rate-limit returns 429 after threshold on `/auth/*`.
  - [ ] RLS isolation suite passes.
  - [ ] Account deletion removes all couple data; no orphans.
  - [ ] Dependency-update bot is open for PRs.

**🚀 MVP ship gate:** EPIC-01 through EPIC-07 done = launch the MVP to Stef + partner in real life.

---

## P1 — v1.1 (soon after MVP)

These follow within ~2–3 weeks of MVP launch, based on what we actually use day-to-day.

### EPIC-08 — Personal vs Shared Lists
- **Priority:** P1 · **Size:** M (~3d) · **Status:** Backlog
- **Depends on:** EPIC-05
- **Milestone:** v1.1 · **FEATURES.md ref:** § v1.1 / Personal vs Shared
- **Why:** Each partner needs a private list alongside the shared one ("things only I care about today"), with a soft-share toggle.
- **Scope:** new `visibility` column on todos (`personal` | `shared`); RLS updated; UI tab switch; "share my today with partner" toggle that flips a personal todo's visibility for the day.
- **DoD:** RLS enforces partner can't see other partner's `personal` todos unless explicitly shared; UI shows distinct lists; toggle works.

### EPIC-09 — Recurring Household Tasks
- **Priority:** P1 · **Size:** L (~5d) · **Status:** Backlog
- **Depends on:** EPIC-05
- **Milestone:** v1.1 · **FEATURES.md ref:** § v1.1 / Recurring Household Tasks
- **Why:** "Shopping, cleaning, taking out the trash" is half of why this app exists.
- **Scope:** `recurrences` table (rule: weekly / every-N-days / specific days), use case to mark a todo recurring, scheduled job (Supabase function or cron) that recreates the next instance on completion. New use case: `setRecurrence`, `completeRecurrent`. UI: a "🔁 repeat" affordance on the todo form.
- **DoD:** completing a weekly recurring todo creates the next instance with the right date; missed instances don't pile up indefinitely; tests cover the rule engine.

### EPIC-10 — Activity Stream (light)
- **Priority:** P1 · **Size:** M (~3d) · **Status:** Backlog
- **Depends on:** EPIC-05
- **Milestone:** v1.1 · **FEATURES.md ref:** § v1.1 / Activity Stream
- **Why:** "What your partner just did today" — the warm, low-pressure feedback loop.
- **Scope:** `activities` view (or table) derived from todo events; small panel on `/todos` showing today's activity for both partners; warm copy ("Stef finished groceries · 2m ago").
- **DoD:** activity reflects within 2s of the originating event; only shows today; only shows your couple.

---

## P2 — v2 (once MVP is loved)

Delight features. Don't pull these until v1.1 is shipped and we know what we actually reach for.

### EPIC-11 — Web Push Notifications
- **Priority:** P2 · **Size:** L (~5d) · **Status:** Backlog · **Depends on:** EPIC-06, EPIC-10
- **FEATURES.md ref:** § v2 / Push notifications
- Web Push for PWA, iOS 16.4+ supported. Quiet hours. "Partner added X" / "Don't forget Y due today".

### EPIC-12 — Categories / Tags
- **Priority:** P2 · **Size:** M (~3d) · **Status:** Backlog · **Depends on:** EPIC-05
- **FEATURES.md ref:** § v2 / Categories
- Tags table m:n with todos, filter chips on `/todos`, default starter tags (groceries, cleaning, errands, kids).

### EPIC-13 — Shopping List Mode
- **Priority:** P2 · **Size:** M (~3d) · **Status:** Backlog · **Depends on:** EPIC-12
- **FEATURES.md ref:** § v2 / Shopping list
- Optimized one-handed view: large quick-add input, swipe-to-complete, auto-archive completed items after 12h.

### EPIC-14 — Today / Week View
- **Priority:** P2 · **Size:** M (~3d) · **Status:** Backlog · **Depends on:** EPIC-05, EPIC-09
- **FEATURES.md ref:** § v2 / Today/Week view
- Time-bucketed views; recurring tasks render in their week slot.

### EPIC-15 — Streaks & Gentle Stats
- **Priority:** P2 · **Size:** S (~2d) · **Status:** Backlog · **Depends on:** EPIC-05
- **FEATURES.md ref:** § v2 / Streaks
- "You two crushed 14 chores this week" — calm, never shame-y.

### EPIC-16 — Quick-add via Share Sheet
- **Priority:** P2 · **Size:** S (~2d) · **Status:** Backlog · **Depends on:** EPIC-06
- **FEATURES.md ref:** § v2 / Quick-add share sheet
- PWA share-target API; "Share to Couples App" from any iOS/Android share sheet.

### EPIC-17 — Dark Mode
- **Priority:** P2 · **Size:** S (~1d) · **Status:** Backlog · **Depends on:** EPIC-01
- **FEATURES.md ref:** § v2 / Dark mode
- System default; manual toggle in settings; tailwind v4 dark variants honored across shadcn components.

---

## P3 — Maybe / dreaming

Listed so we don't lose the idea. **No commitment, no estimates, no breakdown** until promoted to P2 or sooner. Source: `FEATURES.md` § v3+ / Maybe.

| ID | Title | Notes |
|---|---|---|
| EPIC-18 | Shared Notes | Small things to remember |
| EPIC-19 | Photo Attachments | The broken thing, the grocery item |
| EPIC-20 | Meal Planning + Auto Grocery | Big — likely needs its own ADR |
| EPIC-21 | Shared Budget / Expenses | Even bigger — likely a separate app one day |
| EPIC-22 | Date Ideas / Wishlist Board | Cute, fun |
| EPIC-23 | Calendar Sync (Google / Apple) | OAuth + ICS feed |
| EPIC-24 | Important Dates Reminders | Anniversary, birthdays |
| EPIC-25 | Multi-language (DE / EN) | i18n from the ground up if pulled forward |

---

## Out of scope (per FEATURES.md)

These are explicitly not on the backlog. If a request comes in that implies one of these, raise it for discussion before adding.

- Group households / 3+ people
- Native iOS / Android apps (we are a PWA — see ADR-001)
- Smartwatch apps
- Public sharing of any kind
- Social features beyond the couple
- AI / LLM features that would send couple data to third parties

---

## Recently shipped

_Nothing yet — MVP not started. Move epics here with `✅ shipped <date>` when their DoD is green._

---

## Notes & open questions

- **Estimates assume Stef + Claude Code working at part-time, calendar-day pace.** They will be off; recalibrate after EPIC-01.
- **EPIC-06 (PWA shell) ordering:** technically only needs EPIC-01, but landing it after EPIC-05 means the "installable app" actually contains the core feature. Keeping it as P0 #6 in this order on purpose.
- **EPIC-07 (security hardening):** parts of this — RLS, secure cookies — must already be true by the time each preceding epic lands. EPIC-07 is the final audit + the bits that benefit from the whole system being in place (rate limiting, account deletion, dependency bot).
- **No P3 work without first promoting** the epic to P2 with full scoping. Avoids feature creep.
