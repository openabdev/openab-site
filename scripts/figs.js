// Step player for dev-note figures (scripts/figures.py). Inlined into note pages by build.py.
// Each figure autoplays when it scrolls into view and loops: steps 0..n-1, then the complete
// state held for HOLD ms, then again. Off-screen figures are paused (IntersectionObserver).
// A small Pause/Play toggle stops the motion (WCAG 2.2.2); playing never depends on it.
// No JS or prefers-reduced-motion: the complete static state, no autoplay (Play still works).
// ?fig-step=N freezes every figure at step N (used for preview screenshots).
(function () {
  var HOLD = 1800;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var freeze = new URLSearchParams(location.search).get("fig-step");
  document.querySelectorAll("figure.anim").forEach(function (fig) {
    var n = +fig.dataset.steps, ms = +fig.dataset.ms || 1100;
    var at = -1, timer = null, visible = false, paused = reduce;
    var els = fig.querySelectorAll("[data-show],[data-hl]");
    var ctl = fig.querySelector(".figctl"), btn = fig.querySelector(".figbtn");
    function has(list, k) { return (" " + list + " ").indexOf(" " + k + " ") >= 0; }
    function render() {
      fig.classList.toggle("playing", at >= 0);
      els.forEach(function (e) {
        var s = e.dataset.show, h = e.dataset.hl;
        e.classList.toggle("off", at >= 0 && s !== undefined && +s > at);
        e.classList.toggle("hl", at >= 0 && h !== undefined && has(h, at));
      });
      btn.textContent = btn.dataset[paused ? "play" : "pause"];
      btn.setAttribute("aria-pressed", paused ? "true" : "false");
    }
    function stop() { clearTimeout(timer); timer = null; }
    function next() {
      at = at + 1 >= n ? -1 : at + 1;   // -1 is the complete state between loops
      render();
      timer = setTimeout(next, at < 0 ? HOLD : ms);
    }
    function sync() {
      stop();
      if (visible && !paused) timer = setTimeout(next, at < 0 ? 400 : ms);
      render();
    }
    btn.addEventListener("click", function () {
      paused = !paused;
      if (paused) at = -1;   // stopping shows the complete diagram
      sync();
    });
    ctl.hidden = false;
    // Link a tree line with its frame on hover, focus or tap; works while the loop runs.
    function link(id, on) {
      fig.querySelectorAll('[data-node="' + id + '"]').forEach(function (e) {
        e.classList.toggle("link", on);
      });
    }
    fig.querySelectorAll("li[data-node]").forEach(function (li) {
      var id = li.dataset.node;
      ["mouseenter", "focus"].forEach(function (ev) {
        li.addEventListener(ev, function () { link(id, true); });
      });
      li.addEventListener("click", function () {
        fig.querySelectorAll(".link").forEach(function (e) { e.classList.remove("link"); });
        link(id, true);
      });
      ["mouseleave", "blur"].forEach(function (ev) {
        li.addEventListener(ev, function () { link(id, false); });
      });
    });
    if (freeze !== null) { at = Math.min(+freeze, n - 1); paused = true; render(); return; }
    render();
    if (!("IntersectionObserver" in window)) { visible = true; sync(); return; }
    new IntersectionObserver(function (es) {
      visible = es[es.length - 1].isIntersecting;
      sync();
    }, { threshold: 0.35 }).observe(fig);
  });
})();
