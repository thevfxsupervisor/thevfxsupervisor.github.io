---
type: note
slug: config-in-coordination-out
title: Config in, coordination out: the shape of an agent fleet
description: Two separate paths carry a rulebook into an AI agent's session, and confusing them is the mistake. What a working multi-agent setup actually looks like, drawn.
date: 2026-09-19
tags: agents, coordination, pipeline, architecture
draft: false
---

I have written here before about [the shared folder the agents coordinate through](/notes/running-ai-agents-as-a-coordinated-team/) and about [keeping a long-running agent current with its own rules](/notes/keeping-a-long-running-ai-agent-in-sync/). Both of those describe one half. This is what the two halves look like together, and the thing that only becomes obvious when you draw it.

![A multi-agent fleet: a pull task keeps every clone current, one shared config directory feeds every seat on a box, and each seat also has its own clone, cursor and hook. On the right, the seats coordinate through four separate channel surfaces.](/static/fleet-architecture.png)

## The mistake the picture exists to prevent

My first attempt at this diagram was wrong, and wrong in an instructive way. I drew the shared machinery, the config directory, the installed commands, the rulebook imports, as a single arrow into one agent. And I drew the one genuinely per-agent mechanism as a single arrow too.

Read back, that says something false: it says one agent is the hub and the other ten are downstream of it. The label on the arrow said "every seat". The topology said "this seat". **When a label and a topology disagree, a reader believes the topology**, because the topology is the part they can trace with a finger.

So the correction is not cosmetic. It is the difference between a peer system and a star.

## Two layers, and they are not the same layer

Git moves bytes to disk on a schedule. That is one thing, and it is the easy one.

Getting those bytes into a running agent's head is a completely different thing, and it happens twice, by two different routes:

- **Per box.** One config directory holds the rulebook imports, the installed commands, and the shared skill. Every agent running on that machine reads the same files at session start. Nobody owns them. If one agent edits those import lines, every other agent on the box silently loses its rulebook, and nothing says so.
- **Per agent.** Its own clone, its own read-cursor, its own hook. That is the half that tracks what this particular agent has and has not read.

Get those two backwards and you will confidently explain a system that does not exist. **A pulled clone is not a rule anyone has read.**

There is a sharp edge worth knowing here. My delta checker compares an agent's cursor against its clone's local head, and never fetches. That is deliberate: it reports what the agent has not read, not what the remote has. The consequence is that a clone nobody pulls has a head that never moves, so it reports "nothing new" forever while sitting behind. **The thing that tells you about new rules is not a staleness check on your copy**, and reading it as one is the trap.

## A channel is only a channel for the machines that can mount it

The right half of the picture is coordination, and its load-bearing fact is unglamorous: **two agents sharing a channel's name do not necessarily share a surface.**

There are four channel surfaces across three different stores. One GPU machine cannot mount the main shared drive at all. The always-on box cannot see the company store. Those two therefore have no common ground whatever, and no amount of correctly addressing a message changes it. Exactly one machine mounts both, which quietly makes it the only relay in the system.

That is not a permissions bug to route around. It is the topology, and it stays true whether or not the diagram admits it. A request that lands on a surface the recipient cannot reach looks, from the sender's side, exactly like a busy colleague.

## What I would tell someone building this

Draw it, and then have someone else read the drawing back to you without your commentary. Not to check the facts, which you already believe, but to find out what the shape says. Three quiet errors in mine were only visible that way: the arity lie above, a machine connected to a drive it cannot mount, and a coordination channel with eight arrows in and none out, which is a strange thing to call a channel.

The diagram is not the system. It is a claim about the system, and claims are worth testing.
