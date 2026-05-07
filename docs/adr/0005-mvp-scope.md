# ADR-005 — MVP scope: Auth + Shared Todos only

**Date:** 2026-05-07
**Status:** Accepted

## Context

The user explicitly asked for a lean MVP. The risk of feature-complete v1 is shipping nothing for months while polishing things that turn out not to matter.

## Options considered

1. **Lean MVP** — auth + couple pairing + shared todos. Ship in weeks.
2. **Feature-complete v1** — also includes recurring tasks, activity feed, notifications, categories. Ship in months.

## Decision

**Lean MVP.** Recurring tasks and activity feed move to v1.1, notifications and categories to v2. See [`../FEATURES.md`](../FEATURES.md) for the full milestone split.

## Trade-offs accepted

- v1.0 will feel basic — that's fine; the goal is to learn what we actually use.
- Recurring tasks are listed as a household must-have ("weekly cleaning, shopping"), so v1.1 needs to follow MVP quickly.

## Revisit when

- MVP is shipped and we know what we actually reach for daily.
