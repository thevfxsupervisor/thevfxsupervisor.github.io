---
type: project
slug: breakdown-studio
title: Case study: Breakdown Studio, a shot-breakdown pipeline for solo VFX supervisors | the vfx supervisor
description: How I built Breakdown Studio, a shot-breakdown pipeline that turns weeks of hand-logging a film cut into an afternoon, solo, on a feature in active production, then open-sourced it.
eyebrow: Case study
h1: I was hand-matching hundreds of shots across every re-cut of a feature. So I built the tool that does it.
lede: Breakdown Studio is the shot-breakdown pipeline I built to survive running a feature's VFX department alone. It is open source now, MIT, and it turns weeks of hand-logging a cut into an afternoon.
cred: Designed, hardened and shipped end to end by one person, on a live feature film.
get_label: Get the tool
get_href: https://thevfxsupervisor.com/breakdown-studio/
stats_h2: The numbers
final_h2: Want this on your show?
final_p: I run AI-assisted VFX pipelines on real productions. If that is useful to your film, let's talk. Or book the course for the method behind the tool.
final_primary_label: Work with me
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: Breakdown Studio
card_eyebrow: Flagship · open source
card_summary: A shot-breakdown pipeline that turns weeks of hand-logging a film cut into an afternoon. Built solo, validated on a feature in active production, MIT.
---

## The problem

A production hands you the edit and needs a number. The shot breakdown is what every bid, schedule and vendor package hangs off, and on an evolving cut it used to mean weeks of hand-logging that got half-thrown-away on every re-cut. I was doing that alone, cut after cut, and losing real work to the noise.

## What it does

Breakdown Studio builds that breakdown straight from the edit and keeps it current: it detects every shot offline, reads the burned-in slates and VFX notes, thumbnails it into a live sheet you can bid immediately, and re-matches each new cut back to your master one to one, so a re-cut is a short review instead of a full re-log. [Get the tool and the full feature list.](https://thevfxsupervisor.com/breakdown-studio/)

## Decisions and trade-offs

I built it offline-first, running on your own machine and your own Google account, on purpose: a breakdown holds unreleased footage and confidential notes, so nothing leaves the machine and there is no service to trust. The hard part was never detecting shots, it was identity, deciding which master row a drifted shot code belongs to across a re-cut, and keeping that match one to one so a rename never silently collides. It ships with a context pack that briefs an AI assistant on those rules, so the mechanical half runs on its own while the judgment calls, what counts as a real drop versus a protected shot, stay with the supervisor. The agent fleet that actually runs it is coordinated with [link-session](/projects/link-session/).

## Proof in production

The pipeline is regression-tested against a real feature in active production: multiple successive cuts, thousands of operator-verified slate reads, and a producer-approved master match as ground truth.

<!-- stats -->
### 1 afternoon::Down from weeks of hand-logging
A full-film breakdown, half-thrown-away on every re-cut, now runs in one pass and updates itself.

### 498::Unit tests, all green
Frame math, slate grammar, boundary repair, and the matching algorithm's uniqueness invariants, all covered.

### 1 production::Validated, not simulated
Every module regression-tested against the operator-verified breakdown of a feature film in active production.

### MIT::Open source, live now
Running today, with a roadmap folding the cross-cut intelligence proven on that production into the public tool.
<!-- /stats -->
