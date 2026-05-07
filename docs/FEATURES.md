# Couples App — Feature Plan

> Source of truth for **what we are building**. Always read this before implementing or proposing a feature.
> Last updated: 2026-05-07

---

## Vision

A simple, warm, secure app for couples and married partners to coordinate the small stuff of daily life — what's on each other's plate today, what needs doing around the house this week, who's grabbing groceries.

**Tagline (working):** "Two people, one plan."

The app should feel like a sticky note on the fridge — quick, calm, no friction — not like a corporate productivity tool.

---

## Core Principles

1. **Shared by default, private when wanted** — most things are visible to both partners; some lists can be personal.
2. **Mobile-first** — built as a PWA, used primarily on phones.
3. **Real-time** — when one partner adds or completes a todo, the other sees it within a second.
4. **Cute, calm, warm** — soft visual language, friendly copy, no aggressive notifications.
5. **Privacy by design** — couples' data is isolated at the database level. No cross-couple data leaks ever.
6. **Low friction, low setup** — pairing should take under 60 seconds.

---

## MVP — v1.0 (ship this first)

The smallest thing that delivers the core value: two paired partners can share a todo list.

### Auth & Account
- Email + password signup
- Email + password login
- Logout
- Password reset (email link)
- Basic profile: display name, optional avatar

### Couple Pairing
- Generate an invite code or invite link
- Partner enters the code / opens the link to pair
- One couple per user (cannot be in two couples at once)
- Disconnect / leave couple (with confirmation)

### Shared Todo List
- Create todo (title, optional notes, optional due date)
- Edit todo
- Delete todo
- Mark done / undone
- Assign todo to: me / partner / either
- Real-time sync — partner sees changes within ~1 second
- Sort by: created, due date, status

### Security & Privacy (MVP baseline)
- HTTPS only
- Secure session management (httpOnly cookies)
- Strong password requirements (min 12 chars, complexity not over-strict)
- Rate limiting on auth endpoints
- Row-level security in the database — a user can only see their own couple's data
- No third-party trackers
- Account deletion deletes all data

---

## v1.1 — Soon after MVP

### Personal vs Shared Lists
- Each partner has a personal list in addition to the shared list
- Toggle "share my today with partner" so personal todos can be visible without being shared

### Recurring Household Tasks
- Mark a todo as recurring (weekly, every X days)
- Auto-recreate the todo on its schedule when completed
- Examples: shopping, cleaning, taking out trash, watering plants

### Activity Stream (light)
- Tiny "what your partner just did today" view (added groceries, completed cleaning, etc.)

---

## v2 — Once MVP is loved

- Push notifications (web push for PWA, with quiet hours)
- Categories / tags (groceries, cleaning, errands, kids, ...)
- Shopping list mode (quick-add, swipe-to-complete)
- Today / Week view
- Streaks and gentle stats ("you two crushed 14 chores this week")
- Quick-add via shared system share sheet
- Dark mode (probably default to system)

---

## v3+ — Maybe / dreaming

- Shared notes (small things to remember)
- Photo attachments on todos (the broken thing, the grocery item)
- Meal planning + auto-generated grocery list
- Shared budget / expense tracking
- Date ideas / wishlist board
- Calendar sync (Google / Apple)
- Anniversary, birthdays, important dates reminders
- Multi-language (DE / EN at least)

---

## Explicitly Out of Scope (for now)

- Group households or roommate scenarios with 3+ people
- Native iOS / Android apps (we're a PWA — see [`./adr/0001-pwa-app-type.md`](./adr/0001-pwa-app-type.md))
- Smartwatch apps
- Public sharing of any kind
- Social features beyond the couple
- AI features that require sending couple data to third-party LLMs

---

## Status legend

When a feature ships, update its line with `✅ shipped <date>`. When it's actively in progress: `🛠️ in progress`. Otherwise it's planned.

Example:
```
- ✅ shipped 2026-06-01 — Create todo
- 🛠️ in progress — Recurring tasks
- Tags / categories
```
