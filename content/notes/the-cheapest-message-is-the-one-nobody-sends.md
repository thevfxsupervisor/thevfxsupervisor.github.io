---
type: note
slug: the-cheapest-message-is-the-one-nobody-sends
title: The cheapest message is the one nobody sends
description: A fleet of AI agents coordinating on the same work gets noisy fast, and the noise is billed. Notes on signal to noise across a multi-agent channel, why the fix is a systems change rather than better instructions, and the two lessons that cost the most.
date: 2026-08-19
tags: agents, coordination, pipeline, link-session
draft: false
---

A fleet of AI agents working the same production gets noisy fast, and the noise is not free.

They coordinate through a shared channel: each agent writes a small file saying what it is doing, and watches the others. That part works. What is easy to miss is the arithmetic underneath it. **Every message an agent writes is pulled into every other agent's context, and paid for again each time it changes.** A long status on a six-agent channel is not one long status. It is that length multiplied by everyone reading it, and again on the next update. Context is a shared, billed, finite resource, and a chatty agent spends everybody's.

In one day the group burned about a fifth of its daily capacity almost entirely on talking to itself. Status updates, corrections, corrections to corrections, reasoning out loud. Not one deliverable moved.

That is a signal to noise problem, and it does not respond to the fix you would reach for with people. You cannot ask a fleet to be more considerate and expect it to hold. What changes the outcome is changing the system: what gets delivered to whom, and what an agent is able to send at all.

The first half is delivery. The watcher each agent runs had been waking on every change, so we made it pickier. **A status became something you pull, not something that pushes.** Statuses change constantly and almost none of those changes are news, so a status update now wakes nobody and you read it when you actually want it. Only a message addressed to you, a broadcast, or a loud marker like a correction interrupts anyone. Change is detected by hashing the meaningful fields rather than by timestamp, so re-saving an identical file wakes no one. And a restarting watcher takes a silent baseline instead of replaying the whole channel history into a session that has just begun.

The second half is emission, and it mattered more.

None of the delivery work stops an agent from choosing to post. What finally named the problem was a single message: an agent narrating fifteen paragraphs of its own progress, every file it had touched, a correction to something it had already corrected, none of which any other agent needed. The rule that closed it is one line. **Write when shared state changes, not to narrate progress.** A step taken, a file read, a decision reached alone: none of that is news to a peer. The file's own modified time already proves the agent is alive.

Two things I did not expect.

The size limits were already written down, and the agent that wrote them broke them five times in one session. Not from malice, just under load, which is when a convention always goes. So we stopped relying on the rule being remembered and moved it to the point of writing, where an over-long message is simply refused. A guardrail beats an instruction.

And a fix landing on disk is not the same as a fix landing in the running process. We shipped an improvement to the watcher and found days later that it had reached none of the running agents. Each had pulled the new file; none had reloaded it. Obvious afterwards, invisible at the time, and exactly the class of thing that looks like it is working.

The plumbing was never really the problem. You can build a perfectly efficient channel and then fill it with a diary. The cheapest message is the one nobody sends, and that is a property of the system, not a matter of asking nicely.

The tool is open source, and there is a longer write-up of how the agents coordinate in [the link-session case study](/projects/link-session/).
