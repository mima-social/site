#!/usr/bin/env python3
"""Render a share image (Open Graph / social card) for every Learn page.

Run after the build, then build again so the pages point at the new images:

    python3 learn-src/build.py && python3 learn-src/og.py && python3 learn-src/build.py

Each image is app-shots/og-learn.html filled with the page's title, a tag
("Learn · Posting") and the first app picture in the guide, rendered with
headless Chrome at 2400 × 1260 and saved as site-assets/og/<page>.jpg. A
sidecar <page>.jpg.json records where it came from and a hash of its inputs,
so unchanged pages are skipped. Needs Google Chrome; sips ships with macOS.
"""

import hashlib
import http.server
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import urllib.parse
from datetime import datetime, timezone
from functools import partial

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build  # noqa: E402

ROOT = build.ROOT
OUT = ROOT / "site-assets" / "og"
TEMPLATE = ROOT / "app-shots" / "og-learn.html"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
DEFAULT_SHOT = "/site-assets/app/board.webp"
FIGURE = re.compile(r"!\[[^\]]*\]\((/site-assets/app/[^)\s]+)")


def aspect(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(ROOT / path.lstrip("/"))],
                         capture_output=True, text=True).stdout
    w, h = (int(x) for x in re.findall(r"pixel(?:Width|Height): (\d+)", out))
    return w / h


def first_shot(body_md):
    """The guide's first app picture that fills the card's window (not a thin strip)."""
    for src in FIGURE.findall(body_md):
        if src.endswith(".mp4"):  # an animation: its poster is the picture
            src = src[:-4] + "-poster.webp"
        if aspect(src) <= 1.8:
            return src
    return DEFAULT_SHOT


def pages():
    """(key, params) for every Learn page; key matches build.og_key()."""
    topics = build.load_topics()
    articles = build.load_articles(topics)
    yield "learn", {"title": "Keep up with your people, not the algorithms", "tag": "Learn", "shot": DEFAULT_SHOT}
    for t in topics:
        if t["articles"]:
            yield f"topic-{t['slug']}", {"title": t["name"], "sub": t["blurb"], "tag": "Learn",
                                         "shot": first_shot(t["articles"][0]["body_md"])}
    for a in articles:
        yield a["slug"], {"title": a["title"], "tag": f"Learn · {a['topic']}", "shot": first_shot(a["body_md"])}


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = partial(Quiet, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    template_hash = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()[:12]
    server = serve()
    port = server.server_address[1]
    rendered = skipped = 0
    for key, params in pages():
        out = OUT / f"{key}.jpg"
        meta = OUT / f"{key}.jpg.json"
        shot = ROOT / params["shot"].lstrip("/")
        inputs = json.dumps(params, sort_keys=True) + template_hash + hashlib.sha256(shot.read_bytes()).hexdigest()[:12]
        digest = hashlib.sha256(inputs.encode()).hexdigest()[:16]
        if out.exists() and meta.exists() and json.loads(meta.read_text()).get("inputs") == digest:
            skipped += 1
            continue
        png = OUT / f"{key}.png"
        url = f"http://127.0.0.1:{port}/app-shots/og-learn.html#" + urllib.parse.quote(json.dumps(params))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--virtual-time-budget=5000",
                        "--window-size=1200,630", f"--screenshot={png}", url],
                       check=True, capture_output=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", str(png), "--out", str(out)],
                       check=True, capture_output=True)
        png.unlink()
        meta.write_text(json.dumps({
            "prompt": f"Origin: rendered by learn-src/og.py from app-shots/og-learn.html with {json.dumps(params)} "
                      "(the app picture is a fictional-content render from app-shots/).",
            "inputs": digest,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        }, indent=2) + "\n")
        rendered += 1
        print("rendered", out.relative_to(ROOT))
    # Remove images for pages that no longer exist.
    keys = {k for k, _ in pages()}
    for f in OUT.glob("*.jpg"):
        if f.stem not in keys:
            f.unlink()
            (OUT / f"{f.name}.json").unlink(missing_ok=True)
            print("removed", f.relative_to(ROOT))
    server.shutdown()
    print(f"{rendered} rendered, {skipped} unchanged.")


if __name__ == "__main__":
    main()
