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
