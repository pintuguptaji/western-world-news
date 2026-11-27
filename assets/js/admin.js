// Western World News: admin panel (admin.html).
// Passcode gate only: this is a static site, so the passcode is a basic
// gate, NOT real server security. Anyone with the site files can read the
// content. Do not rely on it to protect secrets.
// To change the passcode, edit the PASSCODE line below (in this template
// in tools/build_site.py), then rebuild and push.
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
      $("#af-body").value = (a.body || []).join("\n\n");
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
    var body = $("#af-body").value.split(/\n\s*\n/).map(function (p) { return p.trim(); }).filter(Boolean);
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
})();