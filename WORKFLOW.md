# Workflow — How we work on this app together

> How Stef and Claude (across Cowork sessions, Claude Code sessions, etc.) collaborate on this project. Read this once; refer back when adding features or making decisions.

---

## Roles

- **Stef (you)** — product owner, primary user, sole final authority on what ships and what doesn't.
- **Claude in Cowork** — planning partner. Helps you think through features, architecture, scope, copy, design direction. Updates docs.
- **Claude Code** — implementation partner. Reads `CLAUDE.md` first every session, then executes work that Stef has scoped.

---

## Source-of-truth files (this repo)

| File | Purpose | Update when |
|---|---|---|
| `CLAUDE.md` | Orientation for any Claude session | Rarely. When the rules of working on this project change. |
| `FEATURES.md` | What we are building | Every time a feature is planned, scoped, or shipped. |
| `TECH_STACK.md` | What we are building it with | When we adopt or replace a tool / library. |
| `ARCHITECTURE.md` | How the code is structured (layers, diagrams, DI pattern) | When layer rules, the dependency direction, or the diagrams change. |
| `DECISIONS.md` | Why we chose what we chose | Every time a non-trivial technical decision is made. |
| `WORKFLOW.md` | This file. How we work. | When the process changes. |

---

## How to add a feature

1. **Talk it through with Claude (Cowork).** Sketch what it does, why it matters, who it's for.
2. **Add it to `FEATURES.md`** under the right milestone (MVP / v1.1 / v2 / Maybe / Out of scope). Be specific enough that someone reading it cold understands the scope.
3. **If it implies new tech**, write an ADR in `DECISIONS.md` *first*. Don't bolt on a new library silently.
4. **Hand to Claude Code** with a clear scope: "Implement <feature> from FEATURES.md per the stack in TECH_STACK.md."
5. **On ship**, update `FEATURES.md` to mark `✅ shipped <date>`.

---

## How to make a tech / architecture decision

1. **Open `DECISIONS.md`** and copy the ADR template.
2. **List at least two real alternatives** considered. "We picked X" is not a decision — "We picked X over Y because Z" is.
3. **Capture trade-offs** explicitly. What are we giving up?
4. **Set a Status** (Proposed → Accepted, or Superseded by ADR-NNN).
5. **Update `TECH_STACK.md`** if the decision changes the stack.

---

## How any Claude session should start

This is the contract. Every session — Cowork or Claude Code — begins by:

1. Reading `CLAUDE.md`.
2. Reading `FEATURES.md`, `TECH_STACK.md`, `ARCHITECTURE.md`, and `DECISIONS.md` (or skimming for what's relevant to the request).
3. Confirming the task scope with Stef before touching code.
4. Planning before coding.
5. Updating the docs as part of the change.

If a Claude session ever proposes a feature not in `FEATURES.md`, wants to use tech not in `TECH_STACK.md`, or wants to break the layer rules in `ARCHITECTURE.md`, it should *stop and ask Stef* rather than proceeding.

---

## Suggested rhythm

- **Planning sessions** (Cowork) — slow, doc-heavy. Output: changes to `FEATURES.md` / `DECISIONS.md`.
- **Build sessions** (Claude Code) — focused on one feature at a time. Output: code, tests, docs updated.
- **Review session** (either) — every couple of weeks: re-read `FEATURES.md`, check what's actually being used, retire what isn't.

---

## Naming conventions for sessions / branches

- Branch: `feature/<short-name>` or `fix/<short-name>` or `docs/<short-name>`.
- Commit subject: imperative, ≤ 72 chars. ("Add couple pairing via invite code")
- PR description: link to the `FEATURES.md` line being shipped.

---

## When in doubt

Default behavior for Claude in any session:
- Ask, don't assume.
- Smaller change, not bigger.
- Update the docs, not just the code.
- Cute, calm, secure — in that priority? No: secure first, then calm, then cute. Always all three.
