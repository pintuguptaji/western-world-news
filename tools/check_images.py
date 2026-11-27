#!/usr/bin/env python3
"""Recurring image-availability check for Western World News.

Reads every distinct article-image URL from data/articles.json (plus the
two hardcoded build-script fallback images in tools/build_site.py) and
HEAD-checks each one (falling back to a ranged GET). Prints a per-URL
report and exits 1 if any image is dead (non-2xx/3xx after redirects)
so a workflow can raise an issue. Unverifiable hosts (proxy blocks,
timeouts) are reported separately and do NOT fail the run — a blocked
check is not evidence the image is dead.

Run locally: python3 tools/check_images.py
Runs weekly in GitHub Actions (.github/workflows/check-images.yml),
where the Euronews/France 24 CDNs are reachable (they are proxy-blocked
in the dev sandbox, so local runs will list them as unverifiable).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(SITE_ROOT, "data", "articles.json")
BUILD_PATH = os.path.join(SITE_ROOT, "tools", "build_site.py")

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
TIMEOUT = 20


def check_url(url):
    """Return (status, detail): status in ok/dead/unverifiable."""
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            if 200 <= r.status < 400:
                return "ok", str(r.status)
            return "dead", f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            # Some CDNs refuse HEAD; try a ranged GET.
            req2 = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-1023"})
            try:
                with urllib.request.urlopen(req2, timeout=TIMEOUT) as r:
                    if 200 <= r.status < 400:
                        return "ok", f"{r.status} (ranged GET)"
                    return "dead", f"HTTP {r.status} (ranged GET)"
            except Exception as e2:
                return "unverifiable", f"ranged GET failed: {e2}"
        return "dead", f"HTTP {e.code}"
    except Exception as e:
        return "unverifiable", str(e)


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    urls = {}  # url -> [slugs]
    for a in data.get("articles", []):
        img = a.get("image") or ""
        if img:
            urls.setdefault(img, []).append(a["slug"])
    # Hardcoded build-script fallback images (build_site.py IMAGES dict:
    # slug -> (unsplash photo id, caption)). Build the real URL the same
    # way uimg() does; do NOT scrape every unsplash.com string in the
    # file — the uimg() template and the admin form placeholder are not
    # real image URLs.
    with open(BUILD_PATH, encoding="utf-8") as f:
        build_src = f.read()
    m = re.search(r"^IMAGES = \{(.*?)^\}", build_src, re.S | re.M)
    if m:
        for pid in re.findall(r'\("([0-9A-Za-z][0-9A-Za-z_-]*)",', m.group(1)):
            url = (f"https://images.unsplash.com/photo-{pid}"
                   "?auto=format&fit=crop&w=1600&q=80")
            urls.setdefault(url, []).append("(build fallback)")

    print(f"Checking {len(urls)} distinct image URLs "
          f"({len(data.get('articles', []))} articles)")
    ok = dead = unv = 0
    dead_list = []
    for url in sorted(urls):
        status, detail = check_url(url)
        if status == "ok":
            ok += 1
        elif status == "dead":
            dead += 1
            dead_list.append((url, detail, urls[url]))
            print(f"DEAD  {url}  [{detail}]  used by: {', '.join(urls[url])}")
        else:
            unv += 1
            print(f"???   {url}  [unverifiable: {detail}]")
    print(f"\nOK: {ok}  DEAD: {dead}  UNVERIFIABLE: {unv}")
    if dead_list:
        print("\nDead images (fix by replacing the image URL in "
              "data/articles.json and rebuilding):")
        for url, detail, slugs in dead_list:
            print(f"  - {url} ({detail}) — {', '.join(slugs)}")
        return 1
    if unv:
        print("Note: unverifiable URLs are NOT failures — re-check them "
              "from an unblocked network before treating any as dead.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
