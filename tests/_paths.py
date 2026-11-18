"""Put the site's script folders on sys.path so tests can import them."""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
for folder in ("learn-src", "tools"):
    path = str(ROOT / folder)
    if path not in sys.path:
        sys.path.insert(0, path)
