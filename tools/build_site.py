#!/usr/bin/env python3
"""Build script for Western World News (static site).
Generates all HTML pages, sitemap.xml and robots.txt from
data/articles.json (see _load_data below). Run: python3 /tmp/build_site.py
Content refreshed automatically: short summaries of real stories, each
credited to its source with a link. See README.md in the site root.
"""
import datetime
import os

OUT = os.environ.get("WWN_OUT", os.path.expanduser("~/workspace/western-world-news"))
BASE = "https://westernworldnews.com"

# Google Search Console ownership verification. Paste the code Google gives
# (Search Console > Add property > HTML tag) here, rebuild and push.
# Leave empty until Google gives you a code.
GOOGLE_SITE_VERIFICATION = "NygudsKNLm9w7kCNUvEYzlOYcf3eSNafgLbIvtD17Gc"

# Google Analytics 4 measurement ID. Paste the ID (Analytics > Admin >
# Data Streams > Web stream, looks like G-XXXXXXXXXX) here, rebuild and
# push. Leave empty until Google gives you an ID.
GOOGLE_ANALYTICS_ID = "G-1FTJR8MHNF"

# Newsletter (Buttondown — chosen 2026-11-27, free tier). Set this to the
# Buttondown username (the last part of buttondown.com/<username>) once the
# account exists, then rebuild. While it is empty, the newsletter forms
# show an honest "subscriptions open soon" state and never pretend to
# subscribe anyone. No API key is needed: the embed form posts to
# https://buttondown.com/api/emails/embed-subscribe/<username> and
# Buttondown handles double opt-in and its own confirmation page.
NEWSLETTER_BUTTONDOWN_USERNAME = "pintu"

# Contact form endpoint (Formspree recommended — free tier, no backend).
# How to connect it: create a free form at https://formspree.io (sign up,
# create a form, copy its endpoint, which looks like
# https://formspree.io/f/xxxxxxxx), paste it here, rebuild and push.
# While this is empty, the contact page shows the form disabled with an
# honest note pointing at the email address instead — it never pretends
# to send a message. The honeypot field ("website") catches simple bots;
# Formspree also filters spam on its side.
CONTACT_FORM_ENDPOINT = ""

NAV = [
    ("index.html", "Home"),
    ("world.html", "World"),
    ("us.html", "US"),
    ("europe.html", "Europe"),
    ("politics.html", "Politics"),
    ("war-conflict.html", "War &amp; Conflict"),
    ("business-finance.html", "Business"),
    ("technology.html", "Technology"),
    ("culture.html", "Culture"),
]

SECTIONS = {
    "world": "World",
    "europe": "Europe",
    "us": "US",
    "politics": "Politics",
    "war-conflict": "War &amp; Conflict",
    "business-finance": "Business &amp; Finance",
    "technology": "Technology",
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


# --- AdSense readiness helpers: plain labels, dates, alt text, schema ---
# Plain (unescaped) section labels for JSON-LD and other non-HTML contexts.
SECTION_LABELS_PLAIN = {k: v.replace("&amp;", "&") for k, v in SECTIONS.items()}

_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%B %d", "%b %d")


def _parse_date(date_str):
    """Parse an article date string to a datetime.date, or None."""
    if not date_str:
        return None
    text = str(date_str).strip()
    for fmt in _DATE_FORMATS:
        try:
            d = datetime.datetime.strptime(text, fmt)
            year = d.year if "%Y" in fmt else datetime.date.today().year
            return datetime.date(year, d.month, d.day)
        except ValueError:
            continue
    return None


def _iso_date(date_str):
    d = _parse_date(date_str)
    return d.isoformat() if d else datetime.date.today().isoformat()


def _alt_for(slug, cap):
    """Alt text for a story image: the descriptive part of its caption, or
    the article headline when there is no useful caption. Never empty, so
    no <img> on the site is ever rendered without alt text."""
    base = (cap or "").split(". Illustrative")[0]
    if ". Photo:" in base:
        base = base.split(". Photo:")[0]
    base = base.strip()
    if base.startswith("Photo:"):
        base = ""
    if base:
        return base
    if slug in BY_SLUG:
        return BY_SLUG[slug]["headline"]
    return "Western World News"


def _org_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Western World News",
        "url": BASE,
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>")


def _newsarticle_jsonld(s):
    data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": s["headline"],
        "datePublished": _iso_date(s["date"]),
        "dateModified": _iso_date(s["date"]),
        "author": {"@type": "Organization", "name": "Western World News", "url": BASE},
        "publisher": {"@type": "Organization", "name": "Western World News", "url": BASE},
        "mainEntityOfPage": BASE + "/articles/" + s["slug"] + ".html",
    }
    img = s.get("image")
    if not img and s["slug"] in IMAGES:
        img = uimg(IMAGES[s["slug"]][0], 1200)
    if img:
        data["image"] = img
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>")


def _breadcrumb_jsonld(items):
    elements = []
    for i, (name, url) in enumerate(items, start=1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = url
        elements.append(item)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": elements}
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>")


def _breadcrumbs_html(items):
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f"<span>{label}</span>")
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def _load_data():
    path = os.path.join(OUT, "data", "articles.json")
    with open(path, encoding="utf-8") as f:
        return _clean_obj(_json.load(f))

_DATA = _load_data()
STORIES = _DATA["articles"]
JUST_IN = [(it["time"], it["text"], it.get("link")) for it in _DATA.get("justIn", [])]
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



CSS = """/* Western World News: redesign v4 — premium navy/white editorial design.
   Headlines: Merriweather. Body/navigation: Inter (Google Fonts, with
   Georgia/Arial fallbacks). Flat navy, white and light-gray surfaces;
   no heavy gradients, no excess rounding, no clutter. */

:root {
  --navy: #172B45;
  --navy2: #243B53;
  --red: #D93036;
  --red-dark: #A92529;
  --bg: #F5F7FA;
  --gray: #E9EDF2;
  --line: #E5E7EB;
  --text: #303B49;
  --muted: #718096;
  --serif: "Merriweather", Georgia, "Times New Roman", serif;
  --sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: var(--sans);
  color: var(--text);
  background: #fff;
  line-height: 1.55;
  font-size: 16px;
}

h1, h2, h3, h4 { font-family: var(--serif); color: var(--navy); }
a { color: var(--navy); text-decoration: none; }
a:hover { color: var(--red); text-decoration: underline; }
img { max-width: 100%; display: block; height: auto; }
/* Grid/flex children must be allowed to shrink below their content's
   intrinsic width, otherwise a large image forces its track wider than
   the viewport (horizontal scroll on mobile). */
.top-hero > *, .card-grid > *, .split-sections > *, .section-grid > *,
.article-layout > *, .lead-card > *, .top-hero-main, .stack-card, .card, .lead-card,
.latest-item > * { min-width: 0; }
figure { margin: 0; }
figcaption { font-size: 0.78rem; color: var(--muted); padding: 0.35rem 0 0; line-height: 1.4; }

.wrap { max-width: 1760px; margin: 0 auto; padding: 0 1rem; }
.sr-only { position: absolute; left: -9999px; }
.skip-link { position: absolute; left: -999px; top: 0; background: var(--red); color: #fff; padding: 0.5rem 1rem; z-index: 300; }
.skip-link:focus { left: 0; }

.brand-name { font-family: var(--serif); font-size: 1.9rem; font-weight: 900; letter-spacing: -0.01em; line-height: 1.05; color: var(--navy); white-space: nowrap; }
.brand-name span { color: var(--red); }
.brand-name:hover { text-decoration: none; color: var(--navy); }
.social-links { display: flex; gap: 0.4rem; }
.social-links a { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border: 1px solid var(--line); border-radius: 50%; color: var(--navy); }
.social-links a:hover { background: var(--navy); color: #fff; text-decoration: none; border-color: var(--navy); }
.social-links svg { width: 15px; height: 15px; display: block; }

/* ---------- Sticky navy header: brand, nav, search, subscribe ---------- */
.site-header { position: sticky; top: 0; z-index: 100; background: var(--navy); }
.header-row { display: flex; align-items: center; gap: 0.8rem; padding-top: 0; padding-bottom: 0; }
.brand-lockup { flex-shrink: 0; padding: 0.55rem 0.6rem 0.55rem 0; line-height: 1; }
.nav-wordmark { font-family: var(--serif); font-size: 1.45rem; font-weight: 900; color: #fff; white-space: nowrap; display: block; }
.nav-wordmark span { color: var(--red); }
.nav-wordmark:hover { text-decoration: none; color: #fff; }
.nav-tagline { margin: 0.3rem 0 0; font-size: 0.72rem; color: rgba(255,255,255,0.72); font-weight: 600; letter-spacing: 0.05em; white-space: nowrap; }
.main-nav { flex: 1; min-width: 0; }
.main-nav ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; }
.main-nav ul::-webkit-scrollbar { display: none; }
.main-nav a { display: block; color: #fff; padding: 0.75rem 0.65rem; font-size: 0.95rem; font-weight: 600; white-space: nowrap; border-bottom: 3px solid transparent; }
.main-nav a:hover { color: #fff; background: var(--navy2); text-decoration: none; }
.main-nav a.active { color: #fff; background: var(--navy2); border-bottom-color: var(--red); }
.nav-toggle { display: none; background: none; border: 0; color: #fff; font-size: 1.5rem; padding: 0.4rem 0.5rem; cursor: pointer; line-height: 1; }
.header-actions { display: flex; align-items: center; gap: 0.7rem; margin-left: auto; flex-shrink: 0; }
.subscribe-btn { background: var(--red); color: #fff; font-weight: 800; font-size: 0.92rem; padding: 0.55rem 1.1rem; border-radius: 3px; white-space: nowrap; }
.subscribe-btn:hover { background: var(--red-dark); color: #fff; text-decoration: none; }
.search-box { position: relative; display: flex; align-items: center; }
.search-toggle { background: none; border: 0; padding: 0.45rem; cursor: pointer; color: #fff; line-height: 0; }
.search-toggle:hover { color: #fff; }
.search-toggle svg { width: 20px; height: 20px; display: block; }
.search-box input {
  background: #fff; border: 1px solid transparent; color: var(--text);
  border-radius: 4px; padding: 0.45rem 0; font-size: 0.9rem; width: 0; opacity: 0; outline: none;
  transition: width 0.2s ease, opacity 0.2s ease, padding 0.2s ease;
}
.search-box.open input { width: 190px; opacity: 1; padding: 0.45rem 0.8rem; border-color: var(--line); }
.search-box input::placeholder { color: #999; }
.search-results {
  display: none; position: absolute; right: 0; top: 115%; width: 320px; max-width: 90vw;
  background: #fff; color: var(--text); border: 1px solid var(--line); border-radius: 4px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.18); z-index: 200; overflow: hidden;
}
.search-results.open { display: block; }
.search-results a { display: block; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--line); font-size: 0.92rem; color: var(--text); }
.search-results a:last-child { border-bottom: 0; }
.search-results a:hover { background: var(--bg); text-decoration: none; }
.search-results a small { display: block; color: var(--red); font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
.search-results .none { padding: 0.7rem 0.8rem; color: var(--muted); font-size: 0.9rem; }
@media (max-width: 1080px) {
  .nav-toggle { display: block; }
  .main-nav { order: 4; flex-basis: 100%; }
  .main-nav ul { display: none; flex-direction: column; overflow-x: visible; }
  .main-nav.open ul { display: flex; }
  .main-nav a { padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.12); }
  .main-nav a.active { border-bottom-color: var(--red); }
  .header-row { flex-wrap: wrap; padding-top: 0.3rem; padding-bottom: 0.3rem; }
  .search-box.open input { width: 150px; }
  .nav-wordmark { font-size: 1.2rem; }
  .nav-tagline { display: none; }
}

/* ---------- Layout ---------- */
main { padding: 0 0 2rem; }
main > .wrap { padding-top: 1.4rem; }
.section-head {
  font-family: var(--serif); font-size: 1.35rem; font-weight: 900; color: var(--navy);
  border-bottom: 2px solid var(--navy); padding-bottom: 0.45rem; margin: 0 0 1.1rem;
  display: flex; align-items: baseline; justify-content: space-between; gap: 1rem;
}
.section-head a { color: var(--navy); }
.section-head a:hover { color: var(--red); }
.section-head .view-all { font-family: var(--sans); font-size: 0.85rem; font-weight: 700; color: var(--red); white-space: nowrap; }
.kicker { color: var(--red); font-weight: 700; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; }
.byline { color: var(--muted); font-size: 0.85rem; margin: 0.5rem 0 0; }
.byline time { font-weight: 600; color: var(--text); }
.byline a { color: var(--red); font-weight: 700; }
.section-block { margin: 0 0 2.4rem; }
.section-desc { color: var(--muted); margin: -0.6rem 0 1.1rem; font-size: 0.95rem; }

/* ---------- Breadcrumbs ---------- */
.breadcrumbs { font-size: 0.85rem; color: var(--muted); margin: 0 0 1rem; }
.breadcrumbs a { color: var(--muted); }
.breadcrumbs a:hover { color: var(--red); }
.breadcrumbs span { color: var(--navy); font-weight: 600; }

/* ---------- Trending ticker strip ---------- */
.trend-strip { display: flex; align-items: center; gap: 1rem; background: #fff; border-bottom: 1px solid var(--line); padding: 0.55rem 0; margin: 0 0 1.3rem; }
.trend-badge { background: var(--red); color: #fff; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.32rem 0.65rem; border-radius: 2px; white-space: nowrap; flex-shrink: 0; }
.trend-live { display: flex; align-items: center; gap: 0.35rem; margin-left: auto; color: var(--red); font-weight: 800; font-size: 0.85rem; letter-spacing: 0.04em; text-transform: uppercase; white-space: nowrap; flex-shrink: 0; }
.trend-live:hover { color: var(--red-dark); text-decoration: none; }
.trend-live .live-dot { margin-right: 0; }
.ticker { overflow: hidden; flex: 1; min-width: 0; mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent); -webkit-mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent); }
.ticker-track { display: inline-flex; gap: 2.5rem; white-space: nowrap; animation: ticker 60s linear infinite; will-change: transform; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-track a, .ticker-track span { font-size: 0.9rem; color: var(--text); font-weight: 600; }
.ticker-track a:hover { color: var(--red); }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (max-width: 700px) {
  .ticker { overflow-x: auto; mask-image: none; -webkit-mask-image: none; scrollbar-width: none; }
  .ticker::-webkit-scrollbar { display: none; }
  .ticker-track { animation: none; }
  .trend-strip { gap: 0.7rem; }
}

/* ---------- Homepage top hero: intro + top story + stacked stories ---------- */
.top-hero { display: grid; grid-template-columns: 1fr; gap: 1.6rem; margin: 0 0 1.2rem; }
@media (min-width: 1100px) { .top-hero { grid-template-columns: 1.45fr 1.2fr 1fr; gap: 1.5rem; align-items: stretch; } }

/* Left: brand statement, like a newspaper masthead block. */
.top-hero-intro { display: flex; flex-direction: column; justify-content: center; padding: 0.6rem 0.4rem 0.6rem 0; background-image: radial-gradient(#E4EAF1 1.2px, transparent 1.2px); background-size: 15px 15px; }
.top-hero-title { font-family: var(--serif); font-size: 2.5rem; line-height: 1.12; margin: 0 0 0.9rem; font-weight: 900; color: var(--navy); }
@media (min-width: 1100px) { .top-hero-title { font-size: 3.05rem; } }
.top-hero-pulse { color: var(--red); margin: 0 0 1.1rem; }
.top-hero-pulse svg { width: 64px; height: 18px; display: block; }
.top-hero-intro .lede { font-size: 1.02rem; color: var(--text); line-height: 1.6; margin: 0 0 1.4rem; max-width: 34rem; }
.btn-red { display: inline-block; background: var(--red); color: #fff; font-weight: 800; font-size: 1rem; padding: 0.75rem 1.5rem; border-radius: 3px; align-self: flex-start; }
.btn-red:hover { background: var(--red-dark); color: #fff; text-decoration: none; }

/* Center: large top-story card, navy body under the photo. */
.top-hero-main { background: var(--navy); border-radius: 12px; overflow: hidden; box-shadow: 0 6px 24px rgba(23,43,69,0.18); display: flex; flex-direction: column; }
.top-hero-media { position: relative; display: block; overflow: hidden; }
.top-hero-media img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.top-hero-media .art { aspect-ratio: 16 / 9; }
.top-story-badge { position: absolute; left: 0.9rem; bottom: 0.9rem; background: var(--red); color: #fff; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.3rem 0.6rem; border-radius: 2px; }
.top-hero-body { padding: 1.1rem 1.2rem 1.25rem; }
.top-hero-body h1 { font-size: 1.5rem; line-height: 1.25; margin: 0 0 0.55rem; font-weight: 900; color: #fff; }
.top-hero-body h1 a { color: #fff; }
.top-hero-body h1 a:hover { color: #fff; }
.top-hero-body .dek { color: rgba(255,255,255,0.85); font-size: 0.98rem; line-height: 1.55; margin: 0 0 0.7rem; }
.top-hero-body .byline { color: rgba(255,255,255,0.65); font-size: 0.85rem; margin: 0; }
.top-hero-body .byline time { color: rgba(255,255,255,0.85); }
.top-hero-body .byline a { color: #fff; }

/* Right: four stacked stories, one per top section. */
.top-hero-side { display: flex; flex-direction: column; gap: 0.85rem; justify-content: space-between; }
.stack-card { display: flex; gap: 0.85rem; background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 0.65rem; flex: 1; align-items: center; }
.stack-thumb { width: 120px; height: 100px; flex-shrink: 0; display: block; overflow: hidden; border-radius: 4px; }
.stack-thumb img, .stack-thumb .art { width: 100%; height: 100%; object-fit: cover; }
.stack-thumb .art { aspect-ratio: auto; }
.stack-body { min-width: 0; }
.stack-body p { margin: 0 0 0.2rem; }
.stack-kicker { font-weight: 800; font-size: 0.72rem; letter-spacing: 0.09em; text-transform: uppercase; }
.stack-card h3 { font-size: 0.98rem; line-height: 1.3; margin: 0 0 0.3rem; font-weight: 700; }
.stack-card h3 a { color: var(--navy); }
.stack-card h3 a:hover { color: var(--red); }
.stack-meta { margin: 0; color: var(--muted); font-size: 0.82rem; }

/* ---------- Category quick bar ---------- */
.quick-bar { display: grid; grid-template-columns: repeat(4, 1fr); background: var(--navy); border-radius: 8px; margin: 0 0 1.7rem; overflow: hidden; }
.quick-bar a { display: flex; align-items: center; justify-content: center; gap: 0.6rem; color: #fff; font-weight: 800; font-size: 0.95rem; letter-spacing: 0.04em; text-transform: uppercase; padding: 0.95rem 0.5rem; }
.quick-bar a:hover { background: var(--navy2); text-decoration: none; color: #fff; }
.quick-bar a + a { border-left: 1px solid rgba(255,255,255,0.12); }
.quick-bar svg { width: 22px; height: 22px; flex-shrink: 0; }
@media (max-width: 700px) {
  .quick-bar { grid-template-columns: repeat(2, 1fr); }
  .quick-bar a { font-size: 0.82rem; padding: 0.75rem 0.3rem; }
  .quick-bar a:nth-child(3) { border-left: 0; }
  .quick-bar a:nth-child(n+3) { border-top: 1px solid rgba(255,255,255,0.12); }
}

/* ---------- Featured articles row ---------- */
.featured-card { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(23,43,69,0.06); }
.featured-card figure { margin: 0 0 0.6rem; }
.featured-card figure img { border-radius: 0; }
.featured-card > h3, .featured-card > p { padding-left: 0.9rem; padding-right: 0.9rem; }
.featured-card .byline { padding-bottom: 0.9rem; }

/* ---------- Cards & grids ---------- */
.card-grid { display: grid; grid-template-columns: 1fr; gap: 1.6rem; }
@media (min-width: 640px) { .card-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 980px) { .card-grid.four { grid-template-columns: repeat(4, 1fr); } }
@media (min-width: 980px) { .card-grid.three { grid-template-columns: repeat(3, 1fr); } }
.card { background: #fff; }
.card figure { margin: 0 0 0.6rem; }
.card figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.card h3 { font-size: 1.12rem; line-height: 1.32; margin: 0.35rem 0 0.35rem; font-weight: 700; }
.card h3 a { color: var(--navy); }
.card h3 a:hover { color: var(--red); }
.card p { margin: 0; color: var(--muted); font-size: 0.93rem; line-height: 1.5; }
.card .art { margin-bottom: 0.6rem; }
/* Lead card: larger, spans the editorial row */
.lead-card { display: grid; grid-template-columns: 1fr; gap: 0; margin-bottom: 1.6rem; }
@media (min-width: 860px) { .lead-card { grid-template-columns: 1.5fr 1fr; gap: 1.6rem; align-items: start; } }
.lead-card figure { margin: 0; }
.lead-card figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.lead-card .art { aspect-ratio: 16 / 9; }
.lead-card h3 { font-size: 1.5rem; line-height: 1.25; margin: 0.4rem 0 0.5rem; font-weight: 900; }
.lead-card h3 a { color: var(--navy); }
.lead-card h3 a:hover { color: var(--red); }
.lead-card p { color: var(--text); font-size: 1rem; line-height: 1.55; margin: 0; }

/* ---------- Split sections (Business + Technology) ---------- */
.split-sections { display: grid; grid-template-columns: 1fr; gap: 2.4rem; margin: 0 0 2.4rem; }
@media (min-width: 980px) { .split-sections { grid-template-columns: 1fr 1fr; } }
.split-sections .mini-list { list-style: none; margin: 0; padding: 0; }
.split-sections .mini-list li { padding: 0.7rem 0; border-bottom: 1px solid var(--line); }
.split-sections .mini-list li:last-child { border-bottom: 0; }
.split-sections .mini-list a { font-family: var(--serif); font-weight: 700; font-size: 1.02rem; line-height: 1.35; color: var(--navy); }
.split-sections .mini-list a:hover { color: var(--red); }
.split-sections .mini-list small { display: block; color: var(--muted); font-size: 0.8rem; margin-top: 0.2rem; }

/* ---------- Latest news feed ---------- */
.latest-list { list-style: none; margin: 0; padding: 0; }
.latest-item { display: grid; grid-template-columns: 1fr; gap: 0.8rem; padding: 1rem 0; border-bottom: 1px solid var(--line); }
@media (min-width: 700px) { .latest-item { grid-template-columns: 180px 1fr; gap: 1.2rem; } }
.latest-thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.latest-thumb .art { aspect-ratio: 16 / 9; }
.latest-item h3 { font-size: 1.15rem; line-height: 1.3; margin: 0.3rem 0 0.35rem; font-weight: 700; }
.latest-item h3 a { color: var(--navy); }
.latest-item h3 a:hover { color: var(--red); }
.latest-item p { margin: 0; color: var(--muted); font-size: 0.94rem; line-height: 1.5; }
.latest-hidden { display: none; }
.load-more-wrap { text-align: center; margin: 1.4rem 0 0; }
.load-more-btn { background: var(--navy); color: #fff; border: 0; padding: 0.7rem 1.6rem; font-size: 0.95rem; font-weight: 700; border-radius: 3px; cursor: pointer; }
.load-more-btn:hover { background: var(--navy2); }

/* ---------- Live blog ---------- */
.live-dot { display: inline-block; width: 0.6rem; height: 0.6rem; background: var(--red); border-radius: 50%; margin-right: 0.4rem; animation: pulse 1.6s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }
.live-update { border-bottom: 1px solid var(--line); padding: 0 0 1rem; margin: 0 0 1rem; }
.live-update time { font-weight: 700; color: var(--red); font-size: 0.88rem; }
.live-update h3 { margin: 0.25rem 0 0.3rem; font-size: 1.15rem; font-weight: 700; line-height: 1.3; }
.live-update h3 a { color: var(--navy); }
.live-update h3 a:hover { color: var(--red); }
.live-update p { margin: 0; color: var(--text); }

/* ---------- Newsletter ---------- */
.newsletter { background: var(--navy); color: #fff; padding: 2.2rem 1.6rem; margin: 2.4rem 0; text-align: center; }
.newsletter h2 { margin: 0 0 0.4rem; font-size: 1.6rem; font-weight: 900; color: #fff; }
.newsletter p { margin: 0 auto 1.1rem; color: rgba(255,255,255,0.85); max-width: 560px; }
.newsletter form { display: flex; flex-wrap: wrap; gap: 0.6rem; max-width: 520px; margin: 0 auto; justify-content: center; }
.newsletter input[type="email"] { flex: 1 1 240px; padding: 0.7rem 0.9rem; border: 1px solid rgba(255,255,255,0.4); border-radius: 3px; font-size: 1rem; background: #fff; color: var(--text); }
.newsletter input[type="email"]:disabled { background: var(--gray); color: var(--muted); }
.newsletter button { background: var(--red); color: #fff; border: 0; padding: 0.7rem 1.4rem; font-size: 1rem; font-weight: 700; border-radius: 3px; cursor: pointer; }
.newsletter button:hover { background: var(--red-dark); }
.newsletter button:disabled { background: var(--muted); cursor: not-allowed; }
.newsletter .note { font-size: 0.8rem; color: rgba(255,255,255,0.7); margin: 0.8rem auto 0; }
.newsletter .coming-soon { font-weight: 700; color: #fff; margin: 0.8rem auto 0; }

/* ---------- Advertisement slots (reserved, empty) ---------- */
.ad-slot { border: 1px dashed var(--line); background: var(--bg); text-align: center; padding: 1.4rem 1rem; margin: 0 0 2rem; min-height: 96px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.2rem; }
.ad-slot .ad-label { font-size: 0.68rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); font-weight: 700; }
.ad-slot .ad-note { font-size: 0.82rem; color: var(--muted); }
.ad-slot.banner { min-height: 90px; }

/* ---------- Article page ---------- */
.article-layout { display: grid; grid-template-columns: 1fr; gap: 2.2rem; }
@media (min-width: 960px) { .article-layout { grid-template-columns: minmax(0, 760px) 300px; justify-content: center; } }
.article-head h1 { font-size: 1.9rem; line-height: 1.2; margin: 0.5rem 0; font-weight: 900; }
@media (min-width: 860px) { .article-head h1 { font-size: 2.3rem; } }
.article-head .dek { font-size: 1.12rem; color: var(--text); line-height: 1.55; }
.article-hero { margin: 1rem 0 1.4rem; }
.article-hero img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.article-hero .art { aspect-ratio: 16 / 9; }
.article-body { max-width: 760px; }
.article-body p { font-size: 1.06rem; line-height: 1.7; margin: 0 0 1.1rem; }
.article-body h2 { font-size: 1.35rem; margin: 1.6rem 0 0.6rem; }
.article-body h3 { font-size: 1.15rem; margin: 1.4rem 0 0.5rem; }
.source-box { border: 1px solid var(--line); border-left: 4px solid var(--red); background: var(--bg); padding: 0.8rem 1rem; margin: 1.6rem 0; font-size: 0.95rem; }
.source-box strong { display: block; margin-bottom: 0.2rem; }
.source-box a { color: var(--red); font-weight: 700; }
/* Sidebar */
.sidebar { display: flex; flex-direction: column; gap: 1.8rem; }
.sidebar-block h2 { font-family: var(--sans); font-size: 0.9rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--navy); border-left: 4px solid var(--red); padding-left: 0.6rem; margin: 0 0 0.7rem; }
.trending-list { list-style: none; margin: 0; padding: 0; counter-reset: tr; }
.trending-list li { counter-increment: tr; display: flex; gap: 0.8rem; align-items: flex-start; padding: 0.65rem 0; border-bottom: 1px solid var(--line); }
.trending-list li:last-child { border-bottom: 0; }
.trending-list li::before { content: counter(tr); font-weight: 800; font-size: 1.4rem; line-height: 1; color: var(--navy); min-width: 1.4rem; }
.trending-list a { font-size: 0.96rem; line-height: 1.35; font-weight: 700; color: var(--navy); }
.trending-list a:hover { color: var(--red); }
.trending-list small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; font-weight: 400; }
.side-list { list-style: none; margin: 0; padding: 0; }
.side-list li { padding: 0.6rem 0; border-bottom: 1px solid var(--line); }
.side-list li:last-child { border-bottom: 0; }
.side-list a { font-weight: 700; font-size: 0.95rem; line-height: 1.35; color: var(--navy); }
.side-list a:hover { color: var(--red); }
.side-list small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; }
.cat-list { list-style: none; margin: 0; padding: 0; }
.cat-list li { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--line); font-size: 0.94rem; }
.cat-list li:last-child { border-bottom: 0; }
.cat-list a { font-weight: 600; color: var(--navy); }
.cat-list span { color: var(--muted); }
/* Related / prev-next / author */
.related { margin-top: 2rem; border-top: 1px solid var(--line); padding-top: 0.8rem; }
.related h2 { font-family: var(--sans); font-size: 0.95rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; margin: 0 0 0.6rem; }
.related-list { list-style: none; margin: 0; padding: 0; }
.related-list li { padding: 0.7rem 0; border-bottom: 1px solid var(--line); }
.related-list li:last-child { border-bottom: 0; }
.related-list a { font-weight: 700; color: var(--navy); }
.related-list a:hover { color: var(--red); }
.prev-next { display: grid; grid-template-columns: 1fr; gap: 1rem; margin: 1.8rem 0 0; border-top: 1px solid var(--line); padding-top: 1.2rem; }
@media (min-width: 700px) { .prev-next { grid-template-columns: 1fr 1fr; } }
.prev-next a { display: block; border: 1px solid var(--line); padding: 0.8rem 1rem; }
.prev-next a:hover { text-decoration: none; border-color: var(--navy); }
.prev-next small { display: block; color: var(--red); font-size: 0.75rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
.prev-next strong { display: block; font-family: var(--serif); font-size: 1rem; line-height: 1.35; color: var(--navy); margin-top: 0.3rem; }
.author-box { display: flex; gap: 1rem; align-items: flex-start; background: var(--bg); border: 1px solid var(--line); padding: 1rem 1.2rem; margin: 1.8rem 0 0; }
.author-box .avatar { flex-shrink: 0; width: 56px; height: 56px; border-radius: 50%; background: var(--navy); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; }
.author-box h3 { margin: 0 0 0.3rem; font-size: 1.05rem; }
.author-box p { margin: 0; color: var(--muted); font-size: 0.93rem; line-height: 1.5; }
.share-row { display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap; margin: 1.4rem 0 0; }
.share-row span { font-weight: 700; font-size: 0.9rem; color: var(--navy); }
.share-row a { border: 1px solid var(--line); border-radius: 3px; padding: 0.4rem 0.8rem; font-size: 0.88rem; font-weight: 600; color: var(--navy); }
.share-row a:hover { background: var(--navy); color: #fff; text-decoration: none; }

/* ---------- Graphic placeholder (stories without a photo) ---------- */
.art {
  aspect-ratio: 16 / 9;
  background: var(--navy);
  color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.35rem; text-align: center; padding: 1rem;
}
.art .monogram { font-size: 2rem; font-weight: 800; letter-spacing: 0.06em; border: 2px solid rgba(255,255,255,0.85); padding: 0.2rem 0.9rem; }
.art .art-label { font-size: 0.8rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.85; }
.art.small .monogram { font-size: 1.3rem; }

/* ---------- Category pages / pagination ---------- */
.cat-nav { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0 0 1.4rem; }
.cat-nav a { border: 1px solid var(--line); border-radius: 3px; padding: 0.4rem 0.8rem; font-size: 0.88rem; font-weight: 600; color: var(--navy); background: #fff; }
.cat-nav a:hover { background: var(--bg); text-decoration: none; }
.cat-nav a.active { background: var(--navy); color: #fff; border-color: var(--navy); }
.pagination { display: flex; gap: 0.4rem; flex-wrap: wrap; justify-content: center; margin: 1.8rem 0 0; }
.page-btn { border: 1px solid var(--line); background: #fff; color: var(--navy); padding: 0.5rem 0.85rem; font-size: 0.92rem; font-weight: 700; border-radius: 3px; cursor: pointer; }
.page-btn:hover { border-color: var(--navy); }
.page-btn.active { background: var(--navy); color: #fff; border-color: var(--navy); }
.page-btn:disabled { opacity: 0.45; cursor: default; }
.page-count { text-align: center; color: var(--muted); font-size: 0.88rem; margin: 0.7rem 0 0; }

/* ---------- Info pages ---------- */
.info-page { max-width: 760px; }
.info-page h1 { font-size: 1.8rem; margin: 0 0 1rem; }
.info-page p { line-height: 1.7; color: var(--text); }
.info-page a { color: var(--red); font-weight: 600; }

/* ---------- Search page ---------- */
.search-page .search-form { display: flex; gap: 0.6rem; max-width: 560px; margin: 0 0 1.4rem; }
.search-page .search-form input[type="search"] { flex: 1; padding: 0.7rem 0.9rem; border: 1px solid var(--line); border-radius: 3px; font-size: 1rem; }
.search-page .search-form button { background: var(--navy); color: #fff; border: 0; padding: 0.7rem 1.3rem; font-size: 1rem; font-weight: 700; border-radius: 3px; cursor: pointer; }
.search-result { padding: 1rem 0; border-bottom: 1px solid var(--line); }
.search-result h3 { font-size: 1.15rem; margin: 0.3rem 0 0.35rem; }
.search-result h3 a { color: var(--navy); }
.search-result p { margin: 0; color: var(--muted); font-size: 0.94rem; }

/* ---------- Footer ---------- */
footer.site-footer { background: var(--navy); color: rgba(255,255,255,0.85); margin-top: 2.5rem; }
footer.site-footer .wrap { padding-top: 2.2rem; padding-bottom: 1.4rem; }
footer.site-footer a { color: rgba(255,255,255,0.85); }
footer.site-footer a:hover { color: #fff; }
footer.site-footer .cols { display: grid; grid-template-columns: 1fr; gap: 1.8rem; }
@media (min-width: 700px) { footer.site-footer .cols { grid-template-columns: 1.4fr 1fr 1fr 1fr; } }
footer.site-footer h3 { color: #fff; margin: 0 0 0.7rem; font-size: 0.98rem; font-weight: 800; font-family: var(--sans); }
footer.site-footer h3 .news { color: #fff; }
footer.site-footer .brand-name { font-size: 1.35rem; color: #fff; }
footer.site-footer .brand-name span { color: #fff; }
footer.site-footer ul { list-style: none; margin: 0; padding: 0; }
footer.site-footer li { margin: 0.4rem 0; font-size: 0.94rem; }
footer.site-footer p { font-size: 0.94rem; color: rgba(255,255,255,0.75); line-height: 1.6; }
footer.site-footer .fineprint { border-top: 1px solid rgba(255,255,255,0.2); margin-top: 1.8rem; padding-top: 1rem; font-size: 0.82rem; color: rgba(255,255,255,0.65); display: flex; flex-wrap: wrap; gap: 0.4rem 1.2rem; justify-content: space-between; align-items: center; }
footer.site-footer .fineprint .social-links a { border-color: rgba(255,255,255,0.4); color: #fff; }
footer.site-footer .fineprint .social-links a:hover { background: #fff; color: var(--navy); border-color: #fff; }

/* ---------- Cookie banner ---------- */
.cookie-banner { position: fixed; left: 0; right: 0; bottom: 0; z-index: 200; background: #fff; border-top: 1px solid var(--line); box-shadow: 0 -4px 16px rgba(0,0,0,0.08); padding: 0.9rem 1rem; display: none; }
.cookie-banner.show { display: block; }
.cookie-banner .wrap { display: flex; flex-wrap: wrap; gap: 0.6rem 1rem; align-items: center; justify-content: space-between; }
.cookie-banner p { margin: 0; font-size: 0.92rem; color: var(--text); flex: 1; min-width: 200px; }
.cookie-banner .actions { display: flex; gap: 0.5rem; }
.cookie-banner button { border: 0; border-radius: 3px; padding: 0.55rem 1rem; font-weight: 700; font-size: 0.92rem; cursor: pointer; }
.cookie-banner .accept { background: var(--navy); color: #fff; }
.cookie-banner .accept:hover { background: var(--navy2); }
.cookie-banner .decline { background: #fff; color: var(--navy); border: 1px solid var(--line); }

/* ---------- 404 ---------- */
.page-404 { text-align: center; padding: 3rem 0; }
.page-404 h1 { font-size: 3rem; margin: 0 0 0.5rem; }
.page-404 p { color: var(--muted); }
.page-404 .btn { background: var(--navy); color: #fff; padding: 0.7rem 1.4rem; border-radius: 3px; font-weight: 700; display: inline-block; margin-top: 1rem; }
.page-404 .btn:hover { background: var(--navy2); text-decoration: none; }

@media (max-width: 640px) {
  .top-hero-title { font-size: 2rem; }
  .top-hero-body h1 { font-size: 1.3rem; }
  .section-head { font-size: 1.15rem; }
  .article-head h1 { font-size: 1.6rem; }
}
"""


# ---------------- Templates (v2) ----------------

def nav_html(active, prefix=""):
    items = []
    for href, label in NAV:
        cls = "active" if href == active else ""
        items.append(f'<li><a href="{prefix}{href}" class="{cls.strip()}">{label}</a></li>')
    return '<ul>' + "".join(items) + "</ul>"


def header_html(active, prefix=""):
    # Single dark navy header: brand lockup, nav, search, Subscribe.
    # The Subscribe button jumps to the newsletter signup on the homepage.
    subscribe_href = "#newsletter" if not prefix else f"{prefix}index.html#newsletter"
    return f"""<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
<div class="wrap header-row">
<div class="brand-lockup">
<a class="nav-wordmark" href="{prefix}index.html" data-site-name>Western World <span>News</span></a>
<p class="nav-tagline">Independent News. Global Perspective.</p>
</div>
<button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false">&#9776;</button>
<nav class="main-nav" id="main-nav" aria-label="Main navigation">{nav_html(active, prefix)}</nav>
<div class="header-actions">
<div class="search-box">
<button class="search-toggle" id="search-toggle" type="button" aria-label="Search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><line x1="16.5" y1="16.5" x2="21" y2="21"></line></svg></button>
<input type="search" id="site-search" placeholder="Search news..." aria-label="Search news" autocomplete="off">
<div class="search-results" id="search-results" role="listbox" aria-label="Search results"></div>
</div>
<a class="subscribe-btn" href="{subscribe_href}">Subscribe</a>
</div>
</div>
</header>"""



def ad_slot_html(position=""):
    """Reserved advertising area. Empty until AdSense is approved: no fake
    ads, nothing disguised as news. The label makes it unmistakable."""
    return (f'<div class="ad-slot" data-ad-slot="{position}" aria-label="Advertisement space">'
            '<span class="ad-label">Advertisement</span>'
            '<span class="ad-note">Advertising space reserved for future sponsors.</span></div>')


def footer_html(prefix=""):
    return f"""<footer class="site-footer"><div class="wrap">
<div class="cols">
<div>
<a class="brand-name" href="{prefix}index.html">Western World <span>News</span></a>
<p style="margin-top:0.7rem">Independent journalism bringing global developments, important stories and perspectives to readers worldwide.</p>
</div>
<div>
<h3>Explore</h3>
<ul>
<li><a href="{prefix}world.html">World</a></li>
<li><a href="{prefix}us.html">US</a></li>
<li><a href="{prefix}europe.html">Europe</a></li>
<li><a href="{prefix}politics.html">Politics</a></li>
<li><a href="{prefix}war-conflict.html">War &amp; Conflict</a></li>
<li><a href="{prefix}business-finance.html">Business</a></li>
<li><a href="{prefix}technology.html">Technology</a></li>
<li><a href="{prefix}culture.html">Culture</a></li>
<li><a href="{prefix}sport.html">Sport</a></li>
<li><a href="{prefix}live.html">Live</a></li>
</ul>
</div>
<div>
<h3>About</h3>
<ul>
<li><a href="{prefix}about.html">About Us</a></li>
<li><a href="{prefix}authors.html">Our Authors</a></li>
<li><a href="{prefix}contact.html">Contact Us</a></li>
<li><a href="{prefix}editorial-policy.html">Editorial Policy</a></li>
<li><a href="{prefix}corrections.html">Corrections Policy</a></li>
<li><a href="{prefix}advertise.html">Advertise With Us</a></li>
</ul>
</div>
<div>
<h3>Legal</h3>
<ul>
<li><a href="{prefix}privacy.html">Privacy Policy</a></li>
<li><a href="{prefix}terms.html">Terms and Conditions</a></li>
<li><a href="{prefix}disclaimer.html">Disclaimer</a></li>
<li><a href="{prefix}cookie-policy.html">Cookie Policy</a></li>
<li><a href="{prefix}sitemap.xml">Sitemap</a></li>
</ul>
</div>
</div>
<p class="fineprint"><span>&copy; 2026 Western World News (westernworldnews.com). All Rights Reserved. Stories are automated summaries of credited source reports; original reporting is credited and linked. New stories are added automatically during the day.</span><span class="social-links">
<a href="#" data-share="facebook" aria-label="Share on Facebook" title="Share on Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.3 0-1.1-.1-2.1-.1-2.1 0-3.6 1.3-3.6 3.7V11H8.3v3h2.4v7h2.8z"/></svg></a>
<a href="#" data-share="x" aria-label="Share on X" title="Share on X"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.7 3H21l-7.3 8.3L22.2 21h-6.7l-5.2-6.2L4.3 21H1l7.8-8.9L1.8 3h6.9l4.7 5.6L17.7 3zm-1.2 16h1.9L6.4 4.9H4.4L16.5 19z"/></svg></a>
</span></p>
</div></footer>"""


def page(title, description, active, body, canonical, og_type="website", prefix="", extra_head="", og_image=""):
    verify_tag = (f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">'
                  if GOOGLE_SITE_VERIFICATION else "")
    ga_tag = ""
    if GOOGLE_ANALYTICS_ID:
        nl = chr(10)
        ga_tag = ('<script async src="https://www.googletagmanager.com/gtag/js?id='
                  + GOOGLE_ANALYTICS_ID + '"></script>' + nl + '<script>' + nl
                  + '  window.dataLayer = window.dataLayer || [];' + nl
                  + '  function gtag(){dataLayer.push(arguments);}' + nl
                  + "  gtag('consent', 'default', {'analytics_storage': 'denied'});" + nl
                  + "  gtag('js', new Date());" + nl
                  + "  try { if (localStorage.getItem('wwn-cookie-choice') === 'accepted') { gtag('consent', 'update', {'analytics_storage': 'granted'}); } } catch (e) {}" + nl
                  + "  gtag('config', '" + GOOGLE_ANALYTICS_ID + "');" + nl + '</script>')
    full_title = title if title == "Western World News" else f"{title} | Western World News"
    # Default social image: the branded 1200x630 card in assets/img/.
    # Pages with their own photo (article pages, category pages) pass
    # that image instead; pages without one (info pages, 404, no-photo
    # articles) fall back to this so no page shares without an image.
    if not og_image:
        og_image = BASE + "/assets/img/og-default.png"
    og_image_tag = ""
    if og_image:
        og_image_tag = ('<meta property="og:image" content="' + hescape(og_image) + '">' + chr(10)
                        + '<meta name="twitter:image" content="' + hescape(og_image) + '">')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{verify_tag}
{ga_tag}
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Western World News">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
{og_image_tag}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Merriweather:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23172B45'/%3E%3Ctext x='16' y='22' font-family='Georgia' font-size='16' font-weight='bold' fill='white' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E">
{extra_head}
{_org_jsonld()}
</head>
<body>
{header_html(active, prefix)}
<main id="main"><div class="wrap">
{body}
</div></main>
{footer_html(prefix)}
<div class="cookie-banner" id="cookie-banner" role="dialog" aria-label="Cookie consent">
<div class="wrap">
<p>We use cookies to improve your experience. Advertising may appear on this site in the future, once approved; until then, no advertising cookies are used. Read our <a href="{prefix}privacy.html">Privacy Policy</a>.</p>
<div class="actions">
<button class="decline" id="cookie-decline" type="button">Decline</button>
<button class="accept" id="cookie-accept" type="button">Accept</button>
</div>
</div>
</div>
<script src="{prefix}assets/js/content.js"></script>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def art_html(section_label, small=False):
    cls = "art small" if small else "art"
    return (f'<div class="{cls}" role="img" aria-label="Graphic placeholder for {section_label}">'
            f'<span class="monogram">WWN</span><span class="art-label">{section_label}</span></div>')


def img_html(slug, w=800, cls="", caption=True, loading="lazy"):
    """Photo figure for a story, or the navy tile if no photo is set.
    width/height reserve the 16:9 display box so the page does not shift
    while images load."""
    h = w * 9 // 16
    if slug in IMAGES:
        pid, cap = IMAGES[slug]
        alt = _alt_for(slug, cap)
        img = f'<img src="{uimg(pid, w)}" alt="{hescape(alt)}" width="{w}" height="{h}" loading="{loading}">'
        fig = (f'<figure class="{cls}">{img}<figcaption>{hescape(cap)}</figcaption></figure>') if caption else \
              f'<figure class="{cls}">{img}</figure>'
        return fig
    if slug in BY_SLUG and BY_SLUG[slug].get("image"):
        cap = BY_SLUG[slug].get("imageCaption") or "Photo: Unsplash"
        alt = _alt_for(slug, cap)
        img = f'<img src="{hescape(BY_SLUG[slug]["image"])}" alt="{hescape(alt)}" width="{w}" height="{h}" loading="{loading}">'
        fig = (f'<figure class="{cls}">{img}<figcaption>{hescape(cap)}</figcaption></figure>') if caption else \
              f'<figure class="{cls}">{img}</figure>'
        return fig
    sec = SECTIONS[BY_SLUG[slug]["section"]] if slug in BY_SLUG else "News"
    return art_html(sec, small=(w <= 800))


def thumb_html(slug, w=400):
    """Small thumbnail image only (no caption), or the navy tile.
    Alt text always falls back to the article headline, never empty."""
    s = BY_SLUG.get(slug)
    alt = hescape(s["headline"]) if s else "Western World News"
    h = w * 9 // 16
    if s and s.get("image"):
        return f'<img src="{hescape(s["image"])}" alt="{alt}" width="{w}" height="{h}" loading="lazy">'
    if slug in IMAGES:
        pid, _cap = IMAGES[slug]
        return f'<img src="{uimg(pid, w)}" alt="{alt}" width="{w}" height="{h}" loading="lazy">'
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


def _read_time(s):
    """Approximate read time from the article body, e.g. '3 min read'."""
    words = sum(len(p.split()) for p in (s.get("body") or []))
    return f"{max(1, round(words / 200))} min read"


def _short_date(date_str):
    """'November 27, 2026' -> 'Nov 27, 2026' for compact meta lines."""
    m = _re.match(r"(\w+) (\d{1,2}), (\d{4})", date_str or "")
    if not m:
        return date_str or ""
    return f"{m.group(1)[:3]} {m.group(2)}, {m.group(3)}"


# Section accent colors for the homepage top (stacked cards, quick bar).
SECTION_COLORS = {
    "world": "#D93036",
    "us": "#2563EB",
    "europe": "#7C3AED",
    "war-conflict": "#C2410C",
}

# Small stroke icons for the category quick bar (globe, flag, landmark, shield).
QUICK_ICONS = {
    "world": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.9 5.7 3.9 9s-1.4 6.4-3.9 9c-2.5-2.6-3.9-5.7-3.9-9S9.5 5.6 12 3z"/></svg>',
    "us": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21V4"/><path d="M5 4h13l-2.5 4L18 12H5"/></svg>',
    "europe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-6 9 6"/><path d="M6 9v9M10 9v9M14 9v9M18 9v9"/><path d="M3 21h18"/><path d="M3 18h18"/></svg>',
    "war-conflict": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 3v6c0 5-3.5 9.3-8 11-4.5-1.7-8-6-8-11V5l8-3z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',
}

# Red heartbeat divider used under the homepage intro headline.
PULSE_SVG = ('<svg viewBox="0 0 64 18" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<polyline points="0,9 10,9 14,3 20,15 24,9 38,9 43,5 48,9 64,9"/></svg>')


def _top_hero_media(s):
    """Top-story photo with the red TOP STORY badge, or the navy tile."""
    url = _img_url(s["slug"])
    alt = hescape(s["headline"])
    if url:
        media = f'<img src="{hescape(url)}" alt="{alt}" width="1200" height="675" loading="eager">'
    else:
        media = art_html(SECTIONS[s["section"]])
    return (f'<a class="top-hero-media" href="articles/{s["slug"]}.html" aria-label="{alt}">'
            f'{media}<span class="top-story-badge">Top Story</span></a>')


def stack_card_html(s):
    """One stacked story for the hero's right column: thumb, section, headline, date."""
    color = SECTION_COLORS.get(s["section"], "#D93036")
    return f"""<article class="stack-card">
<a class="stack-thumb" href="articles/{s['slug']}.html">{thumb_html(s['slug'], w=320)}</a>
<div class="stack-body">
<p><span class="stack-kicker" style="color:{color}">{SECTIONS[s['section']]}</span></p>
<h3><a href="articles/{s['slug']}.html">{s['headline']}</a></h3>
<p class="stack-meta"><time>{_short_date(s['date'])}</time></p>
</div>
</article>"""


def featured_card_html(s):
    """Featured Articles card: photo, section, headline, dek, date + read time."""
    return f"""<article class="card featured-card">
{img_html(s['slug'], w=800)}
<p><span class="kicker">{SECTIONS[s['section']]}</span></p>
<h3><a href="articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; {_read_time(s)}</p>
</article>"""


def _img_url(slug):
    """Direct image URL for a story, or '' when it has no photo."""
    s = BY_SLUG.get(slug)
    if s and s.get("image"):
        return s["image"]
    if slug in IMAGES:
        return uimg(IMAGES[slug][0], 1200)
    return ""


def _og_image(slug):
    return _img_url(slug)


def _justin_link(text):
    """Link a Just In headline to its article when one exists (exact or
    near title match). Returns the article path, or None when the story
    was never published as an article: those items render as plain text
    instead of pointing at the wrong page."""
    norm = _re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()
    for s in STORIES:
        if _re.sub(r"[^a-z0-9]+", " ", s["headline"].lower()).strip() == norm:
            return f"articles/{s['slug']}.html"
    return None


def _justin_sorted():
    """Just In items, newest first (times are '27 Nov, 15:54' in UTC)."""
    def key(item):
        t, _h, _l = item
        m = _re.match(r"(\d{1,2}) (\w{3}), (\d{2}):(\d{2})", t or "")
        if not m:
            return (0, 0, 0, 0)
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        return (months.get(m.group(2), 0), int(m.group(1)), int(m.group(3)), int(m.group(4)))
    return sorted(JUST_IN, key=key, reverse=True)


def _related_slugs(s, limit=3):
    """Related stories: the article's own list first, then the newest
    stories in the same section, then the same source. Never empty when
    the site has other stories in the section."""
    out = []
    for r in (s.get("related") or []):
        if r in BY_SLUG and r != s["slug"] and r not in out:
            out.append(r)
    if len(out) < limit:
        for x in STORIES:
            if len(out) >= limit:
                break
            if x["slug"] != s["slug"] and x["section"] == s["section"] and x["slug"] not in out:
                out.append(x["slug"])
    if len(out) < limit:
        for x in STORIES:
            if len(out) >= limit:
                break
            if x["slug"] != s["slug"] and x.get("source") == s.get("source") and x["slug"] not in out:
                out.append(x["slug"])
    return out[:limit]


def _live_last_updated():
    """'Last updated' for the live blog, derived from the newest update's
    date instead of a hardcoded string."""
    best = None
    months = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
              "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
              "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"}
    order = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
             "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    for t, _h, _p in LIVE_UPDATES:
        m = _re.match(r"(\w{3}) (\d{1,2})", t or "")
        if not m:
            continue
        key = (order.get(m.group(1), 0), int(m.group(2)))
        if best is None or key > best[0]:
            best = (key, f"{months[m.group(1)]} {int(m.group(2))}, {datetime.date.today().year}")
    return best[1] if best else ""


def lead_card_html(s, prefix=""):
    sec = SECTIONS[s["section"]]
    return f"""<article class="lead-card">
{img_html(s['slug'], w=1200)}
<div>
<p><span class="kicker">{sec}</span></p>
<h3><a href="{prefix}articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; Source: {s['source']}</p>
</div>
</article>"""


def mini_list_html(stories, prefix=""):
    items = "".join(
        f'<li><a href="{prefix}articles/{s["slug"]}.html">{s["headline"]}</a>'
        f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small></li>'
        for s in stories
    )
    return f'<ul class="mini-list">{items}</ul>'


def trending_html(prefix="", limit=10):
    slugs = [s for s in MOST_READ if s in BY_SLUG]
    for s in STORIES:
        if len(slugs) >= limit:
            break
        if s["slug"] not in slugs:
            slugs.append(s["slug"])
    items = "".join(
        f'<li><div><a href="{prefix}articles/{s["slug"]}.html">{s["headline"]}</a>'
        f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small></div></li>'
        for s in (BY_SLUG[slug] for slug in slugs[:limit])
    )
    return f"""<aside class="sidebar-block" aria-label="Trending stories">
<h2>Trending Stories</h2>
<ol class="trending-list" id="most-read-list">{items}</ol>
</aside>"""


def latest_sidebar_html(prefix="", exclude_slug="", limit=5):
    items = []
    for s in STORIES:
        if s["slug"] == exclude_slug:
            continue
        items.append(s)
        if len(items) >= limit:
            break
    rows = "".join(
        f'<li><a href="{prefix}articles/{s["slug"]}.html">{s["headline"]}</a>'
        f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small></li>'
        for s in items
    )
    return f"""<aside class="sidebar-block" aria-label="Latest news">
<h2>Latest News</h2>
<ul class="side-list">{rows}</ul>
</aside>"""


def categories_sidebar_html(prefix=""):
    rows = ""
    for key in ["world", "us", "europe", "politics", "war-conflict",
                "business-finance", "technology", "culture", "sport"]:
        n = len(stories_for(key))
        if n:
            rows += (f'<li><a href="{prefix}{key}.html">{SECTIONS[key]}</a>'
                     f'<span>{n} {("story" if n == 1 else "stories")}</span></li>')
    return f"""<aside class="sidebar-block" aria-label="Popular categories">
<h2>Popular Categories</h2>
<ul class="cat-list">{rows}</ul>
</aside>"""


def section_nav_html(active_file, prefix=""):
    links = []
    for href, label in NAV:
        cls = "active" if href == active_file else ""
        links.append(f'<a href="{prefix}{href}" class="{cls.strip()}">{label}</a>')
    return '<nav class="cat-nav" aria-label="Sections">' + "".join(links) + "</nav>"


def newsletter_html():
    """Newsletter section: 'Stay Informed. Stay Ahead.'

    Wired to Buttondown (NEWSLETTER_BUTTONDOWN_USERNAME). The embed form
    posts straight to Buttondown's public endpoint; Buttondown sends the
    double opt-in confirmation and shows its own confirmation page.
    While the username is unset, the form is honestly disabled with an
    'opening soon' note — it never pretends to subscribe anyone."""
    if NEWSLETTER_BUTTONDOWN_USERNAME:
        action = ("https://buttondown.com/api/emails/embed-subscribe/"
                  + NEWSLETTER_BUTTONDOWN_USERNAME)
        form = f"""<form class="newsletter-form" action="{action}" method="post">
<label for="nl-email" class="sr-only">Email address</label>
<input id="nl-email" type="email" name="email" placeholder="Your email address" required>
<input type="hidden" value="1" name="embed">
<button type="submit">Subscribe</button>
</form>
<p class="note">Powered by Buttondown. Double opt-in: check your inbox to confirm your subscription. You can unsubscribe at any time. We never sell your data.</p>"""
    else:
        form = """<form class="newsletter-form" action="#" method="post" onsubmit="return false;">
<label for="nl-email" class="sr-only">Email address</label>
<input id="nl-email" type="email" name="email" placeholder="Your email address" disabled>
<button type="submit" disabled>Subscribe</button>
</form>
<p class="coming-soon">Subscriptions open soon. We are setting up our newsletter list, and sign-ups will open here shortly.</p>
<p class="note">No spam, no paywall. Unsubscribe any time. We never sell your data.</p>"""
    return f"""<section class="newsletter" id="newsletter" aria-label="Newsletter signup">
<h2>Stay Informed. Stay Ahead.</h2>
<p>Get the latest world news, important developments and expert perspectives delivered to your inbox.</p>
{form}
</section>"""


def contact_form_html():
    """Contact form for the contact page.

    Posts to CONTACT_FORM_ENDPOINT (Formspree) when set; the form
    includes a honeypot field ("website") that real visitors leave
    blank. While the endpoint is unset, the form renders disabled with
    an honest note pointing at the email address — it never pretends
    to send a message.
    """
    if CONTACT_FORM_ENDPOINT:
        return f"""<form class="contact-form" action="{CONTACT_FORM_ENDPOINT}" method="post">
<label for="cf-name">Your name</label>
<input id="cf-name" type="text" name="name" autocomplete="name" required>
<label for="cf-email">Your email</label>
<input id="cf-email" type="email" name="email" autocomplete="email" required>
<label for="cf-subject">Subject</label>
<input id="cf-subject" type="text" name="subject" required>
<label for="cf-message">Message</label>
<textarea id="cf-message" name="message" rows="6" required></textarea>
<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<button type="submit">Send message</button>
</form>
<p class="note">Your message goes to the site operator at lurenmira@gmail.com. Please include the story headline when reporting a correction.</p>"""
    return """<form class="contact-form" action="#" method="post" onsubmit="return false;">
<label for="cf-name">Your name</label>
<input id="cf-name" type="text" name="name" disabled>
<label for="cf-email">Your email</label>
<input id="cf-email" type="email" name="email" disabled>
<label for="cf-subject">Subject</label>
<input id="cf-subject" type="text" name="subject" disabled>
<label for="cf-message">Message</label>
<textarea id="cf-message" name="message" rows="6" disabled></textarea>
<button type="submit" disabled>Send message</button>
</form>
<p class="note">The contact form is not connected yet. Please email lurenmira@gmail.com for now — news tips, corrections and advertising inquiries all go there.</p>"""


def stories_for(section):
    return [s for s in STORIES if section in s["sections"]]


# ---------------- Homepage ----------------

SECTION_DESCRIPTIONS = {
    "world": "Global developments, diplomacy and major stories from every region.",
    "europe": "European politics, the European Union, the UK, Germany, France and the continent's biggest stories.",
    "us": "US politics, the White House, Congress, elections, the US economy and America's role in the world.",
    "politics": "Politics in the West and around the world: elections, governments and the decisions that shape them.",
    "war-conflict": "International conflicts, military developments, security, defense and geopolitics.",
    "business-finance": "The global economy, financial markets, companies and trade.",
    "technology": "Artificial intelligence, science, technology companies and innovation.",
    "sport": "Sport from around the world.",
    "culture": "Culture, arts and ideas.",
}


def build_index():
    hero = BY_SLUG.get(HERO_SLUG) or STORIES[0]
    used = {hero["slug"]}

    def pick_newest(stories):
        for s in stories:
            if s["slug"] not in used:
                used.add(s["slug"])
                return s
        return None

    # --- Trending ticker (A): breaking story first, then Just In items ---
    breaking_link = BREAKING.get("link", "")
    breaking_text = BREAKING.get("text", "")
    if not breaking_link or not breaking_text:
        breaking_link = f"articles/{hero['slug']}.html"
        breaking_text = hero["headline"]

    def _norm_head(t):
        return _re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()

    ticker_items = [f'<a href="{breaking_link}">{breaking_text}</a>']
    seen_heads = {_norm_head(breaking_text)}
    for t, h, stored_link in _justin_sorted():
        if _norm_head(h) in seen_heads:
            continue
        seen_heads.add(_norm_head(h))
        link = stored_link or _justin_link(h)
        if link:
            ext = ' target="_blank" rel="noopener"' if link.startswith("http") else ""
            ticker_items.append(f'<a href="{link}"{ext}>{h}</a>')
        else:
            ticker_items.append(f"<span>{h}</span>")
    ticker = "".join(ticker_items)
    ticker_html = f'<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}{ticker}</div></div>'

    hero_headline = hero["headline"].lower()
    live_link = ""
    if any(w in hero_headline for w in ("ukraine", "russia", "kyiv", "kremlin")):
        live_link = ' &middot; <a href="live.html">Follow live updates</a>'

    # --- B: top-story card (center of the hero) ---
    hero_main_html = f"""<article class="top-hero-main" data-hero>
{_top_hero_media(hero)}
<div class="top-hero-body">
<h1><a href="articles/{hero['slug']}.html">{hero['headline']}</a></h1>
<p class="dek">{hero['dek']}</p>
<p class="byline"><time>{hero['date']}</time> &middot; {_read_time(hero)}{live_link}</p>
</div>
</article>"""

    # --- B: stacked stories (right column), newest per top section ---
    stack_html = "".join(
        stack_card_html(s) for s in (
            pick_newest([x for x in STORIES if x["section"] == sec])
            for sec in ("world", "us", "europe", "war-conflict")
        ) if s
    )

    # --- Quick bar: the same four sections, with icons ---
    quick_html = "".join(
        f'<a href="{sec}.html"><span style="color:{SECTION_COLORS[sec]}">{QUICK_ICONS[sec]}</span>'
        f"{SECTIONS[sec]}</a>"
        for sec in ("world", "us", "europe", "war-conflict")
    )

    # --- C: Featured Articles, the next 4 newest stories ---
    featured = []
    for s in STORIES:
        if len(featured) >= 4:
            break
        if s["slug"] not in used:
            used.add(s["slug"])
            featured.append(s)
    featured_cards = "".join(featured_card_html(s) for s in featured)

    # --- Section blocks D-G: lead + 3 cards each ---
    def section_block(section, title, view_all):
        stories = [s for s in stories_for(section) if s["slug"] not in used]
        if not stories:
            return ""
        lead = stories[0]
        used.add(lead["slug"])
        cards = []
        for s in stories[1:4]:
            used.add(s["slug"])
            cards.append(s)
        cards_html = "".join(card_html(s) for s in cards)
        return f"""<section class="section-block" aria-label="{title}" data-section-block data-section="{section}" data-limit="4">
<h2 class="section-head">{title}<a class="view-all" href="{view_all}">View All &rarr;</a></h2>
<div data-block-content>
{lead_card_html(lead)}
<div class="card-grid three">{cards_html}</div>
</div>
</section>"""

    world_block = section_block("world", "World News", "world.html")
    us_block = section_block("us", "US News &amp; Politics", "us.html")
    europe_block = section_block("europe", "Europe News", "europe.html")
    war_block = section_block("war-conflict", "War &amp; Conflict", "war-conflict.html")

    # --- H: Business + Technology side by side ---
    def split_block(section, title, view_all):
        stories = [s for s in stories_for(section) if s["slug"] not in used]
        if not stories:
            return (f'<div><h2 class="section-head">{title}<a class="view-all" href="{view_all}">View All &rarr;</a></h2>'
                    '<p class="section-desc">More coverage is added daily.</p></div>')
        lead = stories[0]
        used.add(lead["slug"])
        rest_minis = []
        for s in stories[1:4]:
            used.add(s["slug"])
            rest_minis.append(s)
        return f"""<div data-section-block data-section="{section}" data-limit="4" data-layout="split">
<h2 class="section-head">{title}<a class="view-all" href="{view_all}">View All &rarr;</a></h2>
<div data-block-content>
{lead_card_html(lead)}
{mini_list_html(rest_minis)}
</div>
</div>"""

    biz_block = split_block("business-finance", "Business", "business-finance.html")
    tech_block = split_block("technology", "Technology", "technology.html")

    # --- I: Latest News feed (chronological, nothing already featured) ---
    latest = [s for s in STORIES if s["slug"] not in used][:40]
    latest_items = []
    for i, s in enumerate(latest):
        hidden = ' latest-hidden' if i >= 10 else ""
        latest_items.append(f"""<li class="latest-item{hidden}">
<a class="latest-thumb" href="articles/{s['slug']}.html">{thumb_html(s['slug'])}</a>
<div>
<p><span class="kicker">{SECTIONS[s['section']]}</span></p>
<h3><a href="articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; Source: {s['source']}</p>
</div>
</li>""")
    load_more = ""
    if len(latest) > 10:
        load_more = ('<div class="load-more-wrap"><button class="load-more-btn" id="load-more" '
                     'type="button">Load More</button></div>')

    body = f"""
<div class="trend-strip" aria-label="Trending news">
<span class="trend-badge">Trending</span>
{ticker_html}
<a class="trend-live" href="live.html"><span class="live-dot"></span>Live</a>
</div>

{ad_slot_html("below-nav")}

<section class="top-hero" aria-label="Top stories">
<div class="top-hero-intro">
<p class="top-hero-title">Breaking News &amp; Timely Updates</p>
<span class="top-hero-pulse" aria-hidden="true">{PULSE_SVG}</span>
<p class="lede">Stay informed with the latest headlines, expert analysis, and real-time updates from around the globe.</p>
<a class="btn-red" href="#latest">Read Latest News</a>
</div>
{hero_main_html}
<div class="top-hero-side">
{stack_html}
</div>
</section>

<nav class="quick-bar" aria-label="Top categories">
{quick_html}
</nav>

<section class="section-block" aria-label="Featured articles">
<h2 class="section-head">Featured Articles<a class="view-all" href="#latest">View All &rarr;</a></h2>
<div class="card-grid four">{featured_cards}</div>
</section>

{ad_slot_html("mid-homepage")}

{world_block}
{us_block}
{europe_block}
{war_block}

<section class="split-sections" aria-label="Business and Technology">
{biz_block}
{tech_block}
</section>

<section class="section-block" id="latest" aria-label="Latest news">
<h2 class="section-head">Latest News</h2>
<ul class="latest-list" id="latest-list" data-exclude="{','.join(sorted(used))}">{''.join(latest_items)}</ul>
{load_more}
</section>

{newsletter_html()}
"""
    html = page(
        "Western World News",
        "Western World News: breaking news from Western Europe and the world: politics, war, business and culture, free to read.",
        "index.html", body, BASE + "/",
        og_image=_og_image(hero["slug"]),
    )
    return html


# ---------------- Section pages ----------------

def build_section(section, filename):
    stories = stories_for(section)
    label = SECTIONS[section]
    desc = SECTION_DESCRIPTIONS.get(section, "")
    if stories:
        lead = stories[0]
        rest_cards = "".join(card_html(s) for s in stories[1:])
        listing = (f'{lead_card_html(lead)}'
                   f'<div class="card-grid three paginated-grid" data-page-size="12" data-section-list="{section}">{rest_cards}</div>'
                   f'<div class="pagination" id="pagination"></div>'
                   f'<p class="page-count" id="page-count"></p>')
    else:
        listing = "<p>No stories in this section yet. New coverage is added daily.</p>"
    body = f"""
{_breadcrumbs_html([("Home", "index.html"), (label, None)])}
{section_nav_html(filename)}
<h1 class="section-head">{label} News</h1>
<p class="section-desc">{desc}</p>
{listing}
{trending_html()}
{newsletter_html()}
"""
    og = _og_image(stories[0]["slug"]) if stories else ""
    return page(
        f"{label} news",
        f"Latest {label} news from Western World News: {desc}",
        filename, body, BASE + "/" + filename,
        og_image=og,
        extra_head=_breadcrumb_jsonld([("Home", BASE + "/"),
                                       (SECTION_LABELS_PLAIN[section], BASE + "/" + filename)]),
    )


# ---------------- Live page ----------------

def build_live():
    def update_html(t, h, p):
        # Link the update's headline to its article when one exists
        # (live entries added by the publisher use the article headline
        # verbatim, so this matches). Older seed entries with no matching
        # article stay as plain text rather than pointing at the wrong page.
        link = _justin_link(h)
        head = f'<h3><a href="{link}">{h}</a></h3>' if link else f"<h3>{h}</h3>"
        return f"""<div class="live-update">
<time>{t}</time>
{head}
<p>{p}</p>
</div>"""
    updates = "".join(update_html(t, h, p) for t, h, p in LIVE_UPDATES)
    last = _live_last_updated()
    last_line = f"Last updated {last}." if last else ""
    body = f"""
<h1 class="section-head"><span class="live-dot"></span>Live: Ukraine war</h1>
<p>Rolling updates on Russia's war in Ukraine and Europe's response. Times are in UTC. {last_line}</p>
<div id="live-updates">{updates}</div>
<p><a class="btn" href="articles/russia-ukraine-missile-attack.html">Read the full story</a></p>
{newsletter_html()}
"""
    return page(
        "Live: Ukraine war (rolling updates)",
        "Live updates on Russia's war in Ukraine and Europe's response.",
        "live.html", body, BASE + "/live.html",
    )


# ---------------- Article pages ----------------

def _dedup_dek_body(dek, body):
    """The dek is a truncation of the same summary the body starts with,
    so the first body paragraph usually repeats the dek word for word
    (127 of 164 articles at the 2026-11-27 audit). Strip the repeated
    dek text from the start of the first body paragraph, and drop the
    paragraph entirely when nothing is left, so the page does not show
    the same sentence twice. Only exact and clean sentence-boundary
    prefixes are stripped: a mid-sentence cut is left alone rather
    than starting the body mid-sentence. No facts are added or removed.
    """
    if not dek or not body:
        return list(body or [])
    paras = list(body)
    first = paras[0]
    if first == dek:
        return paras[1:]
    if first.startswith(dek):
        rest = first[len(dek):].lstrip(" .")
        if rest:
            paras[0] = rest
        else:
            paras = paras[1:]
    return paras


def build_article(s):
    body_paras = "".join(f"<p>{p}</p>" for p in _dedup_dek_body(s["dek"], s["body"]))
    # Short stories are summaries of the source's own report (feed
    # description), not original WWN reporting — say so, for auto and
    # seed stories alike. Full researched articles (600+ words, written
    # from multiple sources) get the reporting wording instead; the
    # 400-word line cleanly separates them (auto summaries cap at ~150).
    if s["source"].startswith("The "):
        src_phrase = f"a report by {s['source']}"
    else:
        src_phrase = f"a {s['source']} report"
    word_count = sum(len(p.split()) for p in (s.get("body") or []))
    if word_count >= 400:
        source_note = (f"Reporting by Western World News, based on {src_phrase}. "
                       f"Read the original report at {s['source']}: "
                       f"<a href=\"{s['source_url']}\" target=\"_blank\" rel=\"noopener\">Original article: {s['source']}</a>.")
    elif s.get("auto"):
        source_note = (f"This is a short summary of {src_phrase}. "
                       f"Read the full story at {s['source']}: "
                       f"<a href=\"{s['source_url']}\" target=\"_blank\" rel=\"noopener\">Original article: {s['source']}</a>.")
    else:
        # Seed stories (auto is null/false) were written when the site was
        # set up; they are short summaries of the source's own report too,
        # not original WWN reporting — use the same honest wording.
        source_note = (f"This is a short summary of {src_phrase}. "
                       f"Read the full story at {s['source']}: "
                       f"<a href=\"{s['source_url']}\" target=\"_blank\" rel=\"noopener\">Original article: {s['source']}</a>.")
    rel_slugs = _related_slugs(s)
    rel = "".join(
        f'<li><a href="{r}.html">{BY_SLUG[r]["headline"]}</a> <span class="byline">{BY_SLUG[r]["date"]}</span></li>'
        for r in rel_slugs
    )
    related_html = ""
    if rel:
        related_html = f"""<section class="related">
<h2>Related stories</h2>
<ul class="related-list">{rel}</ul>
</section>"""
    idx = STORIES.index(s)
    prev_html = ""
    if idx + 1 < len(STORIES):
        older = STORIES[idx + 1]
        prev_html = (f'<a href="{older["slug"]}.html"><small>&larr; Previous article</small>'
                     f'<strong>{older["headline"]}</strong></a>')
    next_html = ""
    if idx > 0:
        newer = STORIES[idx - 1]
        next_html = (f'<a href="{newer["slug"]}.html"><small>Next article &rarr;</small>'
                     f'<strong>{newer["headline"]}</strong></a>')
    prev_next = ""
    if prev_html or next_html:
        prev_next = f'<nav class="prev-next" aria-label="More articles">{prev_html}{next_html}</nav>'
    sec = SECTIONS[s["section"]]
    crumbs = _breadcrumbs_html([("Home", "../index.html"),
                                (sec, "../" + s["section"] + ".html"),
                                (hescape(s["headline"]), None)])
    body = f"""
{crumbs}
<div class="article-layout">
<div>
<article data-article-slug="{s['slug']}">
<header class="article-head">
<p><span class="kicker">{sec}</span></p>
<h1>{s['headline']}</h1>
<p class="dek">{s['dek']}</p>
<p class="byline">By <a href="../authors.html">Western World News Editorial Team</a> &middot; <time>{s['date']}</time></p>
</header>
<div class="article-hero">{img_html(s['slug'], w=1600, loading="eager")}</div>
<div class="article-body">
{body_paras}
</div>
<div class="source-box">
<strong>Source</strong>
{source_note}
</div>
<div class="share-row"><span>Share this story:</span>
<a href="#" data-share="facebook">Facebook</a>
<a href="#" data-share="x">X</a>
</div>
{related_html}
{prev_next}
<div class="author-box">
<div class="avatar" aria-hidden="true">WWN</div>
<div>
<h3>Western World News Editorial Team</h3>
<p>Stories on Western World News are written by our editorial team: each one is researched from several trusted news sources and written in our own words, with the sources credited and linked. Every story on the site is a full researched article. <a href="../authors.html">More about how our stories are made</a></p>
</div>
</div>
{ad_slot_html("after-article")}
{newsletter_html()}
</article>
</div>
<div class="sidebar">
{trending_html(prefix="../")}
{latest_sidebar_html(prefix="../", exclude_slug=s['slug'])}
{categories_sidebar_html(prefix="../")}
{ad_slot_html("sidebar")}
</div>
</div>
"""
    schema = (_newsarticle_jsonld(s) + "\n" + _breadcrumb_jsonld([
        ("Home", BASE + "/"),
        (SECTION_LABELS_PLAIN[s["section"]], BASE + "/" + s["section"] + ".html"),
        (s["headline"], BASE + "/articles/" + s["slug"] + ".html"),
    ]))
    return page(
        s["headline"], s["dek"], s["section"] + ".html" if s["section"] != "live" else "index.html",
        body, BASE + f"/articles/{s['slug']}.html", og_type="article", prefix="../",
        extra_head=schema, og_image=_og_image(s["slug"]),
    )


ADS_TXT = """# ads.txt for Western World News (westernworldnews.com)
# Advertising is not live yet. This file is a placeholder: add the
# Google AdSense publisher line here once AdSense is approved, e.g.:
# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
"""


def search_index_json():
    """Lightweight search index: headline/dek/section/date/url per story."""
    items = [{
        "slug": s["slug"],
        "headline": s["headline"],
        "dek": s["dek"],
        "section": SECTION_LABELS_PLAIN[s["section"]],
        "date": s["date"],
        "url": "articles/" + s["slug"] + ".html",
    } for s in STORIES]
    return json.dumps(items, ensure_ascii=False, indent=1)


# ---------------- Search page ----------------

def build_search():
    body = """
<div class="search-page">
<h1 class="section-head">Search</h1>
<form class="search-form" action="search.html" method="get" role="search">
<label for="q" class="sr-only">Search news</label>
<input type="search" id="q" name="q" placeholder="Search news..." aria-label="Search news" autocomplete="off">
<button type="submit">Search</button>
</form>
<p id="search-status" class="section-desc">Type a word or phrase above to search every story on Western World News.</p>
<div id="search-page-results"></div>
</div>
"""
    return page(
        "Search",
        "Search every story on Western World News.",
        "index.html", body, BASE + "/search.html",
    )


# ---------------- 404 page ----------------

def build_404():
    body = """
<div class="page-404">
<h1>Page not found</h1>
<p>Sorry, the page you are looking for does not exist or has moved.</p>
<p><a class="btn" href="index.html">Back to the homepage</a></p>
<p style="margin-top:1.2rem"><a href="world.html">World</a> &middot; <a href="us.html">US</a> &middot; <a href="europe.html">Europe</a> &middot; <a href="search.html">Search</a></p>
</div>
"""
    return page(
        "Page not found",
        "The page you are looking for does not exist on Western World News.",
        "index.html", body, BASE + "/404.html",
    )


# ---------------- Info pages ----------------

def build_info(slug, title, description, heading, paragraphs, extra=""):
    body = ('<div class="info-page"><h1 class="section-head">' + heading + "</h1>" + chr(10)
            + chr(10).join(f"<p>{p}</p>" for p in paragraphs)
            + (chr(10) + extra if extra else "") + "</div>")
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
            # Editorial review queue: new auto-published stories carry
            # reviewed=false (set by the publisher); older stories have
            # no flag and count as reviewed, so the queue only shows
            # stories published after the review system was added.
            "reviewed": s.get("reviewed", True),
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
        "justIn": [{"time": t, "text": h, "link": l or _justin_link(h) or ""} for t, h, l in JUST_IN],
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

MAIN_JS = """// Western World News: front-end behavior (v4 redesign).
// Renders dynamic regions from the content store (assets/js/content.js),
// so admin edits in localStorage apply across the whole site.
// Static HTML in each page is the SEO fallback when JS is unavailable.
// Newsletter forms post straight to Buttondown (or are disabled while the
// Buttondown username is unset): this script never fakes a subscription.
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
  // Mirror of the Python _dedup_dek_body in tools/build_site.py: the dek
  // is a truncation of the same summary the body starts with, so strip
  // the repeated dek text from the first body paragraph (dropping the
  // paragraph when nothing is left) instead of showing it twice.
  function dedupDekBody(a) {
    var paras = (a.body || []).slice();
    if (!a.dek || !paras.length) return paras;
    var first = paras[0];
    if (first === a.dek) return paras.slice(1);
    if (first.indexOf(a.dek) === 0) {
      var rest = first.slice(a.dek.length).replace(/^[ .]+/, "");
      if (rest) paras[0] = rest; else paras = paras.slice(1);
    }
    return paras;
  }
  function sectionLabel(slug) {
    var map = { world: "World", europe: "Europe", us: "US", politics: "Politics",
      "war-conflict": "War & Conflict", "business-finance": "Business",
      technology: "Technology", sport: "Sport", culture: "Culture", live: "Live" };
    return map[slug] || slug;
  }
  function readTime(a) {
    var words = (a.body || []).join(" ").split(/\\s+/).filter(function (w) { return w; }).length;
    return Math.max(1, Math.round(words / 200)) + " min read";
  }
  function sectionPage(slug) {
    var map = { world: "world.html", europe: "europe.html", us: "us.html",
      politics: "politics.html", "war-conflict": "war-conflict.html",
      "business-finance": "business-finance.html", technology: "technology.html",
      sport: "sport.html", culture: "culture.html" };
    return map[slug] || "world.html";
  }
  function tileFor(a, w, withCap) {
    w = w || 800;
    var h = Math.round(w * 9 / 16);
    if (a.image) {
      var img = '<img src="' + esc(a.image) + '" alt="' + esc(a.headline) +
        '" width="' + w + '" height="' + h + '" loading="lazy">';
      if (withCap === false) return "<figure>" + img + "</figure>";
      return "<figure>" + img + "<figcaption>" +
        esc(a.imageCaption || "Photo: Unsplash") + "</figcaption></figure>";
    }
    return '<div class="art" role="img" aria-label="Graphic placeholder"><span class="monogram">WWN</span>' +
      '<span class="art-label">' + esc(sectionLabel(a.section)) + "</span></div>";
  }
  function cardFor(a) {
    return '<article class="card">' + tileFor(a, 800) +
      '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
      '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
      "<p>" + esc(a.dek) + "</p>" +
      '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></article>";
  }
  function leadFor(a) {
    return '<article class="lead-card">' + tileFor(a, 1200) + "<div>" +
      '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
      '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
      "<p>" + esc(a.dek) + "</p>" +
      '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></div></article>";
  }
  function miniListFor(list) {
    return '<ul class="mini-list">' + list.map(function (a) {
      return '<li><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a>" +
        "<small>" + esc(sectionLabel(a.section)) + " &middot; " + esc(a.date) + "</small></li>";
    }).join("") + "</ul>";
  }

  var store = window.WWNStore ? window.WWNStore.get() : null;
  if (!store) return;
  var bySlug = {};
  store.articles.forEach(function (a) { bySlug[a.slug] = a; });

  // Load More (Latest News feed): reveal 10 hidden items per click.
  function initLoadMore() {
    var btn = $("#load-more"), list = $("#latest-list");
    if (!btn || !list) return;
    btn.addEventListener("click", function () {
      var hidden = $all(".latest-hidden", list).slice(0, 10);
      hidden.forEach(function (el) { el.classList.remove("latest-hidden"); });
      if (!$all(".latest-hidden", list).length) btn.style.display = "none";
    });
    if (!$all(".latest-hidden", list).length) btn.style.display = "none";
  }

  // Category pagination: 12 cards per page, buttons + count.
  function initPagination() {
    var grid = $(".paginated-grid");
    if (!grid) return;
    var cards = $all(".card", grid);
    var size = parseInt(grid.getAttribute("data-page-size") || "12", 10);
    var pages = Math.max(1, Math.ceil(cards.length / size));
    var pager = $("#pagination"), count = $("#page-count");
    var current = 1;
    function show(p) {
      current = p;
      cards.forEach(function (c, i) {
        c.style.display = (i >= (p - 1) * size && i < p * size) ? "" : "none";
      });
      if (pager) {
        var html = "";
        html += '<button class="page-btn" data-page="prev"' + (p === 1 ? " disabled" : "") + ">&larr; Prev</button>";
        for (var i = 1; i <= pages; i++) {
          html += '<button class="page-btn' + (i === p ? " active" : "") + '" data-page="' + i + '">' + i + "</button>";
        }
        html += '<button class="page-btn" data-page="next"' + (p === pages ? " disabled" : "") + ">Next &rarr;</button>";
        pager.innerHTML = html;
        $all(".page-btn", pager).forEach(function (b) {
          b.addEventListener("click", function () {
            var v = b.getAttribute("data-page");
            if (v === "prev") show(Math.max(1, current - 1));
            else if (v === "next") show(Math.min(pages, current + 1));
            else show(parseInt(v, 10));
          });
        });
      }
      if (count) {
        var from = (p - 1) * size + 1, to = Math.min(p * size, cards.length);
        count.textContent = "Showing " + from + "-" + to + " of " + cards.length + " stories";
      }
    }
    show(1);
  }

  document.addEventListener("DOMContentLoaded", function () {
    // Cookie consent banner.
    var cb = $("#cookie-banner");
    if (cb) {
      var choice = null;
      try { choice = localStorage.getItem("wwn-cookie-choice"); } catch (e) {}
      if (!choice) { cb.classList.add("show"); }
      var saveChoice = function (v) {
        try { localStorage.setItem("wwn-cookie-choice", v); } catch (e) {}
        if (v === "accepted" && typeof gtag === "function") {
          try { gtag("consent", "update", {"analytics_storage": "granted"}); } catch (e) {}
        }
        cb.classList.remove("show");
      };
      var acc = $("#cookie-accept");
      if (acc) acc.addEventListener("click", function () { saveChoice("accepted"); });
      var dec = $("#cookie-decline");
      if (dec) dec.addEventListener("click", function () { saveChoice("declined"); });
    }

    // Dateline (US format).
    $all("[data-today]").forEach(function (el) {
      el.textContent = new Date().toLocaleDateString("en-US", {
        weekday: "long", month: "long", day: "numeric", year: "numeric"
      });
    });

    // Site name from settings.
    $all("[data-site-name]").forEach(function (el) {
      var words = String(store.settings.siteName || "Western World News").split(" ");
      var last = words.pop();
      el.innerHTML = esc(words.join(" ")) + ' <span>' + esc(last) + "</span>";
    });

    // Share links (Facebook / X) point at the current page.
    var pageUrl = encodeURIComponent(window.location.href);
    var pageTitle = encodeURIComponent(document.title);
    $all('[data-share="facebook"]').forEach(function (a) {
      a.href = "https://www.facebook.com/sharer/sharer.php?u=" + pageUrl;
      a.target = "_blank"; a.rel = "noopener";
    });
    $all('[data-share="x"]').forEach(function (a) {
      a.href = "https://twitter.com/intent/tweet?url=" + pageUrl + "&text=" + pageTitle;
      a.target = "_blank"; a.rel = "noopener";
    });

    // Ticker (breaking story first, then Just In headlines, duplicated
    // for the marquee loop).
    var track = $(".ticker-track");
    if (track && store.justIn.length) {
      var normT = function (t) { return String(t || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim(); };
      // The breaking story may also be a Just In item: drop that duplicate
      // and put the breaking story first, matching the server render.
      var list = store.justIn.filter(function (it) {
        return !(store.breaking && store.breaking.text && normT(it.text) === normT(store.breaking.text));
      });
      var items = list.map(function (it) {
        var link = it.link || "";
        if (link) return '<a href="' + fixLink(link) + '">' + esc(it.text) + "</a>";
        return "<span>" + esc(it.text) + "</span>";
      }).join("");
      if (store.breaking && store.breaking.text) {
        var bLink = store.breaking.link || "";
        var bItem = bLink
          ? '<a href="' + fixLink(bLink) + '">' + esc(store.breaking.text) + "</a>"
          : "<span>" + esc(store.breaking.text) + "</span>";
        items = bItem + items;
      }
      track.innerHTML = items + items;
    }

    // Top-story card (homepage hero): photo with TOP STORY badge, navy
    // body with headline, dek and date + read time. The intro column and
    // the stacked stories beside it are server-rendered and stay as-is.
    var heroEl = $("[data-hero]");
    var hero = bySlug[store.settings.heroSlug] || store.articles[0];
    if (heroEl && hero) {
      var heroMedia = hero.image
        ? '<img src="' + esc(hero.image) + '" alt="' + esc(hero.headline) + '" width="1200" height="675" loading="eager">'
        : '<div class="art" role="img" aria-label="Graphic placeholder"><span class="monogram">WWN</span><span class="art-label">' + esc(sectionLabel(hero.section)) + "</span></div>";
      var liveLink = "";
      if (/ukraine|russia|kyiv|kremlin/i.test(hero.headline)) {
        liveLink = ' &middot; <a href="' + fixLink("live.html") + '">Follow live updates</a>';
      }
      heroEl.innerHTML =
        '<a class="top-hero-media" href="' + articleUrl(hero.slug) + '" aria-label="' + esc(hero.headline) + '">' +
        heroMedia + '<span class="top-story-badge">Top Story</span></a>' +
        '<div class="top-hero-body">' +
        '<h1><a href="' + articleUrl(hero.slug) + '">' + esc(hero.headline) + "</a></h1>" +
        '<p class="dek">' + esc(hero.dek) + "</p>" +
        '<p class="byline"><time>' + esc(hero.date) + "</time> &middot; " + readTime(hero) +
        liveLink + "</p></div>";
    }

    // Homepage section blocks (lead + cards, or lead + mini-list).
    $all("[data-section-block]").forEach(function (block) {
      var secs = (block.getAttribute("data-section") || "").split(",");
      var limit = parseInt(block.getAttribute("data-limit") || "4", 10);
      var layout = block.getAttribute("data-layout") || "cards";
      var list = store.articles.filter(function (a) {
        var s = a.sections || [a.section];
        return secs.some(function (x) { return s.indexOf(x) !== -1; });
      }).slice(0, limit);
      var target = $("[data-block-content]", block);
      if (!target || !list.length) return;
      if (layout === "split") {
        target.innerHTML = leadFor(list[0]) + miniListFor(list.slice(1));
      } else {
        target.innerHTML = leadFor(list[0]) +
          '<div class="card-grid three">' + list.slice(1).map(cardFor).join("") + "</div>";
      }
    });

    // Section pages: card grid (the lead card stays server-rendered).
    $all("[data-section-list]").forEach(function (list) {
      var sec = list.getAttribute("data-section-list");
      var items = store.articles.filter(function (a) { return (a.sections || [a.section]).indexOf(sec) !== -1; });
      if (!items.length) return;
      list.innerHTML = items.slice(1).map(cardFor).join("");
      initPagination();
    });

    // Latest News feed (homepage): newest 40, minus featured stories.
    var latestList = $("#latest-list");
    if (latestList) {
      var exclude = (latestList.getAttribute("data-exclude") || "").split(",").filter(Boolean);
      var latest = store.articles.filter(function (a) { return exclude.indexOf(a.slug) === -1; }).slice(0, 40);
      latestList.innerHTML = latest.map(function (a, i) {
        return '<li class="latest-item' + (i >= 10 ? " latest-hidden" : "") + '">' +
          '<a class="latest-thumb" href="' + articleUrl(a.slug) + '">' + tileFor(a, 400, false) + "</a><div>" +
          '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
          '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
          "<p>" + esc(a.dek) + "</p>" +
          '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></div></li>";
      }).join("");
      initLoadMore();
    } else {
      initLoadMore();
    }
    initPagination();

    // Trending Stories: numbered list, up to 10.
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
      var byHeadline = {};
      store.articles.forEach(function (a) {
        byHeadline[String(a.headline || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim()] = a.slug;
      });
      live.innerHTML = store.liveUpdates.map(function (u) {
        var slug = byHeadline[String(u.headline || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim()];
        var h3 = slug ? '<h3><a href="' + articleUrl(slug) + '">' + esc(u.headline) + "</a></h3>"
                      : "<h3>" + esc(u.headline) + "</h3>";
        return '<div class="live-update"><time>' + esc(u.time) + "</time>" + h3 +
          "<p>" + esc(u.text) + "</p></div>";
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
        if (heroBox) heroBox.innerHTML = tileFor(a, 1600);
        var bodyBox = $(".article-body", art);
        if (bodyBox) bodyBox.innerHTML = dedupDekBody(a).map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("");
        var src = $(".source-box", art);
        if (src) {
          var srcPhrase = a.source.indexOf("The ") === 0 ? "a report by " + esc(a.source) : "a " + esc(a.source) + " report";
          var words = (a.body || []).reduce(function (n, p) { return n + p.split(/\s+/).filter(Boolean).length; }, 0);
          if (words >= 400) {
            src.innerHTML = "<strong>Source</strong>Reporting by Western World News, based on " +
              srcPhrase + '. Read the original report at ' + esc(a.source) +
              ': <a href="' + esc(a.source_url) +
              '" target="_blank" rel="noopener">' + "Original article: " + esc(a.source) + "</a>.";
          } else {
            src.innerHTML = "<strong>Source</strong>This is a short summary of " +
              srcPhrase + '. Read the full story at ' + esc(a.source) +
              ': <a href="' + esc(a.source_url) +
              '" target="_blank" rel="noopener">' + "Original article: " + esc(a.source) + "</a>.";
          }
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

    // Search toggle: tap the magnifier to open the search box.
    var sToggle = $("#search-toggle"), sBox = $(".search-box");
    if (sToggle && sBox) {
      sToggle.addEventListener("click", function () {
        var open = sBox.classList.toggle("open");
        if (open) { var si = $("#site-search"); if (si) si.focus(); }
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") sBox.classList.remove("open");
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
        var all = prefix() + "search.html?q=" + encodeURIComponent(input.value.trim());
        box.innerHTML = hits.length
          ? hits.map(function (a) {
              return '<a href="' + articleUrl(a.slug) + '"><small>' + esc(sectionLabel(a.section)) +
                "</small>" + esc(a.headline) + "</a>";
            }).join("") + '<a href="' + all + '"><small>Search</small>See all results &rarr;</a>'
          : '<div class="none">No stories match "' + esc(input.value.trim()) + '".</div>';
        box.classList.add("open");
      });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          window.location.href = prefix() + "search.html?q=" + encodeURIComponent(input.value.trim());
        }
        if (e.key === "Escape") { box.classList.remove("open"); input.blur(); }
      });
      input.addEventListener("blur", function () {
        setTimeout(function () { box.classList.remove("open"); }, 200);
      });
    }

    // Search results page (search.html): filter the generated index.
    var resultsEl = $("#search-page-results");
    if (resultsEl) {
      var params = new URLSearchParams(window.location.search);
      var q = (params.get("q") || "").trim();
      var qInput = $("#q");
      if (qInput) qInput.value = q;
      var status = $("#search-status");
      if (!q) {
        if (status) status.textContent = "Type a word or phrase above to search every story on Western World News.";
        return;
      }
      fetch(prefix() + "search-index.json").then(function (r) { return r.json(); }).then(function (idx) {
        var ql = q.toLowerCase();
        var hits = idx.filter(function (a) {
          return (a.headline + " " + a.dek + " " + a.section).toLowerCase().indexOf(ql) !== -1;
        });
        if (status) status.textContent = hits.length + (hits.length === 1 ? " result" : " results") + ' for "' + q + '"';
        resultsEl.innerHTML = hits.map(function (a) {
          return '<article class="search-result"><p><span class="kicker">' + esc(a.section) + "</span></p>" +
            '<h3><a href="' + prefix() + esc(a.url) + '">' + esc(a.headline) + "</a></h3>" +
            "<p>" + esc(a.dek) + "</p>" +
            '<p class="byline"><time>' + esc(a.date) + "</time></p></article>";
        }).join("") || "<p>No stories match that search. Try a different word or phrase.</p>";
      }).catch(function () {
        if (status) status.textContent = "Search is unavailable right now. Please try again.";
      });
    }
  });
})();
"""


# ---------------- Admin panel ----------------
# NOTE: the admin passcode lives in the ADMIN_JS template below
# (var PASSCODE = ...). It is a basic gate on a static site, not real
# security — anyone who can read the built admin.js can see it. Change
# it there and rebuild; do not print the value on any page or in docs.

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
// To change the passcode, edit the PASSCODE line below (in this template
// in tools/build_site.py), then rebuild and push.
(function () {
  var PASSCODE = "Happy@1221#";
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
    renderReview();
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
    $("#stat-review").textContent = data.articles.filter(function (a) { return a.reviewed === false; }).length;
    $("#saved-note").textContent = store.hasSaved()
      ? "You have unpublished changes saved in this browser. Export JSON below to make them permanent."
      : "No unpublished changes. Showing the site's default content.";
  }
  // Review queue: auto-published stories start unreviewed. Marking one
  // reviewed only records that a human checked it against its source;
  // it does not change the published page. Use Export JSON to make the
  // reviewed flags permanent in the repo.
  function renderReview() {
    var list = $("#review-list");
    var pending = data.articles.filter(function (a) { return a.reviewed === false; });
    list.innerHTML = pending.map(function (a) {
      var src = a.source_url
        ? ' <a href="' + esc(a.source_url) + '" target="_blank" rel="noopener">Source: ' + esc(a.source) + '</a>'
        : " · Source: " + esc(a.source);
      return '<li><div class="t"><b>' + esc(a.headline) + "</b>" +
        "<small>" + esc(SECTION_LABELS[a.section] || a.section) + " · " + esc(a.date) + src + "</small></div>" +
        '<button class="btn small" data-review="' + esc(a.slug) + '">Mark reviewed</button>' +
        '<button class="btn small" data-edit="' + esc(a.slug) + '">Edit</button></li>';
    }).join("") || '<li>Nothing waiting for review.</li>';
    list.querySelectorAll("[data-review]").forEach(function (b) {
      b.addEventListener("click", function () {
        var slug = b.getAttribute("data-review");
        var a = data.articles.find(function (x) { return x.slug === slug; });
        if (!a) return;
        a.reviewed = true;
        save("Marked reviewed: " + a.headline);
      });
    });
    list.querySelectorAll("[data-edit]").forEach(function (b) {
      b.addEventListener("click", function () { openArticleForm(b.getAttribute("data-edit")); });
    });
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
      imageCaption: $("#af-caption").value.trim() || "Photo: Unsplash",
      // A human just wrote or edited this story, so it counts as reviewed.
      reviewed: true
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
<p>Enter the admin passcode to manage the site. (Change the passcode in the ADMIN_JS template in tools/build_site.py. Note: this is a basic gate on a static site, not real server security.)</p>
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
To make them permanent for everyone, use <b>Export JSON</b> below and send the file to Muse, or save it in the site folder as <b>content-export.json</b> and rebuild the site. Until then, other browsers still see the default content.</div>
<div class="admin-grid">
<div class="stat"><b id="stat-articles">0</b><span>Articles</span></div>
<div class="stat"><b id="stat-sections">0</b><span>Sections in use</span></div>
<div class="stat"><b id="stat-justin">0</b><span>Just In items</span></div>
<div class="stat"><b id="stat-live">0</b><span>Live updates</span></div>
<div class="stat"><b id="stat-review">0</b><span>Needs review</span></div>
</div>
<p id="saved-note" style="color:var(--muted)"></p>

<section class="panel"><h2>Review queue</h2><div class="body">
<p class="note">New stories published automatically start here as <b>unreviewed</b> — the publisher does not hold them back, it only flags them. Read each one against its source link, then mark it reviewed. Marking reviewed is a record for the site operator; it does not change what readers see. Older stories published before this system was added do not appear here.</p>
<ul class="admin-list" id="review-list"></ul>
</div></section>

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
<p>Export downloads the site's full content as <b>wwn-content.json</b>. To make admin changes permanent for all visitors, send that file to Muse, or save it in the site folder as <b>content-export.json</b> and re-run the build script (<b>tools/build_site.py</b>). The static pages are then regenerated with your content, including a real page for every new article.</p>
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

A plain static news website (HTML + CSS + JavaScript) with a premium
navy-and-white newspaper design and an admin panel. No build step needed
to view it, no database, no framework. Upload the contents of this folder
to any static host (GitHub Pages, Netlify, Cloudflare Pages, Hostinger)
and it works.

## What's in the design (v4, November 2026 redesign)

- White top bar with the wordmark, the tagline "Independent News. Global
  Perspective.", the date and share links; dark navy sticky navigation
  (Home, World, US, Europe, Politics, War & Conflict, Business,
  Technology, Culture) with a working search box and a mobile hamburger
  menu. Sport stays as a section page, linked from the footer.
- Red BREAKING bar with the newest headline and a scrolling Just In
  ticker; every headline links to a real article.
- Homepage in editorial order: hero (large featured story + two
  secondary stories), Top Stories (one card per category), World, US News
  & Politics, Europe, War & Conflict, Business + Technology side by side,
  a chronological Latest News feed with a Load More button, and the
  newsletter section "Stay Informed. Stay Ahead."
- Article pages: breadcrumb, category label, headline, summary, author,
  dates, featured image, a 700-760px content column, a 300px sidebar
  (Trending Stories, Latest News, Popular Categories, advertising space),
  related stories, previous/next article and an author profile.
- Dark navy footer with four columns (Brand, Explore, About, Legal).
- Reserved, clearly labelled "Advertisement" areas (below the navigation,
  between homepage sections, article sidebar, after article content).
  They are empty until advertising is approved. No fake ads.
- Serif display headlines (Merriweather) + Inter body text.
- Photos are **real photos that match each story** — the feed's own
  image for that story, verified to load, or freely licensed Wikimedia
  Commons / Unsplash images used as clearly labelled illustrations where
  no real photo of the subject exists. Every caption says honestly what
  the photo shows. Stories without a suitable photo get the navy WWN
  tile instead of a misleading image.

## Folder structure

```
western-world-news/
├── index.html                  Homepage: breaking bar, hero, Top Stories,
│                               World, US & Politics, Europe, War &
│                               Conflict, Business + Technology, Latest
│                               News (Load More), newsletter
├── world.html / europe.html / us.html / politics.html
├── war-conflict.html / business-finance.html / technology.html
├── sport.html / culture.html
├── live.html                   Live blog (Ukraine war, rolling updates)
├── search.html                 Search results page (search-index.json)
├── 404.html                    Branded "page not found"
├── about.html / contact.html / privacy.html / terms.html
├── disclaimer.html / editorial-policy.html / corrections.html
├── cookie-policy.html / advertise.html / authors.html
├── admin.html                  Admin panel (passcode gate, see below)
├── articles/                   One HTML page per story
├── assets/
│   ├── css/style.css           All site styling
│   ├── css/admin.css           Admin panel styling
│   └── js/
│       ├── content.js          Central content store (default content +
│       │                       localStorage merge used by every page)
│       ├── main.js             Dateline, search, hamburger, Load More,
│       │                       pagination, dynamic regions from the
│       │                       content store
│       └── admin.js            Admin panel logic (passcode gate; see the
│                               ADMIN_JS template in tools/build_site.py)
├── data/articles.json          All article text (source of truth for the
│                               build; updated by tools/auto_publish.py)
├── data/search-index.json      (generated) lightweight search index
├── tools/build_site.py         Generator — re-run to rebuild every page
├── tools/auto_publish.py       Hourly auto-publisher (RSS feeds → new
│                               stories; see "Automatic publishing" below)
├── .github/workflows/          auto-publish.yml — GitHub Actions schedule
├── content-export.json         (optional) admin export; if present, the
│                               build script uses it as the content source
├── sitemap.xml / news-sitemap.xml / post-sitemap.xml
├── page-sitemap.xml / robots.txt / ads.txt
└── README.md                   This file
```

## Admin panel — how it works

Open **admin.html** and enter the passcode:

- **Passcode:** the admin gate uses a default passcode. Change it in the
  ADMIN_JS template in `tools/build_site.py` (the `var PASSCODE = ...`
  line), then rebuild and push. It is a basic gate, not real security —
  do not print the value on any page or in docs.
- The dashboard shows article/section/Just In/live counts, plus a
  **Review queue** of new auto-published stories waiting for a human
  check (see \"Editorial review\" below).
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
2. Send that file to Muse, **or** save it in this folder as
   `content-export.json` and run `python3 tools/build_site.py`.
3. The script regenerates every static page from your exported content,
   including a real page for each new article, then the updated files
   are committed/pushed as usual.

## Content — how it stays fresh

New articles are researched and written by the editorial team from
several trusted sources and published several times a day. The homepage
hero, the Just In feed and the breaking bar update with every new story.
(The old hourly automatic publisher that posted short summaries is paused
since 2026-11-28 — see `tools/auto_publish.py`, PUBLISHING_PAUSED.)

- Every story is an **original article written in our own words** from
  reporting by trusted sources — nothing is copied from another publication.
- Every story **credits its sources by name and links to the original
  articles** (BBC, Al Jazeera, The Guardian, Euronews, France 24, DW,
  Reuters and others).
- Every story is a full researched article.
- Section classification is done by the publisher from the headline:
  war and conflict, business, technology, US, Europe, or world. Stories
  are re-checked at build time so the Europe section only carries
  European news.

## Newsletter — Buttondown (live)

The newsletter is wired for **Buttondown** (free tier) and live at
`buttondown.com/pintu` ("Western World News"). The forms post to
Buttondown's free embed endpoint
(`buttondown.com/api/emails/embed-subscribe/pintu`), which handles
double opt-in and its own confirmation page. The username is set in
`tools/build_site.py` as `NEWSLETTER_BUTTONDOWN_USERNAME = "pintu"`.

## Advertising — not live yet

- Reserved "Advertisement" areas are built into the layout (below the
  navigation, between homepage sections, article sidebar, after article
  content). They are empty placeholders until advertising is approved.
- `ads.txt` is a placeholder until an AdSense publisher ID exists.
- The privacy policy and terms describe advertising in the future tense
  until ads actually run. Do not present the site as showing ads before
  approval.

## Not yet connected — before launch

- **Newsletter**: live via Buttondown (buttondown.com/pintu).
- **Contact email addresses**: lurenmira@gmail.com (used for both news tips
  and advertising inquiries).
- **Privacy policy** is complete, including the future advertising
  disclosure.
- **Domain**: westernworldnews.com — live since 20 Nov 2026 (GitHub Pages, DNS via Hostinger).
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
The Guardian, Euronews, France 24, DW), adds 1 new story per
hourly run (max 20/day) to `data/articles.json`, refreshes the Just In
feed, feeds Ukraine-war stories into the live blog, rebuilds the site
and pushes — using only the automatic `GITHUB_TOKEN`. Auto stories are
short summaries of the source's own report with a "Read the full
story" link, and the photo is the feed's own image for that story
(verified to load) or no photo at all. Nothing is independently
verified before publication — stories are selected by keyword filters
only. Test locally first: `python3 tools/auto_publish.py --dry-run`.

### Editorial review (flag + queue, no gate by default)

New auto-published stories start with `reviewed: false` and appear in
the admin panel's **Review queue** (dashboard, "Needs review" count).
The publisher does **not** hold them back — they go live immediately
and are only flagged. To review: open the admin, read the story
against its source link, then **Mark reviewed** (or edit and save it —
saving counts as reviewed). Use **Export JSON** to make the reviewed
flags permanent in the repo.

To require human approval **before** a story goes live, set
`REVIEW_GATE = True` in `tools/auto_publish.py`: new stories are then
held in `data/pending-review.json` and nothing is published until the
owner releases them (review in the admin, then move them into
`data/articles.json` and rebuild). Leave it `False` unless the owner
wants that extra step — with the gate on, the site can go quiet if
nobody clears the pending file.

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
            # Review flag survives an admin export round-trip: a story
            # the admin exported without reviewing stays in the queue.
            "reviewed": a.get("reviewed", True),
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
    for section in ["world", "europe", "us", "politics", "war-conflict", "business-finance", "technology", "sport", "culture"]:
        files.append(write(section + ".html", build_section(section, section + ".html")))
    files.append(write("live.html", build_live()))
    files.append(write("search.html", build_search()))
    files.append(write("404.html", build_404()))
    files.append(write("ads.txt", ADS_TXT))
    files.append(write("search-index.json", search_index_json()))
    for s in STORIES:
        files.append(write("articles/" + s["slug"] + ".html", build_article(s)))
    files.append(write("admin.html", build_admin()))

    files.append(write("about.html", build_info(
        "about", "About Western World News",
        "About Western World News: independent news from the West and the world.",
        "About us",
        ["Western World News is an independently run news website covering worldwide news with a main focus on Western and European politics, war and breaking news, plus a small Business &amp; Finance section. It is owned and operated by its publisher and is not part of a larger media group.",
         "Our stories are researched and written by the Western World News editorial team. Each article is based on reporting from several trusted sources — the BBC, Al Jazeera, The Guardian, Euronews, France 24, DW, Reuters and others — rewritten in our own words, checked before publication, and credited with links to the original reporting. Every story on the site is a full researched article. If a detail matters, please read the original article.",
         "The site is free to read. There is no paywall.",
         "Contact us via the contact page."])))
    files.append(write("contact.html", build_info(
        "contact", "Contact Western World News",
        "Contact Western World News: news tips, corrections and advertising inquiries.",
        "Contact",
        ["News tips, corrections and general inquiries: lurenmira@gmail.com.",
         "For corrections, please include the story headline and the fact to be corrected. Corrections are made manually after your report is read; we do not promise a response time.",
         "Advertising inquiries: lurenmira@gmail.com."],
        extra=contact_form_html())))
    files.append(write("privacy.html", build_info(
        "privacy", "Privacy policy | Western World News",
        "Privacy policy for Western World News: what we collect, cookies, and how advertising works.",
        "Privacy policy",
        ["Western World News is a free news website. This privacy policy explains what information we collect when you visit westernworldnews.com, how we use it, and the choices you have. If you do not agree with this policy, please do not use the site.",
         "Information you send us. We do not ask you to create an account, and we do not collect your name, address, or payment details. If you email us, we receive the email address and the message you send, and we use it only to reply to you. If you sign up for our newsletter, your email address is sent to Buttondown, the service that runs our newsletter list: Buttondown stores it, sends you a confirmation email, and handles unsubscribes. Your newsletter address is governed by Buttondown's privacy policy as well as this one. We do not sell your email address or any other personal information, and we do not share it except with the services named here or where the law requires it.",
         "Cookies and advertising. Advertising may appear on this site in the future, once an advertising program such as Google AdSense is approved. Until then, no advertising is shown and no advertising cookies are used. When advertising does appear, third-party vendors, including Google, may use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and other sites on the internet. You can opt out of personalized advertising by visiting <a href='https://adssettings.google.com/'>Google Ads Settings</a>, or by visiting <a href='https://www.aboutads.info/choices/'>www.aboutads.info/choices</a>. This section describes how advertising on this site will work when ads are live.",
         "Analytics. This site uses Google Analytics to understand how visitors use it, such as which stories are read most and where visitors come from. Google Analytics uses cookies and collects anonymous usage data. It does not collect your name, address, or payment details. The Google Analytics tag loads on every page, but with consent mode it stores nothing and collects no analytics data unless you accept cookies on the banner at the bottom of the page. If you decline, no analytics data is stored.",
         "Links to other websites. Our stories link to the original reporting on other websites, such as the BBC, Al Jazeera, The Guardian, Euronews, France 24, and DW. Those sites have their own privacy policies, and we are not responsible for how they handle your information.",
         "Children's privacy. This site is a general news site and is not directed at children under 13. We do not knowingly collect personal information from children under 13. If you believe a child has sent us personal information, please contact us at lurenmira@gmail.com and we will delete it from our mailbox and our newsletter list.",
         "Changes to this policy. We may update this policy from time to time. The current version is always the one published on this page.",
         "Contact. If you have questions about this policy, contact us through the <a href='contact.html'>contact page</a>."])))
    files.append(write("terms.html", build_info(
        "terms", "Terms of Service | Western World News",
        "Terms of Service for Western World News: the rules for using this free news website.",
        "Terms of Service",
        ["These terms explain the rules for using westernworldnews.com. By using the site, you agree to these terms. If you do not agree, please do not use the site.",
         "Free to read. Western World News is free to read. There is no paywall, and you do not need an account to read our stories.",
         "Our content. Our stories are original articles researched and written by Western World News from reporting by the sources we credit and link to. The original reporting belongs to its publishers. You are welcome to share links to our stories. Please do not copy our text and republish it as your own.",
         "Accuracy. News changes fast. Our articles are checked before publication, but facts can change within hours and stories are not routinely updated after publication. We correct mistakes when they are reported to us by email, but we cannot promise that every fact on the site is complete or current at all times, and you should check important facts against the original reporting. See our <a href='corrections.html'>corrections policy</a> for how corrections work.",
         "Not advice. Nothing on this site is financial, legal, medical, or professional advice. Do not rely on a news summary to make financial, legal, or medical decisions.",
         "Advertising. Advertising may appear on this site in the future, once approved. There is currently no advertising on the site. Any advertising that appears will be separate from our editorial content, and advertising will not affect what we report or how we report it. See our <a href='privacy.html'>privacy policy</a> for how advertising cookies work.",
         "Changes and availability. We may change, pause, or remove any part of the site at any time, and we may update these terms. The current terms are always the ones published on this page.",
         "Liability. The site is provided as it is, without warranties of any kind. We are not liable for any loss or damage that comes from using the site or relying on its content.",
         "Contact. If you have questions about these terms, contact us through the <a href='contact.html'>contact page</a>."])))
    files.append(write("disclaimer.html", build_info(
        "disclaimer", "Disclaimer | Western World News",
        "Disclaimer for Western World News: what our news summaries are, and what they are not.",
        "Disclaimer",
        ["Western World News publishes original news articles based on reporting by trusted news organizations, including the BBC, Al Jazeera, The Guardian, Euronews, France 24, DW, and Reuters. Each story credits and links to its original sources.",
         "Our articles are written in our own words from several sources, credited and linked to the originals. Every story on the site is a full researched article. If a detail matters to you, please read the original article we link to.",
         "News changes fast. Facts can change within hours of a story being published. Published articles are not routinely updated after publication. If you spot a mistake, please report it by email and we will correct it manually. But we cannot promise that every page is current at the moment you read it.",
         "Not advice. Nothing on this site is financial, legal, medical, or other professional advice, and nothing here should be treated as a recommendation to buy, sell, or do anything else.",
         "Images. Photos on this site come from freely licensed sources such as Pexels, credited to the photographer, or from the news feed that published the story, credited to that publisher. We are replacing publisher photos with licensed photos. We do not own the news photos we display; they remain the property of their publishers. Photos labelled as illustrations do not show the event described in the story.",
         "Links. Our stories link to other websites. We are not responsible for the content or privacy practices of those sites."])))
    files.append(write("editorial-policy.html", build_info(
        "editorial-policy", "Editorial Policy | Western World News",
        "Editorial Policy for Western World News: how we choose, check, and write our news.",
        "Editorial Policy",
        ["Western World News is an independently run news site. We cover worldwide news with a main focus on Western and European politics, war and conflict, and breaking news, plus a small Business and Finance section.",
         "Trusted sources. Our stories are researched from the reporting of trusted news organizations — the BBC, Al Jazeera, The Guardian, Euronews, France 24, DW, Reuters and others. Each article is written in our own words from several sources and checked before publication. We do not base stories on rumors or anonymous social media posts as a matter of policy, but an unconfirmed claim in a source report can still appear here, so please check important facts against the original report.",
         "How stories are made. Each article is researched from multiple sources, written in our own words, and checked before it is published, with the sources credited by name and linked so readers can check the facts themselves. Every story on the site is a full researched article. We do not copy full articles, and we do not present a source's words as our own reporting.",
         "What we do not publish. We filter out clearly off-topic material (puzzles, celebrity gossip, reviews, horoscopes and similar). We do not publish graphic war detail as a matter of policy.",
         "Corrections. Errors reported by email are fixed manually when noticed. We do not promise a speed for corrections, and there is no standing correction-note format on stories. See our <a href='corrections.html'>corrections policy</a> for the details.",
         "Advertising and sponsorship. There is currently no advertising or sponsored content on this site. If advertising appears in the future, it will be separate from editorial content. We do not present sponsored content as news, and advertisers will not decide what we cover or how we cover it.",
         "Photos. Photos come from freely licensed sources such as Pexels, credited to the photographer, or from the news feed that published the story, credited to that publisher. We are replacing publisher photos with licensed photos. We label illustrations clearly as illustrations. We never present stock or generated imagery as real event footage. This site has no video content."])))
    files.append(write("corrections.html", build_info(
        "corrections", "Corrections Policy | Western World News",
        "Corrections Policy for Western World News: how we fix mistakes, and how to report one.",
        "Corrections Policy",
        ["Western World News aims to get every fact right. When we make a mistake, we fix it.",
         "How we correct. Errors are fixed manually after they are reported to us by email. Small typos and formatting fixes are corrected quietly. If a fact in a story was wrong, we correct the story. We do not promise a response time, and there is no standing correction-note format on story pages.",
         "How to report an error. If you spot a mistake, please tell us through the <a href='contact.html'>contact page</a>. Include the headline of the story and the fact that needs correcting. Reports sent to the contact email are read by the site operator.",
         "What we do not do. We do not remove stories because someone dislikes the news. We correct facts when they are shown to be wrong.",
         "Sources. Most of our facts come from the reporting we credit and link to. If the original source corrects its own report, we update our article when we notice it or when someone reports it to us by email."])))
    files.append(write("authors.html", build_info(
        "authors", "Our Editorial Team | Western World News",
        "Our Editorial Team: the people behind Western World News, and how our stories are made.",
        "Our Editorial Team",
        ["Stories on Western World News are published under the Western World News Editorial Team byline. Each story is researched from several trusted sources and written in our own words by the editorial team, then checked before publication.",
         "How we work. Our team follows the news through trusted outlets — the BBC, Al Jazeera, The Guardian, Euronews, France 24, DW, Reuters and others — and publishes full articles on the most important stories several times a day. Every story on the site is a full researched article.",
         "Each story credits its sources by name and links to the original reports so readers can check the facts themselves.",
         "New stories are added through the day as important news breaks. The live blog is updated only when new Ukraine-war stories are published. When we make a mistake, we correct it manually after it is reported to us by email. See our <a href='editorial-policy.html'>editorial policy</a> and our <a href='corrections.html'>corrections policy</a> for the details.",
         "Contact. Messages go to the site's single contact email address, lurenmira@gmail.com, for news tips, corrections, or questions about our coverage."])))

    files.append(write("cookie-policy.html", build_info(
        "cookie-policy", "Cookie Policy | Western World News",
        "Cookie Policy for Western World News: which cookies we use and how to control them.",
        "Cookie Policy",
        ["This page explains which cookies Western World News uses and how you can control them.",
         "What cookies are. Cookies are small text files that a website asks your browser to store. They let the site remember a choice you made, such as accepting or declining cookies.",
         "Cookies we use. This site stores one cookie-choice record in your browser's local storage (not as a cookie) to remember whether you accepted or declined cookies on the banner at the bottom of the page. The Google Analytics tag loads on every page, but with consent mode it stores no data and collects nothing unless you accept cookies. If you accept cookies, Google Analytics runs and uses its own cookies to collect anonymous usage data, such as which stories are read most and where visitors come from. It does not collect your name, address, or payment details.",
         "Advertising cookies. Advertising may appear on this site in the future, once an advertising program such as Google AdSense is approved. Until then, no advertising is shown and no advertising cookies are used. When advertising does appear, third-party vendors, including Google, may use cookies to serve ads based on your prior visits to this website or other websites. You can opt out of personalized advertising by visiting <a href='https://adssettings.google.com/'>Google Ads Settings</a>, or by visiting <a href='https://www.aboutads.info/choices/'>www.aboutads.info/choices</a>.",
         "How to control cookies. You can accept or decline cookies on the banner at the bottom of every page. You can also delete cookies or block them in your browser settings at any time. Blocking cookies does not stop you reading the site.",
         "Contact. If you have questions about this policy, contact us through the <a href='contact.html'>contact page</a>."])))
    files.append(write("advertise.html", build_info(
        "advertise", "Advertise With Us | Western World News",
        "Advertise with Western World News: reach readers in the United States, the United Kingdom, Europe and Canada.",
        "Advertise With Us",
        ["Western World News covers world news, politics, war and conflict, business and technology, with new stories added automatically through the day.",
         "There are no advertising placements on the site yet, and no advertising program has been approved. Advertising space is reserved for future sponsors.",
         "If you would like to advertise with us, please contact us at lurenmira@gmail.com with details of what you would like to promote. Enquiries are answered by email; availability and rates do not exist yet, because no advertising program has been approved.",
         "Advertising is always separate from editorial content. Advertisers do not decide what we cover or how we cover it, and advertising is never presented as news."])))

    # robots.txt — keep the admin panel out of search engines.
    files.append(write("robots.txt",
        "User-agent: *" + chr(10) + "Allow: /" + chr(10)
        + "Disallow: /admin.html" + chr(10) + chr(10)
        + "Sitemap: " + BASE + "/sitemap.xml" + chr(10)
        + "Sitemap: " + BASE + "/news-sitemap.xml" + chr(10)
        + "Sitemap: " + BASE + "/post-sitemap.xml" + chr(10)
        + "Sitemap: " + BASE + "/page-sitemap.xml" + chr(10)))

    # Sitemaps (admin deliberately excluded from all of them).
    page_urls = ["", "world.html", "europe.html", "us.html", "politics.html",
                 "war-conflict.html", "business-finance.html", "technology.html",
                 "sport.html", "culture.html", "live.html", "about.html",
                 "contact.html", "privacy.html", "terms.html", "disclaimer.html",
                 "editorial-policy.html", "corrections.html", "authors.html",
                 "cookie-policy.html", "advertise.html"]
    article_urls = ["articles/" + s["slug"] + ".html" for s in STORIES]
    urls = page_urls + article_urls
    today_date = datetime.date.today()
    today = today_date.isoformat()
    url_lastmod = {u: today for u in page_urls}
    for s in STORIES:
        url_lastmod["articles/" + s["slug"] + ".html"] = _iso_date(s["date"])
    entries = "".join(
        f"  <url><loc>{BASE}/{u}</loc><lastmod>{url_lastmod[u]}</lastmod></url>\n" for u in urls
    )
    files.append(write("sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "</urlset>\n"))

    # post-sitemap.xml: articles only.
    post_entries = "".join(
        f"  <url><loc>{BASE}/{u}</loc><lastmod>{url_lastmod[u]}</lastmod></url>\n" for u in article_urls
    )
    files.append(write("post-sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + post_entries + "</urlset>\n"))

    # page-sitemap.xml: non-article pages only.
    page_entries = "".join(
        f"  <url><loc>{BASE}/{u}</loc><lastmod>{url_lastmod[u]}</lastmod></url>\n" for u in page_urls
    )
    files.append(write("page-sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + page_entries + "</urlset>\n"))

    # news-sitemap.xml: Google News format, articles from the last 2 days only.
    news_items = []
    for s in STORIES:
        d = _parse_date(s["date"])
        if d and 0 <= (today_date - d).days <= 2:
            news_items.append(s)
    news_entries = "".join(
        "  <url>\n"
        f"    <loc>{BASE}/articles/{s['slug']}.html</loc>\n"
        "    <news:news>\n"
        "      <news:publication>\n"
        "        <news:name>Western World News</news:name>\n"
        "        <news:language>en</news:language>\n"
        "      </news:publication>\n"
        f"      <news:publication_date>{_iso_date(s['date'])}</news:publication_date>\n"
        f"      <news:title>{hescape(s['headline'])}</news:title>\n"
        "    </news:news>\n"
        "  </url>\n" for s in news_items
    )
    files.append(write("news-sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n'
        + news_entries + "</urlset>\n"))

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
