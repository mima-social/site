#!/usr/bin/env python3
"""Tell search engines about new and updated pages after a deploy.

Run by .github/workflows/submit-new-pages.yml when a push to main changes
sitemap.xml. It compares the sitemap with the one at --base, then:

1. waits until the live sitemap matches this commit (Netlify has deployed);
2. sends new and updated URLs to IndexNow (Bing, Yandex, Seznam, Naver);
3. writes a Markdown checklist of the NEW URLs to --issue-body, for someone
   to submit by hand at https://search.brave.com/submit-url (Brave has no
   submission API).

Prints `new=<n>` and `updated=<n>` for GITHUB_OUTPUT. Standard library only.

    python3 tools/submit_pages.py --base HEAD~1 --issue-body /tmp/brave.md
    python3 tools/submit_pages.py --base HEAD~1 --dry-run   # show, send nothing
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.mima.social"
HOST = "www.mima.social"
# The IndexNow key is public by design: it's served at /<key>.txt.
INDEXNOW_KEY = "2cc6a4774d121117fdfe713396e952cb"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
BRAVE_FORM = "https://search.brave.com/submit-url"
UA = "mima-site-deploy (+https://www.mima.social)"


def parse(xml):
    """{url: lastmod or ''} from a sitemap."""
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", xml or "", re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        mod = re.search(r"<lastmod>(.*?)</lastmod>", block)
        if loc:
            out[loc.group(1).strip()] = mod.group(1).strip() if mod else ""
    return out


def sitemap_at(ref):
    try:
        return subprocess.run(["git", "show", f"{ref}:sitemap.xml"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return ""  # no sitemap at that commit: every URL is new


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()


def wait_for_deploy(expected, timeout=900):
    """Poll the live sitemap until it matches this commit's."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if parse(fetch(f"{SITE}/sitemap.xml?t={int(time.time())}")) == expected:
                return True
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(20)
    return False


def indexnow(urls):
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request(INDEXNOW_ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="HEAD~1", help="commit to compare the sitemap with")
    ap.add_argument("--issue-body", help="write the Brave checklist here when there are new URLs")
    ap.add_argument("--dry-run", action="store_true", help="list the URLs; don't wait or send")
    args = ap.parse_args()

    before = parse(sitemap_at(args.base))
    after = parse((ROOT / "sitemap.xml").read_text())
    new = [u for u in after if u not in before]
    updated = [u for u in after if u in before and after[u] and after[u] != before[u]]
    print(f"new={len(new)}")
    print(f"updated={len(updated)}")
    for u in new:
        print(f"  new      {u}", file=sys.stderr)
    for u in updated:
        print(f"  updated  {u}", file=sys.stderr)
    if not (new or updated) or args.dry_run:
        return

    if not wait_for_deploy(after):
        sys.exit("The live sitemap never matched this commit; is the deploy stuck? Nothing was sent.")
    status = indexnow(new + updated)
    ok = status in (200, 202)
    print(f"IndexNow: HTTP {status}", file=sys.stderr)

    if new and args.issue_body:
        lines = [f"These pages went live with this deploy. Brave Search has no submission API, so please submit each one at **{BRAVE_FORM}** and tick it off.", ""]
        lines += [f"- [ ] {u}" for u in new]
        lines += ["", f"IndexNow (Bing, Yandex, Seznam, Naver) {'was notified automatically' if ok else f'returned HTTP {status}; check the workflow log'} "
                  f"about {len(new) + len(updated)} new or updated URL{'s' if len(new) + len(updated) != 1 else ''}.",
                  "", "Close this issue once every box is ticked."]
        pathlib.Path(args.issue_body).write_text("\n".join(lines) + "\n")
    if not ok and not (new and args.issue_body):
        sys.exit(1)  # the issue (when there is one) reports the failure instead


if __name__ == "__main__":
    main()
