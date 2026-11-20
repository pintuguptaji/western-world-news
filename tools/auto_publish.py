#!/usr/bin/env python3
"""Automatic news publisher for Western World News.

Fetches trusted RSS feeds, adds verified new stories to data/articles.json,
refreshes the Just In feed, and rebuilds the static site with
tools/build_site.py. Python standard library only — no pip installs.

Usage:
    python3 tools/auto_publish.py [--dry-run]

Rules (Pintu's):
- Never invent figures, dates or quotes — everything comes from the feeds.
- A story's photo is the feed's own image for that story, verified to load
  (HTTP 200). No image -> the site's navy gradient tile, never a random
  stock photo. Never present stock/generated imagery as event footage.
- Skip items with no usable description rather than fabricating a summary.
- Idempotent: a second run with no new feed items changes nothing.
- Max 4 new articles per run, max 12 per calendar day (UTC).
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(SITE_ROOT, "data", "articles.json")
STATE_PATH = os.path.join(SITE_ROOT, "data", "auto_publish_state.json")
EXPORT_PATH = os.path.join(SITE_ROOT, "content-export.json")

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
FEED_TIMEOUT = 20
IMAGE_TIMEOUT = 10
MAX_NEW_PER_RUN = 4
MAX_PER_DAY = 12

# (source name, feed URL, default section)
FEEDS = [
    ("BBC", "https://feeds.bbci.co.uk/news/world/rss.xml", "world"),
    ("BBC", "https://feeds.bbci.co.uk/news/world/europe/rss.xml", "europe"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "world"),
    ("The Guardian", "https://www.theguardian.com/world/rss", "world"),
    ("Euronews", "https://www.euronews.com/rss?format=mrss", "europe"),
    ("France 24", "https://www.france24.com/en/rss", "world"),
    ("DW", "https://rss.dw.com/xml/rss-en-all", "europe"),
]

# Strong off-topic signals — skip these outright.
SKIP_WORDS = [
    "horoscope", "crossword", "quiz", "sudoku", "celebrity", "love island",
    "big brother", "kardashian", "taylor swift", "gossip", "recipe",
    "how to watch", "match report", "transfer news", "film review",
    "album review", "book review", "restaurant review", "travel guide",
    "weather forecast", "fashion week", "red carpet",
]

# Topics in scope: Western/European politics, war & conflict, US politics,
# world news, business & finance. An article must match at least one.
# Matching is word-start based ("war" must not match "forward").
INCLUDE_WORDS = [
    "ukraine", "russia", "putin", "zelensky", "gaza", "israel", "palestin",
    "trump", "biden", "white house", "senate", "congress", "democrat",
    "republican", "election", "parliament", "prime minister", "president",
    "minister", "chancellor", "summit", "nato", "eu", "european",
    "britain", "british", "france", "french", "germany", "german",
    "italy", "spain", "poland", "polish", "greece", "uk", "england",
    "war", "missile", "airstrike", "ceasefire", "sanction", "military",
    "defence", "defense", "embassy", "diplomat", "treaty", "trade",
    "economy", "market", "inflation", "central bank", "interest rate",
    "stocks", "dow", "ftse", "unemployment", "court", "genocide",
    "climate", "cop31", "cop30", "united nations", "security council",
    "china", "xi", "taiwan", "iran", "syria", "lebanon", "yemen",
    "sudan", "myanmar", "rohingya", "india", "pakistan", "kashmir",
    "nuclear", "energy", "oil", "gas", "migration", "migrant", "asylum",
    "vote", "referendum", "coup", "protest", "strike", "tariff",
]

WAR_WORDS = ["ukraine", "russia", "gaza", "israel", "palestin", "war",
             "missile", "airstrike", "ceasefire", "hamas", "hezbollah",
             "yemen", "sudan", "myanmar", "syria", "iran", "nuclear",
             "kyiv", "kharkiv", "donetsk", "kremlin", "tehran", "beirut",
             "damascus"]
BUSINESS_WORDS = ["market", "stocks", "dow", "ftse", "nikkei", "inflation",
                  "central bank", "interest rate", "economy", "trade",
                  "tariff", "unemployment", "recession", "shares"]
US_WORDS = ["trump", "biden", "white house", "senate", "congress",
            "supreme court", "democrat", "republican", "us", "america",
            "washington", "pentagon"]
EUROPE_WORDS = ["eu", "european", "brussels", "france", "french",
                "germany", "german", "britain", "british", "uk",
                "italy", "spain", "poland", "polish"]

# Link sections that are out of scope for this site (Guardian-style paths
# and feed category domains): society/crime comment, sport, culture,
# lifestyle, video and live-blog pages.
LINK_SKIP_SECTIONS = {
    "society", "sport", "culture", "lifeandstyle", "fashion", "food",
    "travel", "education", "commentisfree", "music", "film", "books",
    "artanddesign", "stage", "tv-and-radio", "games", "money", "media",
    "weather",
}


def has(hay, word):
    """True if word occurs at the start of a word in hay."""
    return re.search(r"\b" + re.escape(word), hay) is not None


def log(msg):
    print(f"[auto_publish] {msg}", flush=True)


def clean_text(raw):
    """Strip HTML tags/entities, collapse whitespace.

    Human-from-USA rules (Pintu, 2026-11-20): no em/en dashes or other
    AI-tell symbols anywhere on the site; US spelling; US date format.
    Applied to every feed-derived headline and summary, so auto-published
    stories stay clean. Same rules live in tools/build_site.py.
    """
    if not raw:
        return ""
    # Keep sentence boundaries where block elements end, so a description
    # made of several <p>...</p> does not run into one giant "sentence".
    raw = re.sub(r"</(p|li|h\d|div|tr)>", ". ", raw, flags=re.IGNORECASE)
    raw = re.sub(r"<br\s*/?>", ". ", raw, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"\s*\.\s*\.", ".", text)
    text = re.sub(r"\s+", " ", text).strip()
    # AI-tell symbols: em/en dash, ellipsis char, star, arrow, bullet.
    text = text.replace(" — ", ", ").replace("—", ", ")
    text = text.replace(" – ", ", ").replace("–", "-")
    text = text.replace("…", "...").replace("★", "")
    text = text.replace(" → ", " to ").replace("→", " to ")
    text = text.replace(" • ", ", ").replace("•", "")
    # British -> US spelling.
    text = _UK_US_RE.sub(_us_word, text)
    # Day-first dates -> US Month Day, Year.
    text = re.sub(r"(\d{1,2})-(\d{1,2}) " + _MONTH_RE + r"\b",
                  lambda m: f"{m.group(3)} {m.group(1)}-{m.group(2)}", text)
    text = re.sub(r"(\d{1,2}) and (\d{1,2}) " + _MONTH_RE + r"\b",
                  lambda m: f"{m.group(3)} {m.group(1)} and {m.group(2)}", text)
    text = re.sub(r"(\d{1,2}) " + _MONTH_RE + r" (\d{4})\b",
                  lambda m: f"{m.group(2)} {m.group(1)}, {m.group(3)}", text)
    text = re.sub(r"(\d{1,2}) " + _MONTH_RE + r"\b",
                  lambda m: f"{m.group(2)} {m.group(1)}", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December",
           "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
           "Sept", "Oct", "Nov", "Dec")
_MONTH_RE = "(" + "|".join(_MONTHS) + ")"
_UK_US = {
    "defence": "defense", "defences": "defenses", "centre": "center",
    "organise": "organize", "organised": "organized", "organiser": "organizer",
    "organisers": "organizers", "organising": "organizing",
    "behaviour": "behavior", "favour": "favor", "favourite": "favorite",
    "labour": "labor", "programme": "program", "travelled": "traveled",
    "travelling": "traveling", "cancelled": "canceled", "whilst": "while",
    "amongst": "among", "realise": "realize", "recognise": "recognize",
    "licence": "license", "grey": "gray", "rumour": "rumor",
    "rumours": "rumors", "enquiry": "inquiry", "enquiries": "inquiries",
    "cheque": "check", "focussed": "focused", "labelled": "labeled",
    "modelling": "modeling", "practise": "practice",
}
_UK_US_RE = re.compile(r"\b(" + "|".join(sorted(_UK_US, key=len, reverse=True)) + r")\b",
                        re.IGNORECASE)


def _us_word(m):
    w = m.group(1)
    rep = _UK_US[w.lower()]
    if w.isupper():
        return rep.upper()
    if w[0].isupper():
        return rep[0].upper() + rep[1:]
    return rep


_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D"
    "\U0001F1E6-\U0001F1FF]")


def clean_title(raw):
    text = clean_text(raw)
    text = _EMOJI_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" -–—:·")
    return text


def slugify(title):
    text = unicodedata.normalize("NFKD", title)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > 60:
        text = text[:60].rsplit("-", 1)[0]
    return text or "news-story"


def norm_url(url):
    """Normalise a link for dedup: lowercase host+path, no query/fragment."""
    from urllib.parse import urlsplit
    try:
        p = urlsplit(url.strip())
        return (p.netloc.lower(), p.path.rstrip("/").lower())
    except Exception:
        return ("", url.strip().lower())


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def first_sentences(text, max_chars=450, max_sentences=2):
    """Take the first 1-2 sentences of plain text, capped at max_chars."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for p in parts:
        if not p:
            continue
        out.append(p)
        if len(out) >= max_sentences:
            break
    result = " ".join(out).strip()
    if len(result) > max_chars:
        cut = result[:max_chars].rsplit(" ", 1)[0]
        result = cut.rstrip(".,;:") + "."
    return result


def truncate_dek(text, max_chars=240):
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if end > 80:
        return cut[:end + 1]
    return cut.rsplit(" ", 1)[0].rstrip(".,;:") + "."


def fetch_url(url, timeout, accept="*/*"):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                              "Accept": accept})
    return urllib.request.urlopen(req, timeout=timeout)


def verify_image(url):
    """True if the URL serves a real image (HEAD, else ranged GET)."""
    if not url or not url.lower().startswith("https://"):
        return False
    for method in ("HEAD", "GET"):
        try:
            headers = {"User-Agent": USER_AGENT}
            if method == "GET":
                headers["Range"] = "bytes=0-1023"
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=IMAGE_TIMEOUT) as resp:
                if resp.status not in (200, 206):
                    continue
                ctype = resp.headers.get("Content-Type", "")
                if ctype and not ctype.startswith("image/"):
                    return False
                return True
        except Exception:
            continue
    return False


def parse_feed(source, url, default_section):
    """Fetch one RSS feed, return a list of item dicts (newest first)."""
    try:
        with fetch_url(url, FEED_TIMEOUT, "application/rss+xml, */*") as resp:
            raw = resp.read()
    except Exception as e:
        log(f"FEED FAILED {source} {url}: {e}")
        return []
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        log(f"FEED PARSE FAILED {source} {url}: {e}")
        return []

    items = []
    for el in root.iter("item"):
        item = {"source": source, "feed_section": default_section}
        for child in el:
            tag = child.tag.rsplit("}", 1)[-1]
            text = (child.text or "").strip()
            if tag == "title":
                item["title"] = clean_title(text)
            elif tag == "link":
                item["link"] = text
            elif tag == "description":
                item["description"] = clean_text(text)
            elif tag == "pubDate":
                try:
                    item["pubdate"] = parsedate_to_datetime(text)
                except Exception:
                    pass
            elif tag == "category":
                item.setdefault("categories", []).append(
                    (text, child.get("domain", "")))
            elif tag in ("content", "thumbnail"):
                u = child.get("url", "")
                if u:
                    w = int(child.get("width") or 0)
                    prev = item.get("image")
                    # Keep the largest image offered.
                    if not prev or w >= prev[1]:
                        item["image"] = (u, w)
            elif tag == "enclosure":
                if (child.get("type") or "").startswith("image/"):
                    u = child.get("url", "")
                    if u and "image" not in item:
                        item["image"] = (u, 0)
        if item.get("title") and item.get("link"):
            items.append(item)
    items.sort(key=lambda i: i.get("pubdate") or dt.datetime.min.replace(
        tzinfo=dt.timezone.utc), reverse=True)
    log(f"FEED OK {source} {url}: {len(items)} items")
    return items


def is_relevant(item, need_include=True):
    hay = (item.get("title", "") + " " + item.get("description", "")).lower()
    title_low = item.get("title", "").lower()
    link = item.get("link", "")
    # Live blogs / live pages / video pages are not articles.
    if re.search(r"[-–—]\s*live\s*$", title_low) \
            or "live blog" in title_low \
            or title_low.startswith("watch live"):
        return False
    from urllib.parse import urlsplit
    try:
        segments = [s for s in urlsplit(link).path.split("/") if s]
    except Exception:
        segments = []
    if any(s == "live" or s.startswith("live-") or s in ("video", "videos")
           for s in segments):
        return False
    if segments and segments[0] in LINK_SKIP_SECTIONS:
        return False
    for _text, domain in item.get("categories", []):
        parts = [p for p in domain.rstrip("/").split("/") if p]
        if parts and parts[-1] in LINK_SKIP_SECTIONS:
            return False
        if any(p in LINK_SKIP_SECTIONS for p in parts):
            return False
    for word in SKIP_WORDS:
        if has(hay, word):
            return False
    if not need_include:
        return True
    return any(has(hay, w) for w in INCLUDE_WORDS)


def pick_section(item):
    # Classify on the headline only: descriptions often mention other
    # countries in passing (e.g. a UK cyber story mentioning Russia).
    hay = item.get("title", "").lower()
    if any(has(hay, w) for w in WAR_WORDS):
        return "war-conflict", ["war-conflict", "world"]
    if any(has(hay, w) for w in BUSINESS_WORDS):
        return "business-finance", ["business-finance", "world"]
    if any(has(hay, w) for w in US_WORDS):
        return "us", ["us", "world"]
    sec = item["feed_section"]
    if sec == "world":
        return "world", ["world"]
    return sec, [sec, "world"]


STOP_WORDS = {
    "top", "new", "latest", "breaking", "live", "says", "said", "after",
    "before", "with", "from", "over", "amid", "among", "about", "into",
    "more", "than", "will", "would", "could", "should", "first", "second",
    "one", "two", "three", "day", "days", "year", "years", "week",
    "today", "yesterday", "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday", "the", "and", "for", "its", "this",
    "that", "what", "when", "how", "why", "who", "are", "was", "were",
    "been", "being", "have", "has", "had", "does", "did", "not", "but",
    "per", "via", "amid", "they", "them", "their", "he", "she", "his",
    "her", "it", "take", "takes", "make", "made", "get", "gets",
}


def stem(word):
    """Crude stem: strip a plural 's', keep the first 5 letters."""
    if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]
    return word[:5]


def sig_words(title):
    """Significant words of a headline, stemmed to word starts."""
    words = re.findall(r"[a-z]+", title.lower())
    stems = set()
    for w in words:
        if len(w) < 4 or w in STOP_WORDS:
            continue
        stems.add(stem(w))
    return stems


def is_near_duplicate(title, existing_sig_sets):
    """Same event, different headline/source: heavy word overlap."""
    mine = sig_words(title)
    if len(mine) < 3:
        return False
    for other in existing_sig_sets:
        shared = mine & other
        if len(shared) >= 3 and len(shared) / min(len(mine), len(other)) >= 0.5:
            return True
    return False


def bbc_bigger(url):
    """BBC ichef thumbnails are 240px; request the 800px rendition."""
    return url.replace("/ace/standard/240/", "/ace/standard/800/")


def resolve_image(item):
    """Return a verified image URL for the item, or ''."""
    img = item.get("image")
    if not img:
        return ""
    url = img[0]
    candidates = [url]
    bigger = bbc_bigger(url)
    if bigger != url:
        candidates.insert(0, bigger)
    for cand in candidates:
        if verify_image(cand):
            return cand
    return ""


def fmt_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_state():
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, encoding="utf-8") as f:
                state = json.load(f)
            if state.get("date") == today:
                return state
        except Exception:
            pass
    return {"date": today, "published_today": 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be published; write nothing.")
    args = ap.parse_args()
    dry_run = args.dry_run

    if os.path.exists(EXPORT_PATH):
        log("ERROR: content-export.json exists in the site root — it would "
            "shadow data/articles.json in the build. Remove it (or move it "
            "out of the site) before auto-publishing.")
        return 2

    data = load_data()
    existing_slugs = {a["slug"] for a in data["articles"]}
    existing_urls = {norm_url(a.get("source_url", "")) for a in data["articles"]}
    existing_titles = {norm_title(a["headline"]) for a in data["articles"]}
    existing_sig = [sig_words(a["headline"]) for a in data["articles"]]

    # --- Fetch all feeds (one failing feed must not stop the rest). ---
    all_items = []
    for source, url, section in FEEDS:
        all_items.extend(parse_feed(source, url, section))
    log(f"Fetched {len(all_items)} items from {len(FEEDS)} feeds")

    # --- Select new articles. ---
    state = load_state()
    remaining_today = MAX_PER_DAY - state["published_today"]
    slots = min(MAX_NEW_PER_RUN, max(0, remaining_today))
    if slots <= 0:
        log(f"Daily cap reached ({MAX_PER_DAY}/day). No new articles this run.")
    new_articles = []
    seen_titles = set()
    seen_urls = set()
    for item in sorted(all_items,
                       key=lambda i: i.get("pubdate") or dt.datetime.min.replace(
                           tzinfo=dt.timezone.utc), reverse=True):
        if len(new_articles) >= slots:
            break
        if not is_relevant(item):
            continue
        desc = item.get("description", "")
        if len(desc) < 40:
            continue
        url = item["link"]
        clean_link = url.split("#")[0].split("?")[0]
        nurl = norm_url(clean_link)
        ntitle = norm_title(item["title"])
        slug = slugify(item["title"])
        if slug in existing_slugs or nurl in existing_urls \
                or ntitle in existing_titles or ntitle in seen_titles \
                or nurl in seen_urls or slug in {a["slug"] for a in new_articles} \
                or is_near_duplicate(item["title"], existing_sig) \
                or is_near_duplicate(item["title"],
                                     [sig_words(a["headline"])
                                      for a in new_articles]):
            continue
        pub = item.get("pubdate") or dt.datetime.now(dt.timezone.utc)
        summary = first_sentences(desc)
        if len(summary) < 40:
            continue
        section, sections = pick_section(item)
        image = resolve_image(item)
        article = {
            "slug": slug,
            "sections": sections,
            "section": section,
            "headline": item["title"],
            "dek": truncate_dek(summary),
            "date": fmt_date(pub),
            "source": item["source"],
            "source_url": clean_link,
            "body": [summary],
            "related": [],
            "image": image,
            "imageCaption": f"Photo: {item['source']}" if image else "",
            "auto": True,
        }
        new_articles.append(article)
        seen_titles.add(ntitle)
        seen_urls.add(nurl)

    # Related stories: other new articles from this same run.
    for a in new_articles:
        a["related"] = [b["slug"] for b in new_articles
                        if b["slug"] != a["slug"]][:3]

    # --- Refresh Just In from the newest relevant items. ---
    just_in = []
    seen_ji = set()
    for item in sorted(all_items,
                       key=lambda i: i.get("pubdate") or dt.datetime.min.replace(
                           tzinfo=dt.timezone.utc), reverse=True):
        if len(just_in) >= 8:
            break
        if not is_relevant(item, need_include=False):
            continue
        title = item["title"]
        if norm_title(title) in seen_ji:
            continue
        seen_ji.add(norm_title(title))
        pub = item.get("pubdate")
        if pub:
            time_str = f"{pub.day} {pub.strftime('%b')}, {pub.strftime('%H:%M')}"
        else:
            time_str = dt.datetime.now(dt.timezone.utc).strftime("%d %b")
        just_in.append({"time": time_str, "text": title[:110]})
    just_in_changed = just_in != data.get("justIn", [])

    # --- Report / dry run. ---
    log(f"Selected {len(new_articles)} new article(s) "
        f"(slots this run: {slots}, published today: {state['published_today']}/{MAX_PER_DAY})")
    print(f"PUBLISHED_COUNT={len(new_articles)}", flush=True)
    for a in new_articles:
        log(f"  NEW: [{a['section']}] {a['headline']} — {a['source']} "
            f"image={'yes' if a['image'] else 'no'}")
    log(f"Just In refreshed: {len(just_in)} items "
        f"({'changed' if just_in_changed else 'unchanged'})")

    if dry_run:
        log("DRY RUN — nothing written, site not rebuilt.")
        return 0

    changed = False
    if new_articles:
        data["articles"] = new_articles + data["articles"]
        data["heroSlug"] = new_articles[0]["slug"]
        data["breaking"] = {
            "text": new_articles[0]["headline"][:110],
            "link": f"articles/{new_articles[0]['slug']}.html",
        }
        state["published_today"] += len(new_articles)
        changed = True
    if just_in_changed:
        data["justIn"] = just_in
        changed = True

    if not changed:
        log("No changes — nothing to write or rebuild.")
        return 0

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    log(f"Wrote data/articles.json ({len(new_articles)} new articles)")

    env = dict(os.environ, WWN_OUT=SITE_ROOT)
    proc = subprocess.run([sys.executable,
                           os.path.join(SITE_ROOT, "tools", "build_site.py")],
                          env=env, capture_output=True, text=True)
    print(proc.stdout, end="")
    if proc.returncode != 0:
        print(proc.stderr, end="", file=sys.stderr)
        log("ERROR: build_site.py failed — pages were NOT regenerated.")
        return 2
    log("Rebuilt site with tools/build_site.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
