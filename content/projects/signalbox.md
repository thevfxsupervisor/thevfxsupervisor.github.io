---
type: project
slug: signalbox
title: SignalBox: a whole episode at a time | the vfx supervisor
description: The slow part was never one video. SignalBox builds a whole episode from what your tracker already knows, revisions included, in the normal review. MIT.
eyebrow: Case study
h1: The slow part was never making one video. It was making a whole episode without hand-assembling every shot.
lede: SignalBox reads the connections already sitting in your production tracker, builds the shot from them, and takes revision notes back through the same review.
cred: Built and run by one person, on one workstation, against a live Autodesk Flow site on an in-development animated short.
get_label: See the code
get_href: https://github.com/thevfxsupervisor/signalbox
code_repo: https://github.com/thevfxsupervisor/signalbox
license: https://opensource.org/licenses/MIT
programming_language: Python
stats_eyebrow: The shape of it
stats_h2: In short
final_h2: Doing something similar?
final_p: If you are wiring a tracker to generative work and want to compare notes, I am always happy to. The course covers the same ground in more depth.
final_primary_label: Get in touch
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: SignalBox
card_eyebrow: Case study · open source
card_summary: The slow part was never making one video. SignalBox builds a whole episode from the connections already in your tracker, revisions included, inside the review a crew already runs.
---

## The idea

Your tracker already holds the graph: which assets are in which shot, which part of the script makes each beat, the prompt fragments on each asset. That is enough to build the picture, so SignalBox builds it.

## What happens

![How SignalBox works: the tracker holds assets, shots and beats, SignalBox composes the picture, versions publish into the normal review, and a note returns a wedge of variations.](/static/signalbox-loop.svg)

Versions publish into the usual review. A reviewer's note goes to an LLM, which rewrites the beat and returns a wedge of variations to pick from. Revise an upstream asset and everything built from it rebuilds. Nobody opens another application, renders a version, and uploads it back.

Autodesk Flow Production Tracking, still widely called ShotGrid. Notes are interpreted by `claude -p`. Every generation step is automatic, and every approval is a person's.

## For the technically minded

![SignalBox architecture: the tracker is the state machine, a standing service polls it and runs twelve watchers, and the deterministic check can only refuse, never approve.](/static/signalbox-architecture.svg)

Nothing in there holds state except the tracker. The check in the middle has one arrow out and it is not an approval: it can park work and say why, and the yes always comes from a person. More in [Every gate is a person](/notes/every-gate-is-a-person/).

## Who built it

I am Geoffrey Hancock, a VFX supervisor and producer, with a VES award for Changeling, a VES nomination for Invictus and a Robert nomination for Skammerens Datter II. I directed a team of AI agents to build SignalBox, and the judgment calls are mine. If you are wiring a tracker to real work, I am at [geoff@thevfxsupervisor.com](mailto:geoff@thevfxsupervisor.com).

## What this is

A snapshot of a larger internal system, not maintained. One gap worth naming: change a model or a LoRA and nothing yet notices that existing versions used the old one.

<!-- stats -->
### 8 and 4::Variations per wedge
Stills and videos. Configurable.

### Switched off::The AI quality check
It failed panels people were happy with.

### 0::New tools to learn
It happens in the tracker.

### MIT::Licence
On GitHub. A snapshot, not a product.
<!-- /stats -->
