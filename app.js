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

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  // "Back and try again" affordance: clear the error and return focus to the form.
  retryBtn.addEventListener("click", function () {
    setError("");
    emailInput.focus();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    setError("");

    var email = emailInput.value.trim();
    if (!validEmail(email)) {
      setError("Enter a valid email address.");
      emailInput.focus();
      return;
    }

    // Guard against duplicate rapid submits.
    var now = Date.now();
    var last = parseInt(localStorage.getItem(RATE_KEY) || "0", 10);
    if (now - last < RATE_MS) {
      setError("Hang on a sec — you just submitted. Give it a moment and try again.");
      return;
    }

    // Build an x-www-form-urlencoded body: &-joined key=value pairs, each value
    // URL-encoded exactly once. The optional fields go in even when empty.
    // The hidden source raw string is encoded here (not pre-encoded) to avoid
    // double-encoding its spaces.
    var body = [
      "email=" + encodeURIComponent(email),
      "signupSource=" + encodeURIComponent(sourceInput.value.trim()),
      "desiredUse=" + encodeURIComponent(goalInput.value.trim()),
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
        } else {
          // Allow an immediate retry after a real error.
          localStorage.removeItem(RATE_KEY);
          reEnable();
          setError((r.data && r.data.message) ? r.data.message : "Something went wrong. Please try again.");
        }
      })
      .catch(function (err) {
        localStorage.removeItem(RATE_KEY);
        reEnable();
        if (err && err.rateLimited) {
          setError("Too many signups, please try again in a little while.");
        } else {
          setError("Couldn’t reach the signup server. Check your connection and try again.");
        }
      });
  });

  emailInput.addEventListener("input", function () { setError(""); });
})();
