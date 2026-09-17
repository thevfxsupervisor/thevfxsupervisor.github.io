---
type: project
slug: signalbox
title: SignalBox: the tracker builds the picture | the vfx supervisor
description: Your tracker already knows which assets are in which shot. SignalBox uses that to build the picture, and the revisions, inside the normal review process. MIT.
eyebrow: Case study
h1: The tracker already knows what goes in every shot. So SignalBox builds the picture.
lede: Once the models and LoRAs are settled, the hard part is not making one picture. It is making them across a whole episode without an artist hand-assembling every shot.
cred: Built and run by one person, on one workstation, against a live Autodesk Flow site on an in-development animated short.
get_label: See the code
get_href: https://github.com/thevfxsupervisor/signalbox
code_repo: https://github.com/thevfxsupervisor/signalbox
license: https://opensource.org/licenses/MIT
programming_language: Python
stats_eyebrow: The shape of it
stats_h2: A few numbers from it
final_h2: Doing something similar?
final_p: If you are wiring a tracker to generative work and want to compare notes, I am always happy to. The course covers the same ground in more depth.
final_primary_label: Get in touch
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: SignalBox
card_eyebrow: Case study · open source
card_summary: The tracker already holds the character and set references, which assets are in which shot, and the beats behind each one. SignalBox uses that to build the picture, and the revisions, inside the normal review process. Open source, MIT.
---

## The idea

Your production tracker already holds the graph: the character and set references, which assets are in which shot, which part of the script makes each action beat, and the prompt fragments on each asset. That is everything you need to build the picture, so SignalBox reads those connections and builds it.

## What happens

![How SignalBox works: the tracker holds assets, shots and beats, SignalBox composes the picture, versions publish into the normal review, and a note returns a wedge of variations.](/static/signalbox-loop.svg)

Versions publish themselves into the usual review. A reviewer's note goes to an LLM, which rewrites the beat or the prompt and returns a wedge of variations to choose between: we used eight for still panels, four for shot videos, and it is configurable.

So the tracker is the interface for iterating. Nobody opens the shot in another application, renders a version, and uploads it back. Revise an upstream asset or an approved panel and everything built from it rebuilds, which they call the cascade. Every trigger is tracker state, so you can ask why any frame exists and get an answer.

### For the technically minded

Autodesk Flow Production Tracking, still widely called ShotGrid. A watcher polls about once a minute, so there is no queue to reconcile and it can be killed mid-render and restarted. Notes are interpreted by `claude -p`. Every generation step is automatic; every approval is a person's.

## Who built it

I am Geoffrey Hancock, a VFX supervisor and producer, with a VES award for Changeling, a VES nomination for Invictus and a Robert nomination for Skammerens Datter II. These days I build the production tooling as well as supervise the work.

I directed a team of AI agents to build SignalBox, and the judgment calls are mine: what had to be deterministic, where a person had to say yes, and which AI component to switch off when it measured badly. If you are wiring a tracker to real work, I am at [geoff@thevfxsupervisor.com](mailto:geoff@thevfxsupervisor.com).

## What this is

A snapshot of a larger internal system, trimmed to the show-agnostic core and not maintained, so please do not adopt it as a tool. One gap worth naming: change a model or a LoRA and nothing yet notices that existing versions used the old one.

<!-- stats -->
### 8 and 4::Variations per wedge
Eight for a still panel, four for a shot video. Configurable.

### Switched off::The AI quality check we tried
It failed too many panels people were happy with. Simpler comparisons did better.

### 0::New tools to learn
It all happens in the tracker the crew already uses.

### MIT::Licence
Open source on GitHub. A snapshot, not a product.
<!-- /stats -->
