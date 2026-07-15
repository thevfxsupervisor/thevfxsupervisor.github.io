---
type: project
slug: breakdown-studio
title: Breakdown Studio launch | the vfx supervisor
description: Breakdown Studio is now open source. A shot-breakdown pipeline that turns weeks of hand-logging a film cut into an afternoon, built solo and validated on a real production.
eyebrow: Project launch
h1: Breakdown Studio is live and open source
lede: I built Breakdown Studio because I was hand-matching hundreds of shots across every re-cut of a feature, alone, and losing real work to the noise. It is now free, MIT licensed, and running on real productions.
live_url: https://thevfxsupervisor.github.io/breakdown-studio/
repo_url: https://github.com/thevfxsupervisor/breakdown-studio
release_url: https://github.com/thevfxsupervisor/breakdown-studio/releases/tag/v1.0.0
cred: Designed, hardened and shipped end to end by one person, on a live feature film.
stats_h2: The numbers
final_h2: Star it, and follow along
final_p: Breakdown Studio is open source and on GitHub now. Star the repo to follow development, or join the course waitlist to learn the method behind it.
soon: Open source · MIT · on GitHub
---

## What it does

A film production hands you the edit and needs a number. Breakdown Studio builds the shot breakdown that every bid, schedule and vendor package hangs off, straight from the cut:

- Detects every shot in the edit, offline
- Reads the burned-in slates and VFX notes
- Builds a live, thumbnailed breakdown you can bid and share immediately
- Re-matches every new cut back to your master, one to one, so a re-cut is a short review instead of a full re-log

## Why it exists

The job that produced it was running the VFX department of an independent feature alone: supervising, budgeting, and keeping the breakdown current through cut after cut. The evolving film cut used to mean weeks of hand-logging that got half-thrown-away on every re-cut. Breakdown Studio turns that into one pass that updates itself.

It also ships with a context pack that briefs an AI assistant on the pipeline's rules and guardrails, so the mechanical half runs on its own and the judgment calls, what counts as a real drop versus a protected shot, which master row a drifted code belongs to, stay with the supervisor.

## Try it

The pipeline is validated against a real feature in active production: multiple successive cuts, thousands of operator-verified slate reads, and a producer-approved master match as ground truth. It runs on your own machine, on your own Google account, offline.

<!-- stats -->
### turnaround::Weeks to an afternoon
A full-film breakdown that used to take weeks of hand-logging, and got half-thrown-away on every re-cut, now runs in one pass and updates itself.

### 498::Unit tests, all green
Frame math, slate grammar, boundary repair, and the matching algorithm's uniqueness invariants, all covered.

### 1 production::Validated, not simulated
Every module regression-tested against the operator-verified breakdown of a feature film in active production.

### MIT::Open source, live now
Running today, with a roadmap folding the cross-cut intelligence proven on that production into the public tool.
<!-- /stats -->
