# Western World News — westernworldnews.com

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
  check (see "Editorial review" below).
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
