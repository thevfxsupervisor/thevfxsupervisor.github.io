---
type: note
slug: the-negative-prompt-that-does-nothing
title: The negative prompt that does nothing
description: On a speed-LoRA recipe at guidance 1.0, the negative prompt is never read. Measured four ways, traced to one line of the sampler, and why it changed how every instruction was written.
date: 2026-09-09
tags: ai, generative, research, method
draft: false
---

A lot of generated-image workflows carry a negative prompt: a list of things you do not want in the frame. Ours did too. Then we asked a question we had not measured. Does it do anything?

On our speed-LoRA recipe, with guidance (cfg) at 1.0, the answer was no. Two completely different negative prompts, same everything else, produced images that differed by exactly zero. Not a small amount. Zero.

The same pair at a guidance of 4.0 produced a large difference, about 27 points. So the test could detect a negative prompt working; there simply was not one working at 1.0.

Then we read the code instead of guessing. The sampler we use skips the unconditioned pass entirely when guidance is 1.0, and the negative prompt lives in that pass. There is a setting that looks like it turns this back on. It does not restore the negative, it only doubles the compute.

So the finding was confirmed four separate ways, including a source read and a positive control that proved the measurement could fail.

The practical consequence was bigger than the bug. **If you want something absent, describe what is there instead.** Ask for an empty corridor, because on this recipe "no people" is a sentence the model never hears. Once we knew that, positively stated instructions beat negations everywhere in the project.

The general version is the one that travels: a setting that exists in the interface is not evidence that it is connected. Before you tune something, prove it moves the output.
