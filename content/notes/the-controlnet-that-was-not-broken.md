---
type: note
slug: the-controlnet-that-was-not-broken
title: The ControlNet that was not broken
description: A depth control that did nothing on one model worked strongly on its sibling. Why model family is not a detail, and why a test only means something when the signals disagree.
date: 2026-09-23
tags: ai, generative, research, method
draft: false
---

I wanted to steer the camera in a generated image with a depth map. Same room, new angle. A depth ControlNet is a common tool for that, so we wired one in and measured what it did.

On the image-edit model we were using, it did nothing. At strength 0.8 it moved the picture by about 3 points of mean pixel difference. Re-running an identical setup on that machine could move it by 5 on its own, so 3 was noise. Turning the strength down to 0.4 gave roughly the same number. No dose response, no effect.

Another route through the same model did move the picture a lot, 35 points. It looked like success until we looked at what had moved. It had read the depth map as content and added a doorway. The change was content, not camera.

That is the first lesson, and it is the one I would put on a wall: **a big effect in the wrong dimension is worse than no effect.** Measure which axis moved, not just how much.

The obvious conclusion was "ControlNet does not work here, move on." It would have been wrong. The edit model and the base model share a name and a family, and they are not the same thing. On the base model the same file scored nearly 50 against that noise floor of 5, with a clear dose response.

What made that result believable is how the test was built. The prompt asked for the opposite framing to the one the depth map described. If the prompt and the control had agreed, a matching picture would have proved nothing, because either one could have produced it. With them in conflict, the camera followed the depth map against the text. **Make your signals disagree, or you cannot tell adherence from coincidence.**

Two honest limits. It was one sample per strength, so this is a strong direction, not a law. And moving the camera is not the same as keeping the room: a later test showed palette held across cameras while the position of features drifted.

Most of AI production work is not getting a model to do something once. It is knowing, with evidence, why it did not, before you throw the tool away.
