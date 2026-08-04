---
type: project
slug: link-session
title: Case study: link-session, coordinating a fleet of AI agents on one production | the vfx supervisor
description: How I coordinate several live AI agents on a single film production over shared files, with no server. A small open-source Claude Code skill.
eyebrow: Case study
h1: How I run a fleet of AI agents on one film, coordinated over shared files, no server
lede: A small utility that does one job well: let several live AI sessions coordinate on the same production, hand off work, and stay out of each other's way. Open source, MIT.
cred: Designed and shipped solo, running daily across three operating systems on a live feature.
get_label: Get the skill
get_href: https://github.com/thevfxsupervisor/link-session
final_h2: Want AI-assisted pipeline work on your show?
final_p: I run AI as a coordinated team on real film productions, with the guardrails that keep it safe. If that is useful to your show, let's talk. Or book the course for the method.
final_primary_label: Work with me
final_primary_href: /about/
final_secondary_label: Book the course, 3 Sept
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: link-session
card_eyebrow: Agent coordination · open source
card_summary: A file-based protocol for coordinating several live AI agents on one production. No server, no message bus.
---

## The problem

Running a film's VFX department with an AI pair is not one chatbot in a window. It is several live agent sessions at once: one on the shot breakdown, one on the vendor bids and finance, others driving GPU jobs across machines. They share the same sheets, the same files, the same production, and left uncoordinated they collide, two sessions editing the same sheet, work redone, a job started twice.

## The design call

I did not want a server, a message bus, or an orchestration framework to babysit a side utility. So link-session coordinates over plain files: each session writes one small JSON outbox into a shared folder, and a lightweight watcher surfaces what every other session is doing, without polling. Files over a service buys three things that matter on a production: zero infrastructure to run or break, a coordination trail you can read by eye, and state that survives a session dying, a restart, or a flaky network mount.

## In production

It runs daily across Windows, macOS and Linux machines on a live feature film, coordinating the agents that drive [Breakdown Studio](/projects/breakdown-studio/), the finance and vendor sheets, and heavier GPU work farmed out to other machines. The rules that keep it safe are the point: one writer per file, long payloads as files rather than single-slot messages, a clean stop protocol, and a hard line that coordination carries metadata, never client or show content. No client names, no show names, ever.

## What it proves

The tool is small on purpose, and I lead with that. The point is not the utility, it is the operating model: I run AI as a coordinated team on real production work, with guardrails, not a single assistant in a tab. That is the hardest half of "a VFX supervisor who orchestrates AI" to demonstrate, and this is the public proof of it.
