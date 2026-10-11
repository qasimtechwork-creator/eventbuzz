/* EventBuzz — Automatic Seasonal Theming Engine (v1)
   ------------------------------------------------------------------
   Picks the nearest upcoming event from the built-in calendar and dresses
   the site in that event's theme, fully automatically:

   - accent colors via CSS variables on <html data-theme="...">
   - homepage hero card image + caption + countdown + chip swap
   - homepage "Featured Event" panel rewrite
   - themed banner (with slow Ken Burns zoom) on every category page hero
   - auto-matching country flag on the National Days page (inline SVG,
     official-style, generated — never AI imagery)
   - subtle CSS-only animated decoration layer (leaves / snow / petals /
     rising sparks / holi powder), disabled under prefers-reduced-motion

   Images: ONLY reuses existing assets/images files. No external requests.
   Adsterra units and all existing content/markup are left untouched.
*/
(function () {
  "use strict";

  /* ---------- paths (works from any page depth) ---------- */
  var scriptEl = document.currentScript;
  var ASSET = "assets/";
  if (scriptEl && scriptEl.src) ASSET = scriptEl.src.replace(/[^\/]+$/, "");
  var IMG = ASSET + "images/";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }

  /* ---------- date helpers ---------- */
  function stripTime(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function easterSunday(y) { // Anonymous Gregorian computus — exact for any year
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4,
        f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3),
        h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
        l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(y, mo - 1, da);
  }
  function thanksgivingUS(y) { // 4th Thursday of November
    var d = new Date(y, 10, 1);
    return new Date(y, 10, 1 + ((4 - d.getDay() + 7) % 7) + 21);
  }
  function lunarShift(y, baseY, baseM, baseD) { // lunar drift ≈ 10.875 days earlier / year
    return new Date(new Date(y, baseM - 1, baseD).getTime() - Math.round((y - baseY) * 10.875 * 86400000));
  }
  var LUNAR = { // confirmed/expected dates, 2026–2028 (others via drift)
    diwali:   [[2026, 11, 8],  [2027, 10, 28], [2028, 10, 17]],
    eidFitr:  [[2026, 3, 20],  [2027, 3, 10],  [2028, 2, 28]],
    eidAdha:  [[2026, 5, 27],  [2027, 5, 17],  [2028, 5, 5]],
    holi:     [[2026, 3, 4],   [2027, 3, 22],  [2028, 3, 11]]
  };
  function lunarDate(key, y) {
    var rows = LUNAR[key], i, r;
    for (i = 0; i < rows.length; i++) { if (rows[i][0] === y) { r = rows[i]; return new Date(r[0], r[1] - 1, r[2]); } }
    r = rows[rows.length - 1];
    return lunarShift(y, r[0], r[1], r[2]);
  }

  /* ---------- event calendar ----------
     flag: ISO country code shown on the National Days page, null = global event */
  var EVENTS = [
    { key: "halloween",   label: "Halloween",        emoji: "🎃", flag: null, date: function (y) { return new Date(y, 9, 31); } },
    { key: "diwali",      label: "Diwali",           emoji: "🪔", flag: "IN", date: function (y) { return lunarDate("diwali", y); } },
    { key: "thanksgiving",label: "Thanksgiving",     emoji: "🦃", flag: "US", date: function (y) { return thanksgivingUS(y); } },
    { key: "christmas",   label: "Christmas",        emoji: "🎄", flag: null, date: function (y) { return new Date(y, 11, 25); } },
    { key: "newyear",     label: "New Year",         emoji: "🥂", flag: null, date: function (y) { return new Date(y, 0, 1); } },
    { key: "valentine",   label: "Valentine's Day",  emoji: "💝", flag: null, date: function (y) { return new Date(y, 1, 14); } },
    { key: "eidFitr",     label: "Eid al-Fitr",      emoji: "🌙", flag: null, date: function (y) { return lunarDate("eidFitr", y); } },
    { key: "holi",        label: "Holi",             emoji: "🎨", flag: "IN", date: function (y) { return lunarDate("holi", y); } },
    { key: "pakistanDay", label: "Pakistan Day",     emoji: "🇵🇰", flag: "PK", date: function (y) { return new Date(y, 2, 23); } },
    { key: "easter",      label: "Easter",           emoji: "🐣", flag: null, date: function (y) { return easterSunday(y); } },
    { key: "eidAdha",     label: "Eid al-Adha",      emoji: "🌙", flag: null, date: function (y) { return lunarDate("eidAdha", y); } },
    { key: "independenceDay", label: "Independence Day", emoji: "🇵🇰", flag: "PK", date: function (y) { return new Date(y, 7, 14); } }
  ];
  var COUNTRIES = { PK: "Pakistan", IN: "India", US: "United States" };
  var MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var MONTHS_L = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  var DAYS = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

  /* ---------- theme packs ----------
     image: existing assets/images file, or null = keep current imagery (colors/fx still apply)
     catHero: per-category banner overrides (default = image) */
  var THEMES = {
    halloween: {
      accent: "#f97316", accentSoft: "rgba(249,115,22,.38)", glow: "rgba(249,115,22,.16)",
      image: "halloween-2026-date-history-significance.jpg",
      alt: "Glowing carved Halloween pumpkins and candles in front of a haunted house",
      chip: { emoji: "🧩", text: "100 Spooky Trivia Questions", href: "articles/halloween-trivia-questions-2026.html" },
      featured: { title: "Halloween", tag: "👻 October 31 · Saturday", headline: "Halloween: Date, History & Significance",
        desc: "When is Halloween, where did it come from, and why do we carve pumpkins, dress up and go trick-or-treating? A warm, clear explainer for families, teachers and first-time celebrants.",
        meta: ["📅 Oct 31", "📖 8 min read", "🎃 Start here"], link: "articles/halloween-2026-date-history-significance.html",
        links: [
          ["💌", "Wishes, Messages & Quotes", "articles/halloween-wishes-messages-quotes-2026.html"],
          ["🧙", "Costume Ideas for Everyone", "articles/halloween-costume-ideas-2026.html"],
          ["🎲", "Party Ideas & Games", "articles/halloween-party-ideas-games-2026.html"],
          ["🍬", "Recipes & Treat Ideas", "articles/halloween-recipes-treat-ideas-2026.html"]] },
      fx: "leaves", fxColors: ["#c2410c", "#b45309", "#92400e", "#a16207"],
      catHero: { "default": "halloween-2026-images.jpg", festivals: "halloween-costume-ideas-2026.jpg",
        holidays: "halloween-party-ideas-games-2026.jpg", seasonal: "halloween-decoration-ideas-2026.jpg",
        shopping: "halloween-candy-guide-2026.jpg" }
    },
    diwali: {
      accent: "#f5b942", accentSoft: "rgba(245,185,66,.40)", glow: "rgba(245,185,66,.18)",
      image: "diwali-images-2026.jpg",
      alt: "Glowing diyas and festive Diwali lights",
      chip: { emoji: "🪔", text: "Diwali Dates & Lakshmi Puja Guide", href: "articles/diwali-2026-date-lakshmi-puja-calendar.html" },
      featured: { title: "Diwali", tag: "🪔 Festival of Lights", headline: "Diwali: Date, Lakshmi Puja & Calendar",
        desc: "When is Diwali, how is Lakshmi Puja timed, and what do the five days celebrate? Dates, rituals, wishes and decoration ideas for the Festival of Lights.",
        meta: ["🪔 Festival of Lights", "📖 7 min read", "✨ Start here"], link: "articles/diwali-2026-date-lakshmi-puja-calendar.html",
        links: [
          ["🏠", "Decoration Ideas at Home", "articles/diwali-decoration-ideas-at-home.html"],
          ["🍬", "Sweets & Recipes", "articles/diwali-sweets-and-recipes.html"],
          ["🖼️", "Diwali Images", "articles/diwali-images-2026.html"],
          ["🪔", "Dhanteras Puja Guide", "articles/dhanteras-2026-date-puja-guide-wishes.html"]] },
      fx: "sparks", fxColors: ["#f5b942", "#f3d47a", "#e8a020"],
      catHero: { "default": "diwali-decoration-ideas-at-home.jpg", festivals: "rangoli-designs-for-diwali-2026.jpg",
        holidays: "happy-diwali-wishes-2026.jpg", shopping: "diwali-sweets-and-recipes.jpg" }
    },
    thanksgiving: {
      accent: "#d97706", accentSoft: "rgba(217,119,6,.38)", glow: "rgba(217,119,6,.16)",
      image: "thanksgiving-dinner-ideas.jpg",
      alt: "Warm Thanksgiving dinner table with autumn dishes",
      chip: { emoji: "🦃", text: "Thanksgiving Wishes & Messages", href: "articles/thanksgiving-wishes-2026.html" },
      featured: { title: "Thanksgiving", tag: "🦃 Fourth Thursday of November", headline: "Thanksgiving: Wishes, Dinner Ideas & History",
        desc: "Gratitude wishes, family dinner ideas and the story behind the holiday — everything to plan a warm, low-stress Thanksgiving table.",
        meta: ["🦃 November", "📖 6 min read", "🍂 Start here"], link: "articles/thanksgiving-wishes-2026.html",
        links: [
          ["💌", "Wishes & Messages", "articles/thanksgiving-wishes-2026.html"],
          ["🙏", "Gratitude Messages", "articles/thanksgiving-messages-2026.html"],
          ["💬", "Quotes", "articles/thanksgiving-quotes-2026.html"],
          ["🍽️", "Dinner Ideas", "articles/thanksgiving-dinner-ideas.html"]] },
      fx: "leaves", fxColors: ["#b45309", "#92400e", "#a16207", "#78350f"],
      catHero: { "default": "thanksgiving-messages-2026.jpg", holidays: "thanksgiving-dinner-ideas.jpg",
        seasonal: "thanksgiving-quotes-2026.jpg" }
    },
    christmas: {
      accent: "#e63946", accentSoft: "rgba(230,57,70,.38)", glow: "rgba(230,57,70,.16)",
      image: "christmas-decoration-ideas-2026.jpg",
      alt: "Beautiful Christmas decorations with glowing tree and ornaments",
      chip: { emoji: "🎄", text: "Christmas Decoration Ideas 2026", href: "articles/christmas-decoration-ideas-2026.html" },
      featured: { title: "Christmas", tag: "🎄 December 25 · Thursday", headline: "Christmas 2026: Dates, Traditions & Celebration Ideas",
        desc: "When is Christmas, how do traditions differ around the world, and how do you plan a calm, joyful celebration? Wishes, decor, recipes and gift ideas.",
        meta: ["📅 Dec 25", "📖 8 min read", "🎄 Start here"], link: "articles/when-is-christmas-2026.html",
        links: [
          ["💌", "Wishes for Family", "articles/christmas-wishes-for-family-2026.html"],
          ["🎬", "Best Christmas Movies", "articles/best-christmas-movies.html"],
          ["🍪", "Recipes & Food Ideas", "articles/christmas-recipes-and-food-ideas.html"],
          ["🎁", "Gift Ideas 2026", "articles/christmas-gift-ideas-2026.html"]] },
      fx: "snow", fxColors: ["#ffffff", "#f1f5f9", "#e2e8f0"],
      catHero: { "default": "christmas-images-2026.jpg", holidays: "merry-christmas-wishes-2026.jpg",
        shopping: "christmas-gift-ideas-2026.jpg", seasonal: "best-christmas-movies.jpg",
        festivals: "christmas-party-ideas-2026.jpg" }
    },
    newyear: {
      accent: "#e8c766", accentSoft: "rgba(232,199,102,.40)", glow: "rgba(232,199,102,.18)",
      image: "new-year-images-2027.jpg",
      alt: "Sparkling New Year celebration with fireworks and lights",
      chip: { emoji: "🥂", text: "New Year Wishes & Messages 2027", href: "articles/new-year-wishes-for-friends-and-family.html" },
      featured: { title: "New Year", tag: "🥂 January 1 · New beginnings", headline: "New Year 2027: Wishes, Quotes & Party Ideas",
        desc: "Fresh-start wishes, inspirational quotes, party ideas and resolutions — everything to welcome the new year with the people who matter.",
        meta: ["📅 Jan 1", "📖 6 min read", "✨ Start here"], link: "articles/new-year-wishes-for-friends-and-family.html",
        links: [
          ["💬", "New Year Quotes", "articles/new-year-quotes-2027.html"],
          ["😄", "Funny Wishes", "articles/funny-new-year-wishes.html"],
          ["🎉", "Party Ideas", "articles/new-year-party-ideas-2027.html"],
          ["🎯", "Resolutions", "articles/new-year-resolutions-ideas.html"]] },
      fx: "sparks", fxColors: ["#e8c766", "#f3d47a", "#fff7d6"],
      catHero: { "default": "new-year-party-ideas-2027.jpg", holidays: "happy-new-year-2027-wishes.jpg",
        seasonal: "new-year-quotes-2027.jpg" }
    },
    valentine: {
      accent: "#e6397a", accentSoft: "rgba(230,57,122,.38)", glow: "rgba(230,57,122,.16)",
      image: "romantic-valentines-day-wishes.jpg",
      alt: "Romantic Valentine's Day roses and soft lights",
      chip: { emoji: "💝", text: "Romantic Valentine's Wishes", href: "articles/romantic-valentines-day-wishes.html" },
      featured: { title: "Valentine's Day", tag: "💝 February 14", headline: "Valentine's Day: Wishes, Quotes & Date Ideas",
        desc: "Romantic wishes, heartfelt quotes, gift ideas and date plans — from grand gestures to quiet evenings at home.",
        meta: ["📅 Feb 14", "📖 6 min read", "💝 Start here"], link: "articles/valentines-day-2027-date-wishes.html",
        links: [
          ["💌", "Romantic Wishes", "articles/romantic-valentines-day-wishes.html"],
          ["💬", "Valentine's Quotes", "articles/valentines-day-quotes.html"],
          ["🎁", "Gift Ideas", "articles/valentines-day-gift-ideas.html"],
          ["🌹", "Date Ideas", "articles/valentines-day-date-ideas.html"]] },
      fx: "petals", fxColors: ["#f9a8d4", "#f472b6", "#fbcfe8", "#e6397a"],
      catHero: { "default": "valentines-day-gift-ideas.jpg", holidays: "valentines-day-2027-date-wishes.jpg",
        shopping: "valentines-day-gift-ideas.jpg" }
    },
    eidFitr: {
      accent: "#10b981", accentSoft: "rgba(16,185,129,.38)", glow: "rgba(16,185,129,.16)",
      image: "eid-mubarak-images-2027.jpg",
      alt: "Eid Mubarak greeting with crescent moon and lanterns",
      chip: { emoji: "🌙", text: "Eid Mubarak Wishes 2027", href: "articles/eid-mubarak-wishes-2027.html" },
      featured: { title: "Eid al-Fitr", tag: "🌙 End of Ramadan", headline: "Eid al-Fitr: Dates, Wishes & Celebration Guide",
        desc: "When is Eid al-Fitr, what does it celebrate, and how do families mark the end of Ramadan? Dates, greetings, recipes and respectful explainers.",
        meta: ["🌙 Shawwal 1", "📖 7 min read", "✨ Start here"], link: "articles/eid-mubarak-wishes-2027.html",
        links: [
          ["🌙", "Eid Mubarak Wishes", "articles/eid-mubarak-wishes-2027.html"],
          ["📅", "Eid al-Fitr Date", "articles/eid-al-fitr-2027-date.html"],
          ["🖼️", "Eid Mubarak Images", "articles/eid-mubarak-images-2027.html"],
          ["🤲", "Ramadan Duas", "articles/ramadan-duas-sehri-iftar.html"]] },
      fx: "sparks", fxColors: ["#f5b942", "#10b981", "#f3d47a"],
      catHero: { "default": "eid-mubarak-wishes-2027.jpg", holidays: "eid-recipes-and-sweets.jpg",
        festivals: "eid-mehndi-designs-2027.jpg" }
    },
    holi: {
      accent: "#ec4899", accentSoft: "rgba(236,72,153,.38)", glow: "rgba(236,72,153,.16)",
      image: null, // no suitable existing image — colors + decoration still apply
      alt: "",
      chip: { emoji: "🎨", text: "Festival Guides", href: "categories/festivals.html" },
      featured: { title: "Holi", tag: "🎨 Festival of Colors", headline: "Holi: the Festival of Colors",
        desc: "Holi celebrates spring, color and togetherness. Explore our festival guides for dates, wishes, party ideas and celebration explainers.",
        meta: ["🎨 Spring", "📖 Guides", "✨ Explore"], link: "categories/festivals.html",
        links: [
          ["🎪", "All Festivals", "categories/festivals.html"],
          ["🎉", "Party Ideas", "articles/how-to-plan-a-party.html"],
          ["💌", "Wishes Collection", "categories/holidays.html"],
          ["📅", "Seasonal Events", "categories/seasonal-events.html"]] },
      fx: "powder", fxColors: ["#ec4899", "#facc15", "#4ade80", "#60a5fa", "#f97316"],
      catHero: {}
    },
    pakistanDay: {
      accent: "#0a9b4d", accentSoft: "rgba(10,155,77,.40)", glow: "rgba(10,155,77,.18)",
      image: "pakistan-day-23-march.jpg",
      alt: "Pakistan Day celebration with national flag colors",
      chip: { emoji: "🇵🇰", text: "Pakistan Day Wishes & Messages", href: "articles/pakistan-day-wishes-and-messages.html" },
      featured: { title: "Pakistan Day", tag: "🇵🇰 23 March · Lahore Resolution", headline: "Pakistan Day — 23 March: History, Wishes & Messages",
        desc: "Commemorating the Lahore Resolution of 1940 — history, parade traditions, wishes, slogans and classroom-friendly explainers.",
        meta: ["📅 Mar 23", "📖 6 min read", "🇵🇰 Start here"], link: "articles/pakistan-day-wishes-and-messages.html",
        links: [
          ["💌", "Wishes & Messages", "articles/pakistan-day-wishes-and-messages.html"],
          ["📜", "Quotes & Slogans", "articles/pakistan-day-quotes-and-slogans.html"],
          ["🎤", "Speech in English", "articles/pakistan-day-speech-in-english.html"],
          ["📅", "23 March Guide", "articles/pakistan-day-23-march.html"]] },
      fx: "sparks", fxColors: ["#0a9b4d", "#ffffff", "#f5b942"],
      catHero: { "default": "pakistan-day-wishes-and-messages.jpg", "national-days": "pakistan-day-23-march.jpg",
        holidays: "pakistan-day-wishes-and-messages.jpg" }
    },
    easter: {
      accent: "#7fb6d9", accentSoft: "rgba(127,182,217,.40)", glow: "rgba(127,182,217,.18)",
      image: null, // no suitable existing image — colors + decoration still apply
      alt: "",
      chip: { emoji: "🐣", text: "Festival Guides", href: "categories/festivals.html" },
      featured: { title: "Easter", tag: "🐣 Spring celebration", headline: "Easter: Spring Celebration Guides",
        desc: "Easter marks spring and new beginnings. Browse our festival guides for dates, wishes, family ideas and celebration explainers.",
        meta: ["🐣 Spring", "📖 Guides", "✨ Explore"], link: "categories/festivals.html",
        links: [
          ["🎪", "All Festivals", "categories/festivals.html"],
          ["🌸", "Seasonal Events", "categories/seasonal-events.html"],
          ["💌", "Wishes Collection", "categories/holidays.html"],
          ["🎉", "Party Ideas", "articles/how-to-plan-a-party.html"]] },
      fx: "petals", fxColors: ["#fbcfe8", "#fef3c7", "#dbeafe", "#e9d5ff"],
      catHero: {}
    },
    eidAdha: {
      accent: "#10b981", accentSoft: "rgba(16,185,129,.38)", glow: "rgba(16,185,129,.16)",
      image: "eid-mubarak-wishes-2027.jpg",
      alt: "Eid greeting with crescent and warm lights",
      chip: { emoji: "🌙", text: "Eid Mubarak Wishes", href: "articles/eid-mubarak-wishes-2027.html" },
      featured: { title: "Eid al-Adha", tag: "🌙 Festival of Sacrifice", headline: "Eid al-Adha: Dates, Wishes & Celebration Guide",
        desc: "The Festival of Sacrifice — dates, greetings, family traditions and respectful explainers for Eid al-Adha.",
        meta: ["🌙 Dhul-Hijjah 10", "📖 6 min read", "✨ Start here"], link: "articles/eid-mubarak-wishes-2027.html",
        links: [
          ["🌙", "Eid Mubarak Wishes", "articles/eid-mubarak-wishes-2027.html"],
          ["🖼️", "Eid Mubarak Images", "articles/eid-mubarak-images-2027.html"],
          ["🤲", "Ramadan & Eid Duas", "articles/ramadan-duas-sehri-iftar.html"],
          ["🎪", "All Festivals", "categories/festivals.html"]] },
      fx: "sparks", fxColors: ["#f5b942", "#10b981", "#f3d47a"],
      catHero: { "default": "eid-mubarak-images-2027.jpg" }
    },
    independenceDay: {
      accent: "#0a9b4d", accentSoft: "rgba(10,155,77,.40)", glow: "rgba(10,155,77,.18)",
      image: null, // no suitable existing image — colors + decoration still apply
      alt: "",
      chip: { emoji: "🇵🇰", text: "National Days", href: "categories/national-days.html" },
      featured: { title: "Independence Day", tag: "🇵🇰 14 August", headline: "Independence Day — 14 August",
        desc: "Independence in 1947 — flag-hoisting, anthems, wishes, speeches and respectful celebration ideas. Full guides publish as the date approaches.",
        meta: ["📅 Aug 14", "📖 Guides", "🇵🇰 Explore"], link: "categories/national-days.html",
        links: [
          ["🇵🇰", "National Days Hub", "categories/national-days.html"],
          ["📅", "Seasonal Events", "categories/seasonal-events.html"],
          ["💌", "Wishes Collection", "categories/holidays.html"],
          ["🎪", "All Festivals", "categories/festivals.html"]] },
      fx: "sparks", fxColors: ["#0a9b4d", "#ffffff", "#f5b942"],
      catHero: {}
    }
  };

  /* ---------- pick nearest event ---------- */
  function pickEvent(now) {
    var today = stripTime(now), best = null;
    EVENTS.forEach(function (ev) {
      var y = today.getFullYear();
      var d = stripTime(ev.date(y));
      var lingered = false, daysPast = 0;
      if (d.getTime() < today.getTime()) {
        var last = d;
        d = stripTime(ev.date(y + 1));
        daysPast = (today.getTime() - last.getTime()) / 86400000;
        if (daysPast <= 5) lingered = true;
      }
      var days = Math.round((d.getTime() - today.getTime()) / 86400000);
      // A just-passed event (≤5 days) keeps its decor briefly, but yields to an
      // event arriving within ~2 days: lingered events score as 2.5 days away.
      var score = lingered ? 2.5 : days;
      var tie = lingered ? daysPast : days;
      if (!best || score < best.score || (score === best.score && tie < best.tie)) {
        best = { ev: ev, date: d, days: days, lingered: lingered, score: score, tie: tie };
      }
    });
    if (!best || best.score > 45) return null; // neutral default beyond ~45 days
    return best;
  }

  /* ---------- official-style flag renders (inline SVG, generated) ---------- */
  function starPoints(cx, cy, r, rot) {
    var pts = [], i, rr, a;
    for (i = 0; i < 10; i++) {
      rr = (i % 2) ? r * 0.382 : r;
      a = rot + i * Math.PI / 5 - Math.PI / 2;
      pts.push((cx + rr * Math.cos(a)).toFixed(2) + "," + (cy + rr * Math.sin(a)).toFixed(2));
    }
    return pts.join(" ");
  }
  function flagSVG(code) {
    var open = '<svg viewBox="__VB__" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">';
    if (code === "PK") { // Pakistan 3:2 — green field, white hoist stripe, crescent + star
      return open.replace("__VB__", "0 0 120 80") +
        '<rect width="120" height="80" fill="#01411C"/>' +
        '<rect width="30" height="80" fill="#ffffff"/>' +
        '<path fill="#ffffff" fill-rule="evenodd" d="M72,40 m-17,0 a17,17 0 1,0 34,0 a17,17 0 1,0 -34,0 M79,40 m-14,0 a14,14 0 1,1 28,0 a14,14 0 1,1 -28,0"/>' +
        '<polygon fill="#ffffff" points="' + starPoints(80, 31, 6.4, -0.26) + '"/></svg>';
    }
    if (code === "IN") { // India 3:2 — saffron/white/green + navy chakra
      var spokes = "", i, a, x2, y2;
      for (i = 0; i < 24; i++) {
        a = i * Math.PI / 12;
        x2 = 60 + 9.4 * Math.cos(a); y2 = 40 + 9.4 * Math.sin(a);
        spokes += '<line x1="60" y1="40" x2="' + x2.toFixed(2) + '" y2="' + y2.toFixed(2) + '" stroke="#06038D" stroke-width="1.1"/>';
      }
      return open.replace("__VB__", "0 0 120 80") +
        '<rect width="120" height="80" fill="#FF9933"/><rect y="26.67" width="120" height="26.67" fill="#ffffff"/><rect y="53.33" width="120" height="26.67" fill="#138808"/>' +
        '<circle cx="60" cy="40" r="10.5" fill="none" stroke="#06038D" stroke-width="1.6"/>' + spokes +
        '<circle cx="60" cy="40" r="1.8" fill="#06038D"/></svg>';
    }
    if (code === "US") { // USA 19:10 — 13 stripes, canton, 50 stars
      var W = 190, H = 100, sh = H / 13, s = "", r, c, rows = [6,5,6,5,6,5,6,5,6], y, x;
      for (r = 0; r < 13; r++) s += '<rect y="' + (r * sh).toFixed(2) + '" width="' + W + '" height="' + (sh + 0.4).toFixed(2) + '" fill="' + (r % 2 ? "#ffffff" : "#B31942") + '"/>';
      var cw = W * 0.4, ch = sh * 7;
      s += '<rect width="' + cw.toFixed(2) + '" height="' + ch.toFixed(2) + '" fill="#0A3161"/>';
      for (r = 0; r < 9; r++) {
        y = ch * (r + 0.5) / 9;
        var n = rows[r], off = (n === 5) ? cw / 12 : 0;
        for (c = 0; c < n; c++) {
          x = cw * (c + 0.5) / 6 + off;
          s += '<polygon fill="#ffffff" points="' + starPoints(x, y, 3.4, 0) + '"/>';
        }
      }
      return open.replace("__VB__", "0 0 190 100") + s + "</svg>";
    }
    return "";
  }

  /* ---------- apply ---------- */
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var now = new Date();
  var pick = pickEvent(now);
  var root = document.documentElement;
  var path = location.pathname.toLowerCase();
  var pageKey = "index";
  if (path.indexOf("/categories/") > -1) {
    var m = path.match(/\/categories\/([a-z-]+)\.html/);
    if (m) pageKey = m[1] === "shopping-events" ? "shopping" : (m[1] === "seasonal-events" ? "seasonal" : (m[1] === "national-days" ? "national-days" : m[1]));
  }
  if (!pick) { root.setAttribute("data-theme", "default"); return; }

  var ev = pick.ev, theme = THEMES[ev.key], d = pick.date;
  root.setAttribute("data-theme", ev.key);
  root.style.setProperty("--theme-accent", theme.accent);
  root.style.setProperty("--theme-accent-soft", theme.accentSoft);
  root.style.setProperty("--theme-glow", theme.glow);

  var dateLong = DAYS[d.getDay()] + ", " + MONTHS_L[d.getMonth()] + " " + d.getDate();
  var dateShort = MONTHS[d.getMonth()] + " " + d.getDate();
  function isoLocal(dt) { return dt.getFullYear() + "-" + pad(dt.getMonth() + 1) + "-" + pad(dt.getDate()) + "T00:00:00"; }

  /* ----- homepage: hero card + countdown + chip + featured panel ----- */
  if (pageKey === "index") {
    if (theme.image) {
      var heroImg = document.querySelector(".hero-card-main img");
      if (heroImg) { heroImg.src = IMG + theme.image; heroImg.alt = theme.alt; }
      var cap = document.querySelector(".hero-card-main figcaption");
      if (cap) cap.textContent = ev.emoji + " " + ev.label + " " + d.getFullYear() + " · " + dateLong;
    }
    var hcb = document.querySelector(".hero-count-badge .hcb-label");
    if (hcb) hcb.textContent = ev.label + " in";
    document.querySelectorAll(".hero-count-badge [data-countdown], .featured-body [data-countdown]").forEach(function (cd) {
      cd.setAttribute("data-countdown", isoLocal(d));
    });
    var chip = document.querySelector(".hero-chip");
    if (chip) {
      chip.href = theme.chip.href;
      var cs = chip.querySelector("span");
      if (cs) cs.textContent = theme.chip.emoji + " " + theme.chip.text;
    }
    var feat = document.querySelector(".featured-card");
    if (feat && theme.featured) {
      var f = theme.featured;
      var fh = document.getElementById("featured-heading");
      if (fh) fh.textContent = f.title + " " + d.getFullYear();
      var tag = feat.querySelector(".featured-body .tag");
      if (tag) tag.textContent = f.tag;
      var h3 = feat.querySelector(".featured-body h3");
      if (h3) h3.textContent = f.headline;
      var fp = feat.querySelector(".featured-body p");
      if (fp) fp.textContent = f.desc;
      var meta = feat.querySelector(".featured-meta");
      if (meta) meta.innerHTML = f.meta.map(function (t) { return "<span>" + esc(t) + "</span>"; }).join("");
      var cta = feat.querySelector(".featured-body .btn-primary");
      if (cta) cta.href = f.link;
      var mini = feat.querySelector(".mini-list");
      if (mini && f.links) {
        mini.innerHTML = f.links.map(function (l) {
          return '<a href="' + esc(l[2]) + '"><span>' + esc(l[0]) + " " + esc(l[1]) + '</span><span>→</span></a>';
        }).join("");
      }
    }
  }

  /* ----- category pages: themed banner with slow Ken Burns zoom ----- */
  var pageHero = document.querySelector(".page-hero");
  if (pageHero && pageKey !== "index") {
    var bannerImg = (theme.catHero && (theme.catHero[pageKey] || theme.catHero["default"])) || theme.image;
    if (bannerImg) {
      var fig = document.createElement("figure");
      fig.className = "theme-banner";
      fig.innerHTML = '<img src="' + IMG + bannerImg + '" alt="' + esc(theme.alt || (ev.label + " celebration")) + '" loading="lazy" decoding="async">' +
        '<figcaption><span class="theme-chip">' + ev.emoji + " " + esc(ev.label) + " · " + esc(dateShort) + "</span></figcaption>";
      pageHero.insertBefore(fig, pageHero.firstChild);
    }
    /* auto-matching country flag on the National Days page */
    if (pageKey === "national-days" && ev.flag) {
      var h1 = pageHero.querySelector("h1");
      if (h1 && h1.innerHTML.indexOf("🏳️") > -1) {
        h1.innerHTML = h1.innerHTML.replace("🏳️",
          '<span class="theme-flag" role="img" aria-label="' + esc(COUNTRIES[ev.flag] || ev.flag) + ' flag">' + flagSVG(ev.flag) + "</span>");
      }
    }
  }

  /* ----- subtle animated decoration layer (CSS-only motion) ----- */
  if (!reduced && theme.fx) {
    var layer = document.createElement("div");
    layer.className = "theme-fx fx-" + theme.fx;
    layer.setAttribute("aria-hidden", "true");
    var N = 14, html = "", i, left, dur, delay, size, col;
    for (i = 0; i < N; i++) {
      left = (Math.random() * 100).toFixed(2);
      dur = (9 + Math.random() * 9).toFixed(2);
      delay = (-Math.random() * 14).toFixed(2);
      size = (4 + Math.random() * 6).toFixed(1);
      col = theme.fxColors[i % theme.fxColors.length];
      html += '<span class="fxp" style="left:' + left + "%;width:" + size + "px;height:" + size +
        "px;background:" + col + ";animation-duration:" + dur + "s;animation-delay:" + delay + 's"></span>';
    }
    layer.innerHTML = html;
    document.body.appendChild(layer);
  }
})();
