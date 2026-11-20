#!/usr/bin/env python3
"""Build script for Western World News (static site).
Generates all HTML pages, sitemap.xml and robots.txt from the STORIES
data below. Run: python3 /tmp/build_site.py
Seed content: original summaries of real stories, 16-20 Nov 2026,
each credited to its source with a link. See README.md in the site root.
"""
import os

OUT = os.path.expanduser("~/workspace/western-world-news")
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
STORIES = [
    {
        "slug": "russia-ukraine-missile-attack",
        "sections": ["war-conflict", "world"],
        "section": "war-conflict",
        "headline": "Russia launches one of the largest missile attacks of the war on Ukraine",
        "dek": "More than 110 missiles were fired overnight, Ukrainian officials say, hours after Trump, Putin and Xi met in China — and as Poland scrambled jets after its airspace was violated.",
        "date": "20 November 2026",
        "source": "CNN",
        "source_url": "https://www.cnn.com/2026/11/20/europe/russia-ukraine-putin-trump-intl-hnk",
        "body": [
            "Russia launched a large overnight missile and drone attack on Ukraine into Friday, Ukrainian officials said, killing at least eight people and injuring at least 28, in what Kyiv described as one of the largest aerial assaults of the war.",
            "Ukraine said Russia fired at least 110 missiles overnight — an unusually large number even by the standards of a war now in its fifth year. The attack lasted more than ten hours, according to Ukrainian authorities.",
            "Russia's defence ministry said it had carried out a \u201cmassive strike\u201d with high-precision weapons launched from land, sea and air, as well as drones, targeting military and energy facilities, port infrastructure in the Odesa region and transport infrastructure in Kyiv. President Volodymyr Zelensky said \u201cabsolutely all the targets were ordinary civilian infrastructure\u201d.",
            "Three bridges in Kyiv were damaged, according to mayor Vitaly Klitschko, cutting transport links between the two sides of the capital.",
            "Poland said fighter jets were scrambled and Patriot air defence systems activated early on Friday after objects flew into and fell inside Polish territory during the attack.",
            "The strikes came hours after President Vladimir Putin met US President Donald Trump and Chinese leader Xi Jinping for trilateral talks in Shenzhen. Trump later spoke with European leaders and, according to a senior European official, described Putin as \u201ctired\u201d and ready for a deal. The talks produced no breakthrough, and no official declaration was released.",
            "Putin had vowed revenge for Ukraine's recent attacks on the bridge linking Russia with occupied Crimea.",
        ],
        "related": ["gaza-ceasefire-collapse-warning", "trump-xi-putin-shenzhen-summit", "eu-ukraine-loan-45-billion"],
    },
    {
        "slug": "trump-xi-putin-shenzhen-summit",
        "sections": ["world", "politics"],
        "section": "world",
        "headline": "Trump, Xi and Putin hold historic trilateral talks — but no breakthrough on Ukraine",
        "dek": "The leaders of the three biggest nuclear powers met in Shenzhen for the first time, agreeing a joint declaration on the UN, nuclear weapons and oil — while the war in Ukraine went on.",
        "date": "19 November 2026",
        "source": "The Times",
        "source_url": "https://www.thetimes.com/world/asia/article/trump-xi-putin-summit-shenzhen-latest-news-ddskr7pcx",
        "body": [
            "The leaders of the United States, China and Russia met in Shenzhen on Thursday for the first trilateral talks between the three nuclear powers.",
            "A joint declaration covered reform of the United Nations, nuclear weapons, oil production and international law, but the meeting produced no breakthrough on the war in Ukraine.",
            "The talks lasted just over an hour. President Donald Trump embraced President Vladimir Putin and called him \u201cmy friend\u201d before the meeting, and left for the airport immediately afterwards.",
            "Trump later spoke with European leaders in the \u201ccoalition of the willing\u201d, who were meeting in Berlin with US envoys Steve Witkoff and Jared Kushner. According to an official present, he told them they were spending too much money on the war and should be spending it on their own countries.",
            "The leaders of the E3 — the UK, Germany and France — and Ukraine called on Russia to agree to a ceasefire on attacks on energy infrastructure for the duration of winter.",
            "Trump also told NBC News that he would meet North Korean leader Kim Jong-un at \u201csome point\u201d.",
        ],
        "related": ["russia-ukraine-missile-attack", "democrats-win-congress-midterms", "denmark-greenland-security-deal"],
    },
    {
        "slug": "gaza-ceasefire-collapse-warning",
        "sections": ["war-conflict", "world"],
        "section": "war-conflict",
        "headline": "Gaza ceasefire at risk of collapse, Board of Peace warns UN Security Council",
        "dek": "The body overseeing the US-brokered truce says the gap between what was agreed and what is happening on the ground is now the main threat to the deal.",
        "date": "18 November 2026",
        "source": "Al Jazeera",
        "source_url": "https://www.aljazeera.com/amp/news/2026/11/18/board-of-peace-warns-gaza-ceasefire-faces-imminent-collapse-without-action",
        "body": [
            "The Board of Peace, the body overseeing the US-brokered ceasefire in Gaza, has warned the UN Security Council that the year-old truce risks collapse if its terms are not fully implemented.",
            "In its first annual assessment, a copy of which was obtained by the Associated Press, the board said \u201cthe distance between what has been agreed and what is happening on the ground\u201d was the principal risk to the process, and that \u201ca ceasefire that delivers nothing visible cannot be sustained indefinitely.\u201d",
            "The ceasefire formally began on 10 October 2025, but attacks have continued. The Palestinian health ministry says more than 1,600 people have been killed in Israeli strikes since then.",
            "At the centre of the stall is the technocratic civil administration created to run Gaza on an interim basis. The board says Israel has still not allowed it to take up its job in the territory, delaying the international stabilisation force, an Israeli troop withdrawal, the disarmament of Hamas and reconstruction.",
            "Israel says reconstruction can begin only after Hamas disarms. Hamas has refused to give up its weapons while Israeli forces remain in Gaza.",
            "The board also noted that Israeli forces had begun a ground operation west of the Yellow Line in central Gaza. The military later said the operation was complete and reopened Salah al-Din Street.",
        ],
        "related": ["russia-ukraine-missile-attack", "trump-xi-putin-shenzhen-summit"],
    },
    {
        "slug": "eu-ukraine-loan-45-billion",
        "sections": ["europe", "politics", "business-finance"],
        "section": "europe",
        "headline": "EU proposes \u20ac45 billion loan to keep Ukraine funded in 2027",
        "dek": "The loan would cover around two-thirds of Kyiv's expected funding gap next year — and would be repaid, the Commission says, through future war reparations by Russia.",
        "date": "18 November 2026",
        "source": "Reuters",
        "source_url": "https://www.reuters.com/world/eu-proposes-new-45-billion-loan-ukraine-2027-be-repaid-by-russia-2026-11-18/",
        "body": [
            "The European Commission has proposed a new \u20ac45 billion (about $49 billion) loan to Ukraine for 2027, to be repaid through future war reparations by Russia.",
            "The loan would cover around two-thirds of Ukraine's expected \u20ac70 billion funding gap next year, with the rest to come from other international partners.",
            "Up to \u20ac25 billion would go to military assistance and up to \u20ac20 billion to general budget support, keeping hospitals, schools and other public services running.",
            "Disbursements would be tied to Kyiv continuing reforms, particularly on the rule of law, anti-corruption efforts and public finance management.",
            "The plan needs approval from EU governments and the European Parliament. The budget amendment underpinning it would need unanimous support from member states.",
            "Commission President Ursula von der Leyen said she was confident all 27 members would back the plan. EU leaders were due to discuss it at a Brussels summit.",
        ],
        "related": ["russia-ukraine-missile-attack", "bank-of-england-raises-rates", "uk-inflation-3-6-percent"],
    },
    {
        "slug": "denmark-greenland-security-deal",
        "sections": ["europe", "world"],
        "section": "europe",
        "headline": "Denmark approves US\u2013Greenland security deal, easing Arctic tensions",
        "dek": "All 109 lawmakers present voted in favour of the agreement, which lets the US build two bases in Greenland while keeping the island under Danish sovereignty.",
        "date": "19 November 2026",
        "source": "Al Jazeera",
        "source_url": "https://www.aljazeera.com/news/2026/11/19/denmark-parliament-approves-security-deal-with-greenland-and-us",
        "body": [
            "Denmark's parliament has unanimously approved a security agreement with the United States covering Greenland, easing months of tension over President Donald Trump's desire to annex the Arctic island.",
            "All 109 lawmakers present in the 179-seat Folketing voted in favour, with no votes against and no abstentions. Greenland's parliament approved the deal earlier in November by 16 votes to none, with seven abstentions.",
            "The agreement, signed in New York on 22 September, supplements a 1951 accord on the US military presence in Greenland. It allows the US to build two military bases in Greenland and blocks countries outside the EU and NATO from strategic sectors, to stop China or Russia gaining influence there.",
            "The deal is an executive agreement and does not need a vote in the US Senate. It enters into force once Denmark's foreign ministry formally notifies the US that procedures are complete.",
            "The agreement reaffirms the sovereignty of the Kingdom of Denmark and the right of Greenland's people to self-determination.",
        ],
        "related": ["trump-xi-putin-shenzhen-summit", "eu-ukraine-loan-45-billion"],
    },
    {
        "slug": "democrats-win-congress-midterms",
        "sections": ["us", "politics"],
        "section": "us",
        "headline": "Democrats seal 56\u201344 Senate majority as final midterm race is called",
        "dek": "Mary Peltola's win in Alaska completes a sweeping Democratic victory in the US midterms — control of both chambers of Congress, and a divided government for Trump's final two years.",
        "date": "19 November 2026",
        "source": "Nikkei Asia",
        "source_url": "https://asia.nikkei.com/politics/u.s.-midterm-elections/us-midterms-democrats-seal-56-44-senate-majority-with-alaska-win",
        "body": [
            "Democrats have completed a sweeping victory in the US midterm elections, winning control of both the House of Representatives and the Senate.",
            "Democrat Mary Peltola defeated two-term Republican Senator Dan Sullivan in Alaska, according to the Associated Press, completing the final unresolved Senate race and giving Democrats a 56\u201344 majority.",
            "Democrats flipped nine Republican-held Senate seats, with wins in traditionally conservative states including Texas, Kansas, Mississippi and South Carolina.",
            "In Texas, James Talarico defeated Ken Paxton — the first Democrat to win statewide office there in 32 years. In Kansas, Adam Hamilton beat Roger Marshall; Democrats last won a Senate seat there in 1932.",
            "Democrats also won the House, passing the 218 seats needed for a majority. All 435 House seats and 35 of the Senate's 100 seats were contested in the 3 November elections.",
            "Democrats have nominated Hakeem Jeffries to be the next House speaker, putting him on course to become the first Black lawmaker to hold the gavel when the new Congress convenes on 3 January.",
            "Voter discontent over inflation, tariffs, AI data centres and the war in Iran drove the result, according to Nikkei Asia's reporting.",
        ],
        "related": ["trump-xi-putin-shenzhen-summit", "uk-inflation-3-6-percent"],
    },
    {
        "slug": "bank-of-england-raises-rates",
        "sections": ["business-finance", "europe"],
        "section": "business-finance",
        "headline": "Bank of England raises rates to 4% \u2014 first increase since 2023",
        "dek": "The Bank acted as energy prices pushed by the Middle East conflict drive inflation higher, and warned it could reach around 5% by mid-2027.",
        "date": "5 November 2026",
        "source": "Reuters",
        "source_url": "https://www.reuters.com/world/uk/britains-long-wait-2-inflation-tests-public-faith-bank-england-2026-11-18/",
        "body": [
            "The Bank of England has raised interest rates to 4%, its first increase in more than three years, as energy prices push inflation higher.",
            "The Monetary Policy Committee voted 8\u20131 to raise Bank Rate by a quarter of a percentage point from 3.75%. Catherine Mann dissented, preferring a larger rise to 4.25%.",
            "The Bank said the Middle East conflict had driven energy prices sharply higher since July, with oil up 38% and UK gas up 81%, and warned inflation could reach around 5% by mid-2027 — far above its 2% target.",
            "Governor Andrew Bailey said the rise should not be seen as the start of an inevitable long sequence of increases, but warned more could follow if the conflict drags on.",
            "The next decision is due on 17 December. Markets had priced in a near-certain rise, and mortgage rates had already climbed since September.",
        ],
        "related": ["uk-inflation-3-6-percent", "eu-ukraine-loan-45-billion"],
    },
    {
        "slug": "uk-inflation-3-6-percent",
        "sections": ["business-finance", "europe"],
        "section": "business-finance",
        "headline": "UK inflation hits 12-month high of 3.6% as fuel costs climb",
        "dek": "Consumer prices rose for a fourth month in a row in October, driven by motor fuel and tobacco duty — complicating the Bank of England's fight against inflation.",
        "date": "18 November 2026",
        "source": "Reuters",
        "source_url": "https://www.reuters.com/world/uk/uk-inflation-one-year-high-weighs-ftse-100-2026-11-18/",
        "body": [
            "UK inflation rose to a 12-month high of 3.6% in October, up from 3.5% in September, official figures showed on Wednesday.",
            "The Office for National Statistics said it was the fourth consecutive monthly increase, driven by motor fuel and tobacco duty changes.",
            "Petrol and diesel prices pushed the annual rate higher, while tobacco prices rose 5.2% in the month and were 12.4% higher than a year earlier.",
            "Core inflation, which strips out volatile energy, food, alcohol and tobacco prices, was unchanged at 2.8%.",
            "The Bank of England expects inflation to approach 5% in the second quarter of 2027. The reading was slightly below the Bank's 3.7% forecast, prompting investors to trim bets on a December rate rise.",
        ],
        "related": ["bank-of-england-raises-rates", "eu-ukraine-loan-45-billion"],
    },
    {
        "slug": "japan-beats-brazil-3-2",
        "sections": ["sport"],
        "section": "sport",
        "headline": "Japan stun Brazil 3\u20132 in Moriyasu's farewell friendly",
        "dek": "A stoppage-time winner from Tatsuhito Sakamoto sealed victory in Singapore — a final win for the coach who has led Japan for eight years.",
        "date": "16 November 2026",
        "source": "Chosun Biz",
        "source_url": "https://biz.chosun.com/en/en-sports/2026/11/16/7LRBK2NGSZCKXP3JUZJ5AUA74Q/",
        "body": [
            "Japan beat Brazil 3\u20132 in a November international friendly in Singapore, in coach Hajime Moriyasu's final match in charge after eight years.",
            "Takefusa Kubo opened the scoring in the 15th minute and Keito Nakamura doubled the lead four minutes later. Brazil's Vin\u00edcius J\u00fanior scored twice to level the match, but Tatsuhito Sakamoto struck the winner in the first minute of second-half stoppage time.",
            "Japan, ranked 17th in the world, converted three of their eight shots, with Kubo, Nakamura and Sakamoto each scoring with their only shot on goal.",
            "The win avenged Japan's 2\u20131 defeat by Brazil in the round of 32 at the 2026 World Cup last summer.",
            "Moriyasu, who has led Japan since 2018, will step down after the November international window. Japan face Paraguay next as they build towards the next World Cup.",
        ],
        "related": ["van-gogh-record-190-million"],
    },
    {
        "slug": "van-gogh-record-190-million",
        "sections": ["culture"],
        "section": "culture",
        "headline": "Van Gogh sells for record $190.4 million at Sotheby's",
        "dek": "\u201cCh\u00e2taigniers en fleurs\u201d, unseen in public for more than 50 years, became the fourth most expensive painting ever sold at auction — a day after a dispute over its Nazi-era sale was settled.",
        "date": "19 November 2026",
        "source": "Reuters",
        "source_url": "https://www.reuters.com/lifestyle/van-goghs-chataigniers-en-fleurs-sells-auction-record-1904-million-2026-11-19/",
        "body": [
            "Vincent van Gogh's 1890 painting \u201cCh\u00e2taigniers en fleurs\u201d (Blossoming Chestnut Trees) has sold for $190.4 million at Sotheby's in New York, an auction record for the artist.",
            "The hammer price was $165 million, with fees taking the total to $190.4 million. The buyer was veteran art dealer Bill Acquavella, head of Acquavella Galleries.",
            "The previous Van Gogh record was $117.2 million, paid in 2022 for \u201cOrchard with Cypresses\u201d from the collection of Microsoft co-founder Paul Allen.",
            "The sale makes it the fourth most expensive painting ever sold at auction, and the second most valuable work ever sold at Sotheby's, behind a Klimt portrait that fetched $236.4 million in November 2025.",
            "The painting, which had not been seen in public for more than 50 years, was the top lot in the sale of 12 works from the Blaquier-Arrieta Collection. All 12 sold for a combined $412 million.",
            "The sale went ahead a day after Sotheby's announced an agreement with the heirs of German Jewish publisher Samuel Fischer, who said the painting had been sold under duress in 1936 during Nazi persecution.",
        ],
        "related": ["japan-beats-brazil-3-2"],
    },
]

# Timestamped "Just In" items — all verified from search results, 18-20 Nov 2026.
JUST_IN = [
    ("20 Nov, 10:33", "Russian barrage damages embassies and a cathedral in Kyiv", None),
    ("20 Nov, 09:15", "Netherlands summons Russian ambassador after Kyiv strike damages its embassy", None),
    ("20 Nov, 08:40", "Six dead in Georgia as gas blast collapses part of a residential block", None),
    ("19 Nov, 19:05", "France rejects Russian claim it is directly involved in the Ukraine war", None),
    ("19 Nov, 17:20", "Trump says he will meet North Korea's Kim Jong-un at \u201csome point\u201d", None),
    ("19 Nov, 15:10", "NATO launches multinational STARLIFT space initiative for military launches", None),
    ("19 Nov, 13:45", "EU Commission confirms AI-generated cyber campaign; no staff-wide breach found", None),
    ("18 Nov, 21:30", "UN court to decide on Thursday if Myanmar's expulsion of Rohingya was genocide", None),
]

# Live-blog updates for live.html — verified facts only, 18-20 Nov 2026.
LIVE_UPDATES = [
    ("20 Nov, 10:33", "Embassies damaged in Kyiv barrage",
     "A daytime Russian barrage blew out windows at the Austrian and Dutch missions in Kyiv and damaged a cathedral, prompting Brussels to summon Moscow's envoy."),
    ("20 Nov, 09:15", "Netherlands summons Russian ambassador",
     "The Dutch government summoned Russia's ambassador after its embassy in Kyiv suffered minor damage when a projectile landed near the building. No one was hurt."),
    ("20 Nov, 08:00", "Poland scrambles jets as airspace is violated",
     "Poland said fighter jets were scrambled and Patriot air defence systems activated early on Friday after objects flew into and fell inside Polish territory during the overnight attack."),
    ("20 Nov, 06:30", "More than 110 missiles fired at Ukraine overnight",
     "Ukraine said Russia fired at least 110 missiles overnight — an unusually large number even amid frequent aerial assaults. At least eight people were killed and 28 injured, and three of Kyiv's bridges were damaged."),
    ("19 Nov, 22:10", "Trump tells European leaders Putin is \u201ctired\u201d and ready for a deal",
     "After the Shenzhen talks, President Trump spoke with the \u201ccoalition of the willing\u201d in Berlin. According to a senior European official, his main message was that \u201cPutin is tired, wants to end this, ready for a deal.\u201d"),
    ("19 Nov, 18:40", "E3 leaders call for winter energy ceasefire",
     "The leaders of the UK, Germany and France and Ukraine called on Russia to agree to a ceasefire on attacks on energy infrastructure for the duration of winter."),
    ("19 Nov, 17:00", "Trilateral talks end without breakthrough",
     "Trump, Xi and Putin met in Shenzhen for just over an hour. A joint declaration covered UN reform, nuclear weapons and oil production, but produced no breakthrough on Ukraine and no official declaration was released."),
    ("18 Nov, 20:15", "EU proposes \u20ac45 billion loan for Ukraine in 2027",
     "The European Commission proposed a new \u20ac45 billion loan to Ukraine for 2027, to be repaid through future war reparations by Russia. Up to \u20ac25 billion would go to military aid and \u20ac20 billion to budget support."),
]

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
    "russia-ukraine-missile-attack": ("1477959858617-67f85cf4f1df", "A city skyline at night. Illustrative photo. Photo: Unsplash"),
    "trump-xi-putin-shenzhen-summit": ("1444723121867-7a241cacace9", "A modern city skyline at dusk. Illustrative photo. Photo: Unsplash"),
    "gaza-ceasefire-collapse-warning": ("1547234935-80c7145ec969", "Desert landscape in the Middle East. Illustrative photo. Photo: Unsplash"),
    "eu-ukraine-loan-45-billion": ("1467269204594-9661b134dd2b", "A street in a European old town. Illustrative photo. Photo: Unsplash"),
    "denmark-greenland-security-deal": ("1519681393784-d120267933ba", "Snow-covered mountains under a night sky. Illustrative photo. Photo: Unsplash"),
    "democrats-win-congress-midterms": ("1529107386315-e1a2ed48a620", "A parliament chamber in session. Illustrative photo. Photo: Unsplash"),
    "bank-of-england-raises-rates": ("1513635269975-59663e0ac1ad", "Westminster, London. Illustrative photo. Photo: Unsplash"),
    "uk-inflation-3-6-percent": ("1488459716781-31db52582fe9", "A food market. Illustrative photo. Photo: Unsplash"),
    "japan-beats-brazil-3-2": ("1522778119026-d647f0596c20", "A football stadium under lights. Illustrative photo. Photo: Unsplash"),
    "van-gogh-record-190-million": ("1541961017774-22349e4a1262", "An abstract painting. Illustrative photo. Photo: Unsplash"),
}

MOST_READ = [
    "russia-ukraine-missile-attack",
    "trump-xi-putin-shenzhen-summit",
    "gaza-ceasefire-collapse-warning",
    "eu-ukraine-loan-45-billion",
    "democrats-win-congress-midterms",
]

# "Watch" strip — video-style cards. NOTE: no real video exists yet; cards
# link to the live blog / full articles. See README.md.
WATCH = [
    {"title": "The night Kyiv was hit — the story so far", "dur": "01:32",
     "img": "1504711434969-e33886168f5c", "link": "live.html"},
    {"title": "Europe's winter energy test, explained", "dur": "02:14",
     "img": "1473341304170-971dccb5ac1e", "link": "articles/eu-ukraine-loan-45-billion.html"},
    {"title": "Markets: rates, inflation and what comes next", "dur": "01:47",
     "img": "1611974789855-9c2a0a7236a3", "link": "articles/bank-of-england-raises-rates.html"},
]

ANALYSIS = [
    {"title": "What the Shenzhen talks really changed — and what they didn't",
     "blurb": "An hour of handshakes, a declaration on the UN and oil — and a war that carried on through the night. The summit mattered, but not in the way its billing suggested.",
     "link": "articles/trump-xi-putin-shenzhen-summit.html"},
    {"title": "Europe's €45bn question: who pays for Ukraine next?",
     "blurb": "The Commission's loan covers two-thirds of Kyiv's gap — and bets the bill on Russian reparations that do not exist yet. The politics of that gamble start in Brussels.",
     "link": "articles/eu-ukraine-loan-45-billion.html"},
    {"title": "The midterms are over. The hard part starts now",
     "blurb": "A 56–44 Senate and a Democratic House mean two years of divided government. The first test is not a vote — it is whether anything can pass at all.",
     "link": "articles/democrats-win-congress-midterms.html"},
]

CSS = """/* Western World News — publisher design v2.
   BBC/CNN-level look: dark navy masthead, red breaking bar with ticker,
   serif display headlines, photo-led cards, Most Read sidebar, Watch strip.
   Mobile-first; no webfonts (system serif/sans stacks only). */

:root {
  --red: #bb1919;
  --red-bright: #e02424;
  --red-dark: #8f1212;
  --ink: #1a1a1a;
  --muted: #5f5f5f;
  --line: #e3e3e3;
  --light: #f6f6f6;
  --navy: #0e2244;
  --navy-dark: #081426;
  --navy-mid: #16294d;
  --gold: #c8a96a;
  --serif: Georgia, "Times New Roman", serif;
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

a { color: var(--ink); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; display: block; }
figure { margin: 0; }
figcaption { font-size: 0.8rem; color: var(--muted); padding: 0.4rem 0.1rem 0; line-height: 1.4; }

.wrap { max-width: 1180px; margin: 0 auto; padding: 0 1rem; }
.sr-only { position: absolute; left: -9999px; }

/* ---------- Top utility bar ---------- */
.topbar { background: var(--navy-dark); color: #cdd6e4; font-size: 0.82rem; }
.topbar .wrap { display: flex; align-items: center; gap: 1rem; padding-top: 0.35rem; padding-bottom: 0.35rem; flex-wrap: wrap; }
.topbar .dateline { color: #cdd6e4; }
.topbar a { color: #fff; font-weight: 600; }
.topbar a:hover { text-decoration: underline; }
.topbar .live-dot { width: 0.5rem; height: 0.5rem; }
.topbar .spacer { flex: 1; }
.search-box { position: relative; }
.search-box input {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  color: #fff;
  border-radius: 3px;
  padding: 0.32rem 0.6rem;
  font-size: 0.85rem;
  width: 210px;
  outline: none;
}
.search-box input::placeholder { color: #9fb0c8; }
.search-box input:focus { border-color: #fff; background: rgba(255,255,255,0.18); }
.search-results {
  display: none;
  position: absolute;
  right: 0;
  top: 110%;
  width: 320px;
  max-width: 90vw;
  background: #fff;
  color: var(--ink);
  border: 1px solid var(--line);
  border-radius: 4px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.25);
  z-index: 200;
  overflow: hidden;
}
.search-results.open { display: block; }
.search-results a {
  display: block;
  padding: 0.6rem 0.8rem;
  border-bottom: 1px solid var(--line);
  font-size: 0.92rem;
  color: var(--ink);
}
.search-results a:last-child { border-bottom: 0; }
.search-results a:hover { background: var(--light); text-decoration: none; }
.search-results a small { display: block; color: var(--red); font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
.search-results .none { padding: 0.7rem 0.8rem; color: var(--muted); font-size: 0.9rem; }

/* ---------- Breaking bar + ticker ---------- */
.breaking-bar { background: var(--red); color: #fff; font-size: 0.95rem; overflow: hidden; }
.breaking-bar .wrap { display: flex; align-items: center; gap: 0.7rem; padding-top: 0.45rem; padding-bottom: 0.45rem; }
.breaking-label {
  background: #fff; color: var(--red); font-weight: 800;
  letter-spacing: 0.08em; font-size: 0.75rem;
  padding: 0.15rem 0.5rem; border-radius: 2px; white-space: nowrap; flex-shrink: 0;
}
.breaking-main { color: #fff; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; max-width: 46%; }
.breaking-main:hover { text-decoration: underline; }
.ticker { overflow: hidden; flex: 1; min-width: 0; border-left: 1px solid rgba(255,255,255,0.4); padding-left: 0.7rem;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 4%, #000 96%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 4%, #000 96%, transparent); }
.ticker-track { display: inline-flex; gap: 2.2rem; white-space: nowrap; animation: ticker-scroll 55s linear infinite; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-track a { color: rgba(255,255,255,0.92); font-size: 0.88rem; }
.ticker-track a:hover { color: #fff; }
.ticker-track a::before { content: "\\25CF  "; color: #ffd2d2; font-size: 0.6rem; }
@keyframes ticker-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (max-width: 860px) { .breaking-main { display: none; } }

/* ---------- Masthead (dark navy) ---------- */
.masthead { background: var(--navy); color: #fff; padding: 1.15rem 0 1.05rem; }
.masthead .wrap { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 0.3rem 1rem; }
.wordmark { font-family: var(--serif); font-size: 2.1rem; font-weight: 800; letter-spacing: -0.01em; line-height: 1.05; color: #fff; }
.wordmark .news { color: #ff5a5a; }
.wordmark:hover { text-decoration: none; }
.tagline { color: #b9c6da; font-size: 0.9rem; font-style: italic; font-family: var(--serif); }
.masthead .dateline { color: #b9c6da; font-size: 0.85rem; }
@media (min-width: 860px) { .wordmark { font-size: 2.6rem; } }

/* ---------- Nav + hamburger ---------- */
nav.main-nav { background: var(--navy-mid); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.25); }
nav.main-nav .wrap { display: flex; align-items: center; }
.nav-toggle {
  display: none; background: none; border: 0; color: #fff; font-size: 1.5rem;
  padding: 0.5rem 0.6rem 0.5rem 0; cursor: pointer; line-height: 1;
}
nav.main-nav ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; }
nav.main-nav a { display: block; color: #fff; padding: 0.68rem 0.8rem; font-size: 0.92rem; font-weight: 600; }
nav.main-nav a:hover { background: rgba(255,255,255,0.12); text-decoration: none; }
nav.main-nav a.active { background: var(--red); }
nav.main-nav a.live-link { color: #ff6b6b; }
nav.main-nav a.live-link.active { color: #fff; }
@media (max-width: 860px) {
  .nav-toggle { display: block; }
  nav.main-nav ul { display: none; flex-direction: column; width: 100%; padding-bottom: 0.4rem; }
  nav.main-nav.open ul { display: flex; }
  nav.main-nav a { padding: 0.6rem 0.2rem; border-top: 1px solid rgba(255,255,255,0.12); }
}

/* ---------- Layout ---------- */
main { padding: 1.3rem 0 2rem; }
.section-head {
  font-family: var(--serif); font-size: 1.55rem; line-height: 1.2;
  border-bottom: 3px solid var(--ink); padding-bottom: 0.35rem; margin: 0 0 1rem;
}
.section-head .tag { color: var(--red); }
.section-head a { color: var(--ink); }
.section-head a:hover { color: var(--red); }
.rule-red { border: 0; border-top: 3px solid var(--red); margin: 0 0 1rem; width: 64px; }

/* ---------- Hero ---------- */
.hero-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; margin-bottom: 2.2rem; }
@media (min-width: 900px) { .hero-grid { grid-template-columns: 2fr 1fr; } }
.hero figure { margin-bottom: 0.7rem; }
.hero figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 3px; }
.hero h1, .hero h2 { font-family: var(--serif); line-height: 1.12; margin: 0.55rem 0; }
.hero h1 { font-size: 2rem; }
.hero h1 a:hover { color: var(--red); }
@media (min-width: 900px) { .hero h1 { font-size: 2.55rem; } }
.hero p.dek { font-size: 1.1rem; color: #333; margin: 0.4rem 0 0.8rem; line-height: 1.5; }
.kicker { color: var(--red); font-weight: 800; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; }
.byline { color: var(--muted); font-size: 0.85rem; margin: 0.5rem 0 0; }
.byline time { font-weight: 600; color: var(--ink); }
.byline a { color: var(--red); font-weight: 700; }

/* ---------- Just In ---------- */
.just-in { border: 1px solid var(--line); background: var(--light); align-self: start; }
.just-in h2 {
  margin: 0; padding: 0.6rem 0.9rem; background: var(--ink); color: #fff;
  font-size: 0.95rem; letter-spacing: 0.1em; text-transform: uppercase;
}
.just-in ul { list-style: none; margin: 0; padding: 0.4rem 0.9rem 0.9rem; }
.just-in li { padding: 0.55rem 0; border-bottom: 1px solid var(--line); font-size: 0.95rem; line-height: 1.45; }
.just-in li:last-child { border-bottom: 0; }
.just-in time { color: var(--red); font-weight: 700; font-size: 0.82rem; margin-right: 0.4rem; }

/* ---------- Most Read ---------- */
.most-read { border-top: 3px solid var(--ink); margin: 0 0 2rem; }
.most-read h2 { font-family: var(--serif); font-size: 1.35rem; margin: 0.7rem 0 0.4rem; }
.most-read ol { list-style: none; margin: 0; padding: 0; counter-reset: mr; }
.most-read li {
  counter-increment: mr; display: flex; gap: 0.85rem; align-items: flex-start;
  padding: 0.7rem 0; border-bottom: 1px solid var(--line);
}
.most-read li:last-child { border-bottom: 0; }
.most-read li::before {
  content: counter(mr); font-family: var(--serif); font-weight: 800;
  font-size: 2rem; line-height: 1; color: var(--red); min-width: 1.6rem;
}
.most-read a { font-family: var(--serif); font-size: 1.05rem; line-height: 1.3; font-weight: 700; }
.most-read a:hover { color: var(--red); }
.most-read small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; font-family: var(--sans); font-weight: 400; }

/* ---------- Cards & grids ---------- */
.card-grid { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 640px) { .card-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 980px) { .card-grid.four { grid-template-columns: repeat(4, 1fr); } }
@media (min-width: 980px) { .card-grid.three { grid-template-columns: repeat(3, 1fr); } }
.card { border-top: 3px solid var(--ink); padding-top: 0; }
.card figure img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 2px; }
.card figure { margin-bottom: 0.55rem; }
.card h3 { font-family: var(--serif); font-size: 1.25rem; line-height: 1.25; margin: 0.4rem 0 0.35rem; }
.card h3 a:hover { color: var(--red); }
.card p { margin: 0; color: #333; font-size: 0.95rem; }
.card .art { margin-bottom: 0.6rem; }
.story-list { list-style: none; margin: 0; padding: 0; }
.story-list li { padding: 1rem 0; border-bottom: 1px solid var(--line); }
.story-list li:first-child { padding-top: 0; }
.story-list h3 { font-family: var(--serif); font-size: 1.3rem; margin: 0.3rem 0 0.3rem; line-height: 1.25; }
.story-list h3 a:hover { color: var(--red); }
.story-list p { margin: 0; color: #333; }
.story-list .thumb { float: left; width: 170px; margin: 0.25rem 1rem 0.5rem 0; }
.story-list .thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 2px; }
.story-list li::after { content: ""; display: table; clear: both; }
@media (max-width: 640px) { .story-list .thumb { float: none; width: 100%; margin: 0 0 0.5rem; } }

/* ---------- Graphic placeholder (stories without a photo) ---------- */
.art {
  aspect-ratio: 16 / 9;
  background: linear-gradient(135deg, var(--navy) 0%, #274b7a 60%, #3d6aa8 100%);
  color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.35rem; text-align: center; padding: 1rem;
}
.art .monogram { font-family: var(--serif); font-size: 2.2rem; font-weight: 800; letter-spacing: 0.06em; border: 2px solid rgba(255,255,255,0.85); padding: 0.2rem 0.9rem; }
.art .art-label { font-size: 0.8rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.85; }
.art.small .monogram { font-size: 1.4rem; }

/* ---------- Watch strip ---------- */
.watch-strip { background: var(--navy-dark); color: #fff; margin: 2.2rem 0; padding: 1.4rem 0 1.6rem; }
.watch-strip h2 { font-family: var(--serif); color: #fff; border-bottom: 3px solid var(--red); padding-bottom: 0.4rem; margin: 0 0 1rem; font-size: 1.5rem; }
.watch-strip h2 .tag { color: #ff5a5a; }
.watch-grid { display: grid; grid-template-columns: 1fr; gap: 1.2rem; }
@media (min-width: 700px) { .watch-grid { grid-template-columns: repeat(3, 1fr); } }
.watch-card a { color: #fff; display: block; }
.watch-card a:hover { text-decoration: none; }
.watch-card a:hover h3 { text-decoration: underline; }
.watch-thumb { position: relative; }
.watch-thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 3px; }
.watch-thumb .play {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
  width: 46px; height: 46px; border-radius: 50%; background: rgba(187,25,25,0.92);
  color: #fff; font-size: 1.05rem; display: flex; align-items: center; justify-content: center; padding-left: 3px;
}
.watch-thumb .dur {
  position: absolute; right: 0.5rem; bottom: 0.5rem; background: rgba(0,0,0,0.8);
  color: #fff; font-size: 0.75rem; font-weight: 700; padding: 0.1rem 0.4rem; border-radius: 2px;
}
.watch-card h3 { font-family: var(--serif); font-size: 1.1rem; line-height: 1.3; margin: 0.55rem 0 0; color: #fff; }

/* ---------- Analysis / Opinion ---------- */
.analysis { margin: 0 0 2.2rem; }
.analysis .cols { display: grid; grid-template-columns: 1fr; gap: 1.2rem; }
@media (min-width: 700px) { .analysis .cols { grid-template-columns: repeat(3, 1fr); } }
.analysis article { background: var(--light); border-top: 3px solid var(--gold); padding: 1rem 1.1rem; }
.analysis .kicker { color: #8a6d2b; }
.analysis h3 { font-family: var(--serif); font-size: 1.18rem; line-height: 1.3; margin: 0.4rem 0 0.4rem; }
.analysis h3 a:hover { color: var(--red); }
.analysis p { margin: 0; font-size: 0.94rem; color: #333; }

/* ---------- Live blog ---------- */
.live-dot { display: inline-block; width: 0.6rem; height: 0.6rem; background: var(--red); border-radius: 50%; margin-right: 0.4rem; animation: pulse 1.6s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }
.live-update { border-left: 3px solid var(--red); padding: 0.2rem 0 0.2rem 1rem; margin: 0 0 1.4rem; }
.live-update time { font-weight: 700; color: var(--red); font-size: 0.9rem; }
.live-update h3 { font-family: var(--serif); margin: 0.2rem 0 0.3rem; font-size: 1.15rem; }
.live-update p { margin: 0; }

/* ---------- Newsletter ---------- */
.newsletter { background: var(--navy); color: #fff; padding: 1.5rem; margin: 2rem 0; border-radius: 4px; }
.newsletter h2 { font-family: var(--serif); margin: 0 0 0.3rem; font-size: 1.4rem; }
.newsletter p { margin: 0 0 0.9rem; opacity: 0.9; }
.newsletter form { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.newsletter input[type="email"] { flex: 1 1 220px; padding: 0.65rem 0.8rem; border: 0; border-radius: 3px; font-size: 1rem; }
.newsletter button, .btn { background: var(--red); color: #fff; border: 0; padding: 0.65rem 1.2rem; font-size: 1rem; font-weight: 700; border-radius: 3px; cursor: pointer; display: inline-block; }
.newsletter button:hover, .btn:hover { background: var(--red-dark); text-decoration: none; }
.newsletter .note { font-size: 0.8rem; opacity: 0.75; margin: 0.6rem 0 0; }
.newsletter .success { display: none; font-weight: 700; margin-top: 0.6rem; }

/* ---------- Article page ---------- */
.article-layout { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 960px) { .article-layout { grid-template-columns: 1fr 300px; } .article-layout .most-read { margin-top: 0.4rem; } }
.article-head h1 { font-family: var(--serif); font-size: 2rem; line-height: 1.15; margin: 0.5rem 0; }
@media (min-width: 860px) { .article-head h1 { font-size: 2.45rem; } }
.article-head .dek { font-size: 1.15rem; color: #333; line-height: 1.5; }
.article-hero { margin: 1rem 0 1.4rem; }
.article-hero img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 3px; }
.article-body p { font-size: 1.06rem; line-height: 1.7; margin: 0 0 1.1rem; }
.article-body p:first-of-type::first-letter { font-family: var(--serif); font-size: 2.6rem; line-height: 1; font-weight: 700; float: left; margin: 0.1rem 0.4rem 0 0; }
.source-box { border: 1px solid var(--line); border-left: 4px solid var(--red); background: var(--light); padding: 0.8rem 1rem; margin: 1.6rem 0; font-size: 0.95rem; }
.source-box strong { display: block; margin-bottom: 0.2rem; }
.source-box a { color: var(--red); font-weight: 700; }
.related { margin-top: 2rem; border-top: 2px solid var(--ink); padding-top: 0.8rem; }
.related h2 { font-family: var(--serif); font-size: 1.3rem; margin: 0 0 0.6rem; }

/* ---------- Footer ---------- */
footer.site-footer { background: var(--navy); color: #d7dbe3; margin-top: 2.5rem; }
footer.site-footer .wrap { padding-top: 1.8rem; padding-bottom: 1.4rem; }
footer.site-footer a { color: #fff; }
footer.site-footer .cols { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 700px) { footer.site-footer .cols { grid-template-columns: 2fr 1fr 1fr 1.4fr; } }
footer.site-footer h3 { color: #fff; font-family: var(--serif); margin: 0 0 0.5rem; font-size: 1.1rem; }
footer.site-footer h3 .news { color: #ff5a5a; }
footer.site-footer ul { list-style: none; margin: 0; padding: 0; }
footer.site-footer li { margin: 0.32rem 0; font-size: 0.94rem; }
footer.site-footer p { font-size: 0.94rem; }
footer.site-footer .mini-form { display: flex; gap: 0.4rem; margin-top: 0.6rem; }
footer.site-footer .mini-form input[type="email"] { flex: 1; min-width: 0; padding: 0.5rem 0.6rem; border: 0; border-radius: 3px; font-size: 0.9rem; }
footer.site-footer .mini-form button { background: var(--red); color: #fff; border: 0; padding: 0.5rem 0.8rem; border-radius: 3px; font-weight: 700; cursor: pointer; }
footer.site-footer .fineprint { border-top: 1px solid rgba(255,255,255,0.2); margin-top: 1.5rem; padding-top: 0.9rem; font-size: 0.82rem; opacity: 0.8; display: flex; flex-wrap: wrap; gap: 0.4rem 1.2rem; justify-content: space-between; }

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


def ticker_items(prefix=""):
    return "".join(f'<a href="{prefix}live.html">{hescape(h)}</a>' for _, h, _ in JUST_IN)


def header_html(active, prefix=""):
    ticker = ticker_items(prefix)
    # ticker content duplicated for a seamless CSS marquee loop
    return f"""<a class="skip-link" href="#main">Skip to main content</a>
<div class="topbar"><div class="wrap">
<span class="dateline" data-today>Friday, 20 November 2026</span>
<a href="{prefix}live.html"><span class="live-dot"></span>Live</a>
<span class="spacer"></span>
<div class="search-box">
<input type="search" id="site-search" placeholder="Search news..." aria-label="Search news" autocomplete="off">
<div class="search-results" id="search-results" role="listbox" aria-label="Search results"></div>
</div>
</div></div>
<div class="breaking-bar"><div class="wrap"><span class="breaking-label">BREAKING</span><a class="breaking-main" id="breaking-link" href="{prefix}articles/russia-ukraine-missile-attack.html">Russia launches one of the largest missile attacks of the war on Ukraine — 110+ missiles fired overnight</a><div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}{ticker}</div></div></div></div>
<header class="masthead"><div class="wrap">
<div>
<a class="wordmark" href="{prefix}index.html" data-site-name>Western World <span class="news">News</span></a>
<div class="tagline" data-tagline>Western and European news, live — politics, war, business and culture.</div>
</div>
<span class="dateline" data-today>Friday, 20 November 2026</span>
</div></header>
<nav class="main-nav" id="main-nav" aria-label="Main navigation"><div class="wrap"><button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false">&#9776;</button>{nav_html(active, prefix)}</div></nav>"""


def footer_html(prefix=""):
    return f"""<footer class="site-footer"><div class="wrap">
<div class="cols">
<div>
<h3 data-site-name>Western World <span class="news">News</span></h3>
<p data-tagline>Independent news from the West and the world — politics, war, business and culture, reported fast and in our own words. Free to read.</p>
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
<p>Our free morning newsletter — the day's Western and European news in your inbox before 8am.</p>
<form class="mini-form newsletter-form" action="#" method="post">
<label for="ft-email" class="sr-only">Email address</label>
<input id="ft-email" type="email" name="email" placeholder="Your email" required>
<button type="submit">Sign up</button>
</form>
<p class="success" style="display:none">Thank you — you are on the list.</p>
</div>
</div>
<p class="fineprint"><span>&copy; 2026 Western World News (westernworldnews.com). All stories are original summaries written by our editors; original reporting is credited and linked. Seed content published 20 November 2026 — see README.md.</span><span>Photos: Unsplash (illustrative).</span></p>
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
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23bb1919'/%3E%3Ctext x='16' y='22' font-family='Georgia' font-size='16' font-weight='bold' fill='white' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E">
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


def img_html(slug, w=800, cls=""):
    """Photo figure for a story, or the gradient tile if no photo is set."""
    if slug in IMAGES:
        pid, cap = IMAGES[slug]
        alt = cap.split(". Illustrative")[0]
        return (f'<figure class="{cls}"><img src="{uimg(pid, w)}" alt="{hescape(alt)}" loading="lazy">'
                f'<figcaption>{hescape(cap)}</figcaption></figure>')
    if slug in BY_SLUG and BY_SLUG[slug].get("image"):
        cap = BY_SLUG[slug].get("imageCaption") or "Photo: Unsplash"
        alt = cap.split(". Illustrative")[0]
        return (f'<figure class="{cls}"><img src="{hescape(BY_SLUG[slug]["image"])}" alt="{hescape(alt)}" loading="lazy">'
                f'<figcaption>{hescape(cap)}</figcaption></figure>')
    sec = SECTIONS[BY_SLUG[slug]["section"]] if slug in BY_SLUG else "News"
    return art_html(sec, small=(w <= 800))


def card_html(s, prefix=""):
    sec = SECTIONS[s["section"]]
    return f"""<article class="card">
{img_html(s['slug'], w=800)}
<p><span class="kicker">{sec}</span></p>
<h3><a href="{prefix}articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; Source: {s['source']}</p>
</article>"""


def most_read_html(prefix=""):
    items = "".join(
        f'<li><div><a href="{prefix}articles/{s["slug"]}.html">{s["headline"]}</a>'
        f'<small>{SECTIONS[s["section"]]} &middot; {s["date"]}</small></div></li>'
        for s in (BY_SLUG[slug] for slug in MOST_READ if slug in BY_SLUG)
    )
    return f"""<aside class="most-read" aria-label="Most read">
<h2>Most Read</h2>
<ol id="most-read-list">{items}</ol>
</aside>"""


def newsletter_html():
    return """<section class="newsletter" aria-label="Newsletter signup">
<h2>The Western Briefing — free, every morning</h2>
<p>Western and European news, war updates and the day's business headlines, in your inbox before 8am.</p>
<form class="newsletter-form" action="#" method="post">
<label for="nl-email" class="sr-only" style="position:absolute;left:-9999px">Email address</label>
<input id="nl-email" type="email" name="email" placeholder="Your email address" required>
<button type="submit">Sign up free</button>
</form>
<p class="success">Thank you — you are on the list. Your first briefing arrives tomorrow morning.</p>
<p class="note">No spam, no paywall. Unsubscribe any time. (Demo form — connect a mailing service before launch; see README.md.)</p>
</section>"""


def stories_for(section):
    return [s for s in STORIES if section in s["sections"]]


def watch_html():
    cards = "".join(
        f"""<div class="watch-card"><a href="{w['link']}">
<div class="watch-thumb"><img src="{uimg(w['img'], 800)}" alt="{hescape(w['title'])}" loading="lazy"><span class="play">&#9654;</span><span class="dur">{w['dur']}</span></div>
<h3>{hescape(w['title'])}</h3></a></div>""" for w in WATCH
    )
    return f"""<section class="watch-strip" aria-label="Watch"><div class="wrap">
<h2><span class="tag">&#9632;</span> Watch</h2>
<div class="watch-grid">{cards}</div>
</div></section>"""


def analysis_html():
    items = "".join(
        f"""<article><p><span class="kicker">Analysis</span></p>
<h3><a href="{a['link']}">{hescape(a['title'])}</a></h3>
<p>{hescape(a['blurb'])}</p></article>""" for a in ANALYSIS
    )
    return f"""<section class="analysis" aria-label="Analysis">
<h2 class="section-head"><span class="tag">&#9632;</span> Analysis</h2>
<div class="cols">{items}</div>
</section>"""


# ---------------- Homepage ----------------

def build_index():
    hero = BY_SLUG["russia-ukraine-missile-attack"]
    just_in = "".join(
        f'<li><time>{t}</time><a href="live.html">{h}</a></li>' for t, h, _ in JUST_IN
    )
    europe = stories_for("europe")
    world = stories_for("world")
    us_pol = stories_for("us") + [s for s in stories_for("politics") if s["slug"] not in [x["slug"] for x in stories_for("us")]]
    biz = stories_for("business-finance")

    def block(title, stories, grid_cls="four", slug=""):
        cards = "".join(card_html(s) for s in stories)
        return f'<h2 class="section-head"><span class="tag">&#9632;</span> {title}</h2><div class="card-grid {grid_cls}" data-section-block data-section="{slug}">{cards}</div>'

    body = f"""
<div class="hero-grid">
<article class="hero" data-hero>
{img_html(hero['slug'], w=1600)}
<p><span class="kicker">War &amp; Conflict &middot; Live</span></p>
<h1><a href="articles/{hero['slug']}.html">{hero['headline']}</a></h1>
<p class="dek">{hero['dek']}</p>
<p class="byline"><time>{hero['date']}</time> &middot; Source: {hero['source']} &middot; <a href="live.html">Follow live updates &rarr;</a></p>
</article>
<div>
<aside class="just-in" aria-label="Just in">
<h2>Just In</h2>
<ul id="just-in-list">{just_in}</ul>
</aside>
{most_read_html()}
</div>
</div>

{block("Europe", europe, slug="europe")}
<div style="height:2rem"></div>
{block("World", world, slug="world")}
<div style="height:2rem"></div>
"""
    # Watch strip sits full-width: close the .wrap div, insert the strip
    # (it carries its own .wrap), then reopen .wrap — all inside one <main>.
    body += "</div>\n" + watch_html() + "\n<div class=\"wrap\">\n"
    body += f"""
{block("US &amp; Politics", us_pol, slug="us,politics")}
<div style="height:2rem"></div>

<section aria-label="Live blog">
<h2 class="section-head"><span class="tag">&#9632;</span> Live: Ukraine war</h2>
<div class="live-update">
<time>20 Nov, 10:33</time>
<h3><a href="live.html">Embassies damaged in Kyiv barrage</a></h3>
<p>A daytime Russian barrage blew out windows at the Austrian and Dutch missions in Kyiv and damaged a cathedral, prompting Brussels to summon Moscow's envoy. <a href="live.html">Follow the live blog &rarr;</a></p>
</div>
</section>

{newsletter_html()}

{analysis_html()}

{block("Business &amp; Finance", biz, slug="business-finance")}
"""
    html = page(
        "Western World News — Western and European news, live",
        "Western World News: breaking news from Western Europe and the world — politics, war, business and culture, free to read.",
        "index.html", body, BASE + "/",
    )
    # page() wraps body in <main><div class="wrap">…</div></main>; the
    # watch-strip break above closes/reopens only the .wrap div, so the
    # final document keeps a single <main> element.
    return html


# ---------------- Section pages ----------------

def build_section(section, filename):
    stories = stories_for(section)
    label = SECTIONS[section]
    if stories:
        items = "".join(
            f"""<li>
<a class="thumb" href="articles/{s['slug']}.html">{img_html(s['slug'], w=400)}</a>
<p><span class="kicker">{SECTIONS[s['section']]}</span></p>
<h3><a href="articles/{s['slug']}.html">{s['headline']}</a></h3>
<p>{s['dek']}</p>
<p class="byline"><time>{s['date']}</time> &middot; Source: {s['source']}</p>
</li>""" for s in stories
        )
        listing = f'<ul class="story-list" data-section-list="{section}">{items}</ul>'
    else:
        listing = "<p>No stories in this section yet. New coverage is added daily.</p>"
    body = f"""
<h1 class="section-head"><span class="tag">&#9632;</span> {label}</h1>
{listing}
{most_read_html()}
{newsletter_html()}
"""
    return page(
        f"{label} news",
        f"Latest {label.lower()} news from Western World News — Western and European coverage, free to read.",
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
<p>Rolling updates on Russia's war in Ukraine — the overnight missile strikes, the Shenzhen summit and Europe's response. Times are in CET. Last updated 20 November 2026.</p>
<div id="live-updates">{updates}</div>
<p><a class="btn" href="articles/russia-ukraine-missile-attack.html">Read the full story &rarr;</a></p>
{newsletter_html()}
"""
    return page(
        "Live: Ukraine war — rolling updates",
        "Live updates on Russia's war in Ukraine: missile strikes, the Trump–Xi–Putin summit and Europe's response.",
        "live.html", body, BASE + "/live.html",
    )


# ---------------- Article pages ----------------

def build_article(s):
    body_paras = "".join(f"<p>{p}</p>" for p in s["body"])
    rel = "".join(
        f'<li><a href="{r}.html">{BY_SLUG[r]["headline"]}</a> <span class="byline">— {BY_SLUG[r]["date"]}</span></li>'
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
This story is an original summary by Western World News, based on reporting by {s['source']} ({s['date']}). Read the original report: <a href="{s['source_url']}" target="_blank" rel="noopener">{s['source']} — original article</a>.
</div>
<section class="related">
<h2>Related stories</h2>
<ul class="story-list">{rel}</ul>
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
    body = f'<h1 class="section-head"><span class="tag">&#9632;</span> {heading}</h1>\n' + "\n".join(f"<p>{p}</p>" for p in paragraphs)
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
            "image": uimg(pid, 1200) if pid else "",
            "imageCaption": cap,
        })
    return {
        "version": 1,
        "settings": {
            "siteName": "Western World News",
            "tagline": "Western and European news, live — politics, war, business and culture.",
            "heroSlug": "russia-ukraine-missile-attack",
        },
        "breaking": {
            "text": "Russia launches one of the largest missile attacks of the war on Ukraine — 110+ missiles fired overnight",
            "link": "articles/russia-ukraine-missile-attack.html",
        },
        "articles": articles,
        "justIn": [{"time": t, "text": h, "link": "live.html"} for t, h, _ in JUST_IN],
        "liveUpdates": [{"time": t, "headline": h, "text": p} for t, h, p in LIVE_UPDATES],
        "mostRead": list(MOST_READ),
    }


CONTENT_JS = """/* Western World News — central content store.
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
      // means the owner deleted it — but only when the saved list was
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

MAIN_JS = """// Western World News — front-end behaviour (v2).
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

    // Hero (homepage).
    var heroEl = $("[data-hero]");
    var hero = bySlug[store.settings.heroSlug] || store.articles[0];
    if (heroEl && hero) {
      heroEl.innerHTML =
        tileFor(hero) +
        '<p><span class="kicker">' + esc(sectionLabel(hero.section)) + " &middot; Live</span></p>" +
        '<h1><a href="' + articleUrl(hero.slug) + '">' + esc(hero.headline) + "</a></h1>" +
        '<p class="dek">' + esc(hero.dek) + "</p>" +
        '<p class="byline"><time>' + esc(hero.date) + "</time> &middot; Source: " + esc(hero.source) +
        ' &middot; <a href="' + fixLink("live.html") + '">Follow live updates &rarr;</a></p>';
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

    // Section pages.
    $all("[data-section-list]").forEach(function (list) {
      var sec = list.getAttribute("data-section-list");
      var items = store.articles.filter(function (a) { return (a.sections || [a.section]).indexOf(sec) !== -1; });
      if (!items.length) return;
      list.innerHTML = items.map(function (a) {
        return "<li>" +
          '<a class="thumb" href="' + articleUrl(a.slug) + '">' + tileFor(a) + "</a>" +
          '<p><span class="kicker">' + esc(sectionLabel(a.section)) + "</span></p>" +
          '<h3><a href="' + articleUrl(a.slug) + '">' + esc(a.headline) + "</a></h3>" +
          "<p>" + esc(a.dek) + "</p>" +
          '<p class="byline"><time>' + esc(a.date) + "</time> &middot; Source: " + esc(a.source) + "</p></li>";
      }).join("");
    });

    // Most Read.
    var mr = $("#most-read-list");
    if (mr) {
      var slugs = (store.mostRead || []).filter(function (s) { return bySlug[s]; });
      if (!slugs.length) slugs = store.articles.slice(0, 5).map(function (a) { return a.slug; });
      mr.innerHTML = slugs.slice(0, 5).map(function (slug) {
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
            '" target="_blank" rel="noopener">' + esc(a.source) + " — original article</a>.";
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

    // Search — filters articles, shows a dropdown of matches.
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

ADMIN_CSS = """/* Western World News — admin panel styles (admin.html only). */
.admin-top { background: var(--navy-dark); color: #fff; padding: 0.9rem 0; }
.admin-top .wrap { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.admin-top .wordmark { font-size: 1.4rem; }
.admin-badge { background: var(--red); color: #fff; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; padding: 0.2rem 0.55rem; border-radius: 3px; text-transform: uppercase; }
.admin-top .spacer { flex: 1; }
.admin-top a { color: #fff; font-weight: 600; }
.admin-top button { background: rgba(255,255,255,0.15); color: #fff; border: 1px solid rgba(255,255,255,0.4); border-radius: 3px; padding: 0.4rem 0.8rem; cursor: pointer; font-weight: 600; }
.admin-top button:hover { background: rgba(255,255,255,0.28); }
.gate-card { max-width: 420px; margin: 3rem auto; border: 1px solid var(--line); border-radius: 6px; padding: 1.6rem; background: #fff; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
.gate-card h1 { font-family: var(--serif); margin: 0 0 0.4rem; font-size: 1.5rem; }
.gate-card p { color: var(--muted); margin: 0 0 1rem; }
.gate-card .error { color: var(--red); font-weight: 700; display: none; margin: 0.6rem 0 0; }
.admin-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0 1.6rem; }
@media (max-width: 860px) { .admin-grid { grid-template-columns: repeat(2, 1fr); } }
.stat { border: 1px solid var(--line); border-top: 3px solid var(--red); border-radius: 4px; padding: 0.8rem 1rem; background: #fff; }
.stat b { display: block; font-family: var(--serif); font-size: 1.9rem; line-height: 1.1; }
.stat span { color: var(--muted); font-size: 0.85rem; }
.panel { border: 1px solid var(--line); border-radius: 6px; margin: 0 0 1.6rem; overflow: hidden; }
.panel > h2 { margin: 0; padding: 0.75rem 1rem; background: var(--navy); color: #fff; font-family: var(--serif); font-size: 1.15rem; }
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

ADMIN_JS = """// Western World News — admin panel (admin.html).
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
    toast(msg || "Saved — live across the site in this browser.");
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
      : "No unpublished changes — showing the site's default content.";
  }
  function renderArticles() {
    var list = $("#article-list");
    list.innerHTML = data.articles.map(function (a) {
      var heroMark = data.settings.heroSlug === a.slug ? ' <b style="color:var(--red)">★ Hero</b>' : "";
      var mrMark = (data.mostRead || []).indexOf(a.slug) !== -1 ? ' <b>· Most Read</b>' : "";
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
      return '<li><div class="t"><b>' + esc(it.time) + "</b> — " + esc(it.text) +
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
      return '<li><div class="t"><b>' + esc(u.time) + " — " + esc(u.headline) + "</b>" +
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
    save("Article saved — it is live on the site in this browser now.");
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
    toast("Exported wwn-content.json — keep it to make changes permanent.");
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
        toast("Imported — content replaced.");
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
<title>Admin — Western World News</title>
<meta name="description" content="Admin panel for Western World News.">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/admin.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23bb1919'/%3E%3Ctext x='16' y='22' font-family='Georgia' font-size='16' font-weight='bold' fill='white' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E">
</head>
<body>
<header class="admin-top"><div class="wrap">
<a class="wordmark" href="index.html">Western World <span class="news">News</span></a>
<span class="admin-badge">Admin</span>
<span class="spacer"></span>
<a href="index.html">View site &rarr;</a>
<button id="logout" type="button">Log out</button>
</div></header>
<main id="main"><div class="wrap">

<div class="gate-card" id="gate">
<h1>Admin login</h1>
<p>Enter the admin passcode to manage the site. (Default passcode: <b>admin123</b> — change it in assets/js/admin.js. Note: this is a basic gate on a static site, not real server security.)</p>
<form id="gate-form">
<div class="field"><label for="passcode">Passcode</label>
<input id="passcode" type="password" autocomplete="current-password" required></div>
<div class="form-actions"><button class="btn" type="submit">Log in</button></div>
<p class="error" id="gate-error">Wrong passcode — try again.</p>
</form>
</div>

<div id="dashboard" class="hidden">
<h1 class="section-head"><span class="tag">&#9632;</span> Dashboard</h1>
<div class="notice"><b>How saving works</b>
Changes you save here apply across the whole site <b>immediately in this browser</b> (they are stored in this browser's localStorage).
To make them permanent for everyone, use <b>Export JSON</b> below and send the file to musu — or save it in the site folder as <b>content-export.json</b> and rebuild the site. Until then, other browsers still see the default content.</div>
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
<h3 id="af-title-text" style="font-family:var(--serif);margin:0 0 0.8rem">Add article</h3>
<div class="form-grid">
<div class="field"><label for="af-title">Headline *</label><input id="af-title" type="text" required></div>
<div class="field"><label for="af-slug">URL slug * <span class="hint">lower-case letters, numbers, hyphens — auto-filled from the headline</span></label><input id="af-slug" type="text" required></div>
<div class="field"><label for="af-section">Section</label><select id="af-section">{options}</select></div>
<div class="field"><label for="af-date">Date</label><input id="af-date" type="text" placeholder="20 November 2026"></div>
<div class="field full"><label for="af-dek">Summary (shows on the homepage and section pages)</label><textarea id="af-dek" style="min-height:70px"></textarea></div>
<div class="field full"><label for="af-body">Article text <span class="hint">one paragraph per block — leave a blank line between paragraphs</span></label><textarea id="af-body"></textarea></div>
<div class="field"><label for="af-image">Photo URL <span class="hint">leave empty for the navy placeholder tile</span></label><input id="af-image" type="url" placeholder="https://images.unsplash.com/photo-..."></div>
<div class="field"><label for="af-caption">Photo caption / credit</label><input id="af-caption" type="text" placeholder="Photo: Unsplash"></div>
<div class="field"><label for="af-source">Source name</label><input id="af-source" type="text" placeholder="Reuters"></div>
<div class="field"><label for="af-source-url">Source link</label><input id="af-source-url" type="url" placeholder="https://..."></div>
<div class="field full"><div class="check-row">
<label><input id="af-hero" type="checkbox"> Make this the homepage hero story</label>
<label><input id="af-mostread" type="checkbox"> Show in Most Read</label>
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
<h3 id="ji-form-title" style="font-family:var(--serif);margin:0 0 0.8rem">Add Just In item</h3>
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
<h3 id="lv-form-title" style="font-family:var(--serif);margin:0 0 0.8rem">Add live update</h3>
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

<section class="panel"><h2>Data — export, import, reset</h2><div class="body">
<p>Export downloads the site's full content as <b>wwn-content.json</b>. To make admin changes permanent for all visitors, send that file to musu, or save it in the site folder as <b>content-export.json</b> and re-run the build script (<b>tools/build_site.py</b>) — the static pages are then regenerated with your content, including a real page for every new article.</p>
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
<p class="fineprint"><span>&copy; 2026 Western World News (westernworldnews.com). Admin panel — passcode gate only, not real server security.</span><span><a href="index.html">Back to site &rarr;</a></span></p>
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
- Photos are **real, openly-licensed Unsplash images** used as generic
  thematic illustrations (city skylines, parliaments, markets, stadiums).
  They are **not** photos of the actual events — every caption says
  "Illustrative photo. Photo: Unsplash". Stories without a photo get the
  navy WWN gradient tile instead of a fake event photo.

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

The 10 articles in `articles/` are **seed content published 20 November
2026**, written to launch the site with real, verified stories from
16–20 November 2026 (Ukraine missile strikes, the Trump–Xi–Putin Shenzhen
summit, the Gaza ceasefire warning, the EU's €45bn Ukraine loan, the
Denmark–Greenland deal, the US midterms, the Bank of England rate rise, UK
inflation, Japan beating Brazil, and the record Van Gogh sale).

- Every story is an **original summary written in our own words** — nothing
  is copied from another publication.
- Every story **credits its source by name and links to the original
  article** (CNN, The Times, Al Jazeera, Reuters, Nikkei Asia, Chosun Biz).
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
- **Domain**: westernworldnews.com (confirmed available on Hostinger,
  20 Nov 2026; Pintu is buying 1 year at $9.99).
- **Ads**: none included yet. Add ad slots only after traffic exists.
- **GitHub**: Pintu is connecting the repo; the site is pushed there and
  the domain pointed at hosting once live.

## Rebuilding

Run `python3 tools/build_site.py` (or `python3 /tmp/build_site_v2.py`).
To change the shared header, footer, navigation or design, edit the
script and re-run it — or edit the HTML/CSS files directly; they are
plain and self-contained.
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
        "About Western World News — independent news from the West and the world.",
        "About us",
        ["Western World News is an independent news site covering worldwide news with a main focus on Western and European politics, war and breaking news, plus a small Business &amp; Finance section.",
         "We write our stories in our own words, based on reporting from trusted sources — and we always credit and link the original reporting. We do not copy articles word for word, and we do not publish rumours or unconfirmed claims as fact.",
         "The site is free to read. There is no paywall at launch.",
         "Contact us via the contact page."])))
    files.append(write("contact.html", build_info(
        "contact", "Contact Western World News",
        "Contact Western World News — news tips, corrections and advertising enquiries.",
        "Contact",
        ["News tips, corrections and general enquiries: tips@westernworldnews.com (mailbox to be set up — see README.md).",
         "For corrections, please include the story headline and the fact to be corrected. We correct errors promptly and transparently.",
         "Advertising enquiries: ads@westernworldnews.com (mailbox to be set up — see README.md)."])))
    files.append(write("privacy.html", build_info(
        "privacy", "Privacy policy — Western World News",
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
    entries = "".join(
        f"  <url><loc>{BASE}/{u}</loc><lastmod>2026-11-20</lastmod></url>\n" for u in urls
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
