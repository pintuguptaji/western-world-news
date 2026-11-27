// Western World News: front-end behavior (v4 redesign).
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
  function sectionLabel(slug) {
    var map = { world: "World", europe: "Europe", us: "US", politics: "Politics",
      "war-conflict": "War & Conflict", "business-finance": "Business",
      technology: "Technology", sport: "Sport", culture: "Culture", live: "Live" };
    return map[slug] || slug;
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
        var link = it.link || "";
        if (link) return '<a href="' + fixLink(link) + '">' + esc(it.text) + "</a>";
        return "<span>" + esc(it.text) + "</span>";
      }).join("");
      track.innerHTML = items + items;
    }

    // Hero (homepage): photo, kicker, headline, dek, byline.
    var heroEl = $("[data-hero]");
    var hero = bySlug[store.settings.heroSlug] || store.articles[0];
    if (heroEl && hero) {
      var heroImg = hero.image
        ? '<figure class="hero-media"><img src="' + esc(hero.image) + '" alt="' + esc(hero.headline) + '" width="1600" height="900"></figure>'
        : '<div class="art" role="img" aria-label="Graphic placeholder"><span class="monogram">WWN</span><span class="art-label">' + esc(sectionLabel(hero.section)) + "</span></div>";
      var isBreaking = store.breaking && store.breaking.link && store.breaking.link.indexOf(hero.slug) !== -1;
      var kick = isBreaking ? "Breaking" : esc(sectionLabel(hero.section));
      var liveLink = "";
      if (/ukraine|russia|kyiv|kremlin/i.test(hero.headline)) {
        liveLink = ' &middot; <a href="' + fixLink("live.html") + '">Follow live updates</a>';
      }
      heroEl.innerHTML =
        heroImg +
        '<p><span class="kicker">' + kick + "</span></p>" +
        '<h1><a href="' + articleUrl(hero.slug) + '">' + esc(hero.headline) + "</a></h1>" +
        '<p class="dek">' + esc(hero.dek) + "</p>" +
        '<p class="byline"><time>' + esc(hero.date) + "</time> &middot; Source: " + esc(hero.source) +
        liveLink + "</p>";
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
        if (heroBox) heroBox.innerHTML = tileFor(a, 1600);
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
