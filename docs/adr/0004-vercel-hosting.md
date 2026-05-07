# ADR-004 — Hosting: Vercel (frontend) + Supabase Cloud (backend)

**Date:** 2026-05-07
**Status:** Accepted

## Context

Want HTTPS, a custom domain, edge performance, and zero ops. Want it free or near-free for personal use.

## Options considered

1. **Vercel + Supabase Cloud** — zero-config, free tiers cover this app's usage, automatic HTTPS, preview deployments per branch.
2. **Self-hosted on a VPS (Hetzner / DigitalOcean)** — cheaper at scale, full control, but real ops work (TLS, deploys, backups, monitoring).
3. **Cloudflare Pages + Workers + D1** — very fast, but D1 is SQLite-flavored and lacks Supabase's auth/realtime out of the box.
4. **Netlify + Supabase Cloud** — similar to Vercel but Vercel has tighter Next.js integration.

## Decision

**Vercel for the Next.js app, Supabase Cloud for the backend.**

## Trade-offs accepted

- Mild vendor coupling to Vercel's Next.js deployment model.
- Free tier limits exist but won't bite for a 2-person personal app.

## Revisit when

- Free tier limits are hit consistently.
- We want everything on one provider for simplicity.
