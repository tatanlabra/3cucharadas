import fs from "node:fs";
import vm from "node:vm";
import { describe, expect, it } from "vitest";

async function flush() { for (let i = 0; i < 12; i += 1) await Promise.resolve(); }

function boot(reduce = false, intersectionObserver = true) {
  const animations: Array<{ finished: Promise<void>; resolve: () => void; cancel: () => void; canceled: boolean; duration: number }> = [];
  class Element {
    text = "";
    children: Element[] = [];
    className = "";
    attributes: Record<string,string> = {};
    classes = new Set<string>();
    isConnected = true;
    top = 100;
    left = 0;
    classList = { add: (s: string) => this.classes.add(s), remove: (s: string) => this.classes.delete(s) };
    get textContent(): string { return this.text + this.children.map(c => c.textContent).join(""); }
    set textContent(s: string) { this.text = s; this.children = []; }
    getBoundingClientRect() { return { top: this.top, bottom: this.top + 40, left: this.left, right: this.left + 180, width: 180, height: 40 }; }
    setAttribute(k: string,v: string) { this.attributes[k] = v; }
    append(child: Element) { this.children.push(child); }
    replaceChildren(...children: Element[]) { this.text = ""; this.children = children; }
    animate(_frames: unknown, options: {duration: number}) {
      let resolve!: () => void;
      let reject!: (error: Error) => void;
      const finished = new Promise<void>((done, fail) => { resolve = done; reject = fail; });
      const animation = { finished, resolve, canceled: false, duration: options.duration, cancel() { this.canceled = true; reject(new Error("canceled")); } };
      animations.push(animation);
      return animation;
    }
  }
  type Entry = { target: Element; isIntersecting: boolean; intersectionRatio: number };
  const observers: Observer[] = [];
  class Observer {
    observed = new Set<Element>();
    constructor(readonly callback: (entries: Entry[]) => void, readonly options: { threshold: number; rootMargin?: string }) { observers.push(this); }
    observe(element: Element) { this.observed.add(element); }
    unobserve(element: Element) { this.observed.delete(element); }
  }
  let onMotionChange = () => {};
  let onVisibilityChange = () => {};
  const media = { matches: reduce, addEventListener: (_: string,fn: () => void) => { onMotionChange = fn; } };
  const window = { innerWidth: 1000, innerHeight: 800, matchMedia: () => media, dispatchEvent() {},
    ...(intersectionObserver ? { IntersectionObserver: Observer } : {}),
    CatastroNumbers: undefined as unknown as { set: (e: Element, v: string) => void } };
  const document = { hidden: false, documentElement: { dataset: {theme:"light"} },
    addEventListener: (name: string, callback: () => void) => { if (name === "visibilitychange") onVisibilityChange = callback; },
    getElementById: () => null, querySelector: () => null, querySelectorAll: () => [],
    createElement: () => new Element(), createTextNode: (text: string) => { const e = new Element(); e.textContent = text; return e; } };
  vm.runInNewContext(fs.readFileSync(process.env.NUMBERS_SCRIPT_FILE ?? "catastro_sii_brecha/assets/site-ui.js", "utf8"), {
    window, document, IntersectionObserver: Observer, CustomEvent: class {}, Promise
  });
  const enter = (...elements: Element[]) => observers[0].callback(elements.map(target => ({ target, isIntersecting: true, intersectionRatio: 1 })));
  const leave = (target: Element) => observers[0].callback([{ target, isIntersecting: false, intersectionRatio: 0 }]);
  return { element: new Element(), createElement: () => new Element(), api: window.CatastroNumbers, animations, observers, enter, leave,
    reduce: () => { media.matches = true; onMotionChange(); }, hide: () => { document.hidden = true; onVisibilityChange(); } };
}

describe("decorative sequential digit reels", () => {
  it("shows final values immediately and starts only near the visible scroll point", async () => {
    const {element,api,animations,observers,enter} = boot();
    element.top = 900;
    api.set(element,"1.234,5%");
    await flush();
    expect(element.textContent).toBe("1.234,5%");
    expect(animations).toHaveLength(0);
    expect(observers[0].options.threshold).toBeGreaterThanOrEqual(0.5);
    expect(observers[0].options.rootMargin).toBe("0px 0px -10% 0px");
    element.top = 100; enter(element); await flush();
    expect(element.children[0].textContent).toBe("1.234,5%");
    expect(element.children[1].attributes["aria-hidden"]).toBe("true");
    expect(animations).toHaveLength(5);
    expect(Math.min(...animations.map(a => a.duration))).toBeGreaterThanOrEqual(850);
    expect(Math.max(...animations.map(a => a.duration))).toBeLessThanOrEqual(1100);
    animations.forEach(a => a.resolve()); await flush();
    expect(element.textContent).toBe("1.234,5%");
    expect(element.children).toHaveLength(0);
  });

  it("runs one number at a time in reading order, without delaying queued real values", async () => {
    const {element:a,createElement,api,animations,enter} = boot();
    const b = createElement(); b.top = 200;
    api.set(b,"345"); api.set(a,"12"); enter(b,a); await flush();
    expect(a.classes.has("number-rolling")).toBe(true);
    expect(b.classes.has("number-rolling")).toBe(false);
    expect(b.textContent).toBe("345");
    expect(animations).toHaveLength(2);
    animations.forEach(animation => animation.resolve()); await flush();
    expect(a.classes.has("number-rolling")).toBe(false);
    expect(b.classes.has("number-rolling")).toBe(true);
    expect(animations).toHaveLength(5);
  });

  it("cancels a number leaving the viewport and discards queued numbers that left", async () => {
    const {element:a,createElement,api,animations,enter,leave} = boot();
    const b = createElement(); b.top = 200;
    api.set(a,"12"); api.set(b,"34"); enter(a,b); await flush();
    leave(b); leave(a); await flush();
    expect(animations.every(animation => animation.canceled)).toBe(true);
    expect(a.textContent).toBe("12"); expect(b.textContent).toBe("34");
    enter(a,b); await flush();
    expect(animations).toHaveLength(2);
  });

  it("rechecks queued geometry before starting while an observer update is pending", async () => {
    const {element:a,createElement,api,animations,enter} = boot();
    const b = createElement(); b.top = 200;
    api.set(a,"12"); api.set(b,"34"); enter(a,b); await flush();
    b.top = 1200;
    animations.forEach(animation => animation.resolve()); await flush();
    expect(animations).toHaveLength(2);
    expect(b.textContent).toBe("34");
  });

  it("rapid replacements cannot animate stale values or let late completion overwrite them", async () => {
    const {element,api,animations,enter} = boot();
    api.set(element,"123"); enter(element); await flush();
    const previous = [...animations];
    api.set(element,"456"); api.set(element,"789");
    expect(previous.every(animation => animation.canceled)).toBe(true);
    expect(element.textContent).toBe("789");
    enter(element); await flush();
    previous.forEach(animation => animation.resolve()); await flush();
    expect(element.children[0].textContent).toBe("789");
    expect(animations).toHaveLength(6);
  });

  for (const reason of ["reduce", "hide"] as const) {
    it("cancels the active effect and clears its entire queue on " + reason, async () => {
      const setup = boot();
      const a = setup.element; const b = setup.createElement(); b.top = 200;
      setup.api.set(a,"12"); setup.api.set(b,"34"); setup.enter(a,b); await flush();
      setup[reason](); await flush();
      expect(a.textContent).toBe("12"); expect(b.textContent).toBe("34");
      expect(a.children).toHaveLength(0); expect(b.children).toHaveLength(0);
      expect(setup.animations.every(animation => animation.canceled)).toBe(true);
      expect(setup.observers[0].observed.size).toBe(0);
    });
  }

  it("renders static values for reduced motion or browsers without intersection observation", async () => {
    for (const setup of [boot(true), boot(false,false)]) {
      setup.api.set(setup.element,"$326,1 billones"); await flush();
      expect(setup.element.textContent).toBe("$326,1 billones");
      expect(setup.animations).toHaveLength(0);
    }
  });

  it("does not animate missing values or repeat unchanged numbers", async () => {
    const {element,api,animations,enter} = boot();
    api.set(element,"—"); expect(animations).toHaveLength(0);
    api.set(element,"123"); api.set(element,"123"); enter(element); await flush();
    expect(animations).toHaveLength(3);
  });
});
