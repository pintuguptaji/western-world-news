#!/usr/bin/env python3
"""Build script for Western World News (static site).
Generates all HTML pages, sitemap.xml and robots.txt from
data/articles.json (see _load_data below). Run: python3 /tmp/build_site.py
Content refreshed 20 Nov 2026: original summaries of real stories, 19-20 Nov 2026,
each credited to its source with a link. See README.md in the site root.
"""
import datetime
import os

OUT = os.environ.get("WWN_OUT", os.path.expanduser("~/workspace/western-world-news"))
BASE = "https://westernworldnews.com"

NAV = [
    ("index.html", "Home"),
    ("world.html", "World"),
    ("europe.html", "Europe"),
    ("us.html", "US"),
    ("politics.html", "Politics"),
    ("war-conflict.html", "War &amp; Conflict"),
    ("business-finance.html", "Business &amp; Finance"),
    ("sport.html", "Sport"),
    ("culture.html", "Culture"),
    ("live.html", "Live"),
]

SECTIONS = {
    "world": "World",
    "europe": "Europe",
    "us": "US",
    "politics": "Politics",
    "war-conflict": "War &amp; Conflict",
    "business-finance": "Business &amp; Finance",
    "sport": "Sport",
    "culture": "Culture",
    "live": "Live",
}

# slug, section(s), headline, deck, date, source name, source url, body paragraphs, related slugs
# --- Content data (data/articles.json) ---
# All article text lives in data/articles.json so the automatic publisher
# (tools/auto_publish.py) can update it without touching this script.
# WATCH / ANALYSIS / IMAGES below stay here: they are curated design blocks.
import json as _json


# --- Human-from-USA text rules (Pintu, 2026-11-20) ---
# No em/en dashes or other AI-tell symbols anywhere on the site; US spelling
# and US date format (November 20, 2026). Applied to loaded article data so
# even imported content comes out clean. Same rules live in
# tools/auto_publish.py (clean_text) for feed-derived stories.
import re as _re

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
_UK_US_RE = _re.compile(r"\b(" + "|".join(sorted(_UK_US, key=len, reverse=True)) + r")\b",
                        _re.IGNORECASE)


def _us_word(m):
    w = m.group(1)
    rep = _UK_US[w.lower()]
    if w.isupper():
        return rep.upper()
    if w[0].isupper():
        return rep[0].upper() + rep[1:]
    return rep


def clean_text(text):
    if not text:
        return text
    text = text.replace(" \u2014 ", ", ")
    text = text.replace("\u2014", ", ")
    text = text.replace(" \u2013 ", ", ")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2026", "...")
    text = text.replace("\u2605", "")
    text = text.replace(" \u2192 ", " to ")
    text = text.replace("\u2192", " to ")
    text = text.replace(" \u2022 ", ", ")
    text = text.replace("\u2022", "")
    text = _UK_US_RE.sub(_us_word, text)
    text = _re.sub(r"(\d{1,2})-(\d{1,2}) " + _MONTH_RE + r"\b",
                   lambda m: f"{m.group(3)} {m.group(1)}-{m.group(2)}", text)
    text = _re.sub(r"(\d{1,2}) and (\d{1,2}) " + _MONTH_RE + r"\b",
                   lambda m: f"{m.group(3)} {m.group(1)} and {m.group(2)}", text)
    text = _re.sub(r"(\d{1,2}) " + _MONTH_RE + r" (\d{4})\b",
                   lambda m: f"{m.group(2)} {m.group(1)}, {m.group(3)}", text)
    text = _re.sub(r"(\d{1,2}) " + _MONTH_RE + r"\b",
                   lambda m: f"{m.group(2)} {m.group(1)}", text)
    text = _re.sub(r",\s*,", ",", text)
    text = _re.sub(r",\s*\.", ".", text)
    text = _re.sub(r"\s{2,}", " ", text)
    return text.strip()


def _clean_obj(obj):
    if isinstance(obj, str):
        return clean_text(obj)
    if isinstance(obj, list):
        return [_clean_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _clean_obj(v) for k, v in obj.items()}
    return obj

def _load_data():
    path = os.path.join(OUT, "data", "articles.json")
    with open(path, encoding="utf-8") as f:
        return _clean_obj(_json.load(f))

_DATA = _load_data()
STORIES = _DATA["articles"]
JUST_IN = [(it["time"], it["text"], None) for it in _DATA.get("justIn", [])]
LIVE_UPDATES = [(u["time"], u["headline"], u["text"]) for u in _DATA.get("liveUpdates", [])]
MOST_READ = list(_DATA.get("mostRead", []))
HERO_SLUG = _DATA.get("heroSlug", STORIES[0]["slug"] if STORIES else "")
BREAKING = _DATA.get("breaking", {"text": "", "link": ""})

# Timestamped "Just In" items — all verified from search results, 18-20 Nov 2026.
# JUST_IN loaded from data/articles.json (see loader above).

# Live-blog updates for live.html — verified facts only, 18-20 Nov 2026.
# LIVE_UPDATES loaded from data/articles.json (see loader above).

BY_SLUG = {s["slug"]: s for s in STORIES}



# ---------------- v2: full publisher design + admin panel ----------------
# Extends the v1 data above (STORIES, JUST_IN, LIVE_UPDATES, NAV, SECTIONS).
# Run: python3 /tmp/build_site_v2.py
# Optional: place a content export from admin.html as
#   ~/workspace/western-world-news/content-export.json
# and re-run — the exported articles/Just In/live updates replace the
# built-in seed data for the regenerated static pages.
import json
from html import escape as hescape

# --- Thematic stock photos (Unsplash, openly licensed). These are GENERIC
# illustrative images (city skylines, parliaments, markets, stadiums) — NOT
# photos of the actual events. Every caption says so. Verified 200/image.
def uimg(photo_id, w=1200):
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w={w}&q=80"

IMAGES = {
    "nations-league-draw": ("1522778119026-d647f0596c20", "A football stadium under lights during a match. Illustrative photo. Photo: Unsplash"),
    "raye-grammy-nominations": ("1493225457124-a3eb161ffa5f", "A singer performs on stage. Illustrative photo. Photo: Unsplash"),
}

# MOST_READ loaded from data/articles.json (see loader above).

# "Watch" strip — video-style cards. NOTE: no real video exists yet; cards
# link to the live blog / full articles. See README.md.
WATCH = [
    {"title": "The night Kyiv was hit: the story so far", "dur": "01:32",
     "img": "1504711434969-e33886168f5c", "link": "live.html"},
    {"title": "Europe\u2019s reset with Britain, explained", "dur": "02:14",
     "img": "1473341304170-971dccb5ac1e", "link": "articles/eu-uk-reset-deal.html"},
    {"title": "Markets: the sell-off, explained", "dur": "01:47",
     "img": "1611974789855-9c2a0a7236a3", "link": "articles/wall-street-selloff.html"},
]

ANALYSIS = [
    {"title": "After Shenzhen, Europe\u2019s answer is: not Yalta",
     "blurb": "An hour of handshakes, a declaration on the UN and oil, and a war that carried on through the night. The summit mattered, but Europe\u2019s reply in Berlin mattered more.",
     "link": "articles/shenzhen-aftermath-europe-pushback.html"},
    {"title": "The EU-UK reset: what the deal actually changes",
     "blurb": "Food checks gone, carbon markets linked, 100,000 young people on the move, and the hardest question, university fees, kicked six months down the road.",
     "link": "articles/eu-uk-reset-deal.html"},
    {"title": "The market\u2019s AI question has turned into a rout",
     "blurb": "Six straight falls, the Dow below 50,000 and the Nikkei down 5 percent. The boom that carried stocks to records is now the thing investors fear most.",
     "link": "articles/wall-street-selloff.html"},
]

CSS = """/* Western World News: publisher design v3.
   Al Jazeera-format look: white page, light hairline rules, single centered
   container, photo-led hero with a red headline box, small-caps section
   labels, numbered Most Popular list. Sans-serif throughout; no webfonts
   (system sans stack only). */

:root {
  --red: #bb1919;
  --red-dark: #8f1212;
  --ink: #111111;
  --muted: #666666;
  --line: #eeeeee;
  --line-strong: #dddddd;
  --light: #fafafa;
  --navy: #0e2244;
  --navy-dark: #081426;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: var(--sans);
  color: var(--ink);
  background: #fff;
  line-height: 1.55;
  font-size: 16px;
}

h1, h2, h3 { font-family: var(--sans); }
a { color: var(--ink); text-decoration: none; }
a:hover { color: var(--red); }
img { max-width: 100%; display: block; }
figure { margin: 0; }
figcaption { font-size: 0.78rem; color: var(--muted); padding: 0.35rem 0 0; line-height: 1.4; }

.wrap { max-width: 1180px; margin: 0 auto; padding: 0 1rem; }
.sr-only { position: absolute; left: -9999px; }

/* ---------- Sticky white header ---------- */
.site-header { position: sticky; top: 0; z-index: 100; background: #fff; border-bottom: 1px solid var(--line); }
.header-row { display: flex; align-items: center; gap: 1.5rem; padding-top: 0.7rem; padding-bottom: 0.7rem; }
.wordmark { font-size: 1.45rem; font-weight: 800; letter-spacing: -0.01em; line-height: 1.1; color: var(--ink); white-space: nowrap; }
.wordmark .news { color: var(--ink); }
.wordmark:hover { text-decoration: none; }
.main-nav { flex: 1; display: flex; justify-content: center; }
.main-nav ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; }
.main-nav a { display: block; color: var(--ink); padding: 0.5rem 0.65rem; font-size: 0.95rem; font-weight: 600; white-space: nowrap; }
.main-nav a:hover { color: var(--red); text-decoration: none; }
.main-nav a.active { color: var(--red); box-shadow: inset 0 -2px 0 var(--red); }
.main-nav a.live-link { color: var(--red); font-weight: 800; }
.nav-toggle {
  display: none; background: none; border: 0; color: var(--ink); font-size: 1.5rem;
  padding: 0.4rem 0.6rem 0.4rem 0; cursor: pointer; line-height: 1; margin-left: auto;
}
.header-actions { display: flex; align-items: center; gap: 0.9rem; margin-left: auto; }
.header-actions .live-link { color: var(--red); font-weight: 800; font-size: 0.95rem; display: flex; align-items: center; gap: 0.35rem; white-space: nowrap; }
.header-actions .live-link:hover { text-decoration: none; }
.btn-black { background: #111; color: #fff; border-radius: 999px; padding: 0.5rem 1.1rem; font-size: 0.9rem; font-weight: 700; white-space: nowrap; }
.btn-black:hover { background: #000; color: #fff; text-decoration: none; }
.search-box { position: relative; }
.search-box input {
  background: #fff; border: 1px solid var(--line-strong); color: var(--ink);
  border-radius: 999px; padding: 0.45rem 0.9rem; font-size: 0.9rem; width: 180px; outline: none;
}
.search-box input::placeholder { color: #999; }
.search-box input:focus { border-color: var(--ink); }
.search-results {
  display: none; position: absolute; right: 0; top: 110%; width: 320px; max-width: 90vw;
  background: #fff; color: var(--ink); border: 1px solid var(--line); border-radius: 8px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.18); z-index: 200; overflow: hidden;
}
.search-results.open { display: block; }
.search-results a { display: block; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--line); font-size: 0.92rem; color: var(--ink); }
.search-results a:last-child { border-bottom: 0; }
.search-results a:hover { background: var(--light); text-decoration: none; }
.search-results a small { display: block; color: var(--red); font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
.search-results .none { padding: 0.7rem 0.8rem; color: var(--muted); font-size: 0.9rem; }
.topic-row { border-top: 1px solid var(--line); }
.topic-row .wrap { display: flex; gap: 1.4rem; padding-top: 0.45rem; padding-bottom: 0.45rem; overflow-x: auto; }
.topic-row a { color: var(--muted); font-size: 0.85rem; font-weight: 600; white-space: nowrap; }
.topic-row a:hover { color: var(--red); text-decoration: none; }
@media (max-width: 960px) {
  .header-row { flex-wrap: wrap; gap: 0.5rem 1rem; }
  .nav-toggle { display: block; }
  .main-nav { order: 4; flex-basis: 100%; justify-content: flex-start; }
  .main-nav ul { display: none; flex-direction: column; width: 100%; }
  .main-nav.open ul { display: flex; }
  .main-nav a { padding: 0.55rem 0; border-top: 1px solid var(--line); }
  .main-nav a.active { box-shadow: none; }
  .search-box input { width: 140px; }
}

/* ---------- Layout ---------- */
main { padding: 1.5rem 0 2rem; }
.section-head {
  font-size: 0.95rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--ink); border-bottom: 1px solid var(--line); padding-bottom: 0.5rem; margin: 0 0 1.1rem;
}
.section-head a { color: var(--ink); }
.section-head a:hover { color: var(--red); }
.tag { color: var(--red); }
.kicker { color: var(--muted); font-weight: 700; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; }
.byline { color: var(--muted); font-size: 0.85rem; margin: 0.5rem 0 0; }
.byline time { font-weight: 600; color: var(--ink); }
.byline a { color: var(--red); font-weight: 700; }

/* ---------- Hero (three-column) ---------- */
.hero-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; margin-bottom: 1.6rem; }
@media (min-width: 1000px) { .hero-grid { grid-template-columns: 1.35fr 1fr 280px; } }
.hero-media { margin: 0; }
.hero-media img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 8px; }
.hero .art { aspect-ratio: 16 / 10; border-radius: 8px; }
.hero-box { background: var(--red); color: #fff; border-radius: 8px; padding: 1.1rem 1.3rem; margin: -3.4rem 1.4rem 0; position: relative; z-index: 2; }
.hero-box .kicker { color: rgba(255,255,255,0.85); }
.hero-box h1 { font-size: 1.75rem; line-height: 1.15; margin: 0.35rem 0 0; font-weight: 800; }
.hero-box h1 a { color: #fff; }
.hero-box h1 a:hover { color: #fff; text-decoration: underline; }
@media (min-width: 1000px) { .hero-box h1 { font-size: 2rem; } }
.hero .dek { color: #444; font-size: 1.02rem; margin: 0.9rem 0.2rem 0.5rem; line-height: 1.5; }
.hero .byline { margin-left: 0.2rem; margin-right: 0.2rem; }

/* Second story + text card (hero middle column) */
.hero-second { display: flex; flex-direction: column; gap: 1.4rem; }
.second-story figure { margin: 0 0 0.6rem; }
.second-story figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; }
.second-story .art { aspect-ratio: 16 / 9; border-radius: 8px; }
.second-story h3 { font-size: 1.25rem; line-height: 1.3; margin: 0.3rem 0 0; font-weight: 800; }
.second-story h3 a:hover { color: var(--red); }
.text-card { display: flex; gap: 1rem; align-items: flex-start; border-top: 1px solid var(--line); padding-top: 1.2rem; }
.text-card h3 { font-size: 1.08rem; line-height: 1.35; margin: 0.3rem 0 0; font-weight: 700; }
.text-card h3 a:hover { color: var(--red); }
.text-card-thumb { flex-shrink: 0; width: 110px; }
.text-card-thumb img { width: 110px; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 6px; }
.text-card-thumb .art { width: 110px; aspect-ratio: 16 / 10; border-radius: 6px; }
.text-card-thumb .art .monogram { font-size: 1rem; padding: 0.1rem 0.5rem; }
.text-card-thumb .art .art-label { display: none; }

/* Right rail: Must Reads / More Headlines */
.hero-rail { display: flex; flex-direction: column; gap: 1.8rem; }
.rail-head { font-size: 0.85rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #666; border-left: 4px solid var(--red); padding-left: 0.6rem; margin: 0 0 0.9rem; }
.rail-list { list-style: none; margin: 0; padding: 0; }
.rail-list li { padding: 0.75rem 0; border-bottom: 1px solid var(--line); }
.rail-list li:first-child { padding-top: 0; }
.rail-list li:last-child { border-bottom: 0; }
.rail-list a { font-weight: 700; font-size: 0.98rem; line-height: 1.35; }
.rail-list a:hover { color: var(--red); }
.rail-list .with-thumb { display: flex; gap: 0.9rem; align-items: flex-start; }
.rail-list .with-thumb > div { flex: 1; }
.rail-thumb { flex-shrink: 0; width: 120px; }
.rail-thumb img { width: 120px; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 6px; }
.rail-thumb .art { width: 120px; aspect-ratio: 16 / 10; border-radius: 6px; }
.rail-thumb .art .monogram { font-size: 1rem; padding: 0.1rem 0.5rem; }
.rail-thumb .art .art-label { display: none; }
.rail-list small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.2rem; font-weight: 400; }

/* ---------- Live Blog strip ---------- */
.liveblog-strip { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 1rem 0 1.2rem; margin: 0 0 2rem; }
.liveblog-label { color: var(--red); font-size: 0.85rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 0.7rem; }
.liveblog-list { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr; gap: 0.55rem 2.5rem; }
@media (min-width: 900px) { .liveblog-list { grid-template-columns: 1fr 1fr; } }
.liveblog-list li { font-size: 0.96rem; line-height: 1.45; }
.liveblog-list time { color: var(--red); font-weight: 700; font-size: 0.82rem; margin-right: 0.5rem; }
.liveblog-list a:hover { color: var(--red); }

/* ---------- Most Popular ---------- */
.most-read { margin: 0 0 2rem; }
.most-read h2 { font-size: 0.95rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); border-left: 4px solid var(--red); padding-left: 0.6rem; margin: 0 0 0.6rem; }
.most-read ol { list-style: none; margin: 0; padding: 0; counter-reset: mr; }
.most-read li { counter-increment: mr; display: flex; gap: 0.9rem; align-items: flex-start; padding: 0.75rem 0; border-bottom: 1px solid var(--line); }
.most-read li:last-child { border-bottom: 0; }
.most-read li::before { content: counter(mr); font-weight: 800; font-size: 1.5rem; line-height: 1; color: var(--ink); min-width: 1.6rem; }
.most-read a { font-size: 1rem; line-height: 1.35; font-weight: 700; }
.most-read a:hover { color: var(--red); }
.most-read small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; font-weight: 400; }
.most-read.two-col ol { display: grid; grid-template-columns: 1fr; column-gap: 2.5rem; }
@media (min-width: 900px) { .most-read.two-col ol { grid-template-columns: 1fr 1fr; } }

/* ---------- Cards & grids ---------- */
.card-grid { display: grid; grid-template-columns: 1fr; gap: 1.6rem; }
@media (min-width: 640px) { .card-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 980px) { .card-grid.four { grid-template-columns: repeat(4, 1fr); } }
@media (min-width: 980px) { .card-grid.three { grid-template-columns: repeat(3, 1fr); } }
.card { border-top: 0; padding-top: 0; }
.card figure { margin: 0 0 0.6rem; }
.card figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; }
.card h3 { font-size: 1.18rem; line-height: 1.3; margin: 0.35rem 0 0.35rem; font-weight: 800; }
.card h3 a:hover { color: var(--red); }
.card p { margin: 0; color: #555; font-size: 0.95rem; line-height: 1.5; }
.card .art { margin-bottom: 0.6rem; border-radius: 8px; }

/* ---------- Graphic placeholder (stories without a photo) ---------- */
.art {
  aspect-ratio: 16 / 9;
  background: linear-gradient(135deg, var(--navy) 0%, #274b7a 60%, #3d6aa8 100%);
  color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.35rem; text-align: center; padding: 1rem; border-radius: 8px;
}
.art .monogram { font-size: 2.2rem; font-weight: 800; letter-spacing: 0.06em; border: 2px solid rgba(255,255,255,0.85); padding: 0.2rem 0.9rem; }
.art .art-label { font-size: 0.8rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.85; }
.art.small .monogram { font-size: 1.4rem; }

/* ---------- Watch ---------- */
.watch-strip { background: #fff; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); margin: 2.2rem 0; padding: 1.4rem 0 1.6rem; }
.watch-strip h2 { font-size: 0.95rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); margin: 0 0 1rem; }
.watch-grid { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 700px) { .watch-grid { grid-template-columns: repeat(3, 1fr); } }
.watch-card a { color: var(--ink); display: block; }
.watch-card a:hover { text-decoration: none; }
.watch-card a:hover h3 { text-decoration: underline; color: var(--red); }
.watch-thumb { position: relative; }
.watch-thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; }
.watch-thumb .play {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
  width: 44px; height: 44px; border-radius: 50%; background: #fff;
  color: var(--red); font-size: 1rem; display: flex; align-items: center; justify-content: center; padding-left: 3px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
.watch-thumb .dur {
  position: absolute; right: 0.5rem; bottom: 0.5rem; background: rgba(0,0,0,0.8);
  color: #fff; font-size: 0.75rem; font-weight: 700; padding: 0.1rem 0.4rem; border-radius: 2px;
}
.watch-card h3 { font-size: 1.08rem; line-height: 1.3; margin: 0.55rem 0 0; color: var(--ink); font-weight: 800; }

/* ---------- Analysis / Opinion ---------- */
.analysis { margin: 0 0 2.2rem; }
.analysis .cols { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 700px) { .analysis .cols { grid-template-columns: repeat(3, 1fr); } }
.analysis article { background: #fff; border-top: 0; padding: 0; }
.analysis figure { margin: 0 0 0.6rem; }
.analysis figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; }
.analysis h3 { font-size: 1.15rem; line-height: 1.3; margin: 0.35rem 0 0.35rem; font-weight: 800; }
.analysis h3 a:hover { color: var(--red); }
.analysis p { margin: 0; font-size: 0.94rem; color: #555; line-height: 1.5; }

/* ---------- Live blog ---------- */
.live-dot { display: inline-block; width: 0.6rem; height: 0.6rem; background: var(--red); border-radius: 50%; margin-right: 0.4rem; animation: pulse 1.6s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }
.live-update { border-bottom: 1px solid var(--line); padding: 0 0 1rem; margin: 0 0 1rem; }
.live-update time { font-weight: 700; color: var(--red); font-size: 0.88rem; }
.live-update h3 { margin: 0.25rem 0 0.3rem; font-size: 1.15rem; font-weight: 800; line-height: 1.3; }
.live-update h3 a:hover { color: var(--red); }
.live-update p { margin: 0; color: #333; }

/* ---------- Newsletter ---------- */
.newsletter { background: #fff; border: 1px solid var(--line-strong); color: var(--ink); padding: 1.6rem; margin: 2rem 0; border-radius: 8px; }
.newsletter h2 { margin: 0 0 0.3rem; font-size: 1.35rem; font-weight: 800; }
.newsletter p { margin: 0 0 0.9rem; color: var(--muted); }
.newsletter form { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.newsletter input[type="email"] { flex: 1 1 220px; padding: 0.65rem 0.8rem; border: 1px solid var(--line-strong); border-radius: 4px; font-size: 1rem; background: #fff; color: var(--ink); }
.newsletter button, .btn { background: #111; color: #fff; border: 0; padding: 0.65rem 1.2rem; font-size: 1rem; font-weight: 700; border-radius: 4px; cursor: pointer; display: inline-block; }
.newsletter button:hover, .btn:hover { background: #000; text-decoration: none; }
.newsletter .note { font-size: 0.8rem; color: var(--muted); margin: 0.6rem 0 0; }
.newsletter .success { display: none; font-weight: 700; margin-top: 0.6rem; color: var(--ink); }

/* ---------- Article page ---------- */
.article-layout { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 960px) { .article-layout { grid-template-columns: 1fr 300px; } .article-layout .most-read { margin-top: 0.4rem; } }
.article-head h1 { font-size: 2rem; line-height: 1.2; margin: 0.5rem 0; font-weight: 800; }
@media (min-width: 860px) { .article-head h1 { font-size: 2.4rem; } }
.article-head .dek { font-size: 1.12rem; color: #444; line-height: 1.5; }
.article-hero { margin: 1rem 0 1.4rem; }
.article-hero img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; }
.article-hero .art { border-radius: 8px; }
.article-body p { font-size: 1.06rem; line-height: 1.7; margin: 0 0 1.1rem; }
.source-box { border: 1px solid var(--line); border-left: 4px solid var(--red); background: var(--light); padding: 0.8rem 1rem; margin: 1.6rem 0; font-size: 0.95rem; }
.source-box strong { display: block; margin-bottom: 0.2rem; }
.source-box a { color: var(--red); font-weight: 700; }
.related { margin-top: 2rem; border-top: 1px solid var(--line); padding-top: 0.8rem; }
.related h2 { font-size: 0.95rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; margin: 0 0 0.6rem; }
.related-list { list-style: none; margin: 0; padding: 0; }
.related-list li { padding: 0.7rem 0; border-bottom: 1px solid var(--line); }
.related-list li:last-child { border-bottom: 0; }
.related-list a { font-weight: 700; }
.related-list a:hover { color: var(--red); }

/* ---------- Footer ---------- */
footer.site-footer { background: #fff; color: var(--ink); margin-top: 2.5rem; border-top: 1px solid var(--line); }
footer.site-footer .wrap { padding-top: 1.8rem; padding-bottom: 1.4rem; }
footer.site-footer a { color: #333; }
footer.site-footer a:hover { color: var(--red); }
footer.site-footer .cols { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 700px) { footer.site-footer .cols { grid-template-columns: repeat(4, 1fr); } }
footer.site-footer h3 { color: var(--ink); margin: 0 0 0.5rem; font-size: 0.95rem; font-weight: 800; }
footer.site-footer h3 .news { color: var(--ink); }
footer.site-footer ul { list-style: none; margin: 0; padding: 0; }
footer.site-footer li { margin: 0.32rem 0; font-size: 0.94rem; }
footer.site-footer p { font-size: 0.94rem; color: #555; }
footer.site-footer .mini-form { display: flex; gap: 0.4rem; margin-top: 0.6rem; }
footer.site-footer .mini-form input[type="email"] { flex: 1; min-width: 0; padding: 0.5rem 0.6rem; border: 1px solid var(--line-strong); border-radius: 4px; font-size: 0.9rem; background: #fff; color: var(--ink); }
footer.site-footer .mini-form button { background: #111; color: #fff; border: 0; padding: 0.5rem 0.8rem; border-radius: 4px; font-weight: 700; cursor: pointer; }
footer.site-footer .mini-form button:hover { background: #000; }
footer.site-footer .fineprint { border-top: 1px solid var(--line); margin-top: 1.5rem; padding-top: 0.9rem; font-size: 0.82rem; color: var(--muted); display: flex; flex-wrap: wrap; gap: 0.4rem 1.2rem; justify-content: space-between; }

.skip-link { position: absolute; left: -999px; top: 0; background: var(--red); color: #fff; padding: 0.5rem 1rem; z-index: 300; }
.skip-link:focus { left: 0; }
"""


# ---------------- Templates (v2) ----------------

def nav_html(active, prefix=""):
    items = []
    for href, label in NAV:
        cls = "active" if href == active else ""
        if href == "live.html":
            cls += " live-link"
        items.append(f'<li><a href="{prefix}{href}" class="{cls.strip()}">{label}</a></li>')
    return '<ul>' + "".join(items) + "</ul>"


def header_html(active, prefix=""):
    topics = "".join(
        f'<a href="{prefix}{href}">{label}</a>' for label, href in TOPICS
    )
    return f"""<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
<div class="wrap header-row">
<a class="wordmark" href="{prefix}index.html" data-site-name>Western World News</a>
<button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false">&#9776;</button>
<nav class="main-nav" id="main-nav" aria-label="Main navigation">{nav_html(active, prefix)}</nav>
<div class="header-actions">
<a class="live-link" href="{prefix}live.html"><span class="live-dot"></span>Live</a>
<div class="search-box">
<input type="search" id="site-search" placeholder="Search news..." aria-label="Search news" autocomplete="off">
<div class="search-results" id="search-results" role="listbox" aria-label="Search results"></div>
</div>
<a class="btn-black" href="#newsletter">Newsletter</a>
</div>
</div>
<div class="topic-row"><div class="wrap">{topics}</div></div>
</header>"""


# Smaller topic links under the header (real current stories).
TOPICS = [
    ("Ukraine war", "live.html"),
    ("Gaza ceasefire", "articles/gaza-yellow-line-raid.html"),
    ("EU-UK reset", "articles/eu-uk-reset-deal.html"),
    ("COP31", "articles/at-cop31-conflict-over-climate-science-slows-action-on.html"),
    ("Wall Street", "articles/wall-street-selloff.html"),
    ("Rwanda return hubs", "articles/eu-rwanda-return-hub.html"),
    ("Nations League", "articles/nations-league-draw.html"),
    ("Grammys", "articles/raye-grammy-nominations.html"),
]


def footer_html(prefix=""):
    return f"""<footer class="site-footer"><div class="wrap">
<div class="cols">
<div>
<h3 data-site-name>Western World <span class="news">News</span></h3>
<p data-tagline>Independent news from the West and the world: politics, war, business and culture, reported fast and in our own words. Free to read.</p>
</div>
<div>
<h3>Sections</h3>
<ul>
<li><a href="{prefix}world.html">World</a></li>
<li><a href="{prefix}europe.html">Europe</a></li>
<li><a href="{prefix}us.html">US</a></li>
<li><a href="{prefix}politics.html">Politics</a></li>
<li><a href="{prefix}war-conflict.html">War &amp; Conflict</a></li>
<li><a href="{prefix}business-finance.html">Business &amp; Finance</a></li>
<li><a href="{prefix}sport.html">Sport</a></li>
<li><a href="{prefix}culture.html">Culture</a></li>
<li><a href="{prefix}live.html">Live</a></li>
</ul>
</div>
<div>
<h3>About</h3>
<ul>
<li><a href="{prefix}about.html">About us</a></li>
<li><a href="{prefix}contact.html">Contact</a></li>
<li><a href="{prefix}privacy.html">Privacy policy</a></li>
<li><a href="{prefix}sitemap.xml">Sitemap</a></li>
<li><a href="{prefix}admin.html">Admin</a></li>
</ul>
</div>
<div>
<h3>The Western Briefing</h3>
<p>Our free morning newsletter: the day's Western and European news in your inbox before 8am.</p>
<form class="mini-form newsletter-form" action="#" method="post">
<label for="ft-email" class="sr-only">Email address</label>
<input id="ft-email" type="email" name="email" placeholder="Your email" required>
<button type="submit">Sign up</button>
</form>
<p class="success" style="display:none">Thank you. You are on the list.</p>
</div>
</div>
<p class="fineprint"><span>&copy; 2026 Western World News (westernworldnews.com). All stories are original summaries written by our editors; original reporting is credited and linked. Content refreshed on the evening of November 20, 2026. See README.md.</span><span>Photos: Unsplash (illustrative).</span></p>
</div></footer>"""


def page(title, description, active, body, canonical, og_type="website", prefix="", extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Western World News</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Western World News">
<meta property="og:title" content="{title} | Western World News">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | Western World News">
<meta name="twitter:description" content="{description}">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23bb1919'/%3E%3Ctext x='16' y='22' font-family='Arial' font-size='16' font-weight='bold' fill='white' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E">
{extra_head}</head>
<body>
{header_html(active, prefix)}
<main id="main"><div class="wrap">
{body}
</div></main>
{footer_html(prefix)}
<script src="{prefix}assets/js/content.js"></script>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def art_html(section_label, small=False):
    cls = "art small" if small else "art"
    return (f'<div class="{cls}" role="img" aria-label="Graphic placeholder for {section_label}">'
            f'<span class="monogram">WWN</span><span class="art-label">{section_label}</span></div>')


def img_html(slug, w=800, cls="", caption=True):
    """Photo figure for a story, or the gradient tile if no photo is set."""
    if slug in IMAGES:
        pid, cap = IMAGES[slug]
        alt = cap.split(". Illustrative")[0]
        fig = (f'<figure class="{cls}"><img src="{uimg(pid, w)}" alt="{hescape(alt)}" loading="lazy">'
               f'<figcaption>{hescape(cap)}</figcaption></figure>') if caption else \
              f'<figure class="{cls}"><img src="{uimg(pid, w)}" alt="{hescape(alt)}" loading="lazy"></figure>'
        return fig
    if slug in BY_SLUG and BY_SLUG[slug].get("image"):
        cap = BY_SLUG[slug].get("imageCaption") or "Photo: Unsplash"
        alt = cap.split(". Illustrative")[0]
        fig = (f'<figure class="{cls}"><img src="{hescape(BY_SLUG[slug]["image"])}" alt="{hescape(alt)}" loading="lazy">'
               f'<figcaption>{hescape(cap)}</figcaption></figure>') if caption else \
              f'<figure class="{cls}"><img src="{hescape(BY_SLUG[slug]["image"])}" alt="{hescape(alt)}" loading="lazy"></figure>'
        return fig
    sec = SECTIONS[BY_SLUG[slug]["section"]] if slug in BY_SLUG else "News"
    return art_html(sec, small=(w <= 800))


def thumb_html(slug, w=400):
    """Small thumbnail image only (no caption), or the gradient tile."""
    s = BY_SLUG.get(slug)
    if s and s.get("image"):
        return f'<img src="{hescape(s["image"])}" alt="" loading="lazy">'
    if slug in IMAGES:
        pid, _cap = IMAGES[slug]
        return f'<img src="{uimg(pid, w)}" alt="" loading="lazy">'
    sec = SECTIONS[s["section"]] if s else "News"
    return art_html(sec, small=True)


def card_html(s, prefix=""):
    sec = SECTIONS[s["section"]]
    return f"""<article class="card">
{img_html(s['slug'], w=800)}
<p><span class="kicker">{sec}</span></p>
<h3><a href="{prefix}articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; Source: {s['source']}</p>
</article>"""


def most_read_html(prefix="", two_col=False):
    slugs = [s for s in MOST_READ if s in BY_SLUG]
    for s in STORIES:
        if len(slugs) >= 10:
            break
        if s["slug"] not in slugs:
            slugs.append(s["slug"])
    items = "".join(
        f'<li><div><a href="{prefix}articles/{s["slug"]}.html">{s["headline"]}</a>'
        f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small></div></li>'
        for s in (BY_SLUG[slug] for slug in slugs)
    )
    cls = "most-read two-col" if two_col else "most-read"
    return f"""<aside class="{cls}" aria-label="Most popular">
<h2>Most Popular</h2>
<ol id="most-read-list">{items}</ol>
</aside>"""


def newsletter_html():
    return """<section class="newsletter" id="newsletter" aria-label="Newsletter signup">
<h2>The Western Briefing: free, every morning</h2>
<p>Western and European news, war updates and the day's business headlines, in your inbox before 8am.</p>
<form class="newsletter-form" action="#" method="post">
<label for="nl-email" class="sr-only" style="position:absolute;left:-9999px">Email address</label>
<input id="nl-email" type="email" name="email" placeholder="Your email address" required>
<button type="submit">Sign up free</button>
</form>
<p class="success">Thank you. You are on the list. Your first briefing arrives tomorrow morning.</p>
<p class="note">No spam, no paywall. Unsubscribe any time. (Demo form: connect a mailing service before launch; see README.md.)</p>
</section>"""


def stories_for(section):
    return [s for s in STORIES if section in s["sections"]]


def watch_html():
    cards = "".join(
        f"""<div class="watch-card"><a href="{w['link']}">
<div class="watch-thumb"><img src="{uimg(w['img'], 800)}" alt="{hescape(w['title'])}" loading="lazy"><span class="play">&#9654;</span><span class="dur">{w['dur']}</span></div>
<h3>{hescape(w['title'])}</h3></a></div>""" for w in WATCH
    )
    return f"""<section class="watch-strip" aria-label="Watch">
<h2>Watch</h2>
<div class="watch-grid">{cards}</div>
</section>"""


def analysis_html():
    def slug_of(link):
        return link.rsplit("/", 1)[-1].replace(".html", "")
    items = "".join(
        f"""<article>
{img_html(slug_of(a['link']), w=800)}
<p><span class="kicker">Analysis</span></p>
<h3><a href="{a['link']}">{hescape(a['title'])}</a></h3>
<p>{hescape(a['blurb'])}</p></article>""" for a in ANALYSIS
    )
    return f"""<section class="analysis" aria-label="Analysis">
<h2 class="section-head">Analysis</h2>
<div class="cols">{items}</div>
</section>"""


# ---------------- Homepage ----------------

def build_index():
    hero = BY_SLUG.get(HERO_SLUG) or STORIES[0]
    rest = [s for s in STORIES if s["slug"] != hero["slug"]]
    second, third = rest[0], rest[1]
    must_slugs = [s for s in MOST_READ if s in BY_SLUG][:4]
    used = {hero["slug"], second["slug"], third["slug"]} | set(must_slugs)
    more = [s for s in STORIES if s["slug"] not in used][:6]
    is_breaking = BREAKING.get("link", "").endswith(hero["slug"] + ".html")
    hero_kicker = "Breaking" if is_breaking else f"{SECTIONS[hero['section']]} &middot; Live"

    def rail_item(s, thumb=False):
        small = f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small>'
        link = f'articles/{s["slug"]}.html'
        if thumb:
            return (f'<li class="with-thumb"><div><a href="{link}">{s["headline"]}</a>{small}</div>'
                    f'<a class="rail-thumb" href="{link}">{thumb_html(s["slug"])}</a></li>')
        return f'<li><a href="{link}">{s["headline"]}</a>{small}</li>'

    must_items = "".join(rail_item(BY_SLUG[s], thumb=(i == 0)) for i, s in enumerate(must_slugs))
    more_items = "".join(rail_item(s) for s in more)
    just_in = "".join(
        f'<li><time>{t}</time><a href="live.html">{h}</a></li>' for t, h, _ in JUST_IN
    )
    europe = stories_for("europe")
    world = stories_for("world")
    us_pol = stories_for("us") + [s for s in stories_for("politics") if s["slug"] not in [x["slug"] for x in stories_for("us")]]
    biz = stories_for("business-finance")

    def block(title, stories, grid_cls="four", slug=""):
        cards = "".join(card_html(s) for s in stories)
        return f'<h2 class="section-head">{title}</h2><div class="card-grid {grid_cls}" data-section-block data-section="{slug}">{cards}</div>'

    body = f"""
<div class="hero-grid">
<article class="hero" data-hero>
{img_html(hero['slug'], w=1600, cls="hero-media", caption=False)}
<div class="hero-box">
<p><span class="kicker">{hero_kicker}</span></p>
<h1><a href="articles/{hero['slug']}.html">{hero['headline']}</a></h1>
</div>
<p class="dek">{hero['dek']}</p>
<p class="byline"><time>{hero['date']}</time> &middot; Source: {hero['source']} &middot; <a href="live.html">Follow live updates</a></p>
</article>
<div class="hero-second">
<article class="second-story">
{img_html(second['slug'], w=800)}
<p><span class="kicker">{SECTIONS[second['section']]}</span></p>
<h3><a href="articles/{second['slug']}.html">{second['headline']}</a></h3>
</article>
<article class="text-card">
<div>
<p><span class="kicker">{SECTIONS[third['section']]}</span></p>
<h3><a href="articles/{third['slug']}.html">{third['headline']}</a></h3>
</div>
<a class="text-card-thumb" href="articles/{third['slug']}.html">{thumb_html(third['slug'])}</a>
</article>
</div>
<div class="hero-rail">
<aside class="rail-block" aria-label="Must reads">
<h2 class="rail-head">Must Reads</h2>
<ul class="rail-list">{must_items}</ul>
</aside>
<aside class="rail-block" aria-label="More headlines">
<h2 class="rail-head">More Headlines</h2>
<ul class="rail-list">{more_items}</ul>
</aside>
</div>
</div>

<section class="liveblog-strip" aria-label="Live blog">
<h2 class="liveblog-label">Live Blog</h2>
<ul id="just-in-list" class="liveblog-list">{just_in}</ul>
</section>

{block("Europe", europe, slug="europe")}
<div style="height:2rem"></div>
{block("World", world, slug="world")}
<div style="height:2rem"></div>

{watch_html()}

{block("US &amp; Politics", us_pol, slug="us,politics")}
<div style="height:2rem"></div>

{most_read_html(two_col=True)}

<section aria-label="Live blog">
<h2 class="section-head"><span class="live-dot"></span>Live: Ukraine war</h2>
<div class="live-update">
<time>Nov 20, 10:33</time>
<h3><a href="live.html">Embassies damaged in Kyiv barrage</a></h3>
<p>A daytime Russian barrage blew out windows at the Austrian and Dutch missions in Kyiv and damaged a cathedral, prompting Brussels to summon Moscow's envoy. <a href="live.html">Follow the live blog</a></p>
</div>
</section>

{newsletter_html()}

{analysis_html()}

{block("Business &amp; Finance", biz, slug="business-finance")}
"""
    html = page(
        "Western World News | Western and European news, live",
        "Western World News: breaking news from Western Europe and the world: politics, war, business and culture, free to read.",
        "index.html", body, BASE + "/",
    )
    return html


# ---------------- Section pages ----------------

def build_section(section, filename):
    stories = stories_for(section)
    label = SECTIONS[section]
    if stories:
        cards = "".join(card_html(s) for s in stories)
        listing = f'<div class="card-grid three" data-section-list="{section}">{cards}</div>'
    else:
        listing = "<p>No stories in this section yet. New coverage is added daily.</p>"
    body = f"""
<h1 class="section-head">{label}</h1>
{listing}
{most_read_html()}
{newsletter_html()}
"""
    return page(
        f"{label} news",
        f"Latest {label.lower()} news from Western World News: Western and European coverage, free to read.",
        filename, body, BASE + "/" + filename,
    )


# ---------------- Live page ----------------

def build_live():
    updates = "".join(
        f"""<div class="live-update">
<time>{t}</time>
<h3>{h}</h3>
<p>{p}</p>
</div>""" for t, h, p in LIVE_UPDATES
    )
    body = f"""
<h1 class="section-head"><span class="live-dot"></span>Live: Ukraine war</h1>
<p>Rolling updates on Russia's war in Ukraine: the overnight missile strikes, the Shenzhen summit and Europe's response. Times are in CET. Last updated November 20, 2026.</p>
<div id="live-updates">{updates}</div>
<p><a class="btn" href="articles/russia-ukraine-missile-attack.html">Read the full story</a></p>
{newsletter_html()}
"""
    return page(
        "Live: Ukraine war (rolling updates)",
        "Live updates on Russia's war in Ukraine: missile strikes, the Trump-Xi-Putin summit and Europe's response.",
        "live.html", body, BASE + "/live.html",
    )


# ---------------- Article pages ----------------

def build_article(s):
    body_paras = "".join(f"<p>{p}</p>" for p in s["body"])
    if s.get("auto"):
        # Auto-published articles are short summaries of the source's own
        # report (feed description), not original WWN summaries — say so.
        source_note = (f"This is a short summary of a {s['source']} report. "
                       f"Read the full story at {s['source']}: "
                       f"<a href=\"{s['source_url']}\" target=\"_blank\" rel=\"noopener\">Original article: {s['source']}</a>.")
    else:
        source_note = (f"This story is an original summary by Western World News, based on reporting by {s['source']} ({s['date']}). "
                       f"Read the original report: <a href=\"{s['source_url']}\" target=\"_blank\" rel=\"noopener\">Original article: {s['source']}</a>.")
    rel = "".join(
        f'<li><a href="{r}.html">{BY_SLUG[r]["headline"]}</a> <span class="byline">{BY_SLUG[r]["date"]}</span></li>'
        for r in s["related"]
    )
    sec = SECTIONS[s["section"]]
    body = f"""
<div class="article-layout">
<div>
<article data-article-slug="{s['slug']}">
<header class="article-head">
<p><span class="kicker">{sec}</span></p>
<h1>{s['headline']}</h1>
<p class="dek">{s['dek']}</p>
<p class="byline">Western World News &middot; <time>{s['date']}</time></p>
</header>
<div class="article-hero">{img_html(s['slug'], w=1600)}</div>
<div class="article-body">
{body_paras}
</div>
<div class="source-box">
<strong>Source</strong>
{source_note}
</div>
<section class="related">
<h2>Related stories</h2>
<ul class="related-list">{rel}</ul>
</section>
</article>
{newsletter_html()}
</div>
<div>
{most_read_html(prefix="../")}
</div>
</div>
"""
    return page(
        s["headline"], s["dek"], s["section"] + ".html" if s["section"] != "live" else "index.html",
        body, BASE + f"/articles/{s['slug']}.html", og_type="article", prefix="../",
    )


# ---------------- Info pages ----------------

def build_info(slug, title, description, heading, paragraphs):
    body = f'<h1 class="section-head">{heading}</h1>\n' + "\n".join(f"<p>{p}</p>" for p in paragraphs)
    return page(title, description, "index.html", body, BASE + "/" + slug + ".html")


# ---------------- Content store (content.js) ----------------

def default_content():
    articles = []
    for s in STORIES:
        pid, cap = IMAGES.get(s["slug"], ("", ""))
        articles.append({
            "slug": s["slug"],
            "sections": s["sections"],
            "section": s["section"],
            "headline": s["headline"],
            "dek": s["dek"],
            "date": s["date"],
            "source": s["source"],
            "source_url": s["source_url"],
            "body": s["body"],
            "related": s["related"],
            "image": s.get("image") or (uimg(pid, 1200) if pid else ""),
            "imageCaption": s.get("imageCaption") or cap,
        })
    return {
        "version": 1,
        "settings": {
            "siteName": "Western World News",
            "tagline": "Western and European news, live: politics, war, business and culture.",
            "heroSlug": HERO_SLUG,
        },
        "breaking": BREAKING,
        "articles": articles,
        "justIn": [{"time": t, "text": h, "link": "live.html"} for t, h, _ in JUST_IN],
        "liveUpdates": [{"time": t, "headline": h, "text": p} for t, h, p in LIVE_UPDATES],
        "mostRead": list(MOST_READ),
    }


CONTENT_JS = """/* Western World News: central content store.
   WWN_DEFAULT_CONTENT is the seed content baked into the static site.
   The admin panel (admin.html) saves edits to localStorage under
   WWNStore.KEY; pages load the merged result, so admin changes apply
   across the whole site immediately (in that browser).
   Export JSON from the admin to make changes permanent in the repo. */
window.WWN_DEFAULT_CONTENT = __DEFAULT_JSON__;

window.WWNStore = (function () {
  var KEY = "wwn_content_v1";
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function loadSaved() {
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }
  function merge(base, saved) {
    if (!saved) return clone(base);
    var out = clone(base);
    if (saved.settings) {
      for (var k in saved.settings) out.settings[k] = saved.settings[k];
    }
    if (saved.breaking) out.breaking = saved.breaking;
    if (Array.isArray(saved.justIn)) out.justIn = saved.justIn;
    if (Array.isArray(saved.liveUpdates)) out.liveUpdates = saved.liveUpdates;
    if (Array.isArray(saved.mostRead)) out.mostRead = saved.mostRead;
    if (Array.isArray(saved.articles)) {
      // Saved articles win by slug; brand-new slugs are appended.
      var bySlug = {};
      out.articles.forEach(function (a) { bySlug[a.slug] = a; });
      saved.articles.forEach(function (a) {
        if (a && a.slug) bySlug[a.slug] = a;
      });
      var order = out.articles.map(function (a) { return a.slug; });
      saved.articles.forEach(function (a) {
        if (a && a.slug && order.indexOf(a.slug) === -1) order.push(a.slug);
      });
      // Honour deletions: a saved article list that omits a default slug
      // means the owner deleted it, but only when the saved list was
      // written by the admin (it always carries version + savedAt).
      if (saved.savedAt) {
        var kept = saved.articles.map(function (a) { return a.slug; });
        order = order.filter(function (slug) { return kept.indexOf(slug) !== -1; });
      }
      out.articles = order.map(function (slug) { return bySlug[slug]; });
    }
    return out;
  }
  return {
    KEY: KEY,
    defaults: function () { return clone(window.WWN_DEFAULT_CONTENT); },
    get: function () { return merge(window.WWN_DEFAULT_CONTENT, loadSaved()); },
    saved: function () { return loadSaved(); },
    save: function (data) {
      data.savedAt = new Date().toISOString();
      try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {}
      return data;
    },
    reset: function () { try { localStorage.removeItem(KEY); } catch (e) {} },
    hasSaved: function () { return !!loadSaved(); }
  };
})();
"""

MAIN_JS = """// Western World News: front-end behavior (v2).
// Renders dynamic regions from the content store (assets/js/content.js),
// so admin edits in localStorage apply across the whole site.
// Static HTML in each page is the SEO fallback when JS is unavailable.
(function () {
  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function prefix() {
    return window.location.pathname.indexOf("/articles/") !== -1 ? "../" : "";
  }
  function fixLink(link) {
    if (!link) return "#";
    if (/^(https?:|mailto:|#)/.test(link)) return link;
    if (link.indexOf("../") === 0) return link;
    return prefix() + link;
  }
  function articleUrl(slug) { return prefix() + "articles/" + slug + ".html"; }
  function sectionLabel(slug) {
    var map = { world: "World", europe: "Europe", us: "US", politics: "Politics",
      "war-conflict": "War & Conflict", "business-finance": "Business & Finance",
      sport: "Sport", culture: "Culture", live: "Live" };
    return map[slug] || slug;
  }
  function tileFor(a, w) {
    if (a.image) {
      return '<figure><img src="' + esc(a.image) + '" alt="' + esc(a.headline) +
        '" loading="lazy"><figcaption>' + esc(a.imageCaption || "Photo: Unsplash") + "</figcaption></figure>";
    }
    return '<div class="art small" role="img" aria-label="Graphic placeholder"><span class="monogram">WWN</span>' +
      '<span class="art-label">' + esc(sectionLabel(a.section)) + "</span></div>";
  }

  var store = window.WWNStore ? window.WWNStore.get() : null;
  if (!store) return;
  var bySlug = {};
  store.articles.forEach(function (a) { bySlug[a.slug] = a; });

  document.addEventListener("DOMContentLoaded", function () {
    // Dateline.
    $all("[data-today]").forEach(function (el) {
      el.textContent = new Date().toLocaleDateString("en-GB", {
        weekday: "long", day: "numeric", month: "long", year: "numeric"
      });
    });

    // Site name + tagline from settings.
    $all("[data-site-name]").forEach(function (el) {
      var words = String(store.settings.siteName || "Western World News").split(" ");
      var last = words.pop();
      el.innerHTML = esc(words.join(" ")) + ' <span class="news">' + esc(last) + "</span>";
    });
    $all("[data-tagline]").forEach(function (el) {
      el.textContent = store.settings.tagline || "";
    });

    // Breaking bar.
    var bl = $("#breaking-link");
    if (bl && store.breaking) {
      bl.textContent = store.breaking.text;
      bl.href = fixLink(store.breaking.link);
    }

    // Ticker (Just In headlines, duplicated for the marquee loop).
    var track = $(".ticker-track");
    if (track && store.justIn.length) {
      var items = store.justIn.map(function (it) {
        return '<a href="' + fixLink(it.link || "live.html") + '">' + esc(it.text) + "</a>";
      }).join("");
      track.innerHTML = items + items;
    }

    // Just In list.
    var ji = $("#just-in-list");
    if (ji) {
      ji.innerHTML = store.justIn.map(function (it) {
        return "<li><time>" + esc(it.time) + '</time><a href="' + fixLink(it.link || "live.html") +
          '">' + esc(it.text) + "</a></li>";
      }).join("");
    }

    // Hero (homepage): photo with the red headline box overlapping it.
    var heroEl = $("[data-hero]");
    var hero = bySlug[store.settings.heroSlug] || store.articles[0];
    if (heroEl && hero) {
      var heroImg = hero.image
        ? '<figure class="hero-media"><img src="' + esc(hero.image) + '" alt="' + esc(hero.headline) + '" loading="lazy"></figure>'
        : '<div class="art" role="img" aria-label="Graphic placeholder"><span class="monogram">WWN</span><span class="art-label">' + esc(sectionLabel(hero.section)) + "</span></div>";
      var isBreaking = store.breaking && store.breaking.link && store.breaking.link.indexOf(hero.slug) !== -1;
      var kick = isBreaking ? "Breaking" : esc(sectionLabel(hero.section)) + " &middot; Live";
      heroEl.innerHTML =
        heroImg +
        '<div class="hero-box"><p><span class="kicker">' + kick + "</span></p>" +
        '<h1><a href="' + articleUrl(hero.slug) + '">' + esc(hero.headline) + "</a></h1></div>" +
        '<p class="dek">' + esc(hero.dek) + "</p>" +
        '<p class="byline"><time>' + esc(hero.date) + "</time> &middot; Source: " + esc(hero.source) +
        ' &middot; <a href="' + fixLink("live.html") + '">Follow live updates</a></p>';
    }

    // Homepage section blocks.
    $all("[data-section-block]").forEach(function (grid) {
      var secs = (grid.getAttribute("data-section") || "").split(",");
      var list = store.articles.filter(function (a) {
        var s = a.sections || [a.section];
        return secs.some(function (x) { return s.indexOf(x) !== -1; });
      });
      if (!list.length) return;
      grid.innerHTML = list.map(function (a) {
        return '<article class="card">' + tileFor(a) +
          '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
          '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
          "<p>" + esc(a.dek) + "</p>" +
          '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></article>";
      }).join("");
    });

    // Section pages: image-above cards.
    $all("[data-section-list]").forEach(function (list) {
      var sec = list.getAttribute("data-section-list");
      var items = store.articles.filter(function (a) { return (a.sections || [a.section]).indexOf(sec) !== -1; });
      if (!items.length) return;
      list.innerHTML = items.map(function (a) {
        return '<article class="card">' + tileFor(a) +
          '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
          '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
          "<p>" + esc(a.dek) + "</p>" +
          '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></article>";
      }).join("");
    });

    // Most Popular: numbered list, up to 10.
    var mr = $("#most-read-list");
    if (mr) {
      var slugs = (store.mostRead || []).filter(function (s) { return bySlug[s]; });
      store.articles.forEach(function (a) {
        if (slugs.length < 10 && slugs.indexOf(a.slug) === -1) slugs.push(a.slug);
      });
      mr.innerHTML = slugs.slice(0, 10).map(function (slug) {
        var a = bySlug[slug];
        return '<li><div><a href="' + articleUrl(slug) + '">' + esc(a.headline) + "</a>" +
          "<small>" + esc(sectionLabel(a.section)) + " &middot; " + esc(a.date) + "</small></div></li>";
      }).join("");
    }

    // Live blog.
    var live = $("#live-updates");
    if (live) {
      live.innerHTML = store.liveUpdates.map(function (u) {
        return '<div class="live-update"><time>' + esc(u.time) + "</time><h3>" + esc(u.headline) +
          "</h3><p>" + esc(u.text) + "</p></div>";
      }).join("");
    }

    // Article page override (lets admin edits show on the article itself).
    var art = $("[data-article-slug]");
    if (art) {
      var a = bySlug[art.getAttribute("data-article-slug")];
      if (a) {
        var h1 = $("h1", art), dek = $(".dek", art), byl = $(".byline time", art);
        if (h1) h1.textContent = a.headline;
        if (dek) dek.textContent = a.dek;
        if (byl) byl.textContent = a.date;
        var heroBox = $(".article-hero", art);
        if (heroBox) heroBox.innerHTML = tileFor(a);
        var bodyBox = $(".article-body", art);
        if (bodyBox) bodyBox.innerHTML = (a.body || []).map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("");
        var src = $(".source-box", art);
        if (src) {
          src.innerHTML = "<strong>Source</strong>This story is an original summary by " +
            esc(store.settings.siteName) + ", based on reporting by " + esc(a.source) + " (" + esc(a.date) +
            '). Read the original report: <a href="' + esc(a.source_url) +
            '" target="_blank" rel="noopener">' + "Original article: " + esc(a.source) + "</a>.";
        }
      }
    }

    // Hamburger nav.
    var toggle = $("#nav-toggle"), nav = $("#main-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }

    // Search: filters articles, shows a dropdown of matches.
    var input = $("#site-search"), box = $("#search-results");
    if (input && box) {
      input.addEventListener("input", function () {
        var q = input.value.trim().toLowerCase();
        if (q.length < 2) { box.classList.remove("open"); box.innerHTML = ""; return; }
        var hits = store.articles.filter(function (a) {
          return (a.headline + " " + a.dek + " " + sectionLabel(a.section)).toLowerCase().indexOf(q) !== -1;
        }).slice(0, 6);
        box.innerHTML = hits.length
          ? hits.map(function (a) {
              return '<a href="' + articleUrl(a.slug) + '"><small>' + esc(sectionLabel(a.section)) +
                "</small>" + esc(a.headline) + "</a>";
            }).join("")
          : '<div class="none">No stories match "' + esc(input.value.trim()) + '".</div>';
        box.classList.add("open");
      });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          var first = box.querySelector("a");
          if (first) window.location.href = first.href;
        }
        if (e.key === "Escape") { box.classList.remove("open"); input.blur(); }
      });
      input.addEventListener("blur", function () {
        setTimeout(function () { box.classList.remove("open"); }, 200);
      });
    }

    // Newsletter forms (demo until a mailing service is connected).
    $all("form.newsletter-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var email = form.querySelector('input[type="email"]');
        var ok = form.parentElement.querySelector(".success");
        if (email && email.value.indexOf("@") > 0) {
          form.style.display = "none";
          if (ok) ok.style.display = "block";
        } else if (email) { email.focus(); }
      });
    });
  });
})();
"""


# ---------------- Admin panel ----------------

ADMIN_PASSCODE = "admin123"

ADMIN_CSS = """/* Western World News: admin panel styles (admin.html only). */
.admin-top { background: var(--navy-dark); color: #fff; padding: 0.9rem 0; }
.admin-top .wrap { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.admin-top .wordmark { font-size: 1.4rem; color: #fff; }
.admin-top .wordmark .news { color: #fff; }
.admin-badge { background: var(--red); color: #fff; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; padding: 0.2rem 0.55rem; border-radius: 3px; text-transform: uppercase; }
.admin-top .spacer { flex: 1; }
.admin-top a { color: #fff; font-weight: 600; }
.admin-top button { background: rgba(255,255,255,0.15); color: #fff; border: 1px solid rgba(255,255,255,0.4); border-radius: 3px; padding: 0.4rem 0.8rem; cursor: pointer; font-weight: 600; }
.admin-top button:hover { background: rgba(255,255,255,0.28); }
.gate-card { max-width: 420px; margin: 3rem auto; border: 1px solid var(--line); border-radius: 6px; padding: 1.6rem; background: #fff; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
.gate-card h1 { font-family: var(--sans); margin: 0 0 0.4rem; font-size: 1.5rem; }
.gate-card p { color: var(--muted); margin: 0 0 1rem; }
.gate-card .error { color: var(--red); font-weight: 700; display: none; margin: 0.6rem 0 0; }
.admin-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0 1.6rem; }
@media (max-width: 860px) { .admin-grid { grid-template-columns: repeat(2, 1fr); } }
.stat { border: 1px solid var(--line); border-top: 3px solid var(--red); border-radius: 4px; padding: 0.8rem 1rem; background: #fff; }
.stat b { display: block; font-family: var(--sans); font-size: 1.9rem; line-height: 1.1; }
.stat span { color: var(--muted); font-size: 0.85rem; }
.panel { border: 1px solid var(--line); border-radius: 6px; margin: 0 0 1.6rem; overflow: hidden; }
.panel > h2 { margin: 0; padding: 0.75rem 1rem; background: var(--navy); color: #fff; font-family: var(--sans); font-size: 1.15rem; }
.panel .body { padding: 1rem; }
.notice { background: #fff8e6; border: 1px solid #ecd27a; border-left: 4px solid #d9a400; border-radius: 4px; padding: 0.8rem 1rem; margin: 0 0 1.4rem; font-size: 0.94rem; }
.notice b { display: block; margin-bottom: 0.2rem; }
.admin-list { list-style: none; margin: 0 0 1rem; padding: 0; }
.admin-list li { display: flex; gap: 0.7rem; align-items: baseline; padding: 0.55rem 0; border-bottom: 1px solid var(--line); flex-wrap: wrap; }
.admin-list li:last-child { border-bottom: 0; }
.admin-list .t { flex: 1; min-width: 200px; }
.admin-list .t small { color: var(--muted); display: block; font-size: 0.8rem; }
.admin-list button, .panel button { cursor: pointer; }
.btn { background: var(--red); color: #fff; border: 0; padding: 0.55rem 1rem; border-radius: 3px; font-weight: 700; font-size: 0.92rem; }
.btn:hover { background: var(--red-dark); }
.btn.ghost { background: #fff; color: var(--ink); border: 1px solid var(--line); }
.btn.ghost:hover { background: var(--light); }
.btn.danger { background: #fff; color: var(--red); border: 1px solid var(--red); padding: 0.35rem 0.7rem; font-size: 0.85rem; }
.btn.danger:hover { background: var(--red); color: #fff; }
.btn.small { padding: 0.35rem 0.7rem; font-size: 0.85rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
@media (max-width: 700px) { .form-grid { grid-template-columns: 1fr; } }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.field.full { grid-column: 1 / -1; }
.field label { font-weight: 700; font-size: 0.88rem; }
.field input, .field select, .field textarea {
  font: inherit; font-size: 0.95rem; padding: 0.55rem 0.65rem;
  border: 1px solid #c9c9c9; border-radius: 3px; width: 100%;
}
.field textarea { min-height: 150px; line-height: 1.5; }
.field .hint { font-size: 0.8rem; color: var(--muted); font-weight: 400; }
.check-row { display: flex; gap: 1.2rem; align-items: center; font-weight: 600; font-size: 0.92rem; }
.form-actions { display: flex; gap: 0.6rem; margin-top: 1rem; flex-wrap: wrap; }
.toast {
  position: fixed; left: 50%; bottom: 1.4rem; transform: translateX(-50%);
  background: var(--navy); color: #fff; padding: 0.7rem 1.2rem; border-radius: 4px;
  font-weight: 600; box-shadow: 0 6px 24px rgba(0,0,0,0.3); display: none; z-index: 500;
}
.hidden { display: none !important; }
"""

ADMIN_JS = """// Western World News: admin panel (admin.html).
// Passcode gate only: this is a static site, so the passcode is a basic
// gate, NOT real server security. Anyone with the site files can read the
// content. Do not rely on it to protect secrets.
(function () {
  var PASSCODE = "admin123";
  var SECTION_OPTIONS = ["world", "europe", "us", "politics", "war-conflict",
    "business-finance", "sport", "culture"];
  var SECTION_LABELS = { world: "World", europe: "Europe", us: "US", politics: "Politics",
    "war-conflict": "War & Conflict", "business-finance": "Business & Finance",
    sport: "Sport", culture: "Culture" };

  function $(s) { return document.querySelector(s); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function toast(msg) {
    var t = $("#toast");
    t.textContent = msg;
    t.style.display = "block";
    setTimeout(function () { t.style.display = "none"; }, 3200);
  }
  function slugify(s) {
    return String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 70) || "article";
  }
  function nowStamp() {
    var d = new Date();
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var hh = String(d.getHours()).padStart(2, "0"), mm = String(d.getMinutes()).padStart(2, "0");
    return d.getDate() + " " + months[d.getMonth()] + ", " + hh + ":" + mm;
  }
  function todayLong() {
    return new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }

  var gate = $("#gate"), dash = $("#dashboard");
  var store = window.WWNStore;
  var data = store.get();
  var editingSlug = null, editingJustIn = -1, editingLive = -1;

  function save(msg) {
    data = store.save(data);
    renderAll();
    toast(msg || "Saved. Live across the site in this browser.");
  }

  // ---------- Gate ----------
  function unlock() {
    try { sessionStorage.setItem("wwn_admin", "1"); } catch (e) {}
    gate.classList.add("hidden");
    dash.classList.remove("hidden");
    renderAll();
  }
  if (window.WWNStore) {
    try {
      if (sessionStorage.getItem("wwn_admin") === "1") { unlock(); }
    } catch (e) {}
  }
  $("#gate-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var v = $("#passcode").value;
    if (v === PASSCODE) { unlock(); }
    else { $("#gate-error").style.display = "block"; $("#passcode").value = ""; $("#passcode").focus(); }
  });
  $("#logout").addEventListener("click", function () {
    try { sessionStorage.removeItem("wwn_admin"); } catch (e) {}
    location.reload();
  });

  // ---------- Render ----------
  function renderAll() {
    renderStats();
    renderArticles();
    renderJustIn();
    renderLive();
    renderBreaking();
    renderSettings();
  }
  function renderStats() {
    var secs = {};
    data.articles.forEach(function (a) { (a.sections || [a.section]).forEach(function (s) { secs[s] = 1; }); });
    $("#stat-articles").textContent = data.articles.length;
    $("#stat-sections").textContent = Object.keys(secs).length;
    $("#stat-justin").textContent = data.justIn.length;
    $("#stat-live").textContent = data.liveUpdates.length;
    $("#saved-note").textContent = store.hasSaved()
      ? "You have unpublished changes saved in this browser. Export JSON below to make them permanent."
      : "No unpublished changes. Showing the site's default content.";
  }
  function renderArticles() {
    var list = $("#article-list");
    list.innerHTML = data.articles.map(function (a) {
      var heroMark = data.settings.heroSlug === a.slug ? ' <b style="color:var(--red)">(Hero)</b>' : "";
      var mrMark = (data.mostRead || []).indexOf(a.slug) !== -1 ? ' <b>· Most Popular</b>' : "";
      return '<li><div class="t"><b>' + esc(a.headline) + "</b>" + heroMark + mrMark +
        "<small>" + esc(SECTION_LABELS[a.section] || a.section) + " · " + esc(a.date) +
        " · Source: " + esc(a.source) + " · /articles/" + esc(a.slug) + ".html</small></div>" +
        '<button class="btn small" data-edit="' + esc(a.slug) + '">Edit</button>' +
        '<button class="btn danger" data-del="' + esc(a.slug) + '">Delete</button></li>';
    }).join("") || '<li>No articles yet.</li>';
    list.querySelectorAll("[data-edit]").forEach(function (b) {
      b.addEventListener("click", function () { openArticleForm(b.getAttribute("data-edit")); });
    });
    list.querySelectorAll("[data-del]").forEach(function (b) {
      b.addEventListener("click", function () {
        var slug = b.getAttribute("data-del");
        var a = data.articles.find(function (x) { return x.slug === slug; });
        if (!a) return;
        if (confirm('Delete "' + a.headline + '"? This cannot be undone except by Reset.')) {
          data.articles = data.articles.filter(function (x) { return x.slug !== slug; });
          data.mostRead = (data.mostRead || []).filter(function (s) { return s !== slug; });
          if (data.settings.heroSlug === slug && data.articles[0]) data.settings.heroSlug = data.articles[0].slug;
          save("Article deleted.");
        }
      });
    });
  }
  function renderJustIn() {
    var list = $("#justin-list");
    list.innerHTML = data.justIn.map(function (it, i) {
      return '<li><div class="t"><b>' + esc(it.time) + "</b>: " + esc(it.text) +
        "<small>Link: " + esc(it.link || "live.html") + "</small></div>" +
        '<button class="btn small" data-ji-edit="' + i + '">Edit</button>' +
        '<button class="btn danger" data-ji-del="' + i + '">Delete</button></li>';
    }).join("") || "<li>No Just In items.</li>";
    list.querySelectorAll("[data-ji-edit]").forEach(function (b) {
      b.addEventListener("click", function () {
        var it = data.justIn[+b.getAttribute("data-ji-edit")];
        editingJustIn = +b.getAttribute("data-ji-edit");
        $("#ji-time").value = it.time; $("#ji-text").value = it.text; $("#ji-link").value = it.link || "live.html";
        $("#ji-form-title").textContent = "Edit Just In item";
        $("#justin-form").scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });
    list.querySelectorAll("[data-ji-del]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (confirm("Delete this Just In item?")) {
          data.justIn.splice(+b.getAttribute("data-ji-del"), 1);
          save("Just In item deleted.");
        }
      });
    });
  }
  function renderLive() {
    var list = $("#live-list");
    list.innerHTML = data.liveUpdates.map(function (u, i) {
      return '<li><div class="t"><b>' + esc(u.time) + ": " + esc(u.headline) + "</b>" +
        "<small>" + esc(u.text) + "</small></div>" +
        '<button class="btn small" data-lv-edit="' + i + '">Edit</button>' +
        '<button class="btn danger" data-lv-del="' + i + '">Delete</button></li>';
    }).join("") || "<li>No live updates.</li>";
    list.querySelectorAll("[data-lv-edit]").forEach(function (b) {
      b.addEventListener("click", function () {
        var u = data.liveUpdates[+b.getAttribute("data-lv-edit")];
        editingLive = +b.getAttribute("data-lv-edit");
        $("#lv-time").value = u.time; $("#lv-headline").value = u.headline; $("#lv-text").value = u.text;
        $("#lv-form-title").textContent = "Edit live update";
        $("#live-form").scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });
    list.querySelectorAll("[data-lv-del]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (confirm("Delete this live update?")) {
          data.liveUpdates.splice(+b.getAttribute("data-lv-del"), 1);
          save("Live update deleted.");
        }
      });
    });
  }
  function renderBreaking() {
    $("#br-text").value = data.breaking.text;
    $("#br-link").value = data.breaking.link;
  }
  function renderSettings() {
    $("#set-name").value = data.settings.siteName;
    $("#set-tagline").value = data.settings.tagline;
    var sel = $("#set-hero");
    sel.innerHTML = data.articles.map(function (a) {
      return '<option value="' + esc(a.slug) + '"' + (data.settings.heroSlug === a.slug ? " selected" : "") +
        ">" + esc(a.headline) + "</option>";
    }).join("");
  }

  // ---------- Article form ----------
  function openArticleForm(slug) {
    var f = $("#article-form");
    f.classList.remove("hidden");
    if (slug) {
      var a = data.articles.find(function (x) { return x.slug === slug; });
      if (!a) return;
      editingSlug = slug;
      $("#af-title-text").textContent = "Edit article";
      $("#af-slug").value = a.slug;
      $("#af-title").value = a.headline;
      $("#af-section").value = a.section;
      $("#af-date").value = a.date;
      $("#af-dek").value = a.dek;
      $("#af-body").value = (a.body || []).join("\\n\\n");
      $("#af-image").value = a.image || "";
      $("#af-caption").value = a.imageCaption || "";
      $("#af-source").value = a.source || "";
      $("#af-source-url").value = a.source_url || "";
      $("#af-hero").checked = data.settings.heroSlug === a.slug;
      $("#af-mostread").checked = (data.mostRead || []).indexOf(a.slug) !== -1;
    } else {
      editingSlug = null;
      $("#af-title-text").textContent = "Add article";
      f.reset();
      $("#af-date").value = todayLong();
      $("#af-section").value = "world";
      $("#af-hero").checked = false;
      $("#af-mostread").checked = false;
    }
    f.scrollIntoView({ behavior: "smooth", block: "center" });
    $("#af-title").focus();
  }
  $("#add-article").addEventListener("click", function () { openArticleForm(null); });
  $("#af-cancel").addEventListener("click", function () {
    $("#article-form").classList.add("hidden");
    editingSlug = null;
  });
  $("#af-title").addEventListener("input", function () {
    if (!editingSlug) $("#af-slug").value = slugify($("#af-title").value);
  });
  $("#article-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var slug = slugify($("#af-slug").value);
    if (!/^[a-z0-9-]+$/.test(slug)) { alert("Slug can only use lower-case letters, numbers and hyphens."); return; }
    var title = $("#af-title").value.trim();
    if (!title) { alert("Headline is required."); return; }
    var section = $("#af-section").value;
    var body = $("#af-body").value.split(/\\n\\s*\\n/).map(function (p) { return p.trim(); }).filter(Boolean);
    var art = {
      slug: slug,
      sections: [section],
      section: section,
      headline: title,
      dek: $("#af-dek").value.trim(),
      date: $("#af-date").value.trim() || todayLong(),
      source: $("#af-source").value.trim() || "Western World News",
      source_url: $("#af-source-url").value.trim(),
      body: body,
      related: [],
      image: $("#af-image").value.trim(),
      imageCaption: $("#af-caption").value.trim() || "Photo: Unsplash"
    };
    var idx = data.articles.findIndex(function (x) { return x.slug === slug; });
    if (editingSlug && editingSlug !== slug) {
      data.articles = data.articles.filter(function (x) { return x.slug !== editingSlug; });
      idx = -1;
    }
    if (idx === -1) {
      // Related: other stories in the same section, newest first (max 3).
      art.related = data.articles.filter(function (x) { return x.section === section; })
        .slice(0, 3).map(function (x) { return x.slug; });
      data.articles.unshift(art);
    } else {
      art.related = data.articles[idx].related || art.related;
      data.articles[idx] = art;
    }
    if ($("#af-hero").checked) data.settings.heroSlug = slug;
    var mr = data.mostRead || [];
    if ($("#af-mostread").checked) {
      if (mr.indexOf(slug) === -1) mr.unshift(slug);
      data.mostRead = mr.slice(0, 5);
    } else {
      data.mostRead = mr.filter(function (s) { return s !== slug; });
    }
    $("#article-form").classList.add("hidden");
    editingSlug = null;
    save("Article saved. It is live on the site in this browser now.");
  });

  // ---------- Just In form ----------
  $("#justin-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var item = {
      time: $("#ji-time").value.trim() || nowStamp(),
      text: $("#ji-text").value.trim(),
      link: $("#ji-link").value.trim() || "live.html"
    };
    if (!item.text) { alert("Text is required."); return; }
    if (editingJustIn >= 0) { data.justIn[editingJustIn] = item; editingJustIn = -1; }
    else { data.justIn.unshift(item); data.justIn = data.justIn.slice(0, 12); }
    $("#ji-text").value = "";
    $("#ji-form-title").textContent = "Add Just In item";
    save("Just In updated.");
  });

  // ---------- Live form ----------
  $("#live-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var u = {
      time: $("#lv-time").value.trim() || nowStamp(),
      headline: $("#lv-headline").value.trim(),
      text: $("#lv-text").value.trim()
    };
    if (!u.headline || !u.text) { alert("Headline and text are required."); return; }
    if (editingLive >= 0) { data.liveUpdates[editingLive] = u; editingLive = -1; }
    else { data.liveUpdates.unshift(u); }
    $("#lv-headline").value = ""; $("#lv-text").value = "";
    $("#lv-form-title").textContent = "Add live update";
    save("Live blog updated.");
  });

  // ---------- Breaking + settings ----------
  $("#breaking-form").addEventListener("submit", function (e) {
    e.preventDefault();
    data.breaking = { text: $("#br-text").value.trim(), link: $("#br-link").value.trim() || "#" };
    save("Breaking banner updated.");
  });
  $("#settings-form").addEventListener("submit", function (e) {
    e.preventDefault();
    data.settings.siteName = $("#set-name").value.trim() || "Western World News";
    data.settings.tagline = $("#set-tagline").value.trim();
    data.settings.heroSlug = $("#set-hero").value;
    save("Settings saved.");
  });

  // ---------- Data: export / import / reset ----------
  $("#export-btn").addEventListener("click", function () {
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "wwn-content.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    toast("Exported wwn-content.json. Keep it to make changes permanent.");
  });
  $("#import-file").addEventListener("change", function (e) {
    var file = e.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var imported = JSON.parse(reader.result);
        if (!imported || !Array.isArray(imported.articles)) throw new Error("bad file");
        if (!confirm("Replace all current content with the imported file?")) return;
        data = store.save(imported);
        renderAll();
        toast("Imported. Content replaced.");
      } catch (err) { alert("That file is not a valid Western World News content export."); }
      e.target.value = "";
    };
    reader.readAsText(file);
  });
  $("#reset-btn").addEventListener("click", function () {
    if (confirm("Reset everything to the site's default content? Your admin changes will be lost.")) {
      store.reset();
      data = store.get();
      renderAll();
      toast("Reset to defaults.");
    }
  });

  // Prefill Just In / Live time fields.
  $("#ji-time").value = nowStamp();
  $("#lv-time").value = nowStamp();
})();"""


# ---------------- Admin page ----------------

def build_admin():
    options = "".join(
        f'<option value="{k}">{v}</option>' for k, v in SECTIONS.items() if k != "live"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Admin | Western World News</title>
<meta name="description" content="Admin panel for Western World News.">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/admin.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23bb1919'/%3E%3Ctext x='16' y='22' font-family='Arial' font-size='16' font-weight='bold' fill='white' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E">
</head>
<body>
<header class="admin-top"><div class="wrap">
<a class="wordmark" href="index.html">Western World <span class="news">News</span></a>
<span class="admin-badge">Admin</span>
<span class="spacer"></span>
<a href="index.html">View site</a>
<button id="logout" type="button">Log out</button>
</div></header>
<main id="main"><div class="wrap">

<div class="gate-card" id="gate">
<h1>Admin login</h1>
<p>Enter the admin passcode to manage the site. (Default passcode: <b>admin123</b>. Change it in assets/js/admin.js. Note: this is a basic gate on a static site, not real server security.)</p>
<form id="gate-form">
<div class="field"><label for="passcode">Passcode</label>
<input id="passcode" type="password" autocomplete="current-password" required></div>
<div class="form-actions"><button class="btn" type="submit">Log in</button></div>
<p class="error" id="gate-error">Wrong passcode. Try again.</p>
</form>
</div>

<div id="dashboard" class="hidden">
<h1 class="section-head"><span class="tag">&#9632;</span> Dashboard</h1>
<div class="notice"><b>How saving works</b>
Changes you save here apply across the whole site <b>immediately in this browser</b> (they are stored in this browser's localStorage).
To make them permanent for everyone, use <b>Export JSON</b> below and send the file to musu, or save it in the site folder as <b>content-export.json</b> and rebuild the site. Until then, other browsers still see the default content.</div>
<div class="admin-grid">
<div class="stat"><b id="stat-articles">0</b><span>Articles</span></div>
<div class="stat"><b id="stat-sections">0</b><span>Sections in use</span></div>
<div class="stat"><b id="stat-justin">0</b><span>Just In items</span></div>
<div class="stat"><b id="stat-live">0</b><span>Live updates</span></div>
</div>
<p id="saved-note" style="color:var(--muted)"></p>

<section class="panel"><h2>Articles</h2><div class="body">
<ul class="admin-list" id="article-list"></ul>
<button class="btn" id="add-article" type="button">+ Add article</button>
<form id="article-form" class="hidden" style="margin-top:1.2rem">
<h3 id="af-title-text" style="font-family:var(--sans);margin:0 0 0.8rem">Add article</h3>
<div class="form-grid">
<div class="field"><label for="af-title">Headline *</label><input id="af-title" type="text" required></div>
<div class="field"><label for="af-slug">URL slug * <span class="hint">lower-case letters, numbers, hyphens. Auto-filled from the headline</span></label><input id="af-slug" type="text" required></div>
<div class="field"><label for="af-section">Section</label><select id="af-section">{options}</select></div>
<div class="field"><label for="af-date">Date</label><input id="af-date" type="text" placeholder="20 November 2026"></div>
<div class="field full"><label for="af-dek">Summary (shows on the homepage and section pages)</label><textarea id="af-dek" style="min-height:70px"></textarea></div>
<div class="field full"><label for="af-body">Article text <span class="hint">one paragraph per block. Leave a blank line between paragraphs</span></label><textarea id="af-body"></textarea></div>
<div class="field"><label for="af-image">Photo URL <span class="hint">leave empty for the navy placeholder tile</span></label><input id="af-image" type="url" placeholder="https://images.unsplash.com/photo-..."></div>
<div class="field"><label for="af-caption">Photo caption / credit</label><input id="af-caption" type="text" placeholder="Photo: Unsplash"></div>
<div class="field"><label for="af-source">Source name</label><input id="af-source" type="text" placeholder="Reuters"></div>
<div class="field"><label for="af-source-url">Source link</label><input id="af-source-url" type="url" placeholder="https://..."></div>
<div class="field full"><div class="check-row">
<label><input id="af-hero" type="checkbox"> Make this the homepage hero story</label>
<label><input id="af-mostread" type="checkbox"> Show in Most Popular</label>
</div></div>
</div>
<div class="form-actions"><button class="btn" type="submit">Save article</button>
<button class="btn ghost" id="af-cancel" type="button">Cancel</button></div>
</form>
</div></section>

<section class="panel"><h2>Breaking news banner</h2><div class="body">
<form id="breaking-form">
<div class="form-grid">
<div class="field full"><label for="br-text">Banner text</label><input id="br-text" type="text"></div>
<div class="field full"><label for="br-link">Link <span class="hint">e.g. articles/my-story.html or a full https:// link</span></label><input id="br-link" type="text"></div>
</div>
<div class="form-actions"><button class="btn" type="submit">Save banner</button></div>
</form>
</div></section>

<section class="panel"><h2>Just In feed</h2><div class="body">
<ul class="admin-list" id="justin-list"></ul>
<form id="justin-form">
<h3 id="ji-form-title" style="font-family:var(--sans);margin:0 0 0.8rem">Add Just In item</h3>
<div class="form-grid">
<div class="field"><label for="ji-time">Time</label><input id="ji-time" type="text" placeholder="20 Nov, 10:33"></div>
<div class="field"><label for="ji-link">Link</label><input id="ji-link" type="text" value="live.html"></div>
<div class="field full"><label for="ji-text">Text *</label><input id="ji-text" type="text" required></div>
</div>
<div class="form-actions"><button class="btn" type="submit">Save Just In item</button></div>
</form>
</div></section>

<section class="panel"><h2>Live blog</h2><div class="body">
<ul class="admin-list" id="live-list"></ul>
<form id="live-form">
<h3 id="lv-form-title" style="font-family:var(--sans);margin:0 0 0.8rem">Add live update</h3>
<div class="form-grid">
<div class="field"><label for="lv-time">Time</label><input id="lv-time" type="text" placeholder="20 Nov, 10:33"></div>
<div class="field full"><label for="lv-headline">Headline *</label><input id="lv-headline" type="text" required></div>
<div class="field full"><label for="lv-text">Update text *</label><textarea id="lv-text" style="min-height:80px" required></textarea></div>
</div>
<div class="form-actions"><button class="btn" type="submit">Save live update</button></div>
</form>
</div></section>

<section class="panel"><h2>Site settings</h2><div class="body">
<form id="settings-form">
<div class="form-grid">
<div class="field"><label for="set-name">Site name</label><input id="set-name" type="text"></div>
<div class="field"><label for="set-tagline">Tagline</label><input id="set-tagline" type="text"></div>
<div class="field full"><label for="set-hero">Homepage hero story</label><select id="set-hero"></select></div>
</div>
<div class="form-actions"><button class="btn" type="submit">Save settings</button></div>
</form>
</div></section>

<section class="panel"><h2>Data: export, import, reset</h2><div class="body">
<p>Export downloads the site's full content as <b>wwn-content.json</b>. To make admin changes permanent for all visitors, send that file to musu, or save it in the site folder as <b>content-export.json</b> and re-run the build script (<b>tools/build_site.py</b>). The static pages are then regenerated with your content, including a real page for every new article.</p>
<div class="form-actions">
<button class="btn" id="export-btn" type="button">Export JSON</button>
<label class="btn ghost" for="import-file" style="cursor:pointer">Import JSON</label>
<input id="import-file" type="file" accept="application/json,.json" class="hidden">
<button class="btn danger" id="reset-btn" type="button">Reset to defaults</button>
</div>
</div></section>

</div>
</div></main>
<footer class="site-footer"><div class="wrap">
<p class="fineprint"><span>&copy; 2026 Western World News (westernworldnews.com). Admin panel: passcode gate only, not real server security.</span><span><a href="index.html">Back to site</a></span></p>
</div></footer>
<div class="toast" id="toast" role="status"></div>
<script src="assets/js/content.js"></script>
<script src="assets/js/admin.js"></script>
</body>
</html>
"""


# ---------------- README ----------------

README_MD = """# Western World News — westernworldnews.com

A plain static news website (HTML + CSS + JavaScript) with a publisher-style
design and an admin panel. No build step needed to view it, no database, no
framework. Upload the contents of this folder to any static host (GitHub
Pages, Netlify, Cloudflare Pages, Hostinger) and it works.

## What's in the design (v2)

- Dark navy masthead with the wordmark and tagline, thin top utility bar
  (date, Live indicator, working search box that filters articles).
- Red BREAKING bar with a scrolling Just In ticker (pauses on hover).
- Big photo-led hero story, section blocks with photos (Europe first),
  numbered **Most Read** sidebar (top 5), a **Watch** strip, an
  **Analysis** block and a full multi-column footer.
- Serif display headlines (Georgia) + clean sans body — the broadsheet look.
- Hamburger navigation on mobile; responsive throughout.
- Photos are **real photos that match each story** \u2014 freely licensed Wikimedia Commons pictures of the actual place or institution (Kyiv, the European Parliament, Shenzhen, the US Capitol, Wall Street, the Peace Palace), and openly licensed Unsplash images used as clearly labelled illustrations where no real photo of the subject exists. Every caption says honestly what the photo shows. Stories without a suitable photo get the navy WWN gradient tile instead of a misleading image.

## Folder structure

```
western-world-news/
├── index.html                  Homepage: breaking ticker, hero, Just In,
│                               Most Read, Europe/World/US & Politics,
│                               Watch strip, live teaser, newsletter,
│                               Analysis, Business & Finance
├── world.html / europe.html / us.html / politics.html
├── war-conflict.html / business-finance.html / sport.html / culture.html
├── live.html                   Live blog (Ukraine war, rolling updates)
├── about.html / contact.html / privacy.html
├── admin.html                  Admin panel (passcode gate, see below)
├── articles/                   One HTML page per story
├── assets/
│   ├── css/style.css           All site styling
│   ├── css/admin.css           Admin panel styling
│   └── js/
│       ├── content.js          Central content store (default content +
│       │                       localStorage merge used by every page)
│       ├── main.js             Dateline, search, hamburger, renders
│       │                       dynamic regions from the content store
│       └── admin.js            Admin panel logic (passcode "admin123")
├── data/articles.json          All article text (source of truth for the
│                               build; updated by tools/auto_publish.py)
├── tools/build_site.py         Generator — re-run to rebuild every page
├── tools/auto_publish.py       Hourly auto-publisher (RSS feeds → new
│                               stories; see "Automatic publishing" below)
├── .github/workflows/          auto-publish.yml — GitHub Actions schedule
├── content-export.json         (optional) admin export; if present, the
│                               build script uses it as the content source
├── sitemap.xml / robots.txt    (robots.txt blocks /admin.html)
└── README.md                   This file
```

## Admin panel — how it works

Open **admin.html** and enter the passcode:

- **Default passcode: `admin123`** (change it in `assets/js/admin.js`).
- The dashboard shows article/section/Just In/live counts.
- You can **add, edit and delete articles** (headline, section, date,
  summary, body, photo URL + caption, source name + link, hero / Most
  Read flags), **edit the breaking banner**, **add/edit/delete Just In
  items and live-blog updates**, and **edit site settings** (site name,
  tagline, hero story).
- **Changes save to this browser's localStorage and apply across the
  whole site immediately** — but only in this browser.

### Honest limits (read this)

- **The passcode is a basic gate, not real security.** This is a static
  site: anyone who can open the files can read the content and the
  passcode in `admin.js`. Do not use it to protect anything secret.
- **Admin edits are per-browser** until they are made permanent (below).
  Visitors on other browsers/devices still see the default content.
- **New articles added in the admin appear in lists, search, Most Read
  and the hero immediately, but their full article page does not exist
  as a file yet** — the link will 404 until the site is rebuilt (below).

### Making admin changes permanent

1. In the admin, click **Export JSON** — it downloads `wwn-content.json`.
2. Send that file to musu, **or** save it in this folder as
   `content-export.json` and run `python3 tools/build_site.py`.
3. The script regenerates every static page from your exported content,
   including a real page for each new article, then the updated files
   are committed/pushed as usual.

## Seed content — read this first

The articles in `articles/` are the current front page, refreshed on the evening of 20 November 2026 with verified stories from 19\u201320 November 2026 (the Kyiv missile strikes, the EU\u2013UK reset deal, the Shenzhen summit fallout, the Gaza Yellow Line raid, the US Congress records fight, the Wall Street sell-off, the Nations League draw, the ICJ\u2019s Myanmar genocide ruling, and RAYE\u2019s Grammy nominations).

- Every story is an **original summary written in our own words** — nothing
  is copied from another publication.
- Every story **credits its source by name and links to the original
  article** (CNN, The Times, Al Jazeera, Reuters, Associated Press).
- **Replace this seed content with fresh daily posts.** News goes stale in
  hours: the homepage hero, the Just In feed and the live blog must be
  updated every day. Do not leave the 20 November 2026 stories on the
  homepage once newer news exists.

## Watch strip — honest note

The "Watch" cards link to the live blog and full articles. There is no
real video yet. Replace the cards with real video embeds when video
exists; until then they are clearly a design element, not a video player.

## Not yet connected — before launch

- **Newsletter form is a front-end demo only.** It shows a thank-you
  message but sends nothing. Connect a mailing service (e.g. Buttondown,
  Mailchimp, ConvertKit) before launch.
- **Contact email addresses** (tips@ / ads@westernworldnews.com) are
  placeholders — set up the mailboxes first.
- **Privacy policy** is a stub — complete it before adding analytics or ads.
- **Domain**: westernworldnews.com \u2014 live since 20 Nov 2026 (GitHub Pages, DNS via Hostinger).
- **Ads**: none included yet. Add ad slots only after traffic exists.
- **GitHub**: the site is pushed to github.com/pintuguptaji/western-world-news (branch main); push updates with the GitHub connector.

## Rebuilding

Run `python3 tools/build_site.py` (or `python3 /tmp/build_site_v2.py`).
To change the shared header, footer, navigation or design, edit the
script and re-run it — or edit the HTML/CSS files directly; they are
plain and self-contained. All article text lives in `data/articles.json`
(the script reads it at build time); `WWN_OUT` env var overrides the
output folder (used by the automatic publisher's tests).

## Automatic publishing (GitHub Actions, no approval needed)

`.github/workflows/auto-publish.yml` runs every hour inside GitHub:
`tools/auto_publish.py` fetches trusted RSS feeds (BBC, Al Jazeera,
The Guardian, Euronews, France 24, DW), adds up to 4 verified new
stories (max 12/day) to `data/articles.json`, refreshes the Just In
feed, rebuilds the site and pushes — using only the automatic
`GITHUB_TOKEN`. Auto stories are short summaries of the source's own
report with a "Read the full story" link, and the photo is the feed's
own image for that story (verified to load) or no photo at all.
Test locally first: `python3 tools/auto_publish.py --dry-run`.

One-time setup (repo owner): Settings → Actions → General → Workflow
permissions → **Read and write permissions** → Save. Without that, the
push step fails with a 403.
"""


# ---------------- Write everything ----------------

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return full


def load_export():
    """If content-export.json exists, use it as the content source."""
    global STORIES, JUST_IN, LIVE_UPDATES, MOST_READ
    exp_path = os.path.join(OUT, "content-export.json")
    if not os.path.exists(exp_path):
        return None
    with open(exp_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("articles"), list):
        raise SystemExit("content-export.json is not a valid WWN content export.")
    stories = []
    for a in data["articles"]:
        stories.append({
            "slug": a["slug"],
            "sections": a.get("sections") or [a.get("section", "world")],
            "section": a.get("section", "world"),
            "headline": a["headline"],
            "dek": a.get("dek", ""),
            "date": a.get("date", ""),
            "source": a.get("source", "Western World News"),
            "source_url": a.get("source_url", ""),
            "body": a.get("body") or [],
            "related": a.get("related") or [],
            "image": a.get("image", ""),
            "imageCaption": a.get("imageCaption", ""),
        })
    STORIES = stories
    JUST_IN = [(it.get("time", ""), it.get("text", ""), None) for it in data.get("justIn", [])]
    LIVE_UPDATES = [(u.get("time", ""), u.get("headline", ""), u.get("text", "")) for u in data.get("liveUpdates", [])]
    if data.get("mostRead"):
        MOST_READ = list(data["mostRead"])
    return data


def main():
    global BY_SLUG
    export = load_export()
    if export is not None:
        print("Using content-export.json as the content source.")
    BY_SLUG = {s["slug"]: s for s in STORIES}
    os.makedirs(os.path.join(OUT, "articles"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "tools"), exist_ok=True)
    files = []

    # CSS
    files.append(write("assets/css/style.css", CSS))
    files.append(write("assets/css/admin.css", ADMIN_CSS))

    # Content store + front-end JS + admin JS
    content_js = CONTENT_JS.replace("__DEFAULT_JSON__", json.dumps(default_content(), ensure_ascii=False, indent=2))
    files.append(write("assets/js/content.js", content_js))
    files.append(write("assets/js/main.js", MAIN_JS))
    files.append(write("assets/js/admin.js", ADMIN_JS))

    # Pages
    files.append(write("index.html", build_index()))
    for section in ["world", "europe", "us", "politics", "war-conflict", "business-finance", "sport", "culture"]:
        files.append(write(section + ".html", build_section(section, section + ".html")))
    files.append(write("live.html", build_live()))
    for s in STORIES:
        files.append(write("articles/" + s["slug"] + ".html", build_article(s)))
    files.append(write("admin.html", build_admin()))

    files.append(write("about.html", build_info(
        "about", "About Western World News",
        "About Western World News: independent news from the West and the world.",
        "About us",
        ["Western World News is an independent news site covering worldwide news with a main focus on Western and European politics, war and breaking news, plus a small Business &amp; Finance section.",
         "We write our stories in our own words, based on reporting from trusted sources, and we always credit and link the original reporting. We do not copy articles word for word, and we do not publish rumors or unconfirmed claims as fact.",
         "The site is free to read. There is no paywall at launch.",
         "Contact us via the contact page."])))
    files.append(write("contact.html", build_info(
        "contact", "Contact Western World News",
        "Contact Western World News: news tips, corrections and advertising inquiries.",
        "Contact",
        ["News tips, corrections and general inquiries: tips@westernworldnews.com (mailbox to be set up. See README.md).",
         "For corrections, please include the story headline and the fact to be corrected. We correct errors promptly and transparently.",
         "Advertising inquiries: ads@westernworldnews.com (mailbox to be set up. See README.md)."])))
    files.append(write("privacy.html", build_info(
        "privacy", "Privacy policy | Western World News",
        "Privacy policy for Western World News.",
        "Privacy policy",
        ["Western World News respects your privacy. This page will be completed before launch with the site's full privacy policy.",
         "Newsletter: if you sign up for our briefing, we use your email address only to send the briefing. You can unsubscribe at any time. We do not sell personal data.",
         "Analytics and advertising: this static site currently uses no tracking. If analytics or advertising are added, this policy will be updated before they go live."])))

    # robots.txt — keep the admin panel out of search engines.
    files.append(write("robots.txt",
        "User-agent: *\nAllow: /\nDisallow: /admin.html\n\nSitemap: " + BASE + "/sitemap.xml\n"))

    # sitemap.xml (admin deliberately excluded)
    urls = ["", "world.html", "europe.html", "us.html", "politics.html",
            "war-conflict.html", "business-finance.html", "sport.html",
            "culture.html", "live.html", "about.html", "contact.html", "privacy.html"]
    urls += ["articles/" + s["slug"] + ".html" for s in STORIES]
    today = datetime.date.today().isoformat()
    entries = "".join(
        f"  <url><loc>{BASE}/{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls
    )
    files.append(write("sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "</urlset>\n"))

    files.append(write("README.md", README_MD))

    # Keep the generator in the repo so the site can be rebuilt anywhere.
    import shutil
    try:
        shutil.copy(__file__, os.path.join(OUT, "tools", "build_site.py"))
        files.append(os.path.join(OUT, "tools", "build_site.py"))
    except Exception as e:
        print("NOTE: could not copy generator into tools/:", e)

    print(f"Wrote {len(files)} files to {OUT}")
    for f in sorted(files):
        print(" -", os.path.relpath(f, OUT))


if __name__ == "__main__":
    main()
