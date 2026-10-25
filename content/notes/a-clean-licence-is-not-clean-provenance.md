---
type: note
slug: a-clean-licence-is-not-clean-provenance
title: A clean licence is not clean provenance
description: Every model file in a generative pipeline matched its publisher by hash, and all but one were permissively licensed. That answers whether you may use the weights. It does not answer what a client actually asks.
date: 2026-10-09
tags: ai, generative, legal, production
draft: false
---

Before a generative pipeline goes near paid work, someone has to answer two questions. Can we use these models commercially? And can we tell the client the output is free of anyone else's rights?

We checked every model file in ours. Seventeen of seventeen matched their publisher's published hash, so we knew exactly which files we were running. Sixteen were under a permissive commercial licence. One was research-only.

That is a clean answer to the first question. It is not an answer to the second, and the gap is easy to miss.

Only two of the thirteen source repositories shipped a licence file at all. And none of the thirteen disclosed what the model was trained on. A permissive licence on the weights tells you nothing about the training data behind them.

So the honest claim you can make to a client is narrower than the one they want. Permissive licence, commercial use of the weights granted, no claim asserted over the output, verified by hash. **Not** "the output is free of third-party rights." That is a legal and indemnity question, and a supervisor who answers it casually is signing something they cannot back.

One method note, because it nearly went wrong. A quick search through one licence returned the first clause that matched and stopped, missing a clause eleven lines further down. It produced a confident blocker that held up other work for an hour. **Read the licence whole. Never grep it.**

On AI-assisted work, chain of title is part of the deliverable. Knowing exactly where your claim stops is worth more than a confident one.
