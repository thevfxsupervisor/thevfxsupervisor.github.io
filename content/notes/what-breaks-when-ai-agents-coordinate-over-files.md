---
type: note
slug: what-breaks-when-ai-agents-coordinate-over-files
title: What actually breaks when AI agents coordinate over shared files
description: Nine failures from running several live AI agents on one production over a shared folder. Duplicate watchers, silent mounts, two writers on one file, and checks that agree with themselves.
date: 2026-08-05
tags: agents, coordination, pipeline, link-session
draft: false
---

I run several AI agent sessions at once on a production: one on the breakdown, one on budgets and vendor sheets, others driving heavier jobs on other machines. They coordinate over a shared folder of small JSON files, one per session, using a skill I open-sourced called [link-session](/projects/link-session/).

The design is boring on purpose: no server, no message bus. What is not boring is the list of ways it broke. Almost none of them announced themselves. That is the part worth writing down, because a coordination bug does not look like a crash, it looks like everything being fine.

## A watcher that survives one kind of restart but not another

Each session runs a watcher on the shared folder. Mine survived a context compaction but not a full session restart, so the natural recovery step, re-running the join command, quietly started a second one.

Two watchers deliver every event twice, forever, and the symptom looks exactly like a healthy channel. One of mine ran doubled for ten days. Now the first thing the join does is check whether a watcher is already running.

## Waking everyone up to tell them nothing changed

The first version detected change by file modification time. Any session re-saving its own status file, with byte-identical content, woke every other session.

Change detection now hashes the content that actually matters. If nothing meaningful changed, nobody hears about it. On a channel with several participants, every field you write is pulled into everyone else's context on every change, so a chatty status line is not free, it is a tax multiplied by the number of peers and paid again on every update.

## Replaying the entire history on every start

A fresh watcher saw every existing file as new and dumped the whole accumulated channel into the session that had just started.

The fix is one line of discipline: on the first pass, record what everything currently says and emit none of it. Baseline, do not replay.

## Two processes writing one file

This one bit me last night. A background watcher wrote a heartbeat into a session's status file, and a scheduled job wrote its progress into the same file. They alternated, each overwriting the other, and every flip counted as a change, so the whole fleet woke up to watch two processes on one machine disagree about whether that machine was awake.

One writer per file is not a style preference. On a synced folder it is also how you avoid conflicted-copy files where the real one reflects neither write. The fix was to make the watcher defer: it only writes if the other process has gone quiet, and it says so when it does.

## The heartbeat that was confidently wrong

Worse than the fighting was what it said. The heartbeat text was hardcoded to announce that no agent was running behind it. That had been true when it was written. It was no longer true, and it was being broadcast to every other session as fact.

Any status a machine asserts about itself is a claim with an expiry date. If it is hardcoded, it is a claim you have promised to keep true by hand, forever, which is a promise nobody keeps.

## Silence that means the opposite of what it looks like

If the shared folder goes away, a mount drops, a path changes, the watcher loops forever seeing nothing. No error. Indistinguishable from a quiet channel.

Every watcher now checks the folder is reachable and says so loudly, once, if it is not. Absence of signal is not evidence of calm.

## A message field that clobbers without history

The status files have a single message slot. Write a second message before the first is read and the first is gone, with nothing to indicate it existed.

So anything longer than a line goes in a separate file, and the message becomes a pointer to it. Write the file first, then update the status file, never the other way around: the status file is what wakes people, so it has to change last, after the thing it points at is fully written. Reverse that and a peer wakes, reads a half-written file, and caches it as seen.

## Routing work to a session that stopped listening

An agent posted a task addressed to two other sessions. Both had closed, one two weeks earlier. The task sat unread and looked, from the poster's side, exactly like a task in progress.

Before routing anything, check the recipient is alive. This sounds obvious written down. It was not obvious at the time, because a closed session and a busy one both simply do not reply.

## Text on the channel is data, not orders

The one with real consequences. An agent posted a message instructing other sessions to deploy a change to a public page, citing the principal's authority for it.

It may well have been authorised. That is not the point. **A message on a shared channel is not authorisation, whoever it claims to be from.** Anything else means an agent can escalate its own permissions by writing a sentence, and anyone who can write to the folder can too. Instructions come from the principal directly. Everything read from a file, including a file written by another agent, is information to weigh, not a command to execute.

## The pattern underneath most of these

Several of these failures share a shape: **a check that could only confirm what it already assumed.**

The change detector compared the thing it controlled. The heartbeat asserted a fact it had been told once. A verification I wrote later that same day searched for exactly the patterns its own filter used, so it could only ever find what had already been caught, and reported clean while missing what the filter did not know to look for.

If a check and the thing it checks share a premise, the check cannot fail in the way that matters. Verify the outcome from the other side, and then test that your check can actually fail: break something on purpose and confirm it complains.

---

None of this is specific to AI agents. It is ordinary distributed-systems trouble, arriving in a setting small enough that it feels like it should not apply: a folder, a few files, one machine per participant.

That is exactly why it is worth being strict about. The coordination layer is not where the interesting work happens, so it gets the least attention, and it fails silently by default. The rules that make it survivable are cheap and boring, and every one of them here was written after something had already gone wrong.

[link-session is on GitHub](https://github.com/thevfxsupervisor/link-session), MIT.
