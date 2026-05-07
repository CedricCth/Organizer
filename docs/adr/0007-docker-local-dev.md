# ADR-007 — Docker for local development

**Date:** 2026-05-07
**Status:** Accepted

## Context

Lean MVP, single primary developer (Stef). The app deploys to Vercel (see [`./0004-vercel-hosting.md`](./0004-vercel-hosting.md)), so production does not use Docker — Vercel has its own build pipeline and ignores Dockerfiles in the repo. But local development still benefits from a containerized setup:

- **Reproducibility** — pinned Node, pnpm, and tool versions, so a new laptop or a future contributor gets identical setup with one command.
- **Eliminates "works on my machine"** — the same container behavior is guaranteed regardless of host OS.
- **Supabase local emulation** uses Docker under the hood anyway (via the Supabase CLI), so Docker Desktop is effectively a soft prerequisite for any local Postgres work.
- **Hedge against Vercel lock-in** — if we ever move off Vercel, a working local Dockerfile is most of a production Dockerfile.
- **Explicit learning value** — using Docker daily on a real project is the most durable way to internalize it.

The question: do we add Docker, and in what scope?

## Options considered

1. **No Docker (status quo)** — install Node + pnpm directly on the host. Simplest. But every laptop reinstall risks version drift, and Supabase local emulation needs Docker regardless.
2. **Docker for local development only (recommended)** — `Dockerfile.dev` + `docker-compose.yml` for the dev environment. Vercel handles production natively. Two paths, each simple.
3. **Docker for both local and production** — same image philosophy everywhere. But Vercel will not run a custom Dockerfile for Next.js deployments — they use their own build runtime. So a production Dockerfile would be wasted unless we also leave Vercel.
4. **Devcontainer (VS Code-specific)** — `.devcontainer/` config. Tighter editor integration but coupled to one IDE.

## Decision

**Option 2 — Docker for local development only.**

- A `docker-compose.yml` at the repo root spins up the Next.js dev server.
- The host project folder is **bind-mounted** into the container, so editing files in VS Code on the host triggers hot-reload inside the container as normal.
- `node_modules` lives in a named Docker volume (not bind-mounted) so the host doesn't need Node installed and there's no permission/perf weirdness on Windows.
- Production stays on Vercel (no change to ADR-004). No production Dockerfile.

## Why this is right

- Local reproducibility today, Vercel simplicity for production — no compromise required.
- The two paths don't conflict: Vercel ignores `Dockerfile*` and `docker-compose.yml`; Docker ignores Vercel.
- Future-proof: if we ever leave Vercel, this Dockerfile is the foundation of a production one.
- Supabase CLI already needs Docker, so Docker Desktop isn't extra weight.

## Trade-offs accepted

- Docker Desktop must be installed on any contributing machine (free for personal/small-team use as of 2026).
- Container startup adds roughly 10–20 seconds vs. running `pnpm dev` directly on the host. Minor.
- Two valid ways to run the dev server (in container or `pnpm dev` directly). We document the container path as canonical and the direct path as a fallback for quick experiments.
- Ports 3000 (Next.js) and any future ones must be free on the host.

## Revisit when

- We decide to move off Vercel — at that point we'd extend the Dockerfile to production-mode (multi-stage, `NODE_ENV=production`, no bind mount, etc.).
- Docker Desktop licensing changes in a way that makes it impractical for personal use.
- Vercel adds first-class Dockerfile support (which would unify the two paths).
