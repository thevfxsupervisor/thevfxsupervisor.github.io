---
type: note
slug: how-a-one-person-vfx-department-orchestrates-ai
title: How a one-person VFX department orchestrates AI
description: The mechanical half automates. The judgment half stays with the supervisor. Notes on briefing an AI assistant with guardrails on a live production.
date: 2026-07-13
tags: pipeline, ai, production
draft: false
---

When there is no department behind you, just one person and a schedule, the question is not whether to use an AI assistant. It is where to let it run unattended, and where to keep your hand on the wheel.

## The mechanical half and the judgment half

A film's shot breakdown splits cleanly into two kinds of work. The mechanical half: detecting where the cuts are, reading a burned-in slate, uploading a thumbnail, formatting a row in a spreadsheet. None of that needs a human in the loop once the rules are right, and all of it is exactly what an AI assistant, or a small offline model, does well and tirelessly.

The judgment half is different. Whether a shot that vanished between cuts is a real drop or a protected shot that never had a slate. Whether two shots that look similar are the same setup re-labelled or two different takes. Which row in a master breakdown a drifted shot code actually belongs to. That is the supervisor's eye, built from doing the job, and it does not delegate cleanly.

The practical answer, running Breakdown Studio's own pipeline as the example: automate the first half completely, and build the second half as a set of narrow, well-briefed tasks with explicit guardrails, not a single open-ended "figure it out" instruction.

## Briefed assistants with guardrails

A briefed assistant is not a chatbot you paste a spreadsheet into. It is an assistant that opens every session already knowing the rules of the pipeline: what identity means in this system (a slate, never a timecode), what counts as a protected shot, what is allowed to touch the master file and what is not. The brief travels with the project, so the fifth session behaves like the first.

The guardrails matter more than the intelligence. A rule as simple as "nothing writes to the master without a human sign-off" turns a fast, occasionally wrong assistant into a safe one. A rule like "protected shots never auto-omit" catches the one mistake that would have quietly cost real shots off a budget. The assistant's job is to stage the change and show its work; the sign-off stays with the person whose name is on the delivery.

## Memory that learns the show

The other piece that makes this work over a whole production is memory that survives between sessions and between re-cuts. A decision made once, this shot is intentionally slate-less, this pair of shots always merges, should not have to be re-argued every time the picture changes. Recording that decision against something stable, a slate identity rather than a timecode that moves with every cut, means each new cut only surfaces what actually changed, not the whole film again.

That is the shape of the method: automate hard, brief narrowly, gate the writes, and give the system a memory that respects how a film cut actually evolves. None of it requires naming the production it was built on. The pattern is the point.
