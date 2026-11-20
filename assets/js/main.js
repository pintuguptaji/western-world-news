// Western World News: front-end behavior (v2).
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
