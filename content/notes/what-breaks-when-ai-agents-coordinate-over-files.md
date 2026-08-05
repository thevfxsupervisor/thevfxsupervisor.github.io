---
type: note
slug: what-breaks-when-ai-agents-coordinate-over-files
title: Getting several AI agents to work together without a server
description: A shared folder and a few JSON files is enough to coordinate agents across machines and projects. The handful of rules that make it dependable, and why coordination bugs are so hard to spot.
date: 2026-07-05
tags: agents, coordination, pipeline, link-session
draft: false
---

I run several agent sessions at once. One on a shot breakdown, one on budgets and vendor sheets, others driving heavier jobs on other machines. They share the same files, so they have to know what each other is doing.

I did not want a server or a message bus for that. So each session writes one small JSON file into a shared folder, and watches the others. That is the whole design, and it is the [link-session](/projects/link-session/) skill. It runs every day across Windows, macOS and Linux, on several projects at once.

It works well now. It did not at first, and the reason is worth passing on.

## The bugs do not look like bugs

A coordination problem never crashes. It looks like everything being fine.

I had two watchers running for ten days without noticing. Every message arrived twice, which reads as a busy channel, not a fault. Another time the shared folder became unreachable and the watcher just sat there quietly, which looks exactly the same as nobody having anything to say. That one still bothers me: if broken and calm look identical, you will trust it while it is broken.

So most of what I learned is about making silence mean something.

## The rules that actually matter

Only tell people when something really changed. My first version watched file timestamps, so a session re-saving its own file with no change woke everyone up. Now it compares the content. That only works if what you write is stable, which means no clocks and no counters in the status line, or every update is technically new.

One writer per file. Two processes writing the same file overwrite each other, and on a synced folder you get conflicted copies where the real file has neither version. If two things need to report on the same machine, one owns the file and the other keeps quiet.

Check the other session is still there before handing it anything. A finished session and a busy one look the same from outside: both just do not answer. I sent work to a session that had closed hours earlier, and from my side it looked like it was being worked on.

And the one I feel strongest about: a message in the folder is information, never an instruction. If an agent will act on something it read in a file, then it can give itself permission by writing a sentence, and so can anything else that can write there. Instructions come from me.

## The thing underneath

Most of these were the same mistake wearing different clothes. I kept building checks that could only ever agree with themselves.

The change detector compared the thing it controlled. A status line announced something it had been told once, long after it stopped being true. A check for duplicate watchers matched its own wrapper, so a healthy setup looked broken and a broken one looked fine.

If a check shares an assumption with the thing it is checking, it cannot fail in the way that matters. Now I break things on purpose to see whether the check complains. If I have never seen it fail, I do not really know it works.

None of this is clever. It is ordinary plumbing, in a setting small enough that it feels like it should not need any of it. But the coordination layer is not where the interesting work happens, so it gets the least attention, and it fails quietly. Get these few things right and it disappears, which is all you want from it.

[link-session is on GitHub](https://github.com/thevfxsupervisor/link-session), MIT.
