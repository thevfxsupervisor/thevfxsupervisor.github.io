---
type: project
slug: signalbox
title: signalbox: the tracker drives the work | the vfx supervisor
description: Your production tracker already knows what needs making. signalbox wires that state straight to the work and records what happened. Open source, MIT.
eyebrow: Case study
h1: The tracker already knew what needed making. We were still retyping it by hand.
lede: signalbox is a working proof that a production tracker can drive the expensive automated steps directly, with a person on every gate and a record of who passed which one. Generative video is what happened to be running through it. The pattern is not specific to AI.
cred: Built and run solo on one GPU against a live tracker, on an in-development animated short.
get_label: See the code
get_href: https://github.com/thevfxsupervisor/signalbox
code_repo: https://github.com/thevfxsupervisor/signalbox
license: https://opensource.org/licenses/MIT
programming_language: Python
stats_h2: What was actually measured
final_h2: Want your tracker to drive the work?
final_p: I build production pipelines that run off the tracker a team already uses, on real shows, with the gates and the audit trail that make them safe to trust. If that is useful to yours, let's talk. Or book the course for the method behind it.
final_primary_label: Work with me
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: signalbox
card_eyebrow: R&D snapshot · open source
card_summary: A proof that the production tracker can be the control surface for expensive automated work, AI or not: every trigger is tracker state, every gate is a person, every artifact records what was actually sent. Trimmed MVP, MIT.
---

## The problem

On an in-development animated short I was running, the tracker already held everything that mattered. Which shot was approved, which note had come back and from whom, which design a character was locked to, which version superseded which. And then a person read that off the screen and retyped it somewhere else: into a prompt, into a queue, into a folder name. The tracker described the work and had no wire to it, so the wire was a human, and that is where the mistakes live. This is not an AI problem. Any shop with an expensive automated step, a render submission, a transcode, a batch conform, a delivery package, has the same gap: the state that says what to make is already written down, and somebody re-enters it by hand.

The generative half made it sharper, because a model is a probabilistic step. Most pipelines built around one do one of two things, and neither survives contact with a real show: they skip review and ship whatever came out, or they bolt on a separate admin tool that nobody on the production ever opens. A production coordinator lives in the tracker. They are not going to open a second interface to press a button, and a system that needs them to is a system that gets driven by an engineer instead, which defeats the whole point.

## What it does

In plain terms: a production tracker is the shared database a crew already uses to say what needs making and who approved it. signalbox watches that database and does the work it implies. Somebody asks for a change in the tracker, the change gets made, and the result comes back to the same place for a person to approve. Nobody opens a second tool, and nobody retypes anything.

![The signalbox loop: a person sets state in the tracker, a watcher reads it and runs the automated step, the result is published with a record of what was sent, and a person approves it or asks again, which returns to the tracker.](/static/signalbox-loop.svg)

In production terms, ShotGrid in this build: a watcher loop reads tracker state about once a minute and acts on it. An operator's Note on a shot, plus a Version moved to revision requested, sends that note and the current prompt components to a model, applies the revised prompt, requeues the shot and recomposes the panel. An approved panel queues its own video. An approved video rebuilds the episode cut from latest-approved.

Every automatic step is automatic. Every gate is a person, and the record of who passed which gate is what a production is actually buying. [The code is public on GitHub, MIT.](https://github.com/thevfxsupervisor/signalbox)

There is no job queue, no scheduler, and no in-memory state that matters, which is the design call the rest of it hangs off. The service can be killed mid-render and restarted with no reconciliation step, because what it was doing is still written down in the tracker. "Why did this render?" is answered by reading the state that caused it, and who set that state, in the tracker's own event log. No separate audit trail can drift from the thing it audits when there is no separate audit trail.

Characters stay on-model the same way a VFX pipeline keeps anything consistent, by compositing from an approved reference rather than from a prompt that hopefully describes the same person twice: an approved character design, an approved set, and a sentence of action go into an edit model together and one frame comes out.

## What it cost, stated plainly

A tracker-driven design has a specific failure mode and I hit it. A state nobody can see is a state nobody can act on. One stage was driven by a custom field with an informal vocabulary, and "this shot has an approved picture and has never been asked for a video" became a state that existed, mattered, and was invisible. A whole batch of shots sat in it, and it was found only because a human opened one of them and asked why. A queue would have shown that as an empty queue. Here it showed as nothing at all. The lesson was not to add more fields, it was that state which drives work belongs in the vocabulary the tracker actually displays.

Polling has a floor, too. A cycle of about a minute means nothing is instant, and a change made while a subprocess is running is not noticed until it finishes. In exchange, there is nothing to keep in sync.

The other expensive lesson was about trusting a model to check a model. I built a QC gate that asked a vision-capable model whether a rendered panel matched the approved design, and it passed 38% of panels a human had already approved as correct. The failure had a shape rather than being noise: an attribute checklist conflates identity with pose, and a legitimate close-up crops out an attribute the checklist expects to see. I switched it off rather than tuning around a number that was never going to move for the right reasons, and replaced it with checks a computer can actually settle: a perceptual hash against the approved reference, which scored 7 of 7 on the same set the vision gate scored badly on, a deterministic figure count, and a direct comparison of what was recorded against what was sent.

That last one earned its place. A record assembled beside the code that acts will diverge from it: one function built the prompt text for the record, another built the text for the model, they agreed when written, and then one of them changed, and three clauses of disagreement shipped for weeks. Now the function that sends is the function that reports, the second assembler was deleted so it cannot come back, and a gate compares the record against what was actually sent. "The record says we sent it" is not evidence that it was sent.

## What a human still decides

The code in this repo is mostly agent-written, under direction, and I would rather say that plainly than let anyone infer otherwise. What is not agent-written is the judgment, and that is the part worth reading for.

Which steps had to be made deterministic instead of left to a model's opinion. Where a person had to be the one to say yes, and where a system that regenerated without asking would have been worth less, not more. What evidence a check has to produce before a clean result from it gets believed: every self-test here is a canary that must be broken on purpose and watched go red before it is trusted, because three canaries written on this project were green from day one and guarding nothing, one built its fixture from the same constant it was testing, one shared an object between fixture and assertion, one compared two literals. Which direction is the safe direction to fail in, which is not the same answer every time: a protection check that cannot complete treats nothing as locked, while a lookup deciding whether work is needed treats its own failure as "work exists", because reading it the other way would have kicked off a batch of renders that were never needed.

And which AI component to switch off the moment it measured badly. That is the one most people skip.

There is a related trap I hit five separate times: a tool that exists, passes its own self-test every day, and is reachable from nothing, because the only thing that ever runs it is a human typing its name. It is not part of the pipeline, and a document describing the pipeline as automatic is then wrong. The fix was to make the service's self-test assert that its own cycle source contains the call, which is honest about what it checks.

## What this actually is, and what it is not

This is a bare-bones MVP and a visible artifact of R&D. It is an extract from a larger internal system, trimmed to the show-agnostic core, the watcher loop, the deploy seam, the provenance gate and the deterministic checks, with the character-consistency experiments and all production-specific data left out. It is published as a snapshot, because the history it came from stays on private infrastructure. Self-tests that need the original GPU models, ffmpeg or a live tracker connection will not pass from a clone.

So: **do not adopt this as a tool.** It is not maintained, it was never packaged for anyone else's show, and it will not stand up on your machine without work I am not doing for you. It is published because the decisions in it are the useful part, and because a case study nobody can check is a brochure. Read it, take the pattern, argue with the trade-offs. Everything above is in the repo's own `ARCHITECTURE.md` and `METHOD.md` in more detail, including the parts that did not work.

It is also honest about its limits in the repo rather than only here. Nothing in it detects a version made by a superseded recipe, because invalidation is a timestamp comparison. Two different characters in one frame is an open research problem in the field, not a bug I have a fix for, and it is worst for same-class subjects, which is every two-hander. A video whose workflow template was not recorded cannot be reproduced, which is the highest-value gap left, because the most valuable output a pipeline produces is the one that was nearly right. And there is no automated quality judgement at all: whether a frame is any good is a person's call, and the system is built to put that call in front of them quickly rather than to make it for them.

If you are wiring a tracker to real work and want to compare notes, email me at [geoff@thevfxsupervisor.com](mailto:geoff@thevfxsupervisor.com).

<!-- stats -->
### 38%::Where the vision-model QC gate landed
Asked to grade a rendered panel against the approved design, it passed 38% of panels a human had already approved as correct. So it was switched off rather than tuned around.

### 7 of 7::What replaced it, on the same set
A perceptual hash against the approved reference, scored on the images the vision gate had graded badly. A computation instead of an opinion, wherever a computation can answer.

### 4 of 4::Replicate pairs, byte-identical
Identical inputs produced byte-identical output across separate runs 40 minutes apart, so differences between test arms are signal and not run-to-run noise.

### 1 GPU::Built and run on one machine
A single 12 GB consumer card against a hosted tracker, producing an in-development animated short. Trimmed snapshot, MIT, not a maintained tool.
<!-- /stats -->
