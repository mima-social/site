(function () {
  "use strict";
  // Loops newsletter form endpoint. Responds with JSON, so we submit via fetch
  // (not a native form POST) and parse the result.
  var ENDPOINT = "https://app.loops.so/api/newsletter-form/cmqbfegi407730j0m5jakbstp";
  // Single localStorage key used purely as a rate-limit guard against rapid
  // duplicate submits. No analytics, no tracking — this is the only thing stored.
  var RATE_KEY = "mima_beta_last_submit";
  var RATE_MS = 8000;

  var form = document.getElementById("beta-form");
  var emailInput = document.getElementById("email");
  var sourceInput = document.getElementById("q-source");
  var goalInput = document.getElementById("q-goal");
  var hiddenSource = document.getElementById("origin-source");
  var errorEl = document.getElementById("form-error");
  var retryBtn = document.getElementById("retry-btn");
  var card = document.getElementById("signup");
  var successEl = document.getElementById("success");
  var button = form.querySelector("button.join");

  function setError(msg) {
    errorEl.textContent = msg || "";
    if (msg) {
      emailInput.setAttribute("aria-invalid", "true");
      retryBtn.classList.add("show");
    } else {
      emailInput.removeAttribute("aria-invalid");
      retryBtn.classList.remove("show");
    }
  }

  function reEnable() {
    button.disabled = false;
    button.removeAttribute("aria-busy");
  }

  // The optional questions aren't on every page, so read them defensively.
  function optional(el) {
    return el ? el.value.trim() : "";
  }

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  // "Back and try again" affordance: clear the error and return focus to the form.
  retryBtn.addEventListener("click", function () {
    setError("");
    emailInput.focus();
  });

  // WebMCP: when an agent submits the form (declarative tool
  // "subscribe_to_mima_updates"), hand it the real outcome via respondWith.
  var agentReply = null;
  function reply(result) {
    if (agentReply) { agentReply(result); agentReply = null; }
    if (window.__mimaAgentReply) { window.__mimaAgentReply(result); window.__mimaAgentReply = null; }
  }

  // If the person cancels the agent's fill (or the form resets), drop any
  // pending reply so a later human submit doesn't resolve a stale call.
  if (document.modelContext && document.modelContext.addEventListener) {
    document.modelContext.addEventListener("toolcancel", function (e) {
      if (e.toolName === "subscribe_to_mima_updates") reply({ ok: false, error: "Cancelled by the user." });
    });
  }

  form.addEventListener("submit", function (e) {
    // preventDefault must come before respondWith (WebMCP declarative API).
    e.preventDefault();
    if (e.agentInvoked && typeof e.respondWith === "function") {
      e.respondWith(new Promise(function (resolve) { agentReply = resolve; }));
    }
    setError("");

    var email = emailInput.value.trim();
    if (!validEmail(email)) {
      setError("Enter a valid email address.");
      emailInput.focus();
      reply({ ok: false, error: "Enter a valid email address." });
      return;
    }

    // Guard against duplicate rapid submits.
    var now = Date.now();
    var last = parseInt(localStorage.getItem(RATE_KEY) || "0", 10);
    if (now - last < RATE_MS) {
      setError("Hang on a sec — you just submitted. Give it a moment and try again.");
      reply({ ok: false, error: "Submitted moments ago; try again in a few seconds." });
      return;
    }

    // Build an x-www-form-urlencoded body: &-joined key=value pairs, each value
    // URL-encoded exactly once. The optional fields go in even when empty.
    // The hidden source raw string is encoded here (not pre-encoded) to avoid
    // double-encoding its spaces.
    var body = [
      "email=" + encodeURIComponent(email),
      "signupSource=" + encodeURIComponent(optional(sourceInput)),
      "desiredUse=" + encodeURIComponent(optional(goalInput)),
      "source=" + encodeURIComponent(hiddenSource.value)
    ].join("&");

    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    localStorage.setItem(RATE_KEY, String(now));

    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body
    })
      .then(function (res) {
        if (res.status === 429) {
          var err429 = new Error("rate-limited");
          err429.rateLimited = true;
          throw err429;
        }
        return res.json()
          .catch(function () { return {}; })
          .then(function (json) { return { ok: res.ok, data: json }; });
      })
      .then(function (r) {
        if (r.ok && r.data && r.data.success) {
          card.classList.add("is-done");
          successEl.focus();
          reply({ ok: true, message: "Subscribed. Mima will email occasional updates to this address." });
        } else {
          // Allow an immediate retry after a real error.
          localStorage.removeItem(RATE_KEY);
          reEnable();
          var msg = (r.data && r.data.message) ? r.data.message : "Something went wrong. Please try again.";
          setError(msg);
          reply({ ok: false, error: msg });
        }
      })
      .catch(function (err) {
        localStorage.removeItem(RATE_KEY);
        reEnable();
        var msg = (err && err.rateLimited)
          ? "Too many signups, please try again in a little while."
          : "Couldn’t reach the signup server. Check your connection and try again.";
        setError(msg);
        reply({ ok: false, error: msg });
      });
  });

  emailInput.addEventListener("input", function () { setError(""); });
})();

// WebMCP imperative fallback. Browsers with the declarative API read the
// form's toolname/tooldescription attributes; some agent browsers only see
// tools registered from script. If WebMCP is present but our form tool isn't
// listed, register the same tool imperatively. It still waits for the person
// to press "Get updates" (no auto-submit), then returns the real outcome.
(function () {
  "use strict";
  var NAME = "subscribe_to_mima_updates";
  var form = document.getElementById("beta-form");
  var email = document.getElementById("email");
  var mc = document.modelContext || navigator.modelContext;
  if (!form || !email || !mc || typeof mc.registerTool !== "function") return;

  function alreadyListed() {
    if (typeof mc.getTools !== "function") return Promise.resolve(false);
    return Promise.resolve(mc.getTools()).then(function (tools) {
      return (tools || []).some(function (t) { return t && t.name === NAME; });
    }).catch(function () { return false; });
  }

  alreadyListed().then(function (listed) {
    if (listed) return;
    mc.registerTool({
      name: NAME,
      description: form.getAttribute("tooldescription"),
      inputSchema: {
        type: "object",
        properties: {
          email: { type: "string", format: "email", description: email.getAttribute("toolparamdescription") }
        },
        required: ["email"]
      },
      execute: function (args) {
        email.value = (args && args.email) || "";
        email.dispatchEvent(new Event("input", { bubbles: true }));
        var button = form.querySelector("button.join");
        button.focus();
        button.scrollIntoView({ block: "center", behavior: "smooth" });
        // Resolve with whatever the real submit reports back (see reply()).
        return new Promise(function (resolve) {
          // Capture phase, so it's set before the main handler can reply.
          form.addEventListener("submit", function () {
            window.__mimaAgentReply = resolve;
          }, { once: true, capture: true });
        });
      }
    });
  });
})();

// WebMCP tool: download Mima. There's no form for this, so it's registered
// imperatively wherever WebMCP exists. It describes the requirements and
// starts the same /download the buttons use.
(function () {
  "use strict";
  var mc = document.modelContext || navigator.modelContext;
  if (!mc || typeof mc.registerTool !== "function") return;
  var url = "https://mima.social/download";

  mc.registerTool({
    name: "download_mima",
    description:
      "Start downloading the Mima desktop app: the free beta installer (.dmg) for Macs with Apple Silicon (M1 or later). " +
      "There are no Intel, Windows or Linux builds yet. Only call this when the person has asked to download Mima " +
      "and is on an Apple Silicon Mac; otherwise offer the newsletter (subscribe_to_mima_updates) instead.",
    inputSchema: { type: "object", properties: {} },
    execute: function () {
      if (typeof window.gtag === "function") {
        window.gtag("event", "download_click", { link_url: url, placement: "agent", transport_type: "beacon" });
      }
      // Navigating to /download starts the .dmg download; the page stays put.
      var a = document.createElement("a");
      a.href = url;
      a.rel = "noopener";
      document.body.appendChild(a);
      a.click();
      a.remove();
      return Promise.resolve({
        ok: true,
        message: "Opened mima.social/download, which downloads the latest Mima beta (Mima-latest-arm64.dmg). When it finishes, open the .dmg and drag Mima to Applications.",
        url: url,
        requirements: "macOS on Apple Silicon (M1 or later)",
        price: "Free (beta)"
      });
    }
  });
})();
