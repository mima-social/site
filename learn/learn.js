// Learn pages: "On this page" follows the section you're reading, and
// Download goes to the home page on phones and tablets, where the
// email-me-the-link sheet lives (a .dmg is no use there).
(function () {
  var toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    var links = {};
    toc.querySelectorAll("a[href^='#']").forEach(function (a) {
      links[decodeURIComponent(a.getAttribute("href").slice(1))] = a;
    });
    var heads = Array.prototype.filter.call(
      document.querySelectorAll(".prose h2[id], .prose h3[id]"),
      function (h) { return links[h.id]; }
    );
    var current = null;
    function mark(id) {
      if (id === current) return;
      if (current && links[current]) links[current].removeAttribute("aria-current");
      current = id;
      if (id && links[id]) links[id].setAttribute("aria-current", "true");
    }
    // The current section is the last heading that has scrolled past the top third.
    function update() {
      var line = window.innerHeight * 0.33, id = heads.length ? null : null;
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top <= line) id = heads[i].id;
        else break;
      }
      mark(id);
    }
    var io = new IntersectionObserver(update, { rootMargin: "0px 0px -60% 0px", threshold: [0, 1] });
    heads.forEach(function (h) { io.observe(h); });
    addEventListener("scroll", function () { requestAnimationFrame(update); }, { passive: true });
    update();
  }

  var touch = window.matchMedia && matchMedia("(hover: none) and (pointer: coarse)").matches;
  if (touch) {
    document.querySelectorAll("[data-download]").forEach(function (a) {
      a.setAttribute("href", "/#get-mima");
    });
  }
})();
