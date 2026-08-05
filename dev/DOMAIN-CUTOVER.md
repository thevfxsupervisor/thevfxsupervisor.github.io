# Point thevfxsupervisor.com at the GitHub Pages site

**Status: CURRENT. Not yet done.** Written 2026-08-05. Everything below is ready to execute; nothing
has been changed on the live site or in DNS yet.

**Cost: zero.** GitHub Pages custom domains are free and include auto-renewing HTTPS via Let's
Encrypt. The only cost stays the easyDNS registration already being paid. Do NOT buy any easyDNS
web-hosting, URL-forwarding, or parking add-on. Plain DNS records are all this needs, and they are
included.

**Before executing any step below, run `./check_cutover.sh` from the repo root.** It is the
automated pre-flight for this runbook (added by the linux seat, same day): it checks what DNS
actually returns and what the domain actually serves, rather than trusting that a step was done, and
it refuses to green-light the cutover while the parking record is still live. It prints the rollback
command on failure. Run it again after each DNS change until it reports Ready.

## Starting state (verified 2026-08-05)

- `thevfxsupervisor.com` and `www` both resolve to **64.68.200.44**, the easyDNS parking page.
- Nameservers are easyDNS (`motorhead.easydns.org`, `rush.easydns.com`, `nirvana.easydns.net`).
- GitHub Pages currently has **no custom domain set** (`cname: null`), serving at
  `https://thevfxsupervisor.github.io/`, HTTPS enforced.
- The repo has two deliberate safety gates: `build.py` has `CUTOVER_DONE = False` so it does not
  emit `docs/CNAME`, and `.gitignore` excludes `docs/CNAME`.

## Why the order matters (this already broke the site once)

The moment a custom domain is set on GitHub, `thevfxsupervisor.github.io` starts **301-redirecting**
to the `.com`. If DNS is not yet pointing at GitHub, every visitor lands on the parked lander and the
site is effectively down. That is exactly what happened on 2026-07-29 when a `docs/CNAME` was
committed while the domain was still parked.

So: **DNS first, GitHub second.** GitHub's own docs suggest the reverse (claim the domain before
pointing DNS at it) to prevent domain takeover. Step 2 below gets both safety and zero downtime.

## Step 1, at easyDNS (Geoff)

Optional but useful: drop the TTL to 300 seconds first so a rollback propagates fast.

1. **Delete** the existing apex `A` record `64.68.200.44`. Do not leave it alongside the new ones, or
   traffic round-robins between GitHub and the parking page.
2. **Add four apex `A` records** for `thevfxsupervisor.com`:

       185.199.108.153
       185.199.109.153
       185.199.110.153
       185.199.111.153

3. Optional IPv6, four `AAAA` records:

       2606:50c0:8000::153
       2606:50c0:8001::153
       2606:50c0:8002::153
       2606:50c0:8003::153

4. **Change `www`** from its current CNAME-to-apex to:

       www.thevfxsupervisor.com.   CNAME   thevfxsupervisor.github.io.

5. **Turn off** easyDNS parking / URL forwarding for the domain.

Verify from any machine before moving on:

    nslookup thevfxsupervisor.com
    nslookup www.thevfxsupervisor.com

Apex should return the four `185.199.x.153` addresses. `www` should resolve via
`thevfxsupervisor.github.io`. Wait until that is true, not just submitted.

## Step 2, prevent domain takeover (Geoff, recommended)

While DNS points at GitHub but the domain is not yet claimed by the account, someone else could in
principle claim it on their own repo. Verifying the domain closes that window without triggering the
redirect:

GitHub, top-right avatar, **Settings, Pages, "Add a verified domain"**. Enter
`thevfxsupervisor.com`. GitHub gives a TXT record named `_github-pages-challenge-thevfxsupervisor`
with a token value. Add that TXT record at easyDNS, then click Verify.

## Step 3, the repo and GitHub side (Claude can do this)

Once step 1 resolves correctly, one commit flips all four gates:

1. `build.py`: `CUTOVER_DONE = False` becomes `True`, so the build emits `docs/CNAME`.
2. `build.py`: `SITE_CANONICAL = "https://thevfxsupervisor.github.io"` becomes
   `"https://thevfxsupervisor.com"`. That single line also corrects the canonical link tags, the
   Open Graph and Twitter URLs, the `og:image` absolute URL, `sitemap.xml` and `robots.txt`.
3. `.gitignore`: remove the `docs/CNAME` line (and the warning comment above it).
4. Rebuild with the ShotGrid interpreter, commit, push.

Then set the custom domain on Pages:

    gh api -X PUT repos/thevfxsupervisor/thevfxsupervisor.github.io/pages \
      -f cname=thevfxsupervisor.com -F https_enforced=true

(or Settings, Pages, Custom domain in the web UI).

## Step 4, HTTPS

After the custom domain is set, GitHub provisions a Let's Encrypt certificate. This usually takes
minutes and can take up to an hour. Until it completes, "Enforce HTTPS" may be greyed out. Once
available, ensure it is ticked. Do not panic at a certificate warning during that window.

## Verify

    curl -sI https://thevfxsupervisor.com | head -3
    curl -sI https://www.thevfxsupervisor.com | head -3
    curl -sI https://thevfxsupervisor.github.io | head -3

Expect: apex serves 200, `www` redirects to apex, and the old github.io address 301s to the `.com`.
Then click through the live pages once, since the internal links are root-relative and should all
still resolve.

## Rollback

Remove the custom domain in GitHub Settings, Pages. The site immediately serves from
`thevfxsupervisor.github.io` again. If the repo side was already flipped, set `CUTOVER_DONE = False`,
restore the `.gitignore` line, delete `docs/CNAME`, rebuild and push.

## Decisions already made

- **Apex is canonical**, `www` redirects to it. The record set above gives that.
- Breakdown Studio stays at `thevfxsupervisor.github.io/breakdown-studio/` (separate repo, its own
  `gh-pages` branch). It is not affected by this cutover, but its backlinks point at the main site,
  so re-check them after the domain moves.
