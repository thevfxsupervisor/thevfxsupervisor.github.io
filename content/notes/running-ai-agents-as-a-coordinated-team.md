---
type: note
slug: running-ai-agents-as-a-coordinated-team
title: Running several AI agents as one coordinated team
description: A shared folder and a few JSON files let a fleet of AI agents work the same production together: hand off work, stay out of each other's way, and keep going across machines and restarts. What that makes possible, and the discipline that keeps it dependable as the fleet grows.
date: 2026-07-05
tags: agents, coordination, pipeline, link-session
draft: false
---

I run several AI agent sessions at once, and I run them as one team. One works a shot breakdown, one works budgets and vendor sheets, others drive heavier jobs on other machines. They share the same production and the same files, and they move as a group: picking up each other's handoffs, staying out of each other's way, and carrying on when a machine or a session drops out.

The thing that lets them do that is deliberately small. Each session writes one little JSON file into a shared folder and watches the others. No server, no message bus, no orchestration framework to keep alive. That is the whole design, and it is the [link-session](/projects/link-session/) skill, open source and MIT. It runs every day across Windows, macOS and Linux, on several projects at once.

## What it lets a team of agents actually do

Coordinate with no infrastructure. There is nothing to stand up or keep running. A session joins by dropping its file in the folder, and the others see it on their next look. Add a seat and it announces itself.

Hand off work cleanly. A session posts what it has done and what it is passing on, and the next one picks it up. The whole exchange is plain text you can read by eye, so when something is off you can see why rather than guess.

Survive the real world. The coordination state is just files, so it outlasts a session dying, a restart, or a network mount that blinks out. Nothing to replay, nothing to reconcile: the folder is still the folder when everything comes back.

Stay safe by design. One writer per file. Coordination carries only metadata, never client or show content. And a message in the folder is information, never an instruction: permission comes from me, not from a sentence an agent read. Those lines are what make it safe to point at real production work.

## What keeps it dependable as the fleet grows

The interesting work does not happen in the coordination layer, so it gets the least attention and is the easiest place to fool yourself. Most of the recent work went into making it hold up when you genuinely lean on it, and into making silence mean something.

It speaks only when something truly changed. It compares content, not timestamps, so a busy channel means real news rather than a session re-saving itself. Idle seats stay quiet, so what does arrive is worth reading.

It counts its own watchers, so an event is never quietly delivered twice. It runs the same across all three operating systems, down to the older shells. It stays lean on purpose: the layer that is not where the value is should cost almost nothing in attention or context, and this one does.

And a dropped mount now says so, out loud, instead of sitting there looking calm. If broken and quiet look identical, you will trust it while it is broken, so they are not allowed to look the same.

## Why I write this down

Running AI on a real film production is not one assistant in a tab. It is a team of agents doing real work in parallel, with the guardrails that keep it safe, and the unglamorous half of that is the coordination. Get it right and it disappears, which is exactly what you want from it. This is the layer I run every day, and it is small enough to hand you: [link-session is on GitHub](https://github.com/thevfxsupervisor/link-session), MIT.

If you want AI run as a coordinated team on your show, with those guardrails, [let's talk](/about/), or [book the course](/course/) for the method.
