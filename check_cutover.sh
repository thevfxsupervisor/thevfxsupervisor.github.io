#!/usr/bin/env bash
# Pre-flight for pointing thevfxsupervisor.com at GitHub Pages.
#
# WHY THIS EXISTS: a previous CNAME change took the live site down. The failure mode is specific and
# silent. If the easyDNS parking A record is still present, or a committed docs/CNAME lands before
# DNS resolves, Pages 301-redirects the working github.io site into the parking lander and the whole
# site disappears while every check still "succeeds".
#
# So this checks the OUTCOME (what DNS actually returns, what the domain actually serves) rather than
# trusting that the steps were followed. Read-only: it changes nothing, it only tells you whether the
# next step is safe.
#
# THE FULL PROCEDURE is dev/DOMAIN-CUTOVER.md (written by another seat). This script is its
# pre-flight, not a replacement: that file explains WHY the order matters and what to click,
# this one verifies the world actually matches before you take the irreversible step.
#
# Usage:  ./check_cutover.sh
set -uo pipefail

DOMAIN="thevfxsupervisor.com"
PAGES_HOST="thevfxsupervisor.github.io"
# GitHub Pages apex addresses, current as of 2026-08.
EXPECTED_A=("185.199.108.153" "185.199.109.153" "185.199.110.153" "185.199.111.153")
PARKING="64.68.200.44"   # the easyDNS parking record that must be GONE first

pass=0; fail=0; warn=0
ok(){   echo "  PASS  $1"; pass=$((pass+1)); }
bad(){  echo "  FAIL  $1"; fail=$((fail+1)); }
note(){ echo "  WARN  $1"; warn=$((warn+1)); }

need(){ command -v "$1" >/dev/null 2>&1 || { echo "missing tool: $1"; exit 1; }; }
need dig; need curl

echo "Cutover pre-flight for $DOMAIN"
echo

echo "1. Apex A records"
mapfile -t got < <(dig +short A "$DOMAIN" 2>/dev/null | sort)
if [ ${#got[@]} -eq 0 ]; then
  note "no A records yet. DNS not configured, or not propagated."
else
  for g in "${got[@]}"; do
    if [ "$g" = "$PARKING" ]; then
      bad "PARKING RECORD STILL PRESENT ($PARKING). Delete it in easyDNS BEFORE anything else."
    elif printf '%s\n' "${EXPECTED_A[@]}" | grep -qx "$g"; then
      ok "$g is a GitHub Pages address"
    else
      note "$g is not a known Pages address and not the parking record. Check what it is."
    fi
  done
  missing=0
  for e in "${EXPECTED_A[@]}"; do printf '%s\n' "${got[@]}" | grep -qx "$e" || missing=$((missing+1)); done
  [ "$missing" -eq 0 ] && ok "all four Pages A records present" || note "$missing of 4 Pages A records missing"
fi
echo

echo "2. www CNAME"
w=$(dig +short CNAME "www.$DOMAIN" 2>/dev/null | head -1)
if [ -z "$w" ]; then note "no www CNAME yet"
elif [ "$w" = "$PAGES_HOST." ]; then ok "www -> $w"
else note "www -> $w (expected $PAGES_HOST.)"; fi
echo

echo "3. What the domain actually serves"
code=$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 25 "https://$DOMAIN/" 2>/dev/null || echo 000)
final=$(curl -sS -o /dev/null -w '%{url_effective}' -L --max-time 25 "https://$DOMAIN/" 2>/dev/null || echo "")
body=$(curl -sS -L --max-time 25 "https://$DOMAIN/" 2>/dev/null | head -c 4000)
if [ "$code" = "000" ]; then note "no response yet (DNS or cert still pending)"
elif echo "$body" | grep -qi "the vfx supervisor\|Breakdown Studio"; then ok "serving the real site (HTTP $code)"
elif echo "$body" | grep -qiE "parked|domain for sale|easydns|sponsored listings"; then
  bad "serving a PARKING LANDER (HTTP $code). Do NOT commit docs/CNAME."
else note "HTTP $code, content unrecognised. Landed at: $final"; fi
echo

echo "4. Repo side"
if grep -q '^docs/CNAME' .gitignore 2>/dev/null; then ok "docs/CNAME still gitignored (correct until DNS is verified)"
else note "docs/CNAME is NOT ignored. Only correct AFTER checks 1 to 3 pass."; fi
if grep -q 'CUTOVER_DONE = False' build.py 2>/dev/null; then ok "CUTOVER_DONE is False (correct until DNS is verified)"
else note "CUTOVER_DONE is not False. Only correct AFTER checks 1 to 3 pass."; fi
echo

echo "-------------------------------------------"
echo "  $pass passed, $fail failed, $warn warnings"
if [ "$fail" -gt 0 ]; then
  echo
  echo "  DO NOT PROCEED. Fix the failures above first."
  echo "  Rollback if the site is already down:"
  echo "    gh api --method PUT repos/thevfxsupervisor/thevfxsupervisor.github.io/pages -F cname=null"
  exit 1
fi
if [ "$warn" -gt 0 ]; then
  echo
  echo "  Not ready yet. DNS is probably still propagating; re-run in 15 minutes."
  exit 0
fi
echo
echo "  Ready. Now, and only now:"
echo "    1. remove 'docs/CNAME' from .gitignore"
echo "    2. set CUTOVER_DONE = True in build.py"
echo "    3. set SITE_CANONICAL = https://$DOMAIN in build.py"
echo "    4. python3 build.py && git add -A && git commit && git push"
echo "    5. enable Enforce HTTPS once the cert provisions"
