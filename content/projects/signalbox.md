---
type: project
slug: signalbox
title: signalbox: the tracker builds the shots | the vfx supervisor
description: Your tracker already knows which assets are in which shot. signalbox uses that to generate shots and revisions inside the normal review process. MIT.
eyebrow: Experiment
h1: The tracker already knows what is in every shot. So it can build them.
lede: On a repeatable show, once the models and LoRAs are settled, the interesting problem is not generating a picture. It is doing it for a few hundred shots without an artist hand-assembling each one.
cred: Built and run on one workstation against a live Autodesk Flow site, on an in-development animated short.
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
card_title: signalbox
card_eyebrow: Experiment · open source
card_summary: The tracker already holds the character and location references, which assets are in which shot, and the beats behind each one. signalbox uses that to generate shots and revisions inside the normal review process. Open source, MIT.
---

## The idea

Your production tracker already holds the whole graph. The character and location references. Which assets appear in which shot. Which portion of the script makes up each action beat. The prompt fragments attached to each of those assets.

That is everything you need to build a shot. So rather than an artist opening a template, hunting down the references and writing a prompt for every shot, signalbox reads those connections and makes the shot from them.

## What happens

![The signalbox loop: the tracker holds assets, shots and beats, signalbox synthesises a shot from those connections, versions publish into the normal review, and a note sends back a wedge of new versions.](/static/signalbox-loop.svg)

Shots generate from what the tracker already knows, and the results publish themselves as Versions, ready in the usual review process. Nobody learns a new tool.

When a reviewer leaves a note asking for a change, an LLM reads it, adjusts the prompt or the asset connections it points at, and renders a wedge of four to eight variations. Those publish for review too. The reviewer picks one.

And it tracks dependencies. Revise an upstream asset or a keyframe panel, and every shot downstream of it regenerates instead of quietly going stale.

Models, LoRAs and workflow templates swap out without touching any of this. The part that matters is not the generator, it is that all of it happens inside the review process a crew already runs.

### For the technically minded

Autodesk Flow Production Tracking, still widely called ShotGrid. A watcher polls state about once a minute, so there is no queue to keep in sync and the service can be killed mid-render and restarted with nothing to reconcile. Note interpretation runs through `claude -p`. Every generation step is automatic; every approval is a person's.

## What this is

A bare-bones snapshot of a larger internal system, trimmed to the show-agnostic core and published in case the decisions in it are useful. It is not maintained and was never packaged for anyone else's show, so please do not adopt it as a tool. The repo's `ARCHITECTURE.md` and `METHOD.md` go further, including the parts that did not work.

<!-- stats -->
### 4 to 8::Versions per note
A reviewer's note comes back as a wedge of variations to choose from, not a single guess.

### Switched off::The AI quality check we tried
It graded rendered panels against the approved design and failed too many that people were happy with. Simpler comparisons did better.

### 0::New tools to learn
Everything happens in the tracker and the review process the crew already uses.

### MIT::Licence
Open source on GitHub. A snapshot, not a maintained tool.
<!-- /stats -->
