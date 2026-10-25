---
type: note
slug: pin-the-deliverable-not-the-recipe
title: Pin the deliverable, not the recipe
description: Re-running an approved generative shot does not reliably give it back, and raising the resolution quietly re-frames it. Why the approved file is the asset, not the settings.
date: 2026-10-02
tags: ai, generative, pipeline, production
draft: false
---

In traditional VFX, if you keep the scene file you can re-render the shot. Generative pipelines inherit that assumption, and on our setup it was not reliably true.

**Same settings, different picture.** Two runs of an identical configuration came out identical in one GPU state and about 5 points of mean pixel difference apart in another. That retracted an earlier, stronger claim we had made that the lane was bit-for-bit deterministic. It also gave us something useful: 5 became the project's noise floor. Any effect smaller than that could not be told apart from nothing.

The rule that came out of it is short. **Pin the deliverable, not the recipe.** When a person approves a frame, the approved file is the asset. The settings are the history of how you got there.

**Higher resolution is not a neutral upgrade.** The obvious way to improve quality is to render bigger. At native 1920 wide the model framed the subject wider than it did at 1280, with the same prompt and the same seed, on all four seeds we tried. Changing resolution changed the shot size, so a composition approved at one resolution can be invalidated by moving to the other.

Rendering at 1280 and upscaling sidesteps the re-framing, and it came out sharper on our edge measure on all four seeds, and cost about 50 seconds a frame against 78 for native. On a 16 GB card, native 1920 was clean on eight of eight seeds; 2048 wide failed three times in eight. A setting that fails sometimes is worse than one that always fails, because every frame then needs a person to check it.

Limits, stated so these are not over-quoted: stills only, one prompt, and frame-to-frame consistency of the upscale on moving images was not tested.

For anyone budgeting a generative project, the point is not the numbers. It is that "we can always re-render it" needs to be tested on your setup before it goes in a schedule.
