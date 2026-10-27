import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

class FakeElement {
  constructor(attributes = {}, dataset = {}) {
    this.attributes = { ...attributes };
    this.dataset = { ...dataset };
    this.listeners = {};
    this.style = {};
  }

  addEventListener(name, callback) {
    this.listeners[name] = callback;
  }

  getAttribute(name) {
    return this.attributes[name] ?? null;
  }

  setAttribute(name, value) {
    this.attributes[name] = String(value);
  }
}

const lightSrc = "/assets/images/tesis-post3/sample-flow-es-light.svg";
const darkSrc = "/assets/images/tesis-post3/sample-flow-es-dark.svg";
const lightSrcset = `${lightSrc} 1600w`;
const darkSrcset = `${darkSrc} 1600w`;
const lightMobileSrcset = lightSrc.replace(".svg", "-mobile.svg");
const darkMobileSrcset = darkSrc.replace(".svg", "-mobile.svg");
const source = new FakeElement(
  { srcset: lightMobileSrcset, media: "(max-width: 47.99em)" },
  { lightSrcset: lightMobileSrcset, darkSrcset: darkMobileSrcset },
);
const image = new FakeElement(
  { src: lightSrc, srcset: lightSrcset },
  {
    lightSrc,
    darkSrc,
    lightSrcset,
    darkSrcset,
  },
);
const link = new FakeElement(
  { href: lightSrc },
  { lightHref: lightSrc, darkHref: darkSrc },
);
const button = new FakeElement({}, { themeLightLabel: "Claro", themeDarkLabel: "Oscuro" });
const root = new FakeElement({ "data-theme": "light" });
const storage = new Map();
const windowListeners = {};

const document = {
  documentElement: root,
  readyState: "complete",
  querySelector(selector) {
    return selector === "meta[data-theme-color]" ? null : null;
  },
  querySelectorAll(selector) {
    if (selector === "[data-theme-toggle]") return [button];
    if (selector === ".post3-theme-source") return [source];
    if (selector === ".post3-theme-image") return [image];
    if (selector === ".post3-theme-link") return [link];
    return [];
  },
};
const window = {
  addEventListener(name, callback) {
    windowListeners[name] = callback;
  },
  localStorage: {
    getItem(key) {
      return storage.has(key) ? storage.get(key) : null;
    },
    setItem(key, value) {
      storage.set(key, String(value));
    },
  },
};

// Sin JavaScript, los atributos HTML ya apuntan a una variante clara legible.
assert.equal(image.getAttribute("src"), lightSrc);
assert.equal(image.getAttribute("srcset"), lightSrcset);
assert.equal(source.getAttribute("srcset"), lightMobileSrcset);
assert.equal(link.getAttribute("href"), lightSrc);

const script = fs.readFileSync(new URL("../assets/js/theme-toggle.js", import.meta.url), "utf8");
vm.runInNewContext(script, { document, window });

assert.equal(root.getAttribute("data-theme"), "light");
assert.equal(typeof button.listeners.click, "function");
button.listeners.click();
assert.equal(root.getAttribute("data-theme"), "academic-night");
assert.equal(image.getAttribute("src"), darkSrc);
assert.equal(image.getAttribute("srcset"), darkSrcset);
assert.equal(source.getAttribute("srcset"), darkMobileSrcset);
assert.equal(link.getAttribute("href"), darkSrc);

assert.equal(typeof windowListeners.beforeprint, "function");
assert.equal(typeof windowListeners.afterprint, "function");
windowListeners.beforeprint();
assert.equal(image.getAttribute("src"), lightSrc);
assert.equal(source.getAttribute("srcset"), lightMobileSrcset);
assert.equal(link.getAttribute("href"), lightSrc);
windowListeners.afterprint();
assert.equal(image.getAttribute("src"), darkSrc);
assert.equal(source.getAttribute("srcset"), darkMobileSrcset);
assert.equal(link.getAttribute("href"), darkSrc);

button.listeners.click();
assert.equal(root.getAttribute("data-theme"), "light");
assert.equal(image.getAttribute("src"), lightSrc);
assert.equal(image.getAttribute("srcset"), lightSrcset);
assert.equal(source.getAttribute("srcset"), lightMobileSrcset);
assert.equal(link.getAttribute("href"), lightSrc);

for (const post of [
  "../_posts/2026-10-23-costos-cierre-escolar-trayectorias.md",
  "../_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md",
]) {
  const markdown = fs.readFileSync(new URL(post, import.meta.url), "utf8");
  const figures = [
    ...markdown.matchAll(
      /<figure class="[^"]*\bpost3-figure\b[^"]*"[^>]*>([\s\S]*?)<\/figure>/g,
    ),
  ];
  assert.equal(figures.length, 3, `${post}: debe integrar tres figuras Post III`);
  const identified = [
    ...markdown.matchAll(
      /<figure class="[^"]*\bpost3-figure\b[^"]*\bdata-visualization\b[^"]*"/g,
    ),
  ];
  assert.equal(identified.length, 3, `${post}: las tres figuras usan identidad visual`);
  for (const [, figure] of figures) {
    assert.equal((figure.match(/<img\b/g) ?? []).length, 1, `${post}: un solo img ODT-safe`);
    assert.equal(
      (figure.match(/<source\b/g) ?? []).length,
      1,
      `${post}: un source móvil para art direction`,
    );
    assert.match(figure, /class="post3-theme-source"/);
    assert.match(figure, /media="\(max-width: 47\.99em\)"/);
    assert.match(figure, /data-light-srcset="[^"]+-light-mobile\.svg/);
    assert.match(figure, /data-dark-srcset="[^"]+-dark-mobile\.svg/);
  }
}

console.log("PASS: Post III light/dark sources and links round-trip");
