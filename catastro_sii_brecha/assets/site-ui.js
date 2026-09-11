// Finite odometer effect: the accessible value is final from the first frame.
// Visual reels are decorative and run only while the number is on screen.
(() => {
  "use strict";
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const active = new Map();
  const queue = [];
  let running = null;
  let drainScheduled = false;
  const visibilityThreshold = 0.55;
  const observer = "IntersectionObserver" in window ? new IntersectionObserver(entries => {
    for (const entry of entries) {
      const record = active.get(entry.target);
      if (!record) continue;
      const wasVisible = record.visible;
      record.visible = entry.isIntersecting && entry.intersectionRatio >= visibilityThreshold;
      if (record.visible && record.phase === "waiting") {
        record.phase = "queued";
        queue.push(record);
      } else if (!record.visible && wasVisible) {
        record.finish();
      }
    }
    scheduleDrain();
  }, { threshold: visibilityThreshold, rootMargin: "0px 0px -10% 0px" }) : null;

  function inTriggerViewport(element) {
    if (!element.isConnected) return false;
    const box = element.getBoundingClientRect();
    if (box.width <= 0 || box.height <= 0) return false;
    // IntersectionObserver percentage root margins resolve against root width.
    const bottom = window.innerHeight - window.innerWidth * 0.1;
    const width = Math.max(0, Math.min(box.right, window.innerWidth) - Math.max(box.left, 0));
    const height = Math.max(0, Math.min(box.bottom, bottom) - Math.max(box.top, 0));
    return width * height / (box.width * box.height) >= visibilityThreshold;
  }

  function scheduleDrain() {
    if (drainScheduled) return;
    drainScheduled = true;
    // Batch visibility and selection updates before choosing the next number.
    Promise.resolve().then(() => {
      drainScheduled = false;
      if (running || motion.matches || document.hidden) return;
      queue.sort((a, b) => {
        const first = a.element.getBoundingClientRect();
        const second = b.element.getBoundingClientRect();
        return first.top - second.top || first.left - second.left;
      });
      while (queue.length) {
        const record = queue.shift();
        if (active.get(record.element) !== record) continue;
        if (!record.visible || !inTriggerViewport(record.element)) { record.finish(); continue; }
        running = record;
        record.start();
        break;
      }
    });
  }

  function setNumber(element, value) {
    const text = String(value);
    if (active.get(element)?.text === text || (!active.has(element) && element.textContent === text)) return;
    active.get(element)?.finish();
    element.textContent = text;
    if (motion.matches || document.hidden || !/[0-9]/.test(text) || !element.animate || !observer) return;
    let started = false;
    const animations = [];
    const record = { element, text, start, finish, phase: "waiting", visible: false };
    function finish() {
      if (active.get(element) !== record) return;
      active.delete(element);
      observer?.unobserve(element);
      const queued = queue.indexOf(record);
      if (queued !== -1) queue.splice(queued, 1);
      if (running === record) running = null;
      animations.forEach(animation => animation.cancel());
      element.classList.remove("number-rolling");
      element.textContent = text;
      scheduleDrain();
    }
    function start() {
      if (started || active.get(element) !== record) return;
      started = true;
      record.phase = "running";
      if (motion.matches || document.hidden) { finish(); return; }
      const exact = document.createElement("span");
      exact.className = "number-exact";
      exact.textContent = text;
      const visual = document.createElement("span");
      visual.className = "number-reels";
      visual.setAttribute("aria-hidden", "true");
      let index = 0;
      for (const char of text) {
        if (!/[0-9]/.test(char)) { visual.append(document.createTextNode(char)); continue; }
        const window = document.createElement("span");
        window.className = "number-window";
        const track = document.createElement("span");
        track.className = "number-track";
        const target = 10 + Number(char);
        for (let digit = 0; digit <= target; digit++) {
          const cell = document.createElement("span");
          cell.textContent = String(digit % 10);
          track.append(cell);
        }
        window.append(track);
        visual.append(window);
        animations.push({ track, target, duration: 850 + Math.min(index++, 8) * 30 });
      }
      element.replaceChildren(exact, visual);
      element.classList.add("number-rolling");
      const reels = animations.splice(0);
      for (const reel of reels) animations.push(reel.track.animate([
        { transform: "translateY(0)" }, { transform: `translateY(-${reel.target}em)` }
      ], { duration: reel.duration, easing: "cubic-bezier(.16,1,.3,1)", fill: "forwards" }));
      Promise.all(animations.map(animation => animation.finished)).then(finish, finish);
    }
    active.set(element, record);
    observer.observe(element);
  }
  window.CatastroNumbers = { set: setNumber };
  motion.addEventListener?.("change", () => { if (motion.matches) [...active.values()].forEach(record => record.finish()); });
  document.addEventListener("visibilitychange", () => { if (document.hidden) [...active.values()].forEach(record => record.finish()); });
  document.querySelectorAll("[data-roll-number]").forEach(element => {
    const text = element.textContent;
    element.textContent = "";
    setNumber(element, text);
  });
})();

(() => {
  "use strict";

  const root = document.documentElement;
  const storageKey = "catastro-brecha-theme";
  const button = document.getElementById("theme-toggle");

  function setTheme(theme, persist = true) {
    root.dataset.theme = theme;
    const dark = theme === "dark";
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (button) {
      button.setAttribute("aria-pressed", String(dark));
      button.setAttribute("aria-label", dark ? "Activar apariencia clara" : "Activar apariencia oscura");
      button.title = dark ? "Activar apariencia clara" : "Activar apariencia oscura";
    }
    if (themeColor) themeColor.content = dark ? "#07070c" : "#e9edf4";
    if (persist) {
      try { localStorage.setItem(storageKey, theme); } catch (_) { /* El visor también funciona sin almacenamiento. */ }
    }
    window.dispatchEvent(new CustomEvent("catastro:theme", { detail: { theme } }));
  }

  setTheme(root.dataset.theme === "light" ? "light" : "dark", false);
  if (button) button.addEventListener("click", () => setTheme(root.dataset.theme === "dark" ? "light" : "dark"));

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveal = [...document.querySelectorAll(".reveal")];
  if (reducedMotion || !("IntersectionObserver" in window)) {
    reveal.forEach((element) => element.classList.add("in"));
    return;
  }

  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("in");
      currentObserver.unobserve(entry.target);
    });
  }, { threshold: 0.1 });
  reveal.forEach((element) => observer.observe(element));
})();
