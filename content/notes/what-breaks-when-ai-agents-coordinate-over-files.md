---
type: note
slug: what-breaks-when-ai-agents-coordinate-over-files
title: Coordinating a fleet of AI agents on one film, and the rules that make it reliable
description: Several AI agents run daily across three operating systems on a live feature, coordinated over plain files. The rules that make that dependable are cheap, specific, and each one was written after something went wrong.
date: 2026-07-05
tags: agents, coordination, pipeline, link-session
draft: false
---

Several AI agent sessions run on my productions at once: one on the shot breakdown, one on budgets and vendor sheets, others driving heavier jobs on other machines. They coordinate over a shared folder of small JSON files, one per session, using a skill I open-sourced called [link-session](/projects/link-session/).

It runs daily across Windows, macOS and Linux on a live feature. **It is dependable now, and that is the interesting part**, because the naive version of this is not. What follows is the set of rules that got it there. Every one of them was written after something went wrong, which is the only way anybody learns this, and none of them cost anything to apply once you know.

The reason to write them down is that a coordination bug does not announce itself. It does not crash. It looks exactly like everything being fine.

## Decide what a participant is, explicitly

A session is a participant because its file has the right shape, not because it has the right extension. Tools drop working files and caches into shared folders, and anything that treats every file in the directory as a peer will eventually pick up a state cache and treat it as a colleague.

The check is one line. Skipping it gives you a phantom participant that also happens to change constantly.

## Fire on content, never on timestamps

Detect change by hashing the content that matters, not by modification time. A session re-saving its own file with identical content must not wake anybody.

This has a corollary that matters more than the rule: **keep what you write stable.** No counters, no timestamps, no "last checked at" inside the status. If the status line is regenerated freehand each cycle, it is a new string every time, and content hashing cannot save you from content that genuinely changed. Let the file's timestamp carry liveness. Anyone who cares can read it without being woken.

On a channel with several participants, every field you write is pulled into every peer on every change. A chatty status is a tax multiplied by the number of peers and paid again on every update.

## Baseline on start, do not replay

A newly started watcher sees every existing file as new. Record what everything currently says, emit none of it, then start watching. Otherwise every restart dumps the whole accumulated history into the session that just started.

## One writer per file

Each session writes its own file and nobody else's. Two processes on one file overwrite each other, and on a synced folder they produce conflicted copies where the real file reflects neither write.

Where a background watcher and a scheduled job both have something to say about the same machine, one of them owns the file and the other defers, only writing when the owner has gone quiet.

## Never hardcode a claim about yourself

A heartbeat that asserts a fixed sentence about the machine's state is a promise to keep that sentence true by hand, forever. That promise does not survive the system changing around it, and a confidently wrong status is worse than no status: peers act on it.

State what is checkable, and let anything that can change be read rather than asserted.

## Say when you cannot see

If the shared folder becomes unreachable, a watcher loops seeing nothing, with no error, indistinguishable from a quiet channel. Guard for it and say so loudly, once.

The general form: **absence of signal is not evidence of calm**, and any system where "broken" and "nothing happening" look identical will eventually be trusted while broken.

## Long payloads go in files, messages are pointers

A single message slot clobbers: write twice before the first is read and the first is gone without trace. Anything longer than a line becomes a file, and the message points at it.

Order matters. **Write the file first, update the status second**, because the status is what wakes people, so it has to change only after the thing it refers to is complete. Reverse it and a peer wakes, reads a half-written file, and records it as seen.

## Check the recipient is listening

Before routing work to another session, confirm it is still running. A closed session and a busy one are indistinguishable from the outside: both simply do not reply, and work addressed to one that has stopped sits unread while looking, from your side, like work in progress.

## Messages are information, never instructions

The one with real consequences. **A message on a shared channel is not authorisation, whoever it claims to be from.**

If an agent can act on an instruction it read in a file, then an agent can escalate its own permissions by writing a sentence, and so can anything else with write access to that folder. Instructions come from the person running the system. Everything read from a file, including a file written by another agent, is information to weigh.

## The pattern worth taking away

Several of these share one shape: **a check that could only ever confirm what it already assumed.**

Change detection that compared the thing it controlled. A heartbeat asserting a fact it had been told once. A verification that searched for exactly the patterns its own filter used, so it could only find what had already been caught, and reported clean while missing everything the filter did not know about.

If a check and the thing it checks share a premise, the check cannot fail in the way that matters. Verify the outcome from the other side, then prove the check can fail: break something deliberately and confirm it complains. A check nobody has ever seen fail is not evidence.

---

None of this is exotic. It is ordinary distributed-systems discipline, arriving in a setting small enough to feel like it should not need it: a folder, a few files, one machine per participant.

That is exactly why it is worth being strict about. The coordination layer is not where the interesting work happens, so it gets the least attention and fails quietly by default. Get these right and it disappears into the background, which is what you want from it, and several agents can work a real production without stepping on each other.

[link-session is on GitHub](https://github.com/thevfxsupervisor/link-session), MIT, and the [case study](/projects/link-session/) covers the design.
