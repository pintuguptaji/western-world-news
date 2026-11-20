/* Western World News — central content store.
   WWN_DEFAULT_CONTENT is the seed content baked into the static site.
   The admin panel (admin.html) saves edits to localStorage under
   WWNStore.KEY; pages load the merged result, so admin changes apply
   across the whole site immediately (in that browser).
   Export JSON from the admin to make changes permanent in the repo. */
window.WWN_DEFAULT_CONTENT = {
  "version": 1,
  "settings": {
    "siteName": "Western World News",
    "tagline": "Western and European news, live — politics, war, business and culture.",
    "heroSlug": "russia-ukraine-missile-attack"
  },
  "breaking": {
    "text": "Russia launches one of the largest missile attacks of the war on Ukraine — 110+ missiles fired overnight",
    "link": "articles/russia-ukraine-missile-attack.html"
  },
  "articles": [
    {
      "slug": "russia-ukraine-missile-attack",
      "sections": [
        "war-conflict",
        "world"
      ],
      "section": "war-conflict",
      "headline": "Russia launches one of the largest missile attacks of the war on Ukraine",
      "dek": "More than 110 missiles were fired overnight, Ukrainian officials say, hours after Trump, Putin and Xi met in China — and as Poland scrambled jets after its airspace was violated.",
      "date": "20 November 2026",
      "source": "CNN",
      "source_url": "https://www.cnn.com/2026/11/20/europe/russia-ukraine-putin-trump-intl-hnk",
      "body": [
        "Russia launched a large overnight missile and drone attack on Ukraine into Friday, Ukrainian officials said, killing at least eight people and injuring at least 28, in what Kyiv described as one of the largest aerial assaults of the war.",
        "Ukraine said Russia fired at least 110 missiles overnight — an unusually large number even by the standards of a war now in its fifth year. The attack lasted more than ten hours, according to Ukrainian authorities.",
        "Russia's defence ministry said it had carried out a “massive strike” with high-precision weapons launched from land, sea and air, as well as drones, targeting military and energy facilities, port infrastructure in the Odesa region and transport infrastructure in Kyiv. President Volodymyr Zelensky said “absolutely all the targets were ordinary civilian infrastructure”.",
        "Three bridges in Kyiv were damaged, according to mayor Vitaly Klitschko, cutting transport links between the two sides of the capital.",
        "Poland said fighter jets were scrambled and Patriot air defence systems activated early on Friday after objects flew into and fell inside Polish territory during the attack.",
        "The strikes came hours after President Vladimir Putin met US President Donald Trump and Chinese leader Xi Jinping for trilateral talks in Shenzhen. Trump later spoke with European leaders and, according to a senior European official, described Putin as “tired” and ready for a deal. The talks produced no breakthrough, and no official declaration was released.",
        "Putin had vowed revenge for Ukraine's recent attacks on the bridge linking Russia with occupied Crimea."
      ],
      "related": [
        "gaza-ceasefire-collapse-warning",
        "trump-xi-putin-shenzhen-summit",
        "eu-ukraine-loan-45-billion"
      ],
      "image": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A city skyline at night. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "trump-xi-putin-shenzhen-summit",
      "sections": [
        "world",
        "politics"
      ],
      "section": "world",
      "headline": "Trump, Xi and Putin hold historic trilateral talks — but no breakthrough on Ukraine",
      "dek": "The leaders of the three biggest nuclear powers met in Shenzhen for the first time, agreeing a joint declaration on the UN, nuclear weapons and oil — while the war in Ukraine went on.",
      "date": "19 November 2026",
      "source": "The Times",
      "source_url": "https://www.thetimes.com/world/asia/article/trump-xi-putin-summit-shenzhen-latest-news-ddskr7pcx",
      "body": [
        "The leaders of the United States, China and Russia met in Shenzhen on Thursday for the first trilateral talks between the three nuclear powers.",
        "A joint declaration covered reform of the United Nations, nuclear weapons, oil production and international law, but the meeting produced no breakthrough on the war in Ukraine.",
        "The talks lasted just over an hour. President Donald Trump embraced President Vladimir Putin and called him “my friend” before the meeting, and left for the airport immediately afterwards.",
        "Trump later spoke with European leaders in the “coalition of the willing”, who were meeting in Berlin with US envoys Steve Witkoff and Jared Kushner. According to an official present, he told them they were spending too much money on the war and should be spending it on their own countries.",
        "The leaders of the E3 — the UK, Germany and France — and Ukraine called on Russia to agree to a ceasefire on attacks on energy infrastructure for the duration of winter.",
        "Trump also told NBC News that he would meet North Korean leader Kim Jong-un at “some point”."
      ],
      "related": [
        "russia-ukraine-missile-attack",
        "democrats-win-congress-midterms",
        "denmark-greenland-security-deal"
      ],
      "image": "https://images.unsplash.com/photo-1444723121867-7a241cacace9?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A modern city skyline at dusk. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "gaza-ceasefire-collapse-warning",
      "sections": [
        "war-conflict",
        "world"
      ],
      "section": "war-conflict",
      "headline": "Gaza ceasefire at risk of collapse, Board of Peace warns UN Security Council",
      "dek": "The body overseeing the US-brokered truce says the gap between what was agreed and what is happening on the ground is now the main threat to the deal.",
      "date": "18 November 2026",
      "source": "Al Jazeera",
      "source_url": "https://www.aljazeera.com/amp/news/2026/11/18/board-of-peace-warns-gaza-ceasefire-faces-imminent-collapse-without-action",
      "body": [
        "The Board of Peace, the body overseeing the US-brokered ceasefire in Gaza, has warned the UN Security Council that the year-old truce risks collapse if its terms are not fully implemented.",
        "In its first annual assessment, a copy of which was obtained by the Associated Press, the board said “the distance between what has been agreed and what is happening on the ground” was the principal risk to the process, and that “a ceasefire that delivers nothing visible cannot be sustained indefinitely.”",
        "The ceasefire formally began on 10 October 2025, but attacks have continued. The Palestinian health ministry says more than 1,600 people have been killed in Israeli strikes since then.",
        "At the centre of the stall is the technocratic civil administration created to run Gaza on an interim basis. The board says Israel has still not allowed it to take up its job in the territory, delaying the international stabilisation force, an Israeli troop withdrawal, the disarmament of Hamas and reconstruction.",
        "Israel says reconstruction can begin only after Hamas disarms. Hamas has refused to give up its weapons while Israeli forces remain in Gaza.",
        "The board also noted that Israeli forces had begun a ground operation west of the Yellow Line in central Gaza. The military later said the operation was complete and reopened Salah al-Din Street."
      ],
      "related": [
        "russia-ukraine-missile-attack",
        "trump-xi-putin-shenzhen-summit"
      ],
      "image": "https://images.unsplash.com/photo-1547234935-80c7145ec969?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "Desert landscape in the Middle East. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "eu-ukraine-loan-45-billion",
      "sections": [
        "europe",
        "politics",
        "business-finance"
      ],
      "section": "europe",
      "headline": "EU proposes €45 billion loan to keep Ukraine funded in 2027",
      "dek": "The loan would cover around two-thirds of Kyiv's expected funding gap next year — and would be repaid, the Commission says, through future war reparations by Russia.",
      "date": "18 November 2026",
      "source": "Reuters",
      "source_url": "https://www.reuters.com/world/eu-proposes-new-45-billion-loan-ukraine-2027-be-repaid-by-russia-2026-11-18/",
      "body": [
        "The European Commission has proposed a new €45 billion (about $49 billion) loan to Ukraine for 2027, to be repaid through future war reparations by Russia.",
        "The loan would cover around two-thirds of Ukraine's expected €70 billion funding gap next year, with the rest to come from other international partners.",
        "Up to €25 billion would go to military assistance and up to €20 billion to general budget support, keeping hospitals, schools and other public services running.",
        "Disbursements would be tied to Kyiv continuing reforms, particularly on the rule of law, anti-corruption efforts and public finance management.",
        "The plan needs approval from EU governments and the European Parliament. The budget amendment underpinning it would need unanimous support from member states.",
        "Commission President Ursula von der Leyen said she was confident all 27 members would back the plan. EU leaders were due to discuss it at a Brussels summit."
      ],
      "related": [
        "russia-ukraine-missile-attack",
        "bank-of-england-raises-rates",
        "uk-inflation-3-6-percent"
      ],
      "image": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A street in a European old town. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "denmark-greenland-security-deal",
      "sections": [
        "europe",
        "world"
      ],
      "section": "europe",
      "headline": "Denmark approves US–Greenland security deal, easing Arctic tensions",
      "dek": "All 109 lawmakers present voted in favour of the agreement, which lets the US build two bases in Greenland while keeping the island under Danish sovereignty.",
      "date": "19 November 2026",
      "source": "Al Jazeera",
      "source_url": "https://www.aljazeera.com/news/2026/11/19/denmark-parliament-approves-security-deal-with-greenland-and-us",
      "body": [
        "Denmark's parliament has unanimously approved a security agreement with the United States covering Greenland, easing months of tension over President Donald Trump's desire to annex the Arctic island.",
        "All 109 lawmakers present in the 179-seat Folketing voted in favour, with no votes against and no abstentions. Greenland's parliament approved the deal earlier in November by 16 votes to none, with seven abstentions.",
        "The agreement, signed in New York on 22 September, supplements a 1951 accord on the US military presence in Greenland. It allows the US to build two military bases in Greenland and blocks countries outside the EU and NATO from strategic sectors, to stop China or Russia gaining influence there.",
        "The deal is an executive agreement and does not need a vote in the US Senate. It enters into force once Denmark's foreign ministry formally notifies the US that procedures are complete.",
        "The agreement reaffirms the sovereignty of the Kingdom of Denmark and the right of Greenland's people to self-determination."
      ],
      "related": [
        "trump-xi-putin-shenzhen-summit",
        "eu-ukraine-loan-45-billion"
      ],
      "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "Snow-covered mountains under a night sky. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "democrats-win-congress-midterms",
      "sections": [
        "us",
        "politics"
      ],
      "section": "us",
      "headline": "Democrats seal 56–44 Senate majority as final midterm race is called",
      "dek": "Mary Peltola's win in Alaska completes a sweeping Democratic victory in the US midterms — control of both chambers of Congress, and a divided government for Trump's final two years.",
      "date": "19 November 2026",
      "source": "Nikkei Asia",
      "source_url": "https://asia.nikkei.com/politics/u.s.-midterm-elections/us-midterms-democrats-seal-56-44-senate-majority-with-alaska-win",
      "body": [
        "Democrats have completed a sweeping victory in the US midterm elections, winning control of both the House of Representatives and the Senate.",
        "Democrat Mary Peltola defeated two-term Republican Senator Dan Sullivan in Alaska, according to the Associated Press, completing the final unresolved Senate race and giving Democrats a 56–44 majority.",
        "Democrats flipped nine Republican-held Senate seats, with wins in traditionally conservative states including Texas, Kansas, Mississippi and South Carolina.",
        "In Texas, James Talarico defeated Ken Paxton — the first Democrat to win statewide office there in 32 years. In Kansas, Adam Hamilton beat Roger Marshall; Democrats last won a Senate seat there in 1932.",
        "Democrats also won the House, passing the 218 seats needed for a majority. All 435 House seats and 35 of the Senate's 100 seats were contested in the 3 November elections.",
        "Democrats have nominated Hakeem Jeffries to be the next House speaker, putting him on course to become the first Black lawmaker to hold the gavel when the new Congress convenes on 3 January.",
        "Voter discontent over inflation, tariffs, AI data centres and the war in Iran drove the result, according to Nikkei Asia's reporting."
      ],
      "related": [
        "trump-xi-putin-shenzhen-summit",
        "uk-inflation-3-6-percent"
      ],
      "image": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A parliament chamber in session. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "bank-of-england-raises-rates",
      "sections": [
        "business-finance",
        "europe"
      ],
      "section": "business-finance",
      "headline": "Bank of England raises rates to 4% — first increase since 2023",
      "dek": "The Bank acted as energy prices pushed by the Middle East conflict drive inflation higher, and warned it could reach around 5% by mid-2027.",
      "date": "5 November 2026",
      "source": "Reuters",
      "source_url": "https://www.reuters.com/world/uk/britains-long-wait-2-inflation-tests-public-faith-bank-england-2026-11-18/",
      "body": [
        "The Bank of England has raised interest rates to 4%, its first increase in more than three years, as energy prices push inflation higher.",
        "The Monetary Policy Committee voted 8–1 to raise Bank Rate by a quarter of a percentage point from 3.75%. Catherine Mann dissented, preferring a larger rise to 4.25%.",
        "The Bank said the Middle East conflict had driven energy prices sharply higher since July, with oil up 38% and UK gas up 81%, and warned inflation could reach around 5% by mid-2027 — far above its 2% target.",
        "Governor Andrew Bailey said the rise should not be seen as the start of an inevitable long sequence of increases, but warned more could follow if the conflict drags on.",
        "The next decision is due on 17 December. Markets had priced in a near-certain rise, and mortgage rates had already climbed since September."
      ],
      "related": [
        "uk-inflation-3-6-percent",
        "eu-ukraine-loan-45-billion"
      ],
      "image": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "Westminster, London. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "uk-inflation-3-6-percent",
      "sections": [
        "business-finance",
        "europe"
      ],
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
        "The Bank of England expects inflation to approach 5% in the second quarter of 2027. The reading was slightly below the Bank's 3.7% forecast, prompting investors to trim bets on a December rate rise."
      ],
      "related": [
        "bank-of-england-raises-rates",
        "eu-ukraine-loan-45-billion"
      ],
      "image": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A food market. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "japan-beats-brazil-3-2",
      "sections": [
        "sport"
      ],
      "section": "sport",
      "headline": "Japan stun Brazil 3–2 in Moriyasu's farewell friendly",
      "dek": "A stoppage-time winner from Tatsuhito Sakamoto sealed victory in Singapore — a final win for the coach who has led Japan for eight years.",
      "date": "16 November 2026",
      "source": "Chosun Biz",
      "source_url": "https://biz.chosun.com/en/en-sports/2026/11/16/7LRBK2NGSZCKXP3JUZJ5AUA74Q/",
      "body": [
        "Japan beat Brazil 3–2 in a November international friendly in Singapore, in coach Hajime Moriyasu's final match in charge after eight years.",
        "Takefusa Kubo opened the scoring in the 15th minute and Keito Nakamura doubled the lead four minutes later. Brazil's Vinícius Júnior scored twice to level the match, but Tatsuhito Sakamoto struck the winner in the first minute of second-half stoppage time.",
        "Japan, ranked 17th in the world, converted three of their eight shots, with Kubo, Nakamura and Sakamoto each scoring with their only shot on goal.",
        "The win avenged Japan's 2–1 defeat by Brazil in the round of 32 at the 2026 World Cup last summer.",
        "Moriyasu, who has led Japan since 2018, will step down after the November international window. Japan face Paraguay next as they build towards the next World Cup."
      ],
      "related": [
        "van-gogh-record-190-million"
      ],
      "image": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "A football stadium under lights. Illustrative photo. Photo: Unsplash"
    },
    {
      "slug": "van-gogh-record-190-million",
      "sections": [
        "culture"
      ],
      "section": "culture",
      "headline": "Van Gogh sells for record $190.4 million at Sotheby's",
      "dek": "“Châtaigniers en fleurs”, unseen in public for more than 50 years, became the fourth most expensive painting ever sold at auction — a day after a dispute over its Nazi-era sale was settled.",
      "date": "19 November 2026",
      "source": "Reuters",
      "source_url": "https://www.reuters.com/lifestyle/van-goghs-chataigniers-en-fleurs-sells-auction-record-1904-million-2026-11-19/",
      "body": [
        "Vincent van Gogh's 1890 painting “Châtaigniers en fleurs” (Blossoming Chestnut Trees) has sold for $190.4 million at Sotheby's in New York, an auction record for the artist.",
        "The hammer price was $165 million, with fees taking the total to $190.4 million. The buyer was veteran art dealer Bill Acquavella, head of Acquavella Galleries.",
        "The previous Van Gogh record was $117.2 million, paid in 2022 for “Orchard with Cypresses” from the collection of Microsoft co-founder Paul Allen.",
        "The sale makes it the fourth most expensive painting ever sold at auction, and the second most valuable work ever sold at Sotheby's, behind a Klimt portrait that fetched $236.4 million in November 2025.",
        "The painting, which had not been seen in public for more than 50 years, was the top lot in the sale of 12 works from the Blaquier-Arrieta Collection. All 12 sold for a combined $412 million.",
        "The sale went ahead a day after Sotheby's announced an agreement with the heirs of German Jewish publisher Samuel Fischer, who said the painting had been sold under duress in 1936 during Nazi persecution."
      ],
      "related": [
        "japan-beats-brazil-3-2"
      ],
      "image": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=1200&q=80",
      "imageCaption": "An abstract painting. Illustrative photo. Photo: Unsplash"
    }
  ],
  "justIn": [
    {
      "time": "20 Nov, 10:33",
      "text": "Russian barrage damages embassies and a cathedral in Kyiv",
      "link": "live.html"
    },
    {
      "time": "20 Nov, 09:15",
      "text": "Netherlands summons Russian ambassador after Kyiv strike damages its embassy",
      "link": "live.html"
    },
    {
      "time": "20 Nov, 08:40",
      "text": "Six dead in Georgia as gas blast collapses part of a residential block",
      "link": "live.html"
    },
    {
      "time": "19 Nov, 19:05",
      "text": "France rejects Russian claim it is directly involved in the Ukraine war",
      "link": "live.html"
    },
    {
      "time": "19 Nov, 17:20",
      "text": "Trump says he will meet North Korea's Kim Jong-un at “some point”",
      "link": "live.html"
    },
    {
      "time": "19 Nov, 15:10",
      "text": "NATO launches multinational STARLIFT space initiative for military launches",
      "link": "live.html"
    },
    {
      "time": "19 Nov, 13:45",
      "text": "EU Commission confirms AI-generated cyber campaign; no staff-wide breach found",
      "link": "live.html"
    },
    {
      "time": "18 Nov, 21:30",
      "text": "UN court to decide on Thursday if Myanmar's expulsion of Rohingya was genocide",
      "link": "live.html"
    }
  ],
  "liveUpdates": [
    {
      "time": "20 Nov, 10:33",
      "headline": "Embassies damaged in Kyiv barrage",
      "text": "A daytime Russian barrage blew out windows at the Austrian and Dutch missions in Kyiv and damaged a cathedral, prompting Brussels to summon Moscow's envoy."
    },
    {
      "time": "20 Nov, 09:15",
      "headline": "Netherlands summons Russian ambassador",
      "text": "The Dutch government summoned Russia's ambassador after its embassy in Kyiv suffered minor damage when a projectile landed near the building. No one was hurt."
    },
    {
      "time": "20 Nov, 08:00",
      "headline": "Poland scrambles jets as airspace is violated",
      "text": "Poland said fighter jets were scrambled and Patriot air defence systems activated early on Friday after objects flew into and fell inside Polish territory during the overnight attack."
    },
    {
      "time": "20 Nov, 06:30",
      "headline": "More than 110 missiles fired at Ukraine overnight",
      "text": "Ukraine said Russia fired at least 110 missiles overnight — an unusually large number even amid frequent aerial assaults. At least eight people were killed and 28 injured, and three of Kyiv's bridges were damaged."
    },
    {
      "time": "19 Nov, 22:10",
      "headline": "Trump tells European leaders Putin is “tired” and ready for a deal",
      "text": "After the Shenzhen talks, President Trump spoke with the “coalition of the willing” in Berlin. According to a senior European official, his main message was that “Putin is tired, wants to end this, ready for a deal.”"
    },
    {
      "time": "19 Nov, 18:40",
      "headline": "E3 leaders call for winter energy ceasefire",
      "text": "The leaders of the UK, Germany and France and Ukraine called on Russia to agree to a ceasefire on attacks on energy infrastructure for the duration of winter."
    },
    {
      "time": "19 Nov, 17:00",
      "headline": "Trilateral talks end without breakthrough",
      "text": "Trump, Xi and Putin met in Shenzhen for just over an hour. A joint declaration covered UN reform, nuclear weapons and oil production, but produced no breakthrough on Ukraine and no official declaration was released."
    },
    {
      "time": "18 Nov, 20:15",
      "headline": "EU proposes €45 billion loan for Ukraine in 2027",
      "text": "The European Commission proposed a new €45 billion loan to Ukraine for 2027, to be repaid through future war reparations by Russia. Up to €25 billion would go to military aid and €20 billion to budget support."
    }
  ],
  "mostRead": [
    "russia-ukraine-missile-attack",
    "trump-xi-putin-shenzhen-summit",
    "gaza-ceasefire-collapse-warning",
    "eu-ukraine-loan-45-billion",
    "democrats-win-congress-midterms"
  ]
};

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
