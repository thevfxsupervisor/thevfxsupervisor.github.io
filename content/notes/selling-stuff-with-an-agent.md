---
type: note
slug: selling-stuff-with-an-agent
title: My agent sold my old furniture and saved me more than 50 hours
description: Ten days of listing, pricing and replying across two marketplaces, handed to an AI agent while I did everything else: 96 listings, about 290 buyer messages, more than 50 hours saved. What it was good at, what it still needed me for, and the traps marketplace sites set for automation.
date: 2026-10-30
tags: agents, ai
draft: false
---

I had a room full of furniture and gear to sell: desks, chairs, lamps, a printer, random electronics. Normally that is a job that eats a week of evenings: photographing things, writing listings, watching two marketplace apps for messages, and answering the same five questions over and over in Danish. This time I handed the whole loop to the AI agent I already use for everything else and let it run alongside my actual job.

Here is what it was good at, what I kept, and the traps to watch for.

**What I let it do.** Write and post the listings, in Danish, with the right category and condition wording for each platform. Watch both marketplace inboxes and an email relay all day, and surface only what actually needed a decision, not every message. Answer the routine stuff on its own once the policy was clear: pickup address, pickup times, payment method, "is this still available." Keep one list of who was promised what. Run price cuts across every listing for an item on the Danish site in one pass, then check each one on the public page rather than trusting that the edit went through. Recognise scam patterns (the "still available?" message that turns into a courier or off-platform payment pitch) and stop engaging with that pattern once the first one was confirmed.

Over ten days the agent created 96 listings (78 on a Danish marketplace site, 18 on Facebook Marketplace), made 119 edits to them, sent about 290 messages to buyers, and saw about 35 pickups through to the end, all while I was doing my actual job. Counted against my own rough timings, fifteen minutes to write a listing in Danish, five to edit one and five to answer a buyer properly, that is more than 50 hours of typing and clicking I did not do. It is an estimate built from the log, not a stopwatch number. It also was not free: I still answered the agent's questions and gave a go-ahead dozens of times over those ten days. But a thirty-second "yes, do that" is a very different cost from fifteen minutes in a listing form.

**To be clear about who was typing.** The replies went out under my name, written and sent by the agent under rules I had set. Buyers were not told an agent was writing, and none of them asked. People still did the handovers, apart from a last-day pile of free odds and ends left out for anyone to take. As far as I can tell the buyers liked it. The messages coming back read like this: "Thanks for the quick reply." "Perfect, and thanks so much for your patience." Even the people who missed out wrote back: "Shame, but thanks for answering, and good evening." Fast, clear, polite answers in the buyer's own language turn out to be most of what makes a second-hand sale pleasant.

**What I kept for myself.** Every price and every accepted offer came from me, or from the one other person I trusted to decide. The agent could propose and track, but it did not set a price or accept an offer. For free items it ran a first-come list, under a rule I had agreed. And the pickups themselves still needed a person there to hand things over.

**The traps.** Marketplace sites do not make this easy, and some of it is fiddly for automation: shadow DOM components, a cap on how many listings you can post as a guest seller before the site simply stops letting you, form fields that quietly revert if you fill them the "normal" way. The agent found working paths around most of it, but they are fragile enough that I'd sanity-check a batch afterwards, not trust it blind.

The best catch, and the one that would have genuinely burned me: Chrome's own translator rewrote a buyer's initials into an unrelated word inside the inbox, and it translates first names too. Match buyers by what is on screen and a reply, or a reservation, will eventually go to the wrong person. The fix is simple once you see it: match the conversation by its own ID, and take names from the raw email, never from the page.

**The mistakes worth admitting.** One list of who was promised what kept things mostly straight, but not perfectly. Once, a desk that had been promised to a paying buyer was handed to someone else at pickup. The list was right; the handover was not. It was caught the same evening and the first buyer got an apology and an alternative. Another time a price got cut on something that had already sold, which is now a standing rule: check it has not gone before you cut. Some older Facebook listings were left at their old prices. And the agent made its own mistakes: once it told a buyer to come whenever suited them, which promised someone else's time it did not have; another time it reported a sweep of every live listing as done when half of them sat on a second page it had not opened. Both were caught and fixed, and both are now rules it follows. I would rather know about all of it than read a tidy report that hides it.

**The other thing worth stealing.** Late in the sale, I had the agent post free listings for a handful of cheap items that had not moved. Within about two hours, seven of them had someone lined up to take them.

None of this needed a custom build. This is the same agent I use for everything else, pointed at a different problem for ten days, with a short list of rules about what it was and was not allowed to decide on its own.

I have cleaned up the playbook and the inbox-watching scripts and put them on GitHub, free to use: [marketplace-agent](https://github.com/thevfxsupervisor/marketplace-agent). If you have a garage, a studio or a storeroom to clear, point your own agent at it.
