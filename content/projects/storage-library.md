---
type: project
slug: storage-library
title: Case study: storage-library, one archive from a shelf of old drives, with nothing lost | the vfx supervisor
description: How I turned decades of drives into one organized library and proved every copy by its content before deleting a single file. Open-source tools and agent skills, MIT.
eyebrow: Case study
h1: I turned a shelf of old drives into one library, and proved every copy by its content before deleting a single file
lede: storage-library fingerprints every file, counts only the copies it can prove, and blocks any delete until the other copies are proven by content. Open source, MIT.
cred: Designed and run by me on my own archive, with AI agents doing the hands-on work under rules they cannot skip.
get_label: Get the tools
get_href: https://github.com/thevfxsupervisor/storage-library
final_h2: Your archive is your career. Prove it is safe before you clean it up.
final_p: I run AI as a coordinated team on real film work, with the guardrails that keep a person in charge of every decision that matters. Bring me in before the expensive mistake, while it is still cheap to fix. Or book the course for the method.
final_primary_label: Skip the expensive lessons
final_primary_href: /work-with-me/
final_secondary_label: Join the course waitlist
final_secondary_href: /course/
soon: Open source · MIT · on GitHub
card_title: storage-library
card_eyebrow: Archive tools · open source
card_summary: Tools and agent skills that turn a pile of old drives into one organized library. Every file is proven by its content fingerprint before anything is copied, moved or deleted.
---

## The problem

Anyone who has worked in VFX for a while owns a shelf of drives. Mine held finished work, project archives, family photos and old laptop images, spread across internal disks, USB drives of every age, a small NAS and drives nobody had plugged in for years. Backups of backups, and no honest answer to the only question that matters: if this drive dies tonight, what is gone?

Three things made it urgent. A large cloud folder had to be cut down by a deadline, and before deleting anything online I had to know, file by file, that a real copy existed at home. One 12 TB drive held the core of the archive, so everything else was arranged around never writing to it. And the hardware was old: pending sectors, a USB bridge that reset itself at full speed, an intermittent cable, a drive knocked loose twice in one day.

The goal was not more backups; more backups is how the mess got built. The goal was one organized library, with every irreplaceable file in two proven places, and fewer drives at the end. No new hardware: everything had to fit on drives I already owned.

## The design calls

AI coding agents did most of the hands-on work while I made the calls. That only works with rules that hold when nobody is watching, so the rules went into code wherever code could hold them.

- **Content decides, names never do.** Two files are the same only when their BLAKE3 content fingerprints match. A matching name and size is a lead to check, never proof. Different content means a different file, and both are kept.
- **Proof expires.** A fingerprint proves a copy only if it was read after that drive's last write. Every read-write mount lands in a write ledger, and the next write voids the old proofs on that drive.
- **Only counted copies count.** A short, deliberate list of drives counts as backup, and a drive joins it only after a full health test. Everything else is a lead or a spare.
- **Gates before any delete.** A delete is a list, every physical copy is re-checked by content at that moment, and the final call is mine. Before any risky repair, everything on the drive needs two counted copies somewhere else.
- **Sources are read-only.** A drive being copied from is mounted read-only, and the tools refuse to touch it otherwise.
- **Canary on the real destination.** Before a bulk copy, one file goes end to end onto the actual target drive: final name, size, fingerprint read back. A test on another filesystem proves nothing.
- **Unknown is not zero.** A file that was not hashed, a folder that would not open, a drive that was not attached: each is reported as UNKNOWN, with the reason. Never "no copies", never "unique".

## What storage-library caught

Every tool in the box exists because something went wrong once, or very nearly did.

- **Real files dressed as empty cloud placeholders.** Very small files on Windows drives store their data inside the file table and show zero disk blocks, exactly like online-only cloud stubs. A "zero blocks means placeholder" shortcut nearly dropped 2,184 real files. The rule now: a placeholder is a file whose read fails or returns zeros, nothing less.
- **A copy that never finished.** About 130,000 verified copies sat under temporary names for six hours, because the destination drive's filesystem (exFAT) cannot make hard links, and the copy's last step relied on one. The progress check only looked at free space. Now every bulk job starts with a canary on the real destination, and every progress check reads the error count and lists real file names.
- **A drive that looked written but was not.** A drive knocked loose came back mounted read-write by the operating system. Instead of starting its fingerprints over or trusting luck, a re-attach check took a fresh listing and, once the resumed hash had finished, re-read a random 1% of the files hashed before the drop. All 2,122 matched, so the earlier proofs stood on evidence.
- **A read-only network share that reported itself writable**, because the first line of the mount table belonged to the automounter, not the share. One helper now reads the mount that actually serves the path.
- **A label taken for a definition.** A data column called a whole project-archive tree "portfolio", and a plan got built on that word. The plan now carries a glossary, and a word that could mean two things gets asked, not guessed.

## The results

- **16 drives on the counted list**, the only places a copy is allowed to count.
- **A 2 TB copy drive proven against the main archive at 1,014,073 fingerprints, 0 different.**
- **Every proof survives a reboot honestly.** A drive swap or restart costs a listing and a 1% re-read, not a full re-hash.
- **An honest gap, written down from day one:** a set of very large raw folders still lacks a second counted copy on drives I own. They sit on a named shortfall list, not hidden in an average.

## What storage-library is not

storage-library is not a backup app, a sync service or a cloud product, and it will not decide where your files belong. It is a set of small, tested command-line tools, a read-only web dashboard and agent skills for the main workflows, each ending on a fixed final line so a person or an agent can tell OK from FAILED without guessing. You bring the judgment; storage-library makes sure nothing is lost while you use it. The tests run on invented data and never touch a real drive.

## Try it, and tell me how it holds up

storage-library is open source and MIT, so clone it and point it at your own shelf of drives. If you are sitting on years of work across disks you no longer trust, I would like to hear how it goes: what it caught, what broke, and what you wish it did. Email me at [geoff@thevfxsupervisor.com](mailto:geoff@thevfxsupervisor.com).
