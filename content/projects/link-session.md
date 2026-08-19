---
type: project
slug: link-session
title: Case study: link-session, coordinating a fleet of AI agents across projects | the vfx supervisor
description: How I coordinate several live AI agents across concurrent projects over shared files, with no server. A small open-source Claude Code skill.
eyebrow: Case study
h1: How I run a fleet of AI agents across projects, coordinated over shared files, no server
lede: A small utility that does one job well: let several live AI sessions coordinate on the same production, hand off work, and stay out of each other's way. It also starts a new session straight into a role from a library of bootstrap templates. Open source, MIT.
cred: Designed and shipped solo, running daily across three operating systems and multiple projects.
get_label: Get the skill
get_href: https://github.com/thevfxsupervisor/link-session
final_h2: Want AI-assisted pipeline work on your show?
final_p: I run AI as a coordinated team on real film productions, with the guardrails that keep it safe. If that is useful to your show, let's talk. Or book the course for the method.
final_primary_label: Work with me
final_primary_href: /about/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: link-session
card_eyebrow: Claude Agent Skill · open source
card_summary: A Claude Code skill for coordinating several live AI agent sessions over shared files. No server, no message bus. It now starts a new session straight into a role from a library of bootstrap templates.
---

## The problem

Running a film's VFX department with an AI pair is not one chatbot in a window. It is several live agent sessions at once: one on the shot breakdown, one on the vendor bids and finance, others driving GPU jobs across machines. They share the same sheets, the same files, the same production, and left uncoordinated they collide, two sessions editing the same sheet, work redone, a job started twice.

## The design call

I did not want a server, a message bus, or an orchestration framework to babysit a side utility. So link-session coordinates over plain files: each session writes one small JSON outbox into a shared folder, and a lightweight watcher surfaces what every other session is doing, without polling. Files over a service buys three things that matter on a production: zero infrastructure to run or break, a coordination trail you can read by eye, and state that survives a session dying, a restart, or a flaky network mount.

## In production

It runs daily across Windows, macOS and Linux machines and across several concurrent projects, coordinating the agents that drive [Breakdown Studio](/projects/breakdown-studio/), the finance and vendor sheets, and heavier GPU work farmed out to other machines. The rules that keep it safe are the point: one writer per file, long payloads as files rather than single-slot messages, a clean stop protocol, and a hard line that coordination carries metadata, never client or show content. No client names, no show names, ever.

## Hardened by running it

The recent work on it is the tell that it is real and not a demo. A coordination layer fails quietly, so most of that effort went into making silence mean something: it reports only genuine changes rather than every re-save, keeps idle sessions quiet so what does arrive is worth reading, counts its own watchers so nothing is delivered twice, and runs identically across all three operating systems, down to the older shells. It also grew a clean way to rename and re-identify a session without losing the thread, which is what you hit the moment a one-machine setup becomes a fleet. Every one of those was a real failure caught by running it daily, not a feature I imagined, and the skill is smaller now than it was while doing more.

## Try it, and tell me how it holds up

It is open source and MIT, so clone it and point it at your own sessions. If you are running AI agents on real work, I would genuinely like to know how it behaves for you: what worked, what broke, and what you wish it did. Email me at [geoff@wanglemedia.com](mailto:geoff@wanglemedia.com) and tell me.
