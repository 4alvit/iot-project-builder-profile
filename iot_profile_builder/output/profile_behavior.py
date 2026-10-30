"""Trusted, dependency-free progressive enhancement for public profile pages."""

# ruff: noqa: E501
# This constant is hashed by the renderer's CSP; never interpolate profile data into it.
PROFILE_SCRIPT = r"""
(function () {
  "use strict";
  const main = document.getElementById("main");
  if (!main || main.dataset.profileVersion !== "2") return;
  const username = main.dataset.profileUser;
  if (!/^[a-z\d](?:[a-z\d-]{0,37}[a-z\d])?$/i.test(username || "")) return;
  const base = new URL("./", location.href);
  const routes = new Map([["", "overview"], ["index.html", "overview"],
    [username + "_profile.html", "overview"], ["repositories.html", "repositories"], ["evidence.html", "evidence"]]);
  const TIMEOUT = 8000, MAX_HTML = 2 * 1024 * 1024, MAX_JSON = 128 * 1024;
  const TTL = 20 * 60 * 1000, CACHE_LIMIT = 7 * 24 * 60 * 60 * 1000;
  const HISTORY = "iotProfileDocumentV2", CACHE = "iot-profile.public-repository.v1.";
  const snapshots = new Map();
  let retryUntil = 0, paused = false;
  try { paused = sessionStorage.getItem("iot-profile.motion.v1") === "paused"; } catch { /* Optional storage. */ }

  function route(value) {
    try {
      const url = new URL(value, base);
      if (!/^https?:$/.test(url.protocol) || url.origin !== base.origin || url.username || url.password || !url.pathname.startsWith(base.pathname)) return null;
      return routes.has(url.pathname.slice(base.pathname.length)) ? url : null;
    } catch { return null; }
  }
  function pageName(url) { return routes.get(url.pathname.slice(base.pathname.length)); }
  const siteEnabled = Boolean(route(location.href));
  function count(value) { return Number.isSafeInteger(value) && value >= 0; }
  function validRepo(value) { return typeof value === "string" && /^[a-z\d](?:[a-z\d-]{0,37}[a-z\d])?\/[a-z\d_.-]{1,100}$/i.test(value) && !/[/.]\.($|\/)/.test(value); }
  function snapshot(data, repo, checkedAt = Date.now()) {
    if (!data || data.full_name !== repo || data.private !== false || data.html_url !== "https://github.com/" + repo || !count(data.stargazers_count) || !count(data.forks_count)) return null;
    return { repo, checkedAt, stars: data.stargazers_count, forks: data.forks_count,
      updatedAt: typeof data.updated_at === "string" && Number.isFinite(Date.parse(data.updated_at)) ? data.updated_at : null };
  }
  function cached(repo) {
    let row = snapshots.get(repo);
    if (!row) { try { row = JSON.parse(sessionStorage.getItem(CACHE + repo)); } catch { /* Storage may be unavailable or malformed. */ } }
    if (!row || row.version !== 1 || row.repo !== repo || !count(row.stars) || !count(row.forks) || !Number.isFinite(row.checkedAt) || row.checkedAt < 0 || row.checkedAt > Date.now() || Date.now() - row.checkedAt > CACHE_LIMIT || (row.updatedAt !== null && (typeof row.updatedAt !== "string" || !Number.isFinite(Date.parse(row.updatedAt))))) return null;
    return row;
  }
  async function limitedText(response, limit, signal) {
    if (Number(response.headers.get("content-length")) > limit) throw new Error("Response too large");
    if (!response.body?.getReader) {
      const text = await response.text();
      if (new TextEncoder().encode(text).length > limit || signal.aborted) throw new Error("Response unavailable");
      return text;
    }
    const reader = response.body.getReader(), decoder = new TextDecoder();
    let size = 0, text = "", done = false;
    try {
      while (!done) {
        if (signal.aborted) throw new Error("Request canceled");
        const part = await reader.read(); done = part.done;
        if (part.value) { size += part.value.byteLength; if (size > limit) throw new Error("Response too large"); text += decoder.decode(part.value, { stream: true }); }
      }
      return text + decoder.decode();
    } finally { if (!done) await reader.cancel().catch(() => {}); reader.releaseLock(); }
  }
  function retryDelay(response) {
    const value = response.headers.get("retry-after"), seconds = Number(value);
    const retry = value ? (Number.isFinite(seconds) && seconds >= 0 ? Date.now() + seconds * 1000 : Date.parse(value)) : 0;
    const reset = response.headers.get("x-ratelimit-remaining") === "0" ? Number(response.headers.get("x-ratelimit-reset")) * 1000 : 0;
    return Math.max(Date.now() + 60000, Number.isFinite(retry) ? retry : 0, Number.isFinite(reset) ? reset : 0);
  }
  function mountMetadata(signal) {
    const regions = [...document.querySelectorAll("[data-github-repo]")].filter(node => validRepo(node.dataset.githubRepo));
    const groups = new Map(), jobs = new Map(), queue = [], requests = new Set(), started = new Set();
    let active = 0, observer = null;
    for (const node of regions) {
      const repo = node.dataset.githubRepo;
      if (!groups.has(repo)) groups.set(repo, []);
      groups.get(repo).push(node);
    }
    function status(repo, text) { for (const node of groups.get(repo) || []) { const field = node.querySelector("[data-github-status]"); if (field) field.textContent = text; } }
    function busy(repo, value) {
      for (const node of groups.get(repo) || []) {
        node.setAttribute("aria-busy", String(value));
        const button = node.querySelector("[data-github-refresh]"); if (button) button.disabled = value;
      }
    }
    function render(repo, row, prefix) {
      for (const node of groups.get(repo) || []) {
        for (const [selector, value] of [["stars", row.stars.toLocaleString()], ["forks", row.forks.toLocaleString()], ["updated", row.updatedAt ? new Date(row.updatedAt).toLocaleDateString() : "Not reported"]]) {
          const field = node.querySelector("[data-github-" + selector + "]"); if (field) field.textContent = value;
        }
      }
      status(repo, prefix + " " + new Date(row.checkedAt).toLocaleString() + ". Public GitHub data; the analysis snapshot is unchanged.");
    }
    function unavailable(repo, message) {
      const row = cached(repo);
      if (row) { render(repo, row, "Saved data; checked"); status(repo, "Saved data checked " + new Date(row.checkedAt).toLocaleString() + ". " + message); }
      else status(repo, "Showing the generated snapshot. " + message);
    }
    async function run(repo) {
      const controller = new AbortController(); requests.add(controller);
      const timer = setTimeout(() => controller.abort(), TIMEOUT);
      busy(repo, true); status(repo, "Loading public GitHub data; existing values remain visible.");
      try {
        const response = await fetch("https://api.github.com/repos/" + repo, { signal: controller.signal, credentials: "omit", referrerPolicy: "no-referrer", redirect: "error", headers: { Accept: "application/vnd.github+json" } });
        if (response.status === 403 || response.status === 429) {
          retryUntil = Math.max(retryUntil, retryDelay(response));
          for (const waiting of queue.splice(0)) { jobs.delete(waiting); busy(waiting, false); unavailable(waiting, "GitHub requests are paused after a rate limit. Try Refresh later."); }
          throw new Error("limited");
        }
        if (!response.ok) throw new Error("unavailable");
        const row = snapshot(JSON.parse(await limitedText(response, MAX_JSON, controller.signal)), repo);
        if (!row) throw new Error("unexpected");
        if (signal.aborted || controller.signal.aborted) return;
        const saved = { version: 1, ...row }; snapshots.set(repo, saved);
        try { sessionStorage.setItem(CACHE + repo, JSON.stringify(saved)); } catch { /* Memory cache remains available. */ }
        render(repo, row, "Checked");
      } catch {
        if (!signal.aborted) unavailable(repo, retryUntil > Date.now() ? "GitHub requests are paused after a rate limit. Try Refresh later." : "Live GitHub data is unavailable. Try Refresh or open the repository on GitHub.");
      } finally { clearTimeout(timer); requests.delete(controller); jobs.delete(repo); active--; if (!signal.aborted) { busy(repo, false); drain(); } }
    }
    function drain() {
      if (signal.aborted || document.hidden || retryUntil > Date.now()) return;
      while (active < 2 && queue.length) { active++; void run(queue.shift()); }
    }
    function load(repo, force = false) {
      if (signal.aborted || jobs.has(repo) || (!force && started.has(repo))) return;
      started.add(repo);
      const row = cached(repo);
      if (row) render(repo, row, "Saved data; checked");
      if (!force && row && Date.now() - row.checkedAt < TTL) return;
      if (retryUntil > Date.now()) { unavailable(repo, "GitHub requests are paused after a rate limit. Try Refresh later."); return; }
      jobs.set(repo, true); queue.push(repo); drain();
    }
    for (const [repo, nodes] of groups) {
      const row = cached(repo); if (row) render(repo, row, "Saved data; checked");
      for (const node of nodes) {
        const button = node.querySelector("[data-github-refresh]");
        if (button) { button.hidden = false; button.addEventListener("click", () => load(repo, true), { signal }); }
      }
    }
    if (siteEnabled && "IntersectionObserver" in window) {
      observer = new IntersectionObserver(entries => { for (const entry of entries) if (entry.isIntersecting) { observer.unobserve(entry.target); load(entry.target.dataset.githubRepo); } }, { rootMargin: "80px" });
      regions.forEach(node => observer.observe(node));
    } else if (siteEnabled) groups.forEach((_, repo) => load(repo));
    // Local saved HTML remains offline unless the reader explicitly uses Refresh.
    document.addEventListener("visibilitychange", drain, { signal });
    return () => { observer?.disconnect(); requests.forEach(request => request.abort()); queue.length = 0; };
  }
  function mountFilters(signal) {
    const filters = document.getElementById("repository-filters"), search = document.getElementById("repository-search"), language = document.getElementById("repository-language"), countNode = document.getElementById("repository-count"), empty = document.getElementById("repository-empty");
    const cards = [...document.querySelectorAll(".repo")];
    if (!filters || !search || !language || !countNode || !empty) return;
    const content = new Map(cards.map(card => [card, card.textContent.toLocaleLowerCase()]));
    const apply = () => {
      const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      for (const card of cards) { const matches = terms.every(term => content.get(card).includes(term)) && (!language.value || card.dataset.language === language.value); card.hidden = !matches; if (matches) visible++; }
      countNode.textContent = visible + " of " + cards.length + " repositories"; empty.hidden = visible !== 0;
    };
    filters.hidden = false; search.addEventListener("input", apply, { signal }); language.addEventListener("change", apply, { signal }); apply();
  }
  function mountMotion(signal) {
    const root = document.documentElement, reduced = matchMedia("(prefers-reduced-motion: reduce)"), fine = matchMedia("(hover: hover) and (pointer: fine)");
    const reveals = [...document.querySelectorAll("[data-reveal]")], scenes = [...document.querySelectorAll("[data-scene]")], tiles = [...document.querySelectorAll("[data-tilt]")];
    const frames = new Map(), onscreen = new Set();
    let revealObserver, sceneObserver;
    const reset = tile => { cancelAnimationFrame(frames.get(tile)); frames.delete(tile); tile.style.removeProperty("--tilt-x"); tile.style.removeProperty("--tilt-y"); };
    const buttons = [...document.querySelectorAll("[data-motion-toggle]")];
    function configure() {
      revealObserver?.disconnect(); sceneObserver?.disconnect(); onscreen.clear(); tiles.forEach(reset); scenes.forEach(node => node.classList.remove("is-in-view"));
      const stopped = paused || reduced.matches || document.hidden;
      root.dataset.motion = stopped ? "paused" : "active";
      buttons.forEach(button => { button.hidden = false; button.setAttribute("aria-pressed", String(paused)); button.textContent = paused ? "Resume motion" : "Pause motion"; button.disabled = reduced.matches; button.title = reduced.matches ? "Motion follows your reduced-motion preference" : "Toggle decorative motion"; });
      if (stopped || !("IntersectionObserver" in window)) { root.classList.remove("motion-ready"); reveals.forEach(node => node.classList.add("is-visible")); return; }
      revealObserver = new IntersectionObserver(entries => { for (const entry of entries) if (entry.isIntersecting) { entry.target.classList.add("is-visible"); revealObserver.unobserve(entry.target); } }, { threshold: 0.06 });
      reveals.forEach(node => { if (!node.classList.contains("is-visible")) revealObserver.observe(node); });
      sceneObserver = new IntersectionObserver(entries => { for (const entry of entries) { if (entry.isIntersecting) onscreen.add(entry.target); else { onscreen.delete(entry.target); reset(entry.target); } if (entry.target.hasAttribute("data-scene")) entry.target.classList.toggle("is-in-view", entry.isIntersecting); } });
      [...new Set([...scenes, ...tiles])].forEach(node => sceneObserver.observe(node));
      root.classList.add("motion-ready");
    }
    buttons.forEach(button => button.addEventListener("click", () => { paused = !paused; try { sessionStorage.setItem("iot-profile.motion.v1", paused ? "paused" : "active"); } catch { /* Optional storage. */ } configure(); }, { signal }));
    for (const tile of tiles) {
      tile.addEventListener("pointermove", event => {
        if (paused || reduced.matches || !fine.matches || document.hidden || !onscreen.has(tile) || event.pointerType === "touch") return;
        const box = tile.getBoundingClientRect(); if (!box.width || !box.height) return;
        const x = Math.max(-1, Math.min(1, (event.clientX - box.left) / box.width * 2 - 1)), y = Math.max(-1, Math.min(1, (event.clientY - box.top) / box.height * 2 - 1));
        cancelAnimationFrame(frames.get(tile)); frames.set(tile, requestAnimationFrame(() => { frames.delete(tile); tile.style.setProperty("--tilt-x", (-y * 3).toFixed(2) + "deg"); tile.style.setProperty("--tilt-y", (x * 3).toFixed(2) + "deg"); }));
      }, { signal, passive: true });
      tile.addEventListener("pointerleave", () => reset(tile), { signal }); tile.addEventListener("pointercancel", () => reset(tile), { signal });
    }
    document.addEventListener("focusin", event => { if (event.target instanceof Element) { let node = event.target.closest("[data-reveal]"); while (node) { node.classList.add("is-visible"); node = node.parentElement?.closest("[data-reveal]"); } } }, { signal });
    reduced.addEventListener("change", configure, { signal }); fine.addEventListener("change", configure, { signal }); document.addEventListener("visibilitychange", configure, { signal });
    const header = document.querySelector(".topbar"), measure = () => { if (header) root.style.setProperty("--site-header-height", Math.ceil(header.getBoundingClientRect().height) + "px"); };
    const resize = "ResizeObserver" in window ? new ResizeObserver(measure) : null; if (header) resize?.observe(header);
    window.addEventListener("resize", measure, { signal, passive: true }); measure(); configure();
    return () => { revealObserver?.disconnect(); sceneObserver?.disconnect(); resize?.disconnect(); tiles.forEach(reset); root.classList.remove("motion-ready"); };
  }
  function markNavigation() {
    const name = document.getElementById("main")?.dataset.profilePage;
    document.querySelectorAll("[data-nav-page]").forEach(link => { if (link.dataset.navPage === name) link.setAttribute("aria-current", "page"); else link.removeAttribute("aria-current"); });
  }
  let pageController, cleanups = [], printDetails = [];
  function dispose() { pageController?.abort(); cleanups.forEach(cleanup => cleanup()); cleanups = []; printDetails = []; }
  function mount() {
    pageController = new AbortController(); const signal = pageController.signal;
    cleanups = [mountMetadata(signal), mountMotion(signal)]; mountFilters(signal); markNavigation();
    window.addEventListener("beforeprint", () => { printDetails = [...document.querySelectorAll("details:not([open])")]; printDetails.forEach(detail => { detail.open = true; }); }, { signal });
    window.addEventListener("afterprint", () => { printDetails.forEach(detail => { detail.open = false; }); printDetails = []; }, { signal });
  }
  function parsedDocument(source, target) {
    const page = new DOMParser().parseFromString(source, "text/html"), candidates = page.querySelectorAll("#main"), next = candidates[0];
    if (candidates.length !== 1 || next.tagName !== "MAIN" || !page.title || next.dataset.profileVersion !== "2" || next.dataset.profileUser !== username || next.dataset.profilePage !== pageName(target) || !Number.isFinite(Date.parse(next.dataset.profileGenerated || ""))) throw new Error("Different document");
    next.querySelectorAll("script,style,link,meta,base,iframe,object,embed,form,foreignObject,animate,animateMotion,animateTransform,set").forEach(node => node.remove());
    for (const node of [next, ...next.querySelectorAll("*")]) {
      for (const attr of [...node.attributes]) {
        const name = attr.name.toLowerCase();
        if (name.startsWith("on") || ["srcdoc", "ping", "autofocus", "srcset", "formaction"].includes(name)) { node.removeAttribute(attr.name); continue; }
        if (name === "style") {
          const width = node.style.width, flex = node.style.flex; node.removeAttribute("style");
          if (/^(?:\d+(?:\.\d+)?|\.\d+)%$/.test(width) && Number.parseFloat(width) <= 100) node.style.width = width;
          if (/^\d+(?:\.\d+)?(?:\s+\d+(?:\.\d+)?(?:\s+0%)?)?$/.test(flex)) node.style.flex = flex;
          continue;
        }
        if (!["href", "src", "poster", "action", "xlink:href"].includes(name)) continue;
        if (attr.value.startsWith("#") && node.namespaceURI === "http://www.w3.org/2000/svg") continue;
        try {
          const url = new URL(attr.value, target), isLink = name === "href" && node.tagName === "A";
          if (url.username || url.password || !(isLink ? /^(https?:|mailto:|tel:)$/.test(url.protocol) : /^https?:$/.test(url.protocol) && url.origin === base.origin)) node.removeAttribute(attr.name);
          else node.setAttribute(attr.name, url.href);
        } catch { node.removeAttribute(attr.name); }
      }
    }
    return { page, next };
  }
  function focusDestination(url, position) {
    let target;
    try { target = url.hash ? document.getElementById(decodeURIComponent(url.hash.slice(1))) : null; } catch { /* Invalid fragments use the heading. */ }
    const focus = target || document.querySelector("#main h1") || document.getElementById("main");
    if (focus) { const hadTabindex = focus.hasAttribute("tabindex"); if (!hadTabindex) focus.setAttribute("tabindex", "-1"); focus.focus({ preventScroll: true }); if (!hadTabindex) focus.addEventListener("blur", () => focus.removeAttribute("tabindex"), { once: true }); }
    if (Array.isArray(position) && position.length === 2 && position.every(value => Number.isFinite(value) && value >= 0)) window.scrollTo({ left: position[0], top: position[1], behavior: "instant" });
    else if (target) target.scrollIntoView({ block: "start", behavior: "instant" });
    else window.scrollTo({ left: 0, top: 0, behavior: "instant" });
  }
  function announce(text) {
    let node = document.getElementById("profile-navigation-status");
    if (!node) { node = document.createElement("div"); node.id = "profile-navigation-status"; node.className = "sr-only"; node.setAttribute("role", "status"); node.setAttribute("aria-live", "polite"); node.setAttribute("aria-atomic", "true"); document.body.append(node); }
    node.textContent = text;
  }
  let documentURL = location.href, navigation = null, revision = 0, saveTimer;
  const initialURL = location.href, initialEntry = history.state?.[HISTORY];
  const restored = ["reload", "back_forward"].includes(performance.getEntriesByType?.("navigation")[0]?.type);
  const initialPosition = restored && initialEntry?.url === initialURL ? initialEntry.position : undefined;
  function savePosition() {
    clearTimeout(saveTimer); if (location.href !== documentURL || !siteEnabled) return;
    try { history.replaceState({ ...(history.state && typeof history.state === "object" ? history.state : {}), [HISTORY]: { url: location.href, position: [window.scrollX, window.scrollY] } }, "", location.href); } catch { /* Normal navigation still works. */ }
  }
  function cancelNavigation() { revision++; navigation?.abort(); navigation = null; document.documentElement.removeAttribute("data-profile-loading"); }
  async function navigate(target, pop = false, position) {
    cancelNavigation(); const attempt = revision, controller = new AbortController(); navigation = controller;
    if (!pop) savePosition(); else clearTimeout(saveTimer);
    document.documentElement.setAttribute("data-profile-loading", "true"); announce("Loading page…");
    const timer = setTimeout(() => controller.abort(), TIMEOUT);
    try {
      const response = await fetch(target.href, { signal: controller.signal, credentials: "same-origin", redirect: "error", headers: { Accept: "text/html" } });
      if (!response.ok || !response.headers.get("content-type")?.toLowerCase().includes("text/html")) throw new Error("Document unavailable");
      const { page, next } = parsedDocument(await limitedText(response, MAX_HTML, controller.signal), target);
      if (attempt !== revision) return;
      if (controller.signal.aborted) throw new Error("Navigation timed out");
      if (!pop) history.pushState({ [HISTORY]: { url: target.href, position: null } }, "", target.href);
      dispose(); document.getElementById("main").replaceWith(document.importNode(next, true));
      document.title = page.title; document.documentElement.lang = page.documentElement.lang || "en";
      document.documentElement.dir = page.documentElement.dir || "ltr";
      const description = page.querySelector('meta[name="description"]'); let current = document.querySelector('meta[name="description"]');
      if (description) { if (!current) { current = document.createElement("meta"); current.name = "description"; document.head.append(current); } current.content = description.content; } else current?.remove();
      documentURL = location.href; mount(); focusDestination(target, position); savePosition(); announce(document.title + " loaded.");
      document.dispatchEvent(new CustomEvent("profile:navigated", { detail: { page: pageName(target) } }));
    } catch { if (attempt === revision) location.assign(target.href); }
    finally { clearTimeout(timer); if (attempt === revision) { navigation = null; document.documentElement.removeAttribute("data-profile-loading"); } }
  }
  function ordinaryClick(event, link) { return link && !event.defaultPrevented && event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey && !link.hasAttribute("download") && (!link.target || link.target.toLowerCase() === "_self"); }
  if (siteEnabled) {
    document.addEventListener("click", event => {
      const link = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!ordinaryClick(event, link)) return;
      const target = !link.hasAttribute("data-native-navigation") && route(link.href);
      if (!target) { if (/^https?:$/.test(link.protocol)) cancelNavigation(); return; }
      event.preventDefault(); const current = new URL(documentURL);
      if (target.pathname === current.pathname && target.search === current.search) {
        cancelNavigation(); savePosition();
        try { if (target.href !== location.href) history.pushState({ [HISTORY]: { url: target.href, position: null } }, "", target.href); documentURL = location.href; focusDestination(target); savePosition(); } catch { location.assign(target.href); }
      } else void navigate(target);
    });
    window.addEventListener("popstate", event => {
      const target = route(location.href); if (!target) { location.reload(); return; }
      const current = new URL(documentURL), entry = event.state?.[HISTORY], position = entry?.url === target.href ? entry.position : undefined;
      if (target.pathname === current.pathname && target.search === current.search) { cancelNavigation(); clearTimeout(saveTimer); documentURL = location.href; focusDestination(target, position); savePosition(); }
      else void navigate(target, true, position);
    });
    try { history.scrollRestoration = "manual"; } catch { /* Storage-restricted documents keep normal history. */ }
  }
  window.addEventListener("scroll", () => { clearTimeout(saveTimer); saveTimer = setTimeout(savePosition, 120); }, { passive: true });
  window.addEventListener("pagehide", () => { savePosition(); cancelNavigation(); dispose(); });
  window.addEventListener("pageshow", event => { if (event.persisted) mount(); });
  mount();
  let interacted = false; const initialInput = new AbortController();
  for (const name of ["pointerdown", "wheel", "touchstart", "keydown"]) window.addEventListener(name, () => { interacted = true; }, { signal: initialInput.signal, passive: true });
  requestAnimationFrame(() => { if (!interacted && revision === 0 && location.href === initialURL && (initialPosition || (!restored && location.hash))) focusDestination(new URL(initialURL), initialPosition); savePosition(); initialInput.abort(); });
})();
"""
