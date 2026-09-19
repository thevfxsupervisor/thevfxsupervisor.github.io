---
type: note
slug: every-gate-is-a-person
title: Every gate is a person, and that is the product
description: A generative video pipeline where the production tracker is the state machine, a deterministic check can only refuse, and nothing ever self-approves. Drawn.
date: 2026-09-19
tags: ai, pipeline, production, generative, signalbox
draft: false
---

Most pipelines built around a generative model do one of two things. They skip review and ship whatever came out, or they bolt on a separate admin tool that nobody on the actual production ever opens. Neither survives contact with a real show.

[SignalBox](/projects/signalbox/) takes the third option: make the tool the production already lives in, the tracker, be the trigger and the record.

![SignalBox architecture: an operator writes a note and sets a status, a standing service polls the tracker and runs twelve watchers, automatic steps compose and generate, and results publish back as versions awaiting a person.](/static/signalbox-architecture.svg)

## The tracker is the state machine

There is no queue and no job file. Every arrow in that picture reads or writes a field in the production tracker. The service polls it rather than being pushed to, runs its watchers in a fixed order, and publishes results back as versions.

That sounds like a limitation and is actually the whole point. The record of what ran, and of who asked for it, lands in the tool the production already uses. Nobody has to open a second thing, and nobody can quietly run something that leaves no trace where people look.

## A deterministic check can only refuse

Look at the check in the middle of the diagram. It has one arrow out, and it is not an approval.

It can park the work and say why. It cannot pass anything. Approval only ever comes from a person, at a gate above it. That asymmetry is deliberate: a check that can approve is a check that will eventually approve something wrong, and then you have automation that signed off on itself.

This replaced a vision model doing quality control. That model measured 38% pass on panels that were correct, because attribute checklists conflate identity with pose and a legitimate close-up crops something out of frame. It got switched off rather than tuned, and what replaced it compares against a reference instead of asking a model for an opinion. **The same discipline a VFX pipeline already applies to every other automated step.**

## The expensive step re-reads the approval

One step in that pipeline costs real GPU time. It does not trust the link it was handed. It goes back to the tracker and re-reads the approval on the way in, and refuses before spending anything if it is not a real one.

That is a small piece of paranoia that has paid for itself. A pipeline that regenerated without asking would be worth less, not more.

## Provenance reports, it does not block

The stored record of what was sent for a shot gets compared against what the model actually received. A disagreement is posted as a note on the version, where a human will see it, rather than into a log nobody reads.

Note that it reports rather than blocks. A provenance mismatch is a reporting defect, not a reason to throw away a rendered frame. And the record is written by the code that did the sending, because **"the record says we sent it" is not evidence that it was sent.**

## What a production actually buys

Every automatic step in this system is automatic. Every gate is a person. The gates are not friction left over from a system that could not be fully automated, they are the product, and the record of who passed which one is the thing a production is actually paying for.

The code is [public, MIT](https://github.com/thevfxsupervisor/signalbox), including the architecture notes on what each decision cost.

The team of agents that built it runs on the same principle, drawn out in [config in, coordination out](/notes/config-in-coordination-out/).
