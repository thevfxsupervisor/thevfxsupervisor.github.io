---
type: project
slug: feature-vfx-shot-pipeline
title: Case study: a five-vendor shot list through several re-cuts, and the errors we caught | the vfx supervisor
description: Several re-cuts, five vendors, several hundred VFX shots: how the shot list reached a clean final cut, and the errors we caught on the way, from a one-frame bug that halved the apparent VFX count to ten shots wrongly flagged missing.
eyebrow: Case study
h1: Every re-cut changed every timecode. We caught the errors that would have scrambled the shot list, and the final cut landed clean.
lede: As VFX Producer, I ran the VFX production office and the shot pipeline on a Nordic feature with five vendors and several hundred VFX shots, through several re-cuts, from the first breakdown to deliveries coming back. My AI agents did the mechanical work, with the footage pipeline on our own machines. Every pipeline call and every send were mine.
cred: Shot IDs, re-cut tracking, vendor reference clips and delivery tracking, run by one person across several re-cuts.
get_label: Put me on your show's shot list
get_href: /work-with-me/
stats_h2: Four numbers from the shot list
final_h2: Stop rebuilding your shot list by hand at every re-cut.
final_p: I'll set up your shot list before the first bid package goes out, so a re-cut means reviewing what changed, not re-logging the film. My AI production office cross-checks from your first breakdown, and every pipeline call is mine.
final_primary_label: Lock your shot list before the first re-cut
final_primary_href: /work-with-me/
final_secondary_label: Get the free breakdown tool
final_secondary_href: /projects/breakdown-studio/
soon: Nordic feature · client details under NDA
card_title: Feature VFX shot list
card_eyebrow: Case study · shot list
card_summary: Several re-cuts, five vendors, and the shot-list errors we caught, from a one-frame bug that halved the apparent VFX count to ten shots wrongly flagged missing.
---

## Every re-cut changes every timecode

On a Nordic feature with several hundred VFX shots and five vendors, that is how a bid, a reference clip or a status ends up pinned to the wrong shot without anyone noticing. My job was to stop that happening quietly. The shot breakdown was rebuilt and reconciled to the shot list across several re-cuts, and on the final cut the update went in with no duplicate shots and no broken links.

## A shot's ID lives on the slate, not the timecode

Every shot was identified by the slate burned into the picture, not by its timecode. Timecodes change with every edit; the slate does not. The ID carried the take as well, because a different take of the same setup is a different plate, and I need that visible before anyone bids.

The slate has its own grammar. Scene parts, joined scenes and insert series all look like slates to a naive reader, and teaching the software that grammar removed a whole class of false shot IDs. A slate change is evidence of a cut, not proof: a screen in frame or a swish pan can show two slates in one shot, so those get flagged for review instead of split.

## No edit data? The picture already carries the shot list.

Edit data does not always arrive, and when it does not, most shows stall or start typing. Every cut we received carried three things burned into the picture: the slate, the timecode and the editor's VFX note. So when the data could not be delivered, I rebuilt the breakdown from the picture itself. The software reads all three off every shot, on our own machines, and turns a cut into a shot list with IDs, timecodes and VFX notes attached.

Reading text off a picture goes wrong in predictable ways, so the reads are guarded. A VFX note counts only if it appears at the start, middle and end of a shot, so a stray overlay cannot invent a VFX shot. Look-alike characters are corrected against the slate grammar. And a read is a candidate until it is checked: it never writes itself into the shot list unchecked. Checked against nearly ten thousand human-verified slate reads, the reader agreed on 98 percent. That reader now ships free in [Breakdown Studio](/projects/breakdown-studio/).

## The software proposes cuts. The doubtful ones get reviewed.

Cut-finding software misses real cuts and invents false ones, so I never take its list as final. At its default sensitivity the software missed a few percent of cuts, and turning the sensitivity up invented cuts on camera moves. So the clear cases are accepted automatically, and the doubtful ones go to a review queue as a strip of frames, which I reviewed with Claude; nothing in that queue is applied automatically. A detected cut was confirmed when the slate changed across it, and a slate change with no detected cut was flagged as a possible missed one.

Some missed cuts hide behind placeholder slates, where there is no clean slate change to catch. I had a list kept of each case and its fix, tied to the shot's ID, so the same problem gets flagged when the next re-cut is checked, instead of being rediscovered. And of 21 suggested cut fixes on the final cut, only one touched a VFX shot. I applied that one and logged the others, because tidying shots that do not affect the VFX list adds risk for no benefit.

## What went wrong, and what caught it

**A one-frame bug halved the apparent VFX count.** A one-frame slip in frame grabbing made every shot's last-frame thumbnail show the next shot. Earlier builds only used the middle frame, so nobody had seen it. The bug surfaced on the final cut because a stricter check of the burned-in notes read the neighbour's note on the last frame, and the strict count of VFX shots came back at roughly half the loose count of the same cut. That gap between two counts of the same thing was the clue. After the fix, the two counts landed within a handful of shots of each other.

**A shortcut that worked on one re-cut failed on the next.** Comparing one frame per shot was fine between cuts delivered the same way. When the next cut arrived as a different delivery, the one-frame comparison called most of the film changed. Comparing several frames per shot separated same shots from different shots cleanly, and the first run of that fix was itself checked and corrected.

**99 shots in the new cut claimed 42 shots on the list that can each belong to only one.** We changed the matching so each listed shot can be claimed by one new shot only, with the slate overriding any look-alike. Replayed later against my approved matches from the final cut, the open-source version of the matcher reproduced about 95 percent of them wherever a match could be made, with zero collisions.

**The first automatic match also called about a quarter of the VFX shots dropped. They were not.** One camera take can be cut into several shots, so nothing was called dropped without more checks and a human decision. Separately, some invisible-VFX shots had been added to the list by hand and carry no on-set slate. An audit found an automatic "dropped from cut" rule had wrongly marked some of them as dropped. Those shots are now protected from automatic removal, and only I can omit them.

**Matching on the slate alone said ten shots were missing from a vendor's bid.** They were all there: the vendor had renumbered the slate but kept the plate name. I caught it, and the match now uses three names instead of one: slate, alias and plate name. That cleared all ten.

**A status script let a resubmitted shot outrank the reviewer's verdict.** Another overwrote three hand-set verdicts, and a third silently stopped reading partway down the sheet. Each became a rule: only verdicts rank, nothing downgrades a verdict, and every read covers the whole sheet.

**Snapshot first, compare after.** Consolidating four report tabs into one, we saved a snapshot of the schedule first and compared it afterwards. The comparison caught the rebuild itself zeroing part of the plan, and after the fix the schedule matched the snapshot on every row. A separate check found a schedule status that had never worked.

## The reviewer's verdict beats the vendor's own report

Each vendor was sent a set of per-shot reference clips, watermarked with their own name and limited to the VFX shots up for bid. The clip set was cut frame-accurately from the edit in about a minute and a half on one local machine, then watermarked per vendor.

Vendors name shots in different ways, so deliveries did not match up uniformly. For the hardest scheme we built a lookup of verified name prefixes rather than guess from spelling: 97 of 98 names decoded, and the odd one out was flagged, not forced.

Every delivery went into a delivery log that is only ever added to, and the weekly report was built from that log, so any past week's figure could be re-derived and defended. The counting rules were fixed in advance: a resubmitted shot is one shot, a test never counts. A vendor's own status report is a claim. The tracker took the reviewer's verdict over the vendor's own claim, with set rules for which wins when email and the production-tracking system disagree.

Email tracking only sees what happens in email: when approvals happen in a review tool or on a call, a report can show work as behind when it is not. When a report did exactly that, we named the blind spot and kept the report out of any vendor conversation until the review tool had been checked.

## The slate grouped shots better than image matching

A shot wall of hundreds of tiles was built to put the whole VFX scope in front of the VFX consultant in one view. Each tile was built to be dragged, and later updates renamed tiles but never moved them, because the layout was the consultant's. Off-the-shelf image similarity could not tell one shot from another on footage that all looked alike. For a grouped copy of the wall, the camera setup already recorded in the slate did the job better, and a local image model then confirmed the slate grouping was visually coherent.

## Agents gathered and cross-checked. I decided and sent.

Specialist AI agents coordinated through shared files, one writer per file, and anything that mattered was kept in the project, not in the chat between them. They drafted the procedural emails. I wrote the important ones and made every send. They gathered and cross-checked; I kept the pipeline judgment calls. The standing rule became: no summary counts until someone opens the real file. When an agent broke it, the miss went into a visible log of the agents' own mistakes, and each class of mistake became a check or a rule.

The shot-list software became an open-source, free tool: [Breakdown Studio](/projects/breakdown-studio/). It was tested against this production: nearly ten thousand human-verified slate reads, 98 percent of them matching what the software read.

The money side of this show is its own case study: [five vendors, a moving cut and every cost change in the client's next report](/projects/feature-vfx-production-office/).

## Our own machines, and one cloud model

The footage pipeline ran on our own machines. Vendors were sent watermarked reference clips. The only cloud model was Claude Code, on a private account with training off, and it looked at stills, mostly when we reviewed doubtful cuts together.

<!-- stats -->
### 97 of 98::Vendor shot names decoded from the hardest naming scheme
The one that did not decode was flagged, not forced.

### Half::The VFX count a one-frame bug would have hidden
Caught because two counts of the same cut disagreed.

### 1 of 21::Suggested cut fixes on the final cut that touched a VFX shot
I applied that one and logged the others.

### 42::Shots on the list claimed by two or more new shots
On the first match. Each listed shot can now be claimed once.
<!-- /stats -->

## What this means for your show

The expensive old way: someone rebuilds the shot list by hand after every re-cut, and a vendor prices the wrong shot. On this show the final-cut update went in with no duplicate shots and no broken links, and the matcher, replayed against my approved matches, reproduced about 95 percent of them wherever a match could be made. Bring me in before the first cut moves, and I'll build your shot list to keep every shot tied to the right plate, bid and status, so a re-cut means reviewing what changed.
