---
type: project
slug: signalbox
title: signalbox: the tracker drives the work | the vfx supervisor
description: Your production tracker already knows what needs making. signalbox wires it straight to the work, so nobody retypes it. Open source, MIT.
eyebrow: Experiment
h1: The tracker already knows what needs making. So we stopped retyping it.
lede: signalbox is a small experiment in wiring a production tracker directly to the work it describes. Generative video happened to be what we ran through it, but the idea is not really about AI.
cred: Built and run on one workstation against a live Autodesk Flow site, on an in-development animated short.
get_label: See the code
get_href: https://github.com/thevfxsupervisor/signalbox
code_repo: https://github.com/thevfxsupervisor/signalbox
license: https://opensource.org/licenses/MIT
programming_language: Python
stats_eyebrow: The shape of it
stats_h2: A few numbers from it
final_h2: Doing something similar?
final_p: If you are wiring a tracker to real work and want to compare notes, I am always happy to. The course covers the same ground in more depth.
final_primary_label: Get in touch
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: signalbox
card_eyebrow: Experiment · open source
card_summary: Wiring a production tracker straight to the work it describes, so the tracker stays the only place anyone has to look. Open source, MIT.
---

## The problem

On a small animated short, our tracker already held everything that mattered: which shot was approved, which note came back and from whom, which version superseded which. And then a person read that off the screen and typed it somewhere else. The tracker described the work but had no wire to it, so the wire was a human, and that is where the mistakes live.

This is not an AI problem. Any shop with an expensive automated step, a render submission, a transcode, a delivery package, has the same gap.

## How it works

![The signalbox loop: a person sets state in the tracker, a watcher reads it and runs the automated step, the result is published with a record of what was sent, and a person approves it or asks again, which returns to the tracker.](/static/signalbox-loop.svg)

A production tracker is the shared database a crew already uses to say what needs making and who approved it. Ours is Autodesk Flow Production Tracking, which most people still call ShotGrid. signalbox watches it and does the work it implies.

Somebody asks for a change in the tracker. The change gets made. The result comes back to the same place for a person to approve. Nobody opens a second tool, and coordinators keep working where they already work, which is the part that made it stick.

### For the technically minded

A watcher loop polls tracker state about once a minute and acts on it. There is no queue and no scheduler, so the service can be killed mid-render and restarted with nothing to reconcile: what it was doing is still written down in the tracker. "Why did this render?" is answered by reading the state that caused it, in the tracker's own event log.

## What worked, and what didn't

The thing that surprised us: asking a vision model to check another model's output did not work. We built a gate to grade each rendered panel against its approved design, and it failed a lot of panels a person had already been happy with. We switched it off rather than tune it. Plain comparisons against the approved reference did the job instead, and they are cheaper and easier to trust.

The thing that caught us out: a batch of shots sat waiting and nobody noticed, until someone opened one and asked why. The stage holding them used a field that did not appear on any of the pages people actually look at. A queue would at least have looked full. This looked like nothing at all. A state nobody can see is a state nobody acts on.

Everything expensive is automatic. Every approval is a person. That split is the whole design.

### For the technically minded

Characters stay consistent by compositing from an approved reference rather than from a prompt, the same way a VFX pipeline keeps anything consistent. Checks that gate work are deterministic, and each one has to be broken on purpose and watched fail before we trust a clean result from it.

## What this is

A bare-bones snapshot of a larger internal system, trimmed to the show-agnostic core and published because the decisions in it might be useful to somebody. It is not maintained and it was never packaged for anyone else's show, so please do not adopt it as a tool. Self-tests needing the original models or a live tracker will not pass from a clone.

The repo's `ARCHITECTURE.md` and `METHOD.md` go further, including the parts that did not work.

<!-- stats -->
### Switched off::The AI quality check we tried
It graded each rendered panel against the approved design, and failed too many that people were perfectly happy with. Simpler comparisons did the job better.

### 1 GPU::What it ran on
A single 12 GB consumer card against a hosted tracker, producing an in-development animated short.

### 0::Automated approvals
Every approval is a person's. The system is built to put the decision in front of them quickly.

### MIT::Licence
Open source on GitHub. A snapshot, not a maintained tool.
<!-- /stats -->
