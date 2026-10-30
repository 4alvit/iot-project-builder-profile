"""Self-contained HTML presentation for generated engineering profiles."""

# ruff: noqa: E501
# Embedded HTML keeps related attributes and template expressions together.

PROFILE_STYLE = r"""
:root {
  color-scheme:dark;
  --bg:#111214;
  --surface:#191a1e;
  --ink:#f3f1ed;
  --muted:#aaa8b2;
  --line:#323139;
  --accent:#c6b5ff;
  --green:#a7d9c0;
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif
}

* {
  box-sizing:border-box
}
html {
  scroll-behavior:smooth;
  scroll-padding-top:100px
}
body {
  margin:0;
  background:var(--bg);
  color:var(--ink);
  line-height:1.6
}
a {
  color:inherit;
  text-decoration:none
}
a:hover {
  color:var(--accent)
}
button,input,select {
  font:inherit
}
:focus-visible {
  outline:2px solid var(--accent);
  outline-offset:5px
}
summary {
  cursor:pointer
}
svg {
  display:block;
  max-width:100%
}
h1,h2,h3,p {
  margin:0
}
h1,h2,h3 {
  line-height:1.13;
  font-weight:500;
  letter-spacing:-.04em
}
h1 {
  font-size:clamp(3.2rem,6.6vw,6.1rem);
  max-width:10ch
}
h2 {
  font-size:clamp(2rem,4vw,3.7rem)
}
h3 {
  font-size:1.18rem;
  letter-spacing:-.02em
}
p {
  color:var(--muted)
}
[hidden] {
  display:none!important
}
.container {
  width:min(1200px,calc(100% - 80px));
  margin-inline:auto
}
.skip {
  position:fixed;
  left:20px;
  top:-80px;
  background:var(--accent);
  color:var(--bg);
  padding:12px 20px;
  z-index:100
}
.skip:focus {
  top:12px
}
.topbar {
  position:sticky;
  top:0;
  z-index:20;
  border-bottom:1px solid var(--line);
  background:rgba(17,18,20,.94);
  backdrop-filter:blur(16px)
}
.nav {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  min-height:78px
}
.brand {
  display:flex;
  align-items:center;
  gap:12px;
  font-size:.96rem;
  font-weight:600;
  letter-spacing:-.03em
}
.brand-mark {
  display:grid;
  grid-template-columns:repeat(2,6px);
  gap:3px;
  transform:rotate(-9deg)
}
.brand-mark i {
  width:6px;
  height:6px;
  background:var(--ink);
  border-radius:1px
}
.brand-mark i:last-child {
  background:var(--accent)
}
.nav-links {
  display:flex;
  align-items:center;
  gap:28px;
  font-size:.82rem;
  color:var(--muted)
}
.nav-links a {
  padding-block:8px
}
.nav-links a[aria-current] {
  color:var(--ink)
}
.nav-source {
  border:1px solid var(--line);
  padding:8px 15px;
  border-radius:8px;
  color:var(--ink)
}
.label {
  display:block;
  font-family:ui-monospace,SFMono-Regular,Consolas,monospace;
  font-size:.67rem;
  letter-spacing:.13em;
  text-transform:uppercase;
  color:var(--muted)
}
.eyebrow {
  display:flex;
  align-items:center;
  gap:10px
}
.status-dot {
  width:6px;
  height:6px;
  flex-shrink:0;
  border-radius:50%;
  background:var(--green)
}
.hero {
  padding-block:88px 72px;
  display:grid;
  grid-template-columns:1.07fr 1fr;
  gap:64px;
  align-items:center
}
.hero h1 {
  margin-top:24px
}
.hero h1 span {
  color:var(--accent)
}
.hero-copy {
  max-width:43ch;
  margin-top:25px;
  font-size:1rem;
  line-height:1.8
}
.hero-copy strong {
  color:var(--ink);
  font-weight:500;
  overflow-wrap:anywhere
}
.actions {
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  margin-top:30px
}
.button {
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:22px;
  padding:13px 20px;
  border-radius:8px;
  font-size:.82rem;
  font-weight:600;
  border:1px solid var(--line)
}
.button-primary {
  background:var(--ink);
  border-color:var(--ink);
  color:#18191c
}
.button-primary:hover {
  background:var(--accent);
  border-color:var(--accent);
  color:#18191c
}
.button-secondary:hover {
  border-color:var(--muted)
}
.hero-note {
  font-size:.69rem;
  margin-top:22px
}
.signal-card {
  background:radial-gradient(ellipse at 60% 42%,#373047 0%,#202027 48%,#1b1c20 80%);
  border:1px solid #4d4557;
  border-radius:20px;
  padding:26px 26px 22px;
  overflow:hidden;
  box-shadow:0 25px 70px #0003
}
.signal-card-top {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:10px
}
.signal-card .label {
  font-size:.59rem
}
.signal-window {
  display:flex;
  gap:5px
}
.signal-window i {
  width:5px;
  height:5px;
  border-radius:50%;
  background:#857c90
}
.signal-card svg {
  width:100%;
  margin-block:12px
}
.signal-card-bottom {
  border-top:1px solid #ffffff20;
  padding-top:17px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  font-size:.7rem;
  color:var(--muted);
  gap:12px
}
.signal-card-bottom strong {
  color:var(--ink);
  font-weight:500
}
.stats {
  display:grid;
  grid-template-columns:repeat(4,1fr);
  border-block:1px solid var(--line);
  padding-block:30px;
  gap:28px
}
.stat {
  padding-left:27px;
  border-left:1px solid var(--line)
}
.stat:first-child {
  padding-left:0;
  border-left:0
}
.stat strong {
  display:block;
  font-size:2.25rem;
  line-height:1.25;
  font-weight:500;
  letter-spacing:-.05em;
  font-variant-numeric:tabular-nums
}
.stat span {
  display:block;
  font-size:.72rem;
  color:var(--muted);
  margin-top:7px
}
.section {
  padding-block:84px;
  border-bottom:1px solid var(--line)
}
.section-heading {
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:30px;
  margin-bottom:35px
}
.section-heading .label {
  margin-bottom:16px
}
.section-heading>p {
  max-width:37ch;
  font-size:.85rem
}
.intro {
  display:grid;
  grid-template-columns:.85fr 1.15fr;
  gap:75px
}
.intro .label {
  margin-bottom:20px
}
.intro-copy {
  font-size:.94rem;
  line-height:1.9
}
.intro-copy p+p {
  margin-top:20px
}
.summary-more {
  margin-top:16px
}
.summary-more summary {
  display:inline-block;
  color:var(--accent);
  font-size:.8rem
}
.summary-more summary::after {
  content:" +"
}
.summary-more[open] summary::after {
  content:" −"
}
.summary-more p {
  margin-top:15px
}
.snapshot-note {
  margin-top:22px;
  padding-left:15px;
  border-left:2px solid #887398;
  font-size:.75rem;
  line-height:1.75
}
.focus-layout {
  display:grid;
  grid-template-columns:1.3fr 1fr;
  gap:24px
}
.panel {
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:12px;
  padding:28px
}
.panel-title {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:15px;
  margin-bottom:26px
}
.panel-title h3 {
  font-size:1rem
}
.panel-title .label {
  font-size:.56rem
}
.focus-list {
  display:grid;
  grid-template-columns:1fr 1fr;
  column-gap:30px;
  row-gap:20px
}
.score-caption {
  display:flex;
  justify-content:space-between;
  gap:15px;
  align-items:center;
  font-size:.71rem;
  margin-bottom:8px
}
.score-caption span {
  color:#d0ced6
}
.score-caption strong {
  font-size:.67rem;
  font-weight:400;
  color:var(--muted);
  font-variant-numeric:tabular-nums
}
.score-track {
  height:4px;
  border-radius:10px;
  background:#333139;
  overflow:hidden
}
.score-track i {
  display:block;
  height:100%;
  background:var(--accent);
  border-radius:10px
}
.complexity-chart {
  display:flex;
  gap:5px;
  height:12px;
  margin-bottom:26px;
  overflow:hidden;
  border-radius:4px
}
.complexity-chart span {
  background:var(--accent);
  min-width:2px
}
.complexity-chart span:nth-child(2) {
  background:#858192
}
.complexity-chart span:nth-child(3) {
  background:var(--green)
}
.complexity-chart span:nth-child(4) {
  background:#e9c494
}
.complexity-list {
  display:grid;
  gap:14px
}
.complexity-row {
  display:flex;
  align-items:center;
  gap:9px;
  font-size:.77rem
}
.complexity-row i {
  width:7px;
  height:7px;
  background:var(--accent);
  border-radius:2px
}
.complexity-row:nth-child(2) i {
  background:#858192
}
.complexity-row:nth-child(3) i {
  background:var(--green)
}
.complexity-row:nth-child(4) i {
  background:#e9c494
}
.complexity-row strong {
  margin-left:auto;
  font-weight:500
}
.chart-note {
  font-size:.68rem;
  line-height:1.75;
  margin-top:24px
}
.skills {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:16px;
  margin-top:24px
}
.skill {
  border:1px solid var(--line);
  border-radius:12px;
  padding:23px;
  background:linear-gradient(160deg,#1b1b20,#17181b);
  min-width:0
}
.skill .label {
  font-size:.56rem;
  margin-bottom:14px
}
.skill h3 {
  font-size:.96rem;
  min-height:2.8em;
  line-height:1.4
}
.skill-value {
  display:flex;
  flex-wrap:wrap;
  gap:6px;
  align-items:baseline;
  margin-block:19px 12px
}
.skill-value strong {
  font-size:2rem;
  font-weight:400;
  letter-spacing:-.05em
}
.skill-value span {
  color:var(--muted);
  font-size:.7rem
}
.confidence {
  font-size:.63rem;
  color:var(--muted);
  margin-left:auto
}
.evidence-toggle {
  font-size:.68rem;
  margin-top:18px
}
.evidence-toggle summary {
  padding-block:4px;
  color:var(--muted)
}
.evidence-toggle[open] summary {
  margin-bottom:12px
}
.evidence-toggle ul {
  margin:0;
  padding-left:14px;
  display:grid;
  gap:7px
}
.evidence-toggle li {
  overflow-wrap:anywhere;
  color:var(--muted)
}
.evidence-toggle a {
  color:var(--accent)
}
.filters {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:18px;
  margin-bottom:22px
}
.filter-fields {
  display:flex;
  gap:10px;
  flex:1;
  min-width:0
}
.search-label {
  position:relative;
  max-width:340px;
  width:100%;
  min-width:0
}
.search-label svg {
  position:absolute;
  top:14px;
  left:14px;
  width:15px;
  height:15px;
  color:var(--muted)
}
.search-label input {
  width:100%;
  min-width:0
}
.filters input,.filters select {
  background:var(--surface);
  color:var(--ink);
  border:1px solid var(--line);
  border-radius:7px;
  min-height:44px;
  font-size:.74rem;
  padding:10px 12px
}
.filters .search-label input {
  padding-left:40px
}
.filters select {
  min-width:150px
}
.result-count {
  font-size:.68rem;
  color:var(--muted);
  white-space:nowrap
}
.sr-only {
  position:absolute;
  width:1px;
  height:1px;
  padding:0;
  margin:-1px;
  overflow:hidden;
  clip:rect(0,0,0,0);
  white-space:nowrap;
  border:0
}
.repositories {
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:16px
}
.repo {
  border:1px solid var(--line);
  border-radius:12px;
  padding:25px;
  display:flex;
  flex-direction:column;
  transition:border-color .2s,background .2s;
  background:var(--surface);
  min-width:0
}
.repo:hover {
  border-color:#77707f;
  background:#1d1d23
}
.repo-top {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:15px;
  margin-bottom:24px
}
.repo-owner {
  font-family:ui-monospace,SFMono-Regular,Consolas,monospace;
  font-size:.62rem;
  color:var(--muted);
  overflow-wrap:anywhere
}
.repo-arrow {
  font-size:1.1rem;
  color:var(--muted)
}
.repo h3 {
  font-size:1.1rem;
  overflow-wrap:anywhere;
  line-height:1.4
}
.repo p {
  font-size:.8rem;
  line-height:1.8;
  margin-top:12px;
  overflow-wrap:anywhere
}
.repo-tags {
  display:flex;
  flex-wrap:wrap;
  gap:6px;
  margin-block:21px
}
.tag {
  display:inline-flex;
  background:#24252b;
  border:1px solid #3a3a43;
  border-radius:5px;
  padding:3px 7px;
  color:#c6c3d0;
  font-size:.58rem;
  overflow-wrap:anywhere;
  max-width:100%
}
.repo-meta {
  border-top:1px solid var(--line);
  padding-top:14px;
  margin-top:auto;
  display:flex;
  align-items:center;
  flex-wrap:wrap;
  gap:14px;
  color:var(--muted);
  font-size:.64rem
}
.language {
  display:flex;
  align-items:center;
  gap:6px
}
.language:before {
  content:"";
  width:5px;
  height:5px;
  border-radius:50%;
  background:var(--accent)
}
.empty {
  border:1px dashed var(--line);
  border-radius:12px;
  text-align:center;
  padding:40px;
  font-size:.85rem
}
.insights {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:24px
}
.insight h3 {
  font-size:1.08rem;
  margin-bottom:24px
}
.insight ul {
  list-style:none;
  margin:0;
  padding:0;
  display:grid;
  gap:22px
}
.insight li {
  display:grid;
  grid-template-columns:22px 1fr;
  gap:10px;
  font-size:.8rem;
  color:var(--muted);
  line-height:1.8
}
.insight li span:first-child {
  color:var(--green)
}
.insight:last-child li span:first-child {
  color:var(--accent)
}
.evidence-grid {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:24px
}
.evidence-group {
  min-width:0
}
.evidence-group>h3 {
  font-size:1rem;
  padding-bottom:18px;
  border-bottom:1px solid var(--line)
}
.evidence-group>h3 span {
  font-family:ui-monospace,monospace;
  font-size:.65rem;
  color:var(--muted);
  margin-left:10px;
  letter-spacing:0
}
.source-row {
  border-bottom:1px solid var(--line);
  font-size:.73rem
}
.source-row summary {
  padding:17px 24px 17px 0;
  position:relative;
  list-style:none;
  overflow-wrap:anywhere;
  color:#d0ced5
}
.source-row summary::-webkit-details-marker {
  display:none
}
.source-row summary:after {
  content:"+";
  position:absolute;
  right:2px;
  top:16px;
  color:var(--muted)
}
.source-row[open] summary:after {
  content:"−"
}
.source-data {
  display:grid;
  gap:8px;
  padding-bottom:20px;
  color:var(--muted);
  font-size:.7rem;
  overflow-wrap:anywhere
}
.source-data strong {
  color:#d0ced5;
  font-weight:500
}
.source-data ul {
  margin:0;
  padding-left:17px
}
.footer {
  padding-block:40px;
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:24px
}
.footer p {
  font-size:.68rem;
  max-width:58ch;
  overflow-wrap:anywhere
}
.footer-links {
  display:flex;
  gap:22px;
  font-size:.7rem
}
.footer-links a {
  white-space:nowrap
}
.section-index {
  font-family:ui-monospace,monospace;
  font-size:.6rem;
  margin-right:9px
}
.back-top {
  color:var(--accent)
}
.quiet-state {
  font-size:.78rem;
  color:var(--muted);
  padding:20px 0
}

@media(min-width:1450px) {
  .hero {
  padding-top:110px;
  padding-bottom:90px
}

}
@media(max-width:1000px) {
  .container {
  width:calc(100% - 48px)
}
.hero {
  gap:35px;
  padding-top:62px
}
h1 {
  font-size:clamp(3rem,6.8vw,5rem)
}
.intro {
  gap:40px
}
.focus-layout {
  grid-template-columns:1.2fr 1fr
}
.focus-list {
  grid-template-columns:1fr
}
.skills {
  grid-template-columns:repeat(2,1fr)
}
.nav-links {
  gap:18px
}
.nav-source {
  display:none
}
.signal-card {
  padding:20px
}
.signal-card-bottom {
  font-size:.6rem
}
.section {
  padding-block:64px
}

}

@media(max-width:720px) {
  html {
  scroll-padding-top:125px
}
.container {
  width:calc(100% - 40px)
}
.nav {
  min-height:88px;
  align-items:flex-start;
  justify-content:center;
  flex-direction:column;
  gap:12px;
  padding-block:16px
}
.nav-links {
  width:100%;
  justify-content:space-between;
  gap:12px;
  font-size:.7rem
}
.brand {
  font-size:.88rem
}
.hero {
  grid-template-columns:1fr;
  padding-block:45px 40px;
  gap:35px
}
h1 {
  font-size:clamp(3.1rem,12.5vw,5.4rem)
}
.hero h1 {
  max-width:12ch
}
.hero-copy {
  font-size:.91rem;
  max-width:40ch
}
.hero-note {
  font-size:.64rem
}
.signal-card {
  max-width:510px;
  width:100%;
  margin-inline:auto;
  padding:22px
}
.signal-card svg {
  max-height:330px
}
.stats {
  grid-template-columns:repeat(2,1fr);
  gap:24px;
  padding-block:25px
}
.stat {
  padding-left:20px
}
.stat:nth-child(3) {
  border:0;
  padding-left:0
}
.stat strong {
  font-size:2rem
}
.stat span {
  font-size:.66rem
}
.section {
  padding-block:50px
}
.section-heading {
  align-items:flex-start;
  flex-direction:column;
  gap:18px;
  margin-bottom:28px
}
.section-heading>p {
  max-width:50ch;
  font-size:.78rem
}
.intro {
  grid-template-columns:1fr;
  gap:26px
}
.intro-copy {
  font-size:.86rem
}
.intro h2 {
  max-width:14ch
}
.focus-layout,.insights,.evidence-grid {
  grid-template-columns:1fr
}
.focus-list {
  grid-template-columns:1fr 1fr;
  gap:22px
}
.panel {
  padding:22px
}
.panel-title .label {
  font-size:.5rem
}
.skills {
  gap:12px
}
.skill {
  padding:18px
}
.skill h3 {
  font-size:.87rem
}
.skill .label {
  font-size:.48rem;
  letter-spacing:.09em;
  overflow-wrap:anywhere
}
.confidence {
  margin-left:0;
  width:100%;
  font-size:.57rem
}
.repositories {
  grid-template-columns:1fr
}
.repo {
  padding:22px
}
.filters {
  align-items:flex-start;
  flex-direction:column;
  gap:10px
}
.filter-fields {
  width:100%
}
.filters select {
  min-width:110px;
  width:110px;
  font-size:.68rem
}
.search-label {
  max-width:none
}
.filters input {
  font-size:.7rem
}
.footer {
  flex-direction:column
}
.footer-links {
  flex-wrap:wrap
}
.evidence-grid {
  gap:35px
}
.score-caption {
  font-size:.65rem;
  gap:8px
}
.signal-card-bottom {
  font-size:.65rem
}

}

@media(max-width:390px) {
  .focus-list,.skills {
  grid-template-columns:1fr
}
.confidence {
  margin-left:auto;
  width:auto
}
.skill h3 {
  min-height:0
}
.skill-value {
  margin-block:12px 9px
}
.actions {
  gap:9px
}
.button {
  font-size:.73rem;
  padding:12px 15px
}
.signal-card {
  padding:15px
}
.signal-card-bottom {
  font-size:.57rem
}
.label {
  font-size:.59rem
}
.nav-links {
  gap:9px;
  font-size:.65rem
}

}

@media(prefers-reduced-motion:reduce) {
  html {
  scroll-behavior:auto
}
* {
  transition:none!important
}

}
@media print {
  :root {
  color-scheme:light;
  --bg:#fff;
  --surface:#fff;
  --ink:#111;
  --muted:#444;
  --line:#bbb;
  --accent:#554080
}
body {
  font-size:10pt
}
.topbar {
  position:static;
  background:#fff
}
.nav-links,.actions,.filters,.back-top {
  display:none!important
}
.container {
  width:100%
}
.hero {
  padding:30px 0;
  gap:25px
}
.hero h1 {
  font-size:40pt
}
.signal-card {
  display:none
}
.hero {
  display:block
}
.hero-note {
  margin-top:12px
}
.section {
  padding-block:30px
}
.panel,.skill,.repo {
  background:#fff;
  break-inside:avoid
}
.repo[hidden] {
  display:flex!important
}
.repo p,.source-row summary,.score-caption span {
  color:#333
}
.tag {
  background:#eee;
  color:#333
}
.section-heading h2 {
  font-size:25pt
}
.stats {
  break-inside:avoid
}
.complexity-chart,.score-track {
  print-color-adjust:exact;
  -webkit-print-color-adjust:exact
}

}

"""

PROFILE_SCRIPT = r"""
(function () {
  "use strict";

  // The full repository list is the no-JavaScript default.
  const filters = document.getElementById("repository-filters");
  const search = document.getElementById("repository-search");
  const language = document.getElementById("repository-language");
  const count = document.getElementById("repository-count");
  const empty = document.getElementById("repository-empty");
  const cards = Array.from(document.querySelectorAll(".repo"));

  if (filters && search && language && count && empty) {
    function apply() {
      const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(function (card) {
        const content = card.textContent.toLocaleLowerCase();
        const matches = terms.every(function (term) { return content.includes(term); }) &&
          (!language.value || card.dataset.language === language.value);
        card.hidden = !matches;
        if (matches) visible++;
      });
      count.textContent = visible + " of " + cards.length + " repositories";
      empty.hidden = visible !== 0;
    }
    filters.hidden = false;
    search.addEventListener("input", apply);
    language.addEventListener("change", apply);
    apply();
  }

  if ("IntersectionObserver" in window) {
    const links = Array.from(document.querySelectorAll('.nav-links a[href^="#"]'));
    const visible = new Map();
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { visible.set(entry.target.id, entry.isIntersecting); });
      const current = links.find(function (link) { return visible.get(link.hash.slice(1)); });
      links.forEach(function (link) {
        if (link === current) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    }, { rootMargin: "-18% 0px -52% 0px", threshold: 0 });
    links.forEach(function (link) {
      const section = document.getElementById(link.hash.slice(1));
      if (section) observer.observe(section);
    });
  }

  // Print all evidence, then restore the reader's expansion choices.
  let printDetails = [];
  window.addEventListener("beforeprint", function () {
    printDetails = Array.from(document.querySelectorAll("details:not([open])"));
    printDetails.forEach(function (detail) { detail.open = true; });
  });
  window.addEventListener("afterprint", function () {
    printDetails.forEach(function (detail) { detail.open = false; });
    printDetails = [];
  });
})();
"""

PROFILE_HTML = (
    r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#111214">
<meta name="description" content="Explore {{ profile.username }}'s IoT engineering profile: public repository signals, focus areas, skills and source evidence. Generated {{ profile.generated_at.strftime('%B %d, %Y') }}.">
<title>{{ profile.username }} — IoT Engineering Profile</title>
<style>"""
    + PROFILE_STYLE
    + r"""</style>
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
<nav class="container nav" aria-label="Main navigation">
<a class="brand" href="#top">
<span class="brand-mark" aria-hidden="true">
<i>
</i>
<i>
</i>
<i>
</i>
<i>
</i>
</span>IoT / Engineering profile</a>
<div class="nav-links">
<a href="#overview">Overview</a>
<a href="#capabilities">Capabilities</a>
<a href="#repositories">Repositories</a>
<a href="#evidence">Evidence</a>
<a class="nav-source" href="https://github.com/{{ profile.username|urlencode }}">GitHub ↗</a>
</div>
</nav>
</header>
<main id="main" class="container">
<section class="hero" aria-labelledby="hero-title">
<div>
<p class="label eyebrow">
<span class="status-dot" aria-hidden="true">
</span>Public repository snapshot · {{ profile.generated_at.strftime('%b %Y') }}</p>
<h1 id="hero-title">Engineering,<br>
<span>in evidence.</span>
</h1>
<p class="hero-copy">A closer look at <a href="https://github.com/{{ profile.username|urlencode }}">
<strong>@{{ profile.username }}</strong>
</a>’s IoT work. Explore the repositories, technical focus and implementation signals behind this profile.</p>
<div class="actions">
<a class="button button-primary" href="#repositories">Explore the work <span aria-hidden="true">↗</span>
</a>
<a class="button button-secondary" href="#capabilities">View capabilities <span aria-hidden="true">↓</span>
</a>
</div>
<p class="hero-note">Generated {{ profile.generated_at.strftime('%B %d, %Y') }} · A dated analysis of public code.</p>
</div>
<div class="signal-card">
<div class="signal-card-top">
<span class="label">The profile, at a glance</span>
<span class="signal-window" aria-hidden="true">
<i>
</i>
<i>
</i>
<i>
</i>
</span>
</div>
<svg viewBox="0 0 440 332" role="img" aria-labelledby="signal-title signal-description">
<title id="signal-title">From repository evidence to an engineering profile</title>
<desc id="signal-description">{{ profile.total_repos_analyzed }} public repositories scanned, with {{ profile.iot_repos_count }} identified as IoT-related. ESPHome and D-Bus analysis contributes evidence to {{ profile.skills|length }} skill assessments. This illustrates the analysis process, not a deployed system.</desc>
<defs>
<radialGradient id="signal-glow">
<stop stop-color="#ac90ee" stop-opacity=".2"/>
<stop offset="1" stop-color="#ac90ee" stop-opacity="0"/>
</radialGradient>
<linearGradient id="signal-edge" x2="1" y2="1">
<stop stop-color="#a08bbb"/>
<stop offset="1" stop-color="#605869"/>
</linearGradient>
</defs>
<circle cx="220" cy="170" r="150" fill="url(#signal-glow)"/>
<g fill="none" stroke="#8f81a1" stroke-opacity=".18">
<circle cx="220" cy="170" r="63"/>
<circle cx="220" cy="170" r="106"/>
<circle cx="220" cy="170" r="147"/>
<path d="M18 170H422M220 20V320" stroke-dasharray="2 7"/>
</g>
<g fill="none" stroke="url(#signal-edge)" stroke-width="1.1">
<path d="M104 91L184 149M337 103L251 151M220 201V263"/>
<circle cx="220" cy="170" r="41"/>
</g>
<circle cx="220" cy="170" r="33" fill="#292331" stroke="#aa94cd" stroke-opacity=".5"/>
<g fill="#d5c2f8">
<rect x="207" y="157" width="10" height="10" rx="2"/>
<rect x="223" y="157" width="10" height="10" rx="2"/>
<rect x="207" y="173" width="10" height="10" rx="2"/>
<rect x="223" y="173" width="10" height="10" rx="2" opacity=".45"/>
</g>
<g font-family="Inter,system-ui,sans-serif">
<rect x="20" y="52" width="152" height="73" rx="10" fill="#24212b" stroke="#4e455b"/>
<text x="35" y="73" fill="#c4b9d3" font-size="8" letter-spacing="1">01 / REPOSITORIES</text>
<text x="35" y="104" fill="#eee8f6" font-size="23">{{ profile.total_repos_analyzed }}</text>
<text x="78" y="104" fill="#c2b9cf" font-size="9">sources scanned</text>
<rect x="274" y="68" width="146" height="73" rx="10" fill="#24212b" stroke="#4e455b"/>
<text x="289" y="89" fill="#c4b9d3" font-size="8" letter-spacing="1">02 / IOT SIGNALS</text>
<text x="289" y="120" fill="#eee8f6" font-size="23">{{ profile.iot_repos_count }}</text>
<text x="331" y="120" fill="#c2b9cf" font-size="9">related repos</text>
<rect x="132" y="250" width="178" height="66" rx="10" fill="#2d2738" stroke="#736183"/>
<text x="149" y="272" fill="#d3c2e9" font-size="8" letter-spacing="1">03 / ENGINEERING PROFILE</text>
<text x="149" y="299" fill="#eee8f6" font-size="20">{{ profile.skills|length }}</text>
<text x="178" y="297" fill="#d4c6e4" font-size="10">skills with source evidence</text>
</g>
<g fill="#c6b5ff">
<circle cx="154" cy="127" r="3"/>
<circle cx="289" cy="136" r="3"/>
<circle cx="220" cy="227" r="3"/>
</g>
</svg>
<div class="signal-card-bottom">
<span>
<strong>Public code.</strong> Traceable signals.</span>
<span>{{ profile.generated_at.strftime('%Y.%m.%d') }}</span>
</div>
</div>
</section>
<div class="stats" aria-label="Scan totals">
<div class="stat">
<strong>{{ profile.total_repos_analyzed }}</strong>
<span>Public repositories scanned</span>
</div>
<div class="stat">
<strong>{{ profile.iot_repos_count }}</strong>
<span>IoT-related repositories</span>
</div>
<div class="stat">
<strong>{{ profile.esphome_analyses|length }}</strong>
<span>ESPHome configurations</span>
</div>
<div class="stat">
<strong>{{ profile.dbus_analyses|length }}</strong>
<span>D-Bus analysis records</span>
</div>
</div>
<section class="section intro" id="overview" aria-labelledby="overview-title">
<div>
<span class="label">
<span class="section-index">01</span>Overview</span>
<h2 id="overview-title">The work behind<br>the profile.</h2>
</div>
<div class="intro-copy">

{% if profile.narrative_summary %}

{% set paragraphs = profile.narrative_summary.split('\n\n') %}
<p>{{ paragraphs[0] }}</p>
{% if paragraphs|length > 1 %}
<details class="summary-more">
<summary>Read the full analysis</summary>
{% for paragraph in paragraphs[1:] %}
<p>{{ paragraph }}</p>
{% endfor %}
</details>
{% endif %}

{% else %}
<p>This profile collects repository metadata, IoT focus scores and implementation evidence from the analyzed public code.</p>
{% endif %}

<p class="snapshot-note">This is a snapshot from {{ profile.generated_at.strftime('%B %d, %Y') }}. Scores are automated assessments of repository signals, not independent proficiency ratings or deployment verification. Repository descriptions are recorded as they appeared in the scan.</p>
</div>
</section>
<section class="section" id="capabilities" aria-labelledby="capabilities-title">
<div class="section-heading">
<div>
<span class="label">
<span class="section-index">02</span>Capabilities</span>
<h2 id="capabilities-title">Technical focus.<br>Visible evidence.</h2>
</div>
<p>Explore the distribution of work and the repository evidence attached to each skill.</p>
</div>
<div class="focus-layout">
<div class="panel">
<div class="panel-title">
<h3>Focus areas</h3>
<span class="label">Independent scores / 100</span>
</div>
<div class="focus-list">
{% for area, score in profile.focus_areas.items()|sort(attribute='1', reverse=True) %}
<div>
<div class="score-caption">
<span>{{ area.value.replace('_', ' ').title() }}</span>
<strong>{{ '%.0f'|format(score * 100) }}%</strong>
</div>
<div class="score-track" aria-hidden="true">
<i style="width:{{ [0, [score * 100, 100]|min]|max }}%">
</i>
</div>
</div>
{% else %}
<p class="quiet-state">No focus scores in this snapshot.</p>
{% endfor %}
</div>
</div>
<div class="panel">
<div class="panel-title">
<h3>Code complexity</h3>
<span class="label">Analysis records</span>
</div>
{% set total = profile.complexity_distribution.values()|sum %}
<div class="complexity-chart" aria-hidden="true">
{% for level, count in profile.complexity_distribution.items() %}
<span style="flex:{{ [count, 0]|max }}">
</span>
{% endfor %}
</div>
<div class="complexity-list">
{% for level, count in profile.complexity_distribution.items() %}
<div class="complexity-row">
<i aria-hidden="true">
</i>
<span>{{ level.value.capitalize() }}</span>
<strong>{{ count }}</strong>
<span>records</span>
</div>
{% else %}
<p class="quiet-state">No complexity data in this snapshot.</p>
{% endfor %}
</div>
<p class="chart-note">{{ total }} classified analysis records from IoT repositories, ESPHome configurations and D-Bus analyses. Complexity reflects detected code patterns. Focus scores measure overlapping areas and do not add up to 100%.</p>
</div>
</div>
<div class="skills">
{% for skill in profile.skills|sort(attribute='proficiency', reverse=True) %}
<article class="skill">
<span class="label">{{ skill.category.replace('_', ' ') }}</span>
<h3>{{ skill.name }}</h3>
<div class="skill-value">
<strong>{{ skill.proficiency }}</strong>
<span>/ 10</span>
<small class="confidence">{{ '%.0f'|format(skill.confidence * 100) }}% assessment confidence</small>
</div>
<div class="score-track" aria-hidden="true">
<i style="width:{{ [0, [skill.proficiency * 10, 100]|min]|max }}%">
</i>
</div>
<details class="evidence-toggle">
<summary>{{ skill.evidence|length }} source references</summary>
<ul>
{% for evidence in skill.evidence %}

{% set matched = profile.top_repositories|selectattr('full_name', 'equalto', evidence)|list %}
{% if not matched %}
{% set matched = profile.top_repositories|selectattr('name', 'equalto', evidence)|list %}
{% endif %}
<li>
{% if matched|length == 1 %}
<a href="https://github.com/{{ matched[0].full_name|urlencode }}">{{ evidence }} ↗</a>
{% else %}
{{ evidence }}
{% endif %}
</li>
{% endfor %}
</ul>
</details>
</article>
{% endfor %}
</div>
</section>
<section class="section" id="repositories" aria-labelledby="repositories-title">
<div class="section-heading">
<div>
<span class="label">
<span class="section-index">03</span>Selected work</span>
<h2 id="repositories-title">Explore the repositories.</h2>
</div>
<p>The top repositories retained in this scan, with their original descriptions and source links.</p>
</div>
<div class="filters" id="repository-filters" hidden>
<div class="filter-fields">
<label class="search-label">
<span class="sr-only">Search repositories</span>
<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" aria-hidden="true">
<circle cx="8" cy="8" r="5.5"/>
<path d="m12 12 5 5"/>
</svg>
<input id="repository-search" type="search" placeholder="Search name, topic or description" autocomplete="off">
</label>
<label>
<span class="sr-only">Filter by language</span>
<select id="repository-language">
<option value="">All languages</option>
{% for language in profile.top_repositories|map(attribute='language')|select|unique|sort %}
<option>{{ language }}</option>
{% endfor %}
</select>
</label>
</div>
<span class="result-count" id="repository-count" role="status" aria-live="polite">{{ profile.top_repositories|length }} repositories</span>
</div>
<div class="repositories">
{% for repo in profile.top_repositories %}
<article class="repo" data-language="{{ repo.language or '' }}">
<div class="repo-top">
<span class="repo-owner">{{ repo.full_name.split('/')[0] }} /</span>
<span class="repo-arrow" aria-hidden="true">↗</span>
</div>
<h3>
<a href="https://github.com/{{ repo.full_name|urlencode }}">{{ repo.name }}</a>
</h3>
<p>{{ repo.description or 'No description was available in this snapshot.' }}</p>
<div class="repo-tags">
{% for topic in repo.topics[:6] %}
<span class="tag">{{ topic }}</span>
{% endfor %}

{% if repo.topics|length > 6 %}
<span class="tag">+{{ repo.topics|length - 6 }} topics</span>
{% endif %}
</div>
<span class="sr-only">{{ repo.topics|join(' ') }}</span>
<div class="repo-meta">
<span class="language">{{ repo.language or 'Unspecified' }}</span>
<span>{{ repo.complexity.value.capitalize() }} complexity</span>
<span>{{ '%.0f'|format(repo.iot_score * 100) }}% IoT relevance</span>
<span>{{ repo.stars }} stars</span>
</div>
</article>
{% else %}
<p class="quiet-state">No repositories were retained in this snapshot.</p>
{% endfor %}
</div>
<p class="empty" id="repository-empty" hidden>No repositories match these filters. Try another term or language.</p>
</section>

{% if profile.key_strengths or profile.growth_areas %}
<section class="section" aria-labelledby="insights-title">
<div class="section-heading">
<div>
<span class="label">Analysis notes</span>
<h2 id="insights-title">Strengths &amp; next directions.</h2>
</div>
<p>The scan’s conclusions, kept alongside the evidence they were derived from.</p>
</div>
<div class="insights">
<div class="panel insight">
<h3>Where the work is strongest</h3>
<ul>
{% for strength in profile.key_strengths %}
<li>
<span aria-hidden="true">↗</span>
<span>{{ strength }}</span>
</li>
{% endfor %}
</ul>
</div>
<div class="panel insight">
<h3>Suggested growth areas</h3>
<ul>
{% for area in profile.growth_areas %}
<li>
<span aria-hidden="true">→</span>
<span>{{ area }}</span>
</li>
{% endfor %}
</ul>
</div>
</div>
</section>
{% endif %}

<section class="section" id="evidence" aria-labelledby="evidence-title">
<div class="section-heading">
<div>
<span class="label">
<span class="section-index">04</span>Implementation evidence</span>
<h2 id="evidence-title">A closer look at the source.</h2>
</div>
<p>Expand a record to inspect the devices, components and interfaces detected by the analyzers.</p>
</div>
<div class="evidence-grid">
<div class="evidence-group">
<h3>ESPHome configurations <span>{{ profile.esphome_analyses|length }} records</span>
</h3>
{% for item in profile.esphome_analyses %}
<details class="source-row">
<summary>{{ item.file_path }}</summary>
<div class="source-data">
<p>
<strong>Devices:</strong> {{ item.devices|join(', ') or 'Not detected' }}</p>
<p>
<strong>Components:</strong> {{ item.components|length }} · <strong>Complexity:</strong> {{ item.complexity.value }}</p>
<p>
<strong>Focus:</strong> {{ item.focus_areas|map(attribute='value')|map('replace', '_', ' ')|join(', ') or 'Not classified' }}</p>
{% if item.components %}
<ul>
{% for component in item.components %}
<li>{{ component.type }}
{% if component.platform %}
 / {{ component.platform }}
{% endif %}

{% if component.name %}
: {{ component.name }}
{% endif %}
</li>
{% endfor %}
</ul>
{% endif %}
<p>
<strong>Custom components:</strong> {{ item.custom_components|join(', ') or 'None detected' }}</p>
<p>
<strong>External libraries:</strong> {{ item.external_libs|join(', ') or 'None detected' }}</p>
</div>
</details>
{% else %}
<p class="quiet-state">No ESPHome records in this snapshot.</p>
{% endfor %}
</div>
<div class="evidence-group">
<h3>D-Bus analysis <span>{{ profile.dbus_analyses|length }} records</span>
</h3>
{% for item in profile.dbus_analyses %}
<details class="source-row">
<summary>{{ item.service_name }}</summary>
<div class="source-data">
<p>
<strong>Interfaces:</strong> {{ item.interfaces|length }} · <strong>Methods:</strong> {{ item.interfaces|map(attribute='methods')|map('length')|sum }} · <strong>Signals:</strong> {{ item.interfaces|map(attribute='signals')|map('length')|sum }}</p>
<p>
<strong>Object paths:</strong> {{ item.object_paths|join(', ') or 'Not detected' }}</p>
<p>
<strong>Complexity:</strong> {{ item.complexity.value }} · <strong>Focus:</strong> {{ item.focus_areas|map(attribute='value')|map('replace', '_', ' ')|join(', ') or 'Not classified' }}</p>
{% if item.interfaces %}
<ul>
{% for interface in item.interfaces %}
<li>{{ interface.name }} · {{ interface.path }}</li>
{% endfor %}
</ul>
{% endif %}
</div>
</details>
{% else %}
<p class="quiet-state">No D-Bus records in this snapshot.</p>
{% endfor %}
</div>
</div>
</section>
<footer class="footer">
<div>
<p>IoT Engineering Profile / @{{ profile.username }}<br>Generated {{ profile.generated_at.strftime('%B %d, %Y') }} from repository evidence. Check individual repositories for current documentation and installation requirements.</p>
</div>
<div class="footer-links">
<a href="https://github.com/4alvit/iot-project-builder-profile">About the generator ↗</a>
<a class="back-top" href="#top">Back to top ↑</a>
</div>
</footer>
</main>
<script>"""
    + PROFILE_SCRIPT
    + r"""</script>
</body>
</html>
"""
)
