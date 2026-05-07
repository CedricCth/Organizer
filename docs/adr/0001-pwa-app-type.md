# ADR-001 — App type: Progressive Web App (PWA)

**Date:** 2026-05-07
**Status:** Accepted

## Context

Stef is on Android. Partner is on iOS. Stef does not have a Mac, which is required for iOS App Store publishing. The goal is the fastest possible path to a working app both partners can use, with no app-store gatekeepers and no recurring fees.

## Options considered

1. **PWA (Progressive Web App)** — built as a website, installable to home screen on iOS Safari and Android Chrome. Works on desktop too. No stores. Free.
2. **React Native + Expo** — single codebase, native iOS + Android. Excellent DX. But: iOS App Store still requires a Mac for final build/submit (or paid EAS Build at $99+/year), plus $99/year Apple Developer fee.
3. **Flutter** — same store-publishing problem as React Native, plus a new language to learn (Dart) and a smaller backend ecosystem.
4. **Fully native (Swift + Kotlin)** — best polish per platform, but two codebases. Massive overkill for an MVP.

## Decision

**PWA.** Built as a Next.js web app, with a manifest + service worker so it can be added to the home screen and behave like a native app.

## Trade-offs accepted

- iOS only allows PWA installation from Safari (not Chrome on iOS).
- iOS push notifications work but require installing the PWA first, and lag native apps on a few minor features.
- No native widgets or deep OS integrations.
- The "Add to Home Screen" step is one extra friction point compared to App Store install.

## Why this is right *for now*

Zero gatekeepers, zero fees, both partners can use it the day it ships. If we later want native presence, we can wrap the PWA in **Capacitor** without rewriting — most logic stays as-is.

## Revisit when

- We want App Store / Play Store presence for credibility or distribution.
- iOS PWA limitations start blocking a feature we genuinely need.
