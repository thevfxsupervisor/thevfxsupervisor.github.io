---
type: note
slug: the-cheapest-message-is-the-one-nobody-sends
title: The cheapest message is the one nobody sends
description: Every production hits a point where the status updates cost more than the work. Running several AI agents as a team, I hit it too, and the fix turned out to be half plumbing and half manners.
date: 2026-08-19
tags: agents, coordination, pipeline, link-session
draft: false
---

Every production I have worked on eventually hits the point where the coordination costs more than the work. The daily gets longer, the notes get restated, the update on the update arrives, and somewhere underneath it a small number of people are still trying to finish shots.

I hit the same wall running several AI agents as a team, and it was cheaper to measure there, so the shape of it was clearer.

The agents coordinate through a shared channel: each one writes a small file saying what it is doing, and watches the others. That works. What I had not accounted for is that **every message an agent writes gets pulled into every other agent's context, and paid for again each time it changes.** A long status on a six-agent channel is not one long status. It is that length multiplied by everyone reading it, and again on the next update. Attention is a shared budget and a chatty agent spends everybody's.

In one day the group burned about a fifth of its daily capacity almost entirely on talking to itself. Status updates, corrections, corrections to corrections, thinking out loud. Not one deliverable moved.

The first fix was plumbing, and it was the easy half. The watcher each agent runs got pickier. **A status is now something you pull, not something that pushes.** Statuses change constantly and almost none of those changes are news, so a status update wakes nobody, and you read it when you actually want it. Only a message addressed to you, a broadcast, or a loud marker like a correction interrupts anyone. Change is detected by content rather than by timestamp, so re-saving an identical file wakes no one. And a restarting watcher takes a silent baseline instead of replaying the entire history into a session that just started.

The second fix was manners, and that was the half that mattered.

None of the plumbing stops an agent from choosing to post. What finally named the problem was one message: an agent narrating fifteen paragraphs of its own progress, every file it had touched, a correction to something it had already corrected, none of which any other agent needed. The rule that closed it is one line. **Write when shared state changes, not to narrate your progress.** A step you took, a file you read, a decision you reached on your own: none of that is news to anyone else. The file's own timestamp already proves you are alive.

Two things I did not expect.

The size limits were already written down, and the agent that wrote them broke them five times in one session. Not out of malice, just under pressure, which is when conventions always go. So we stopped trusting good intentions and put the limit at the point of writing, where it simply refuses to send something too long. A guardrail beats a rule you have to remember.

And a fix landing on disk is not the same as a fix landing in the running process. We shipped an improvement to the watcher and found days later that it had reached none of the running agents. Each one had the new file and none of them had reloaded it. Obvious in hindsight, invisible at the time, and exactly the kind of thing that looks like it is working.

The plumbing was never really the problem. You can build a perfectly efficient channel and then fill it with a diary. The cheapest message is the one nobody sends, and that is a decision about behaviour, not a feature of the pipe.

The tool itself is open source, and there is a longer write-up of how the agents coordinate in [the link-session case study](/projects/link-session/).
