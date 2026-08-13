---
type: note
slug: keeping-a-long-running-ai-agent-in-sync
title: Keeping a long-running AI agent in sync with its own rules
description: An AI agent that runs for days is working from the rulebook it read on the first morning. When that rulebook keeps improving, how do you update the agent without restarting it or drowning it? Notify always, load on demand, and never call a change handled until it has actually been read.
date: 2026-07-04
tags: agents, coordination, pipeline
draft: false
---

I run AI agent sessions that stay open for days. The instructions they follow, the shared rulebook
for how they work on a production, keep improving while they are running. Which creates a quiet
problem: a session that read the rules on the first morning is now working from a week-old copy, and
worse, it does not know that it is.

The two obvious fixes both fail. **Restart the session** to reload the rules and you throw away
everything it was in the middle of. **Reload everything on a timer** and you drown it, most of the
rulebook is irrelevant to whatever it is doing this minute, and re-reading all of it every half hour
burns the working memory you actually need for the job.

So I split it into three layers, each doing only the thing it is good at.

**Pull the rulebook to disk on a schedule.** Cheap, and it needs no session at all, so the files on
disk are never more than half an hour behind, no matter how long the agent has been running.

**Notify the running session on every step.** A tiny flag: your rulebook moved, here is what changed.
Notifying costs almost nothing because it is a pointer, not the thing it points at. It can fire on
every single message without anyone noticing the cost.

**Load the changed rules into the session only on demand.** Loading is the expensive part, so it
happens when the agent actually needs to trust the rules before doing something that matters, not on
a clock. Cheap things run always; the expensive thing runs when it earns it.

There is one rule underneath that matters more than it sounds. **Never mark a change as handled until
it has actually been read.** Being told is not the same as having understood. If the agent clears the
flag the moment the update is delivered, it will run confidently on rules it never loaded, which is
worse than not being told at all. So delivery and comprehension are kept separate on purpose: the
flag only clears after the reading, never on receipt.

None of this is glamorous. It is the plumbing that lets a team of agents run for weeks against a
rulebook that keeps getting better, without restarting them and without burying them. It is the same
instinct as the rest of how I run AI on a film: cheap things run always, expensive things run when
they earn it, and nothing is trusted just because it arrived.

This is one piece of the [coordination layer](/notes/running-ai-agents-as-a-coordinated-team/) I run
every day. If you want AI run as a coordinated team on your show, with the guardrails that keep it
safe, [let's talk](/about/), or [book the course](/course/) for the method.
