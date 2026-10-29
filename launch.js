// Launch page motion: the wordmark draw-on, the rotating headline word and the
// feature showcase. Everything is readable without it.
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ease = "cubic-bezier(0.45, 0, 0.55, 1)";

  // Draw the M once, then fade in "ima": 500ms in all.
  var m = document.querySelector(".wordmark-m");
  var ima = document.querySelector(".wordmark-ima");
  if (m && ima) {
    if (reduce || !m.animate) {
      m.style.strokeDashoffset = 0;
      ima.style.opacity = 1;
    } else {
      m.animate([{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 350, easing: ease, fill: "forwards" })
        .finished.then(function () {
          ima.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150, easing: "ease-out", fill: "forwards" });
        });
    }
  }

  // "none of the algorithms. / drama. / ads. …" keeps cycling. The word's box
  // glides to each new width so the rest of the line slides rather than
  // jumps. Only words that keep the heading on its current lines take part
  // ("missed conversations." usually sits out), and the heading height is
  // locked. It holds while the tab is hidden.
  var swap = document.querySelector(".swap");
  if (swap && !reduce) {
    var all = swap.getAttribute("data-words").split("|");
    var h1 = swap.closest("h1");
    var meas = document.createElement("span");
    meas.className = "swap";
    meas.setAttribute("aria-hidden", "true");
    meas.style.cssText = "position:absolute;visibility:hidden;width:auto;left:0;top:0";
    h1.appendChild(meas);
    var widthOf = function (word) {
      meas.textContent = word;
      return meas.getBoundingClientRect().width;
    };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
      var base = h1.offsetHeight;
      var words = all.filter(function (word, i) {
        if (i > 0 && word === all[0]) return false;
        swap.textContent = word;
        return h1.offsetHeight === base;
      });
      swap.textContent = all[0];
      h1.style.minHeight = base + "px";
      if (words.length < 2) return;
      swap.style.width = widthOf(all[0]) + "px";
      swap.classList.add("sizing");
      var w = 0;
      var next = function () {
        if (document.hidden) { setTimeout(next, 1000); return; }
        w = (w + 1) % words.length;
        swap.classList.add("out");
        swap.style.width = widthOf(words[w]) + "px";
        setTimeout(function () {
          swap.textContent = words[w];
          swap.classList.remove("out");
          setTimeout(next, w === 0 ? 2600 : 1600);
        }, 350);
      };
      setTimeout(next, 1100);
    });
  }

  // Feature tabs drive the app window; they auto-advance until the visitor
  // takes over (hover, focus or a click).
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".feature"));
  var shots = Array.prototype.slice.call(document.querySelectorAll("#shot > [data-shot]"));
  var dots = Array.prototype.slice.call(document.querySelectorAll(".dots span"));
  var panel = document.getElementById("shot");
  if (!tabs.length) return;
  var current = 0;
  var timer = null;
  var paused = false;

  function select(i, focus) {
    current = (i + tabs.length) % tabs.length;
    tabs.forEach(function (t, n) {
      var on = n === current;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      if (dots[n]) dots[n].classList.toggle("on", on);
    });
    var key = tabs[current].getAttribute("data-shot");
    shots.forEach(function (img) { img.classList.toggle("on", img.getAttribute("data-shot") === key); });
    panel.setAttribute("aria-labelledby", tabs[current].id);
    if (focus) tabs[current].focus();
    composeScene(key === "compose");
  }

  // Compose: the same board, zooming into the composer while the words type
  // in, then back out to the whole board.
  var zoomWrap = document.querySelector("#shot .zoom-wrap");
  var typing = zoomWrap && zoomWrap.querySelector(".typing");
  var typed = typing && typing.querySelector(".typed");
  var phrase = "Big news: our garden map is live!";
  var sceneTimers = [];
  var typeTimer = null;
  function later(fn, ms) { sceneTimers.push(setTimeout(fn, ms)); }
  function composeScene(on) {
    sceneTimers.forEach(clearTimeout);
    sceneTimers = [];
    clearInterval(typeTimer);
    if (!zoomWrap) return;
    zoomWrap.classList.remove("zoom");
    typing.classList.remove("on");
    typed.textContent = "";
    if (!on) return;
    if (reduce) { typed.textContent = phrase; typing.classList.add("on"); return; }
    later(function () { zoomWrap.classList.add("zoom"); }, 400);
    later(function () {
      typing.classList.add("on");
      var i = 0;
      typeTimer = setInterval(function () {
        i += 1;
        typed.textContent = phrase.slice(0, i);
        if (i >= phrase.length) clearInterval(typeTimer);
      }, 45);
    }, 1400);
    later(function () { zoomWrap.classList.remove("zoom"); }, 4300);
  }

  function start() {
    if (reduce || timer) return;
    timer = setInterval(function () { if (!paused && !document.hidden) select(current + 1); }, 6000);
  }
  var pauseBtn = document.querySelector(".pause");
  function stop() {
    clearInterval(timer);
    timer = null;
    if (pauseBtn) { pauseBtn.setAttribute("aria-pressed", "true"); pauseBtn.setAttribute("aria-label", "Play the feature tour"); }
  }
  if (pauseBtn) {
    if (reduce) pauseBtn.hidden = true;
    pauseBtn.addEventListener("click", function () {
      if (timer) { stop(); return; }
      pauseBtn.setAttribute("aria-pressed", "false");
      pauseBtn.setAttribute("aria-label", "Pause the feature tour");
      select(current + 1);
      start();
    });
  }

  tabs.forEach(function (t, n) {
    t.addEventListener("click", function () { stop(); select(n); });
    t.addEventListener("keydown", function (e) {
      var k = e.key;
      if (k === "ArrowDown" || k === "ArrowRight") { e.preventDefault(); stop(); select(current + 1, true); }
      if (k === "ArrowUp" || k === "ArrowLeft") { e.preventDefault(); stop(); select(current - 1, true); }
      if (k === "Home") { e.preventDefault(); stop(); select(0, true); }
      if (k === "End") { e.preventDefault(); stop(); select(tabs.length - 1, true); }
    });
  });
  var showcase = document.querySelector(".showcase");
  showcase.addEventListener("mouseenter", function () { paused = true; });
  showcase.addEventListener("mouseleave", function () { paused = false; });
  showcase.addEventListener("focusin", function () { paused = true; });
  showcase.addEventListener("focusout", function () { paused = false; });
  // #tour-compose / #tour-conversations open the tour on that tab (for links
  // and previews).
  var hashTab = location.hash.indexOf("#tour-") === 0 ? location.hash.slice(6) : "";
  var hashIndex = tabs.map(function (t) { return t.getAttribute("data-shot"); }).indexOf(hashTab);
  if (hashIndex > 0) { select(hashIndex); stop(); } else start();
})();

// The catch-up timeline scrolls on its own; it pauses on hover, on focus and
// with its button, and stays still under reduced motion.
(function () {
  "use strict";
  var win = document.querySelector(".scroller-win");
  var btn = win && win.querySelector(".scroll-pause");
  if (!win || !btn) return;
  var held = false;
  function apply(paused) { win.classList.toggle("paused", paused); }
  btn.addEventListener("click", function () {
    held = !held;
    btn.setAttribute("aria-pressed", held ? "true" : "false");
    btn.setAttribute("aria-label", held ? "Play the scrolling timeline" : "Pause the scrolling timeline");
    apply(held);
  });
  win.addEventListener("mouseenter", function () { apply(true); });
  win.addEventListener("mouseleave", function () { apply(held); });
})();

// Doodles: every few seconds a brand squiggle draws itself somewhere in the
// hero margins, lingers, then fades. Decorative only; skipped under reduced
// motion and while the tab is hidden.
(function () {
  "use strict";
  var layer = document.querySelector(".doodles");
  if (!layer || !layer.animate || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var shapes = { SimpleHoop: [158, 51], MLoop: [94, 128], DoubleLoop: [201, 122], BounceIn: [191, 97], Repeat: [278, 58], Upset: [178, 169] };
  var names = Object.keys(shapes);
  var colours = ["#c6a3e0", "#b188d2", "#ff7ab0", "#dabfeb"];
  var NS = "http://www.w3.org/2000/svg";
  var live = 0;
  // Outer edges of the headline area only (x as a fraction of the width, y in
  // px from the top), clear of the logo, headline, button and showcase.
  var spots = [[0.03, 160], [0.05, 330], [0.86, 60], [0.88, 250], [0.84, 400], [0.72, 6]];
  function draw() {
    if (document.hidden || live >= 2) return;
    var name = names[Math.floor(Math.random() * names.length)];
    var size = shapes[name];
    var spot = spots[Math.floor(Math.random() * spots.length)];
    if (window.innerWidth < 900) return;
    var w = 100 + Math.random() * 50;
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "doodle");
    svg.setAttribute("viewBox", "-10 -10 " + (size[0] + 20) + " " + (size[1] + 20));
    svg.style.width = w + "px";
    svg.style.left = (spot[0] * 100) + "%";
    svg.style.top = spot[1] + "px";
    svg.style.stroke = colours[Math.floor(Math.random() * colours.length)];
    svg.style.transform = "rotate(" + Math.round(Math.random() * 50 - 25) + "deg)";
    var use = document.createElementNS(NS, "use");
    use.setAttribute("href", "#sq-" + name);
    svg.appendChild(use);
    layer.appendChild(svg);
    live += 1;
    var drawOn = svg.animate([{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 1400, easing: "cubic-bezier(0.45, 0, 0.55, 1)", fill: "forwards" });
    drawOn.finished.then(function () {
      return svg.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 900, delay: 2600, easing: "ease-in", fill: "forwards" }).finished;
    }).then(function () { svg.remove(); live -= 1; });
  }
  setTimeout(draw, 1800);
  setInterval(draw, 4200);
})();

// Count Download clicks (intent, not completed downloads) in Google Analytics and
// in the desktop app's PostHog project, where they're compared with first app
// launches as a cohort funnel (mima-social/site#16). PostHog gets a bare beacon,
// no library: an anonymous one-off id, no cookies, no person profile.
(function () {
  "use strict";
  var POSTHOG_KEY = "phc_ArqsTR3VWXKrFuV3Pv3uV69QuvHAS2xwWjFqDYyVEdE9";
  var POSTHOG_URL = "https://eu.i.posthog.com/i/v0/e/";
  var UTM = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];

  function anonId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  function sendToPostHog(event, link, placement) {
    if (!navigator.sendBeacon) return;
    var params = new URLSearchParams(location.search);
    var props = {
      $process_person_profile: false,
      $current_url: location.href,
      $referrer: document.referrer || "$direct",
      platform: "mac",
      arch: "arm64",
      channel: "beta",
      release: "latest",
      placement: placement,
      link_url: link.href
    };
    UTM.forEach(function (key) { if (params.get(key)) props[key] = params.get(key); });
    // A text/plain body keeps this a simple request (no CORS preflight); PostHog parses it as JSON.
    navigator.sendBeacon(POSTHOG_URL, JSON.stringify({
      api_key: POSTHOG_KEY,
      event: event,
      distinct_id: anonId(),
      timestamp: new Date().toISOString(),
      properties: props
    }));
  }

  function track(event, link, placement) {
    try { sendToPostHog(event, link, placement); } catch (e) { /* never block the download */ }
    if (typeof window.gtag === "function") {
      window.gtag("event", event === "download_clicked" ? "download_click" : event, {
        link_url: link.href,
        placement: placement,
        transport_type: "beacon"
      });
    }
  }

  // Phones and tablets can't run the Mac app, so Download opens a sheet that
  // emails them the link instead (#12).
  var sheet = document.getElementById("desktop-sheet");
  var touch = window.matchMedia && matchMedia("(hover: none) and (pointer: coarse)");
  var useSheet = !!(sheet && typeof sheet.showModal === "function" && touch);
  var sheetLink = null;
  var sheetPlacement = "hero";

  Array.prototype.forEach.call(document.querySelectorAll("[data-download]"), function (link) {
    link.addEventListener("click", function (e) {
      var placement = link.closest(".band") ? "closing_band" : "hero";
      if (useSheet && touch.matches) {
        e.preventDefault();
        sheetLink = link;
        sheetPlacement = placement;
        sheet.showModal();
        return;
      }
      track("download_clicked", link, placement);
    });
  });

  if (!useSheet) return;
  // Ticking "send me updates" subscribes through the same Loops form as the
  // landing-page signup, so Loops sends a confirmation email (double opt-in)
  // before anyone joins the list. A stranger's address can't be signed up.
  var LOOPS_FORM = "https://app.loops.so/api/newsletter-form/cmqbfegi407730j0m5jakbstp";
  var UPDATES_LIST = "cmqydyxrc4l7d0jy7drbq25ig";
  var SHEET_SOURCE = "Mobile download sheet at mima.social 2026.q4";
  var form = document.getElementById("sheet-form");
  var input = document.getElementById("sheet-email");
  var updates = document.getElementById("sheet-updates");
  var error = document.getElementById("sheet-error");
  var done = document.getElementById("sheet-done");
  var submit = form.querySelector("button.join");

  sheet.querySelector("[data-close]").addEventListener("click", function () { sheet.close(); });
  // Tapping the dimmed backdrop closes the sheet too.
  sheet.addEventListener("click", function (e) { if (e.target === sheet) sheet.close(); });
  input.addEventListener("input", function () { error.textContent = ""; input.removeAttribute("aria-invalid"); });

  function fail(msg) {
    error.textContent = msg;
    input.setAttribute("aria-invalid", "true");
    submit.disabled = false;
    submit.removeAttribute("aria-busy");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = input.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { fail("Enter a valid email address."); input.focus(); return; }
    submit.disabled = true;
    submit.setAttribute("aria-busy", "true");
    fetch("/api/email-download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, website: form.elements.website.value })
    })
      .then(function (res) { return res.json().catch(function () { return {}; }).then(function (data) { return { ok: res.ok, data: data, status: res.status }; }); })
      .then(function (r) {
        if (r.ok && r.data.ok) {
          track("download_link_emailed", sheetLink, sheetPlacement);
          if (updates.checked && !form.elements.website.value) {
            fetch(LOOPS_FORM, {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: "email=" + encodeURIComponent(email) +
                "&source=" + encodeURIComponent(SHEET_SOURCE) +
                "&mailingLists=" + encodeURIComponent(UPDATES_LIST),
              keepalive: true
            }).catch(function () { /* the download email already went; updates are optional */ });
            done.querySelector(".sent-confirm").hidden = false;
          }
          sheet.classList.add("is-done");
          done.focus();
        } else {
          fail(r.status === 429 ? "Too many requests. Try again in a minute." : (r.data.error || "Something went wrong. Please try again."));
        }
      })
      .catch(function () { fail("Couldn’t reach the server. Check your connection and try again."); });
  });
})();
