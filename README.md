# Western World News — westernworldnews.com

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
- Photos are **real photos that match each story** — freely licensed Wikimedia Commons pictures of the actual place or institution (Kyiv, the European Parliament, Shenzhen, the US Capitol, Wall Street, the Peace Palace), and openly licensed Unsplash images used as clearly labelled illustrations where no real photo of the subject exists. Every caption says honestly what the photo shows. Stories without a suitable photo get the navy WWN gradient tile instead of a misleading image.

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
├── tools/build_site.py         Generator — re-run to rebuild every page
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

The articles in `articles/` are the current front page, refreshed on the evening of 20 November 2026 with verified stories from 19–20 November 2026 (the Kyiv missile strikes, the EU–UK reset deal, the Shenzhen summit fallout, the Gaza Yellow Line raid, the US Congress records fight, the Wall Street sell-off, the Nations League draw, the ICJ’s Myanmar genocide ruling, and RAYE’s Grammy nominations).

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
- **Domain**: westernworldnews.com — live since 20 Nov 2026 (GitHub Pages, DNS via Hostinger).
- **Ads**: none included yet. Add ad slots only after traffic exists.
- **GitHub**: the site is pushed to github.com/pintuguptaji/western-world-news (branch main); push updates with the GitHub connector.

## Rebuilding

Run `python3 tools/build_site.py` (or `python3 /tmp/build_site_v2.py`).
To change the shared header, footer, navigation or design, edit the
script and re-run it — or edit the HTML/CSS files directly; they are
plain and self-contained.
