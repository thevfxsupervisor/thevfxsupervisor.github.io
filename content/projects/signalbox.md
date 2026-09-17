---
type: project
slug: signalbox
title: SignalBox: the tracker builds the picture | the vfx supervisor
description: Your tracker already knows which assets are in which shot. SignalBox uses that to build the picture, and the revisions, inside the normal review process. MIT.
eyebrow: Experiment
h1: The tracker already knows what goes in every shot. So SignalBox builds the picture.
lede: On a repeatable show, once the models and LoRAs are settled, the interesting problem is not generating a picture. It is doing it across a whole episode without an artist hand-assembling every shot. That is what SignalBox is for.
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
card_eyebrow: Experiment · open source
card_summary: The tracker already holds the character and set references, which assets are in which shot, and the beats behind each one. SignalBox uses that to build the picture, and the revisions, inside the normal review process. Open source, MIT.
---

## The idea

Your production tracker already holds the whole graph. The character and set references. Which assets appear in which shot. Which portion of the script makes up each action beat. The prompt fragments attached to each of those assets.

That is everything you need to build a shot. So rather than an artist opening a template, hunting down the references and writing a prompt for every shot, SignalBox reads those connections and composes the picture from them.

## What happens

![The SignalBox loop: the tracker holds assets, shots and beats, SignalBox composes the picture from those connections, versions publish into the normal review, and a note sends back a wedge of variations.](/static/signalbox-loop.svg)

SignalBox builds each shot's still and then its video from what the tracker already knows, and the results publish themselves as Versions, ready in the usual review process.

When a reviewer leaves a note asking for a change, an LLM reads it, rewrites the beat or the prompt, and renders a wedge of variations. Those publish for review too, and the reviewer picks one. Wedge size is configurable; we used eight for the still panels and four for the shot videos.

So the tracker becomes the interface for iterating revisions. Nobody opens the shot in another application, renders a new version, and uploads it back to the tracker for review. That round trip does not happen.

They call the next part the cascade. Revise an upstream asset design or an approved panel, and everything built from it is invalidated and rebuilt instead of quietly going stale.

Because every trigger is a piece of tracker state, you can ask why any frame exists and get an answer you can act on: the note that caused it, and who approved it.

Models, LoRAs and workflow templates swap out without touching any of SignalBox. The part that matters is not the generator, it is that all of it happens inside the review process a crew already runs.

### For the technically minded

Autodesk Flow Production Tracking, still widely called ShotGrid. A watcher polls state about once a minute, so there is no queue to keep in sync and the service can be killed mid-render and restarted with nothing to reconcile. Note interpretation runs through `claude -p`. Every generation step is automatic; every approval is a person's.

## What this is

SignalBox is a bare-bones snapshot of a larger internal system, trimmed to the show-agnostic core and published in case the decisions in it are useful. It is not maintained and was never packaged for anyone else's show, so please do not adopt it as a tool. One gap worth naming: change a model or a LoRA and nothing yet notices that existing versions were made with the old one. The repo's `ARCHITECTURE.md` and `METHOD.md` go further, including the parts that did not work.

<!-- stats -->
### 8 and 4::Variations per wedge
Eight for a still panel, four for a shot video, and the size is configurable. A note comes back as a set to choose between, not one guess.

### Switched off::The AI quality check we tried
It graded rendered panels against the approved design and failed too many that people were happy with. Simpler comparisons did better.

### 0::New tools to learn
Everything happens in the tracker and the review process the crew already uses.

### MIT::Licence
Open source on GitHub. A snapshot, not a maintained tool.
<!-- /stats -->
