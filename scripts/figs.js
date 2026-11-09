// Step player for dev-note figures (scripts/figures.py). Inlined into note pages by build.py.
// No JS or prefers-reduced-motion: the figure stays in its complete, static state. Reduced
// motion never autoplays; the Replay button still plays it on request, without transitions.
// ?fig-step=N freezes every figure at step N (used for preview screenshots).
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var freeze = new URLSearchParams(location.search).get("fig-step");
  document.querySelectorAll("figure.anim").forEach(function (fig) {
    var n = +fig.dataset.steps, ms = +fig.dataset.ms || 1100, at = -1, timer = null;
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
      btn.textContent = btn.dataset[timer ? "pause" : at >= 0 ? "resume" : "replay"];
    }
    function stop() { clearInterval(timer); timer = null; }
    function tick() {
      at += 1;
      if (at >= n) { stop(); at = -1; }
      render();
    }
    function play() { stop(); timer = setInterval(tick, ms); render(); }
    btn.addEventListener("click", function () {
      if (timer) { stop(); render(); }
      else { if (at < 0) at = -1, tick(); play(); }
    });
    ctl.hidden = false;
    // Link a tree line with its frame (and back) on hover, focus or tap.
    function link(id, on) {
      fig.querySelectorAll('[data-node="' + id + '"]').forEach(function (e) {
        e.classList.toggle("link", on);
      });
    }
    fig.querySelectorAll("li[data-node]").forEach(function (li) {
      var id = li.dataset.node;
      ["mouseenter", "focus"].forEach(function (ev) {
        li.addEventListener(ev, function () { if (timer) { stop(); at = -1; render(); } link(id, true); });
      });
      li.addEventListener("click", function () {
        fig.querySelectorAll(".link").forEach(function (e) { e.classList.remove("link"); });
        link(id, true);
      });
      ["mouseleave", "blur"].forEach(function (ev) {
        li.addEventListener(ev, function () { link(id, false); });
      });
    });
    if (freeze !== null) { at = Math.min(+freeze, n - 1); render(); return; }
    render();
    if (reduce || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); at = -1; tick(); play(); }
    }, { threshold: 0.45 });
    io.observe(fig);
  });
})();
