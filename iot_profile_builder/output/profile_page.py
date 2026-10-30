"""Self-contained HTML presentation for generated engineering profiles."""

# ruff: noqa: E501
# Embedded HTML keeps related attributes and template expressions together.

from .profile_behavior import PROFILE_SCRIPT

PROFILE_STYLE = r"""
:root {
  color-scheme:dark;
  --bg:#0b0e13;
  --surface:#141a22;
  --ink:#f4f5f0;
  --muted:#aab3bf;
  --line:#2a343f;
  --accent:#c6b5ff;
  --green:#b5efd7;
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif
}

* {
  box-sizing:border-box
}
html {
  scroll-behavior:smooth;
  scroll-padding-top:calc(var(--site-header-height,90px) + 36px)
}
body {
  margin:0;
  background:radial-gradient(ellipse at 78% 8%,#29463822,transparent 33%),radial-gradient(ellipse at 9% 22%,#45356120,transparent 36%),var(--bg);
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
  font-size:clamp(3.4rem,6.9vw,6.5rem);
  max-width:11ch
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
  top:16px;
  z-index:20;
  width:min(1320px,calc(100% - 32px));
  margin:16px auto 0;
  border:1px solid #ffffff1a;
  border-radius:22px;
  background:rgba(20,26,34,.82);
  box-shadow:0 10px 40px #0003,inset 0 1px #ffffff09;
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px)
}
.nav {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  min-height:76px;
  width:calc(100% - 44px)
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
  gap:22px;
  font-size:.79rem;
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
  padding-block:98px 82px;
  display:grid;
  grid-template-columns:1.05fr 1fr;
  gap:42px;
  align-items:center;
  min-height:740px
}
.hero h1 {
  margin-top:24px
}
.hero h1 span {
  color:var(--green)
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
  border-radius:12px;
  font-size:.82rem;
  font-weight:600;
  border:1px solid var(--line)
}
.button-primary {
  background:var(--green);
  border-color:var(--green);
  color:#0b211a
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
  border:1px solid var(--line);
  border-radius:20px;
  background:linear-gradient(110deg,#ffffff04,#ffffff01);
  padding:30px;
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

/* The presentation remains complete before any enhancement is mounted. */
.hero-content { position:relative; z-index:1 }
.hero h1 { letter-spacing:-.062em; line-height:1.01 }
.hero h1 span { display:inline-block; margin-top:.08em }
.hero-copy { max-width:40ch; font-size:1.02rem }
.hero .eyebrow { font-size:.61rem; letter-spacing:.11em }
.nav-links a { white-space:nowrap; transition:color .2s }
.nav-links a[aria-current] { color:var(--green) }
.motion-toggle {
  flex-shrink:0; min-height:38px; padding:8px 11px; border:1px solid #ffffff20;
  border-radius:9px; background:#ffffff05; color:var(--muted); font-size:.64rem; cursor:pointer
}
.motion-toggle:hover,.motion-toggle:focus-visible { color:var(--ink); border-color:var(--accent) }
.motion-toggle:disabled { cursor:default; opacity:.6 }
.system-scene { position:relative; min-width:0; isolation:isolate }
.scene-eyebrow { display:flex; justify-content:space-between; gap:12px; padding:0 10px; align-items:center }
.scene-eyebrow .label { font-size:.58rem; color:#a7b5b0 }
.scene-date { color:#7d9489; font: .62rem ui-monospace,SFMono-Regular,Consolas,monospace }
.scene-space { position:relative; height:500px; transform-style:preserve-3d }
.scene-space::before {
  content:""; position:absolute; inset:8% -6%; z-index:-1;
  background-image:linear-gradient(#b5efd706 1px,transparent 1px),linear-gradient(90deg,#b5efd706 1px,transparent 1px);
  background-size:32px 32px; mask-image:radial-gradient(ellipse,#000 20%,transparent 70%)
}
.scene-orbits { position:absolute; width:112%; max-width:none; height:100%; left:-6%; top:0; overflow:hidden }
.scene-core {
  position:absolute; left:calc(50% - 38px); top:calc(50% - 38px); width:76px; height:76px;
  display:grid; place-items:center; border:1px solid #b5efd770; border-radius:22px;
  background:linear-gradient(140deg,#253b36,#101c1d); color:var(--green);
  box-shadow:0 0 65px #96f0c721,inset 0 1px #e8fff524; transform:rotate(-12deg)
}
.scene-core svg { width:46px; height:46px }
.floating-card {
  position:absolute; padding:20px 22px 18px; border:1px solid #ffffff24; border-radius:17px;
  background:linear-gradient(135deg,#27312eed,#151e22f5); box-shadow:0 22px 42px #0005,inset 0 1px #ffffff0d;
  backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  transform:rotate(var(--card-rotate,0deg)); animation:card-float 7s ease-in-out infinite; animation-play-state:paused
}
.card-sources { left:1%; top:8%; width:50%; --card-rotate:-7deg; animation-delay:-1.5s }
.card-signals { right:-1%; top:43%; width:48%; --card-rotate:6deg; animation-delay:-3.8s; background:linear-gradient(135deg,#302c3eed,#191d29f5) }
.card-profile { left:6%; bottom:0; width:58%; --card-rotate:-3deg; animation-delay:-5.5s; background:linear-gradient(135deg,#252c34f5,#151c25f5) }
.card-index { display:block; font:.6rem ui-monospace,SFMono-Regular,Consolas,monospace; color:var(--green); letter-spacing:.04em }
.card-index span { color:#a3b5ae }
.card-signals .card-index { color:#d0c3fa }
.card-signals .card-index span { color:#b4aac8 }
.floating-value { display:flex; align-items:center; gap:15px; font-size:3.6rem; font-weight:500; line-height:1.12; letter-spacing:-.06em; margin-top:15px; font-variant-numeric:tabular-nums }
.floating-value>span { font-size:.64rem; line-height:1.5; letter-spacing:0; color:#bec8c5 }
.card-trace { display:flex; height:20px; align-items:flex-end; gap:5px; margin-top:15px }
.card-trace i { flex:1; height:5px; border-radius:2px; background:#b5efd755 }
.card-trace i:nth-child(3n) { height:12px; background:#b5efd788 }
.card-trace i:nth-child(3n+2) { height:8px }
.card-trace i:nth-last-child(2) { height:17px; background:#b5efd7 }
.card-tags { display:flex; flex-wrap:wrap; gap:5px; margin-top:14px }
.card-tags span { padding:3px 6px; border:1px solid #d2bef52e; border-radius:4px; font:.52rem ui-monospace,SFMono-Regular,Consolas,monospace; color:#d0c3e5 }
.card-footnote { display:flex; justify-content:space-between; gap:10px; border-top:1px solid #ffffff15; padding-top:11px; margin-top:14px; font-size:.55rem; color:#adb9c6 }
.scene-caption { display:flex; justify-content:center; align-items:center; gap:8px; margin-top:28px; font-size:.57rem; color:#81908d }
.scene-caption .status-dot { width:4px; height:4px; opacity:.7 }
.scene-flow { animation:scene-flow 16s linear infinite; animation-play-state:paused }
.is-in-view .floating-card,.is-in-view .scene-flow { animation-play-state:running }
@keyframes card-float { 0%,100% { transform:translateY(0) rotate(var(--card-rotate,0deg)) } 50% { transform:translateY(-8px) rotate(var(--card-rotate,0deg)) } }
@keyframes scene-flow { to { stroke-dashoffset:-120 } }
[data-tilt] { transform:perspective(1000px) rotateX(var(--tilt-x,0deg)) rotateY(var(--tilt-y,0deg)); transition:transform .22s ease,border-color .22s ease,background .22s ease }
[data-reveal] { opacity:1; transition:opacity .65s ease,transform .65s ease }
html.motion-ready [data-reveal]:not(.is-visible) { opacity:0; transform:translateY(18px) }
html.motion-ready [data-reveal]:focus-within { opacity:1; transform:none }
html[data-motion="paused"] .floating-card,html[data-motion="paused"] .scene-flow { animation-play-state:paused }
html[data-motion="paused"] [data-tilt] { transform:none }
html[data-profile-loading] .topbar::after { content:""; position:absolute; bottom:0; left:8%; right:8%; height:2px; background:var(--green); opacity:.8 }
.page-lead { padding:96px 0 34px; max-width:780px }
.page-lead h1 { max-width:13ch; margin:28px 0; font-size:clamp(3.8rem,7.5vw,7rem); letter-spacing:-.06em; line-height:1.03 }
.page-lead h1 span { color:var(--green) }
.page-lead>p:not(.label) { max-width:58ch; font-size:1rem; line-height:1.8 }
.text-link { display:inline-flex; gap:14px; font-size:.76rem; color:var(--green); padding:15px 0; margin-top:10px }
.page-lead+.section { padding-top:48px }
.repo { border-radius:18px; background:linear-gradient(135deg,#192129,#141a21); box-shadow:inset 0 1px #ffffff04 }
.repo:hover { border-color:#77877e; background:linear-gradient(135deg,#202a32,#171e26) }
.github-metadata { margin-top:16px; border-top:1px solid #ffffff0a; padding-top:14px }
.github-counts { display:flex; flex-wrap:wrap; column-gap:16px; row-gap:7px; color:#9faeb7; font-size:.64rem }
.github-counts strong { color:#e0e7e6; font-weight:500 }
.github-status-row { display:flex; align-items:flex-start; gap:16px; margin-top:11px }
.github-status-row p { margin:0; color:#8e9ca5; font-size:.6rem; line-height:1.6; flex:1 }
.github-status-row button { flex-shrink:0; min-height:32px; padding:5px 9px; background:#ffffff04; border:1px solid #ffffff20; border-radius:6px; color:#c4d6cf; font-size:.61rem; cursor:pointer }
.github-status-row button:hover { border-color:var(--green) }
.github-status-row button:disabled { opacity:.55; cursor:wait }
@media(min-width:1450px) { .hero { min-height:800px } }
@media(max-width:1150px) {
  .nav { gap:16px }
  .nav-links { gap:16px }
  .brand-detail { display:none }
  .scene-space { height:450px }
  .floating-card { padding:18px }
  .floating-value { font-size:3.1rem; gap:10px }
}
@media(max-width:1000px) {
  .hero { min-height:650px; padding-block:70px 64px; gap:26px }
  .scene-space { height:400px }
  .floating-card { padding:15px }
  .floating-value { font-size:2.7rem; gap:9px }
  .floating-value>span { font-size:.58rem }
  .card-index { font-size:.53rem }
  .card-tags span { font-size:.47rem; padding:2px 4px }
  .card-profile { width:62% }
  .card-footnote { font-size:.48rem }
  .scene-eyebrow { padding:0 }
  .scene-eyebrow .label { font-size:.5rem }
}
@media(max-width:760px) {
  html { scroll-padding-top:calc(var(--site-header-height,120px) + 28px) }
  .topbar { top:10px; width:calc(100% - 24px); margin-top:10px; border-radius:17px }
  .nav { width:calc(100% - 30px); min-height:108px; flex-wrap:wrap; flex-direction:row; justify-content:space-between; align-items:center; gap:0 12px; padding:12px 0 }
  .brand { font-size:.86rem; order:0 }
  .brand-detail { display:inline }
  .motion-toggle { order:1; font-size:.57rem; min-height:32px; padding:5px 8px }
  .nav-links { order:2; width:100%; justify-content:space-between; gap:14px; font-size:.69rem; margin-top:5px }
  .nav-capabilities { display:none }
  .nav-source { display:block; padding:5px 10px }
  .hero { grid-template-columns:1fr; min-height:0; gap:50px; padding:62px 0 45px }
  .hero h1 { max-width:12ch; font-size:clamp(3.3rem,9.5vw,5.5rem) }
  .hero-copy { max-width:46ch; font-size:.93rem }
  .system-scene { max-width:500px; width:100%; margin-inline:auto }
  .scene-space { height:450px }
  .scene-orbits { width:100%; left:0 }
  .scene-space::before { inset:8% 0 }
  .floating-card { padding:20px }
  .floating-value { font-size:3.5rem; gap:15px }
  .floating-value>span { font-size:.65rem }
  .card-index { font-size:.6rem }
  .card-tags span { font-size:.52rem; padding:3px 6px }
  .card-profile { width:58% }
  .card-footnote { font-size:.55rem }
  .scene-eyebrow .label { font-size:.55rem }
  .stats { padding:25px; gap:24px }
  .page-lead { padding-top:62px }
  .page-lead h1 { font-size:clamp(3.5rem,12vw,5.5rem) }
}
@media(max-width:420px) {
  .container { width:calc(100% - 32px) }
  .nav { width:calc(100% - 24px) }
  .brand-detail { display:none }
  .nav-links { gap:8px; font-size:.65rem }
  .nav-source { padding:5px 8px; font-size:.61rem }
  .hero { padding-top:48px; gap:42px }
  .hero h1 { font-size:clamp(3.05rem,12.6vw,4.5rem) }
  .hero .eyebrow { font-size:.51rem; letter-spacing:.08em }
  .hero-copy { font-size:.88rem }
  .scene-space { height:440px }
  .floating-card { padding:14px; border-radius:13px }
  .floating-value { font-size:2.7rem; gap:9px; margin-top:12px }
  .floating-value>span { font-size:.54rem }
  .card-index { font-size:.48rem }
  .card-tags { gap:3px; margin-top:10px }
  .card-tags span { font-size:.43rem; padding:3px 4px }
  .card-sources { width:52%; top:4% }
  .card-signals { top:38%; right:0 }
  .card-profile { width:60%; left:0 }
  .card-footnote { font-size:.45rem; gap:4px }
  .card-trace { gap:4px; margin-top:9px }
  .scene-core { width:58px; height:58px; left:calc(50% - 29px); top:calc(50% - 29px); border-radius:17px }
  .scene-core svg { width:36px; height:36px }
  .scene-caption { font-size:.5rem; margin-top:23px }
  .scene-date { font-size:.52rem }
  .stats { padding:20px }
  .stat strong { font-size:1.9rem }
  .stat span { font-size:.62rem }
  .repo { padding:20px }
}
@media(prefers-reduced-motion:reduce) {
  html { scroll-behavior:auto }
  *,*::before,*::after { animation:none!important; transition:none!important }
  html.motion-ready [data-reveal] { opacity:1; transform:none }
  [data-tilt] { transform:none!important }
}
@media print {
  body { background:#fff }
  .topbar { width:100%; margin:0; border:0; box-shadow:none; backdrop-filter:none }
  .nav { min-height:0; width:100%; padding:0 }
  .system-scene,.motion-toggle,.github-status-row button { display:none!important }
  .hero { min-height:0 }
  .stats,.repo { background:#fff; box-shadow:none }
  .page-lead { padding:20px 0 }
  .page-lead h1 { font-size:36pt }
  html.motion-ready [data-reveal] { opacity:1!important; transform:none!important }
  [data-tilt] { transform:none!important }
  *,*::before,*::after { animation:none!important; transition:none!important }
  .github-counts,.github-counts strong,.github-status-row p { color:#444 }
}

"""


PROFILE_HTML = (
    r"""{% set current_page = page_kind|default('overview') %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0e13">
<meta http-equiv="Content-Security-Policy" content="{{ content_security_policy|default("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self'; connect-src 'self' https://api.github.com; base-uri 'none'; object-src 'none'; form-action 'none'") }}">
<meta name="description" content="Explore {{ profile.username }}'s IoT engineering profile: public repository signals, focus areas, skills and source evidence. Generated {{ profile.generated_at.strftime('%B %d, %Y') }}.">
<title>{{ profile.username }} — {% if current_page == 'repositories' %}Repositories{% elif current_page == 'evidence' %}Source Evidence{% else %}IoT Engineering Profile{% endif %}</title>
<style>"""
    + PROFILE_STYLE
    + r"""</style>
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
<nav class="container nav" aria-label="Main navigation">
<a class="brand" href="{{ profile.username|urlencode }}_profile.html" data-nav-page="overview">
<span class="brand-mark" aria-hidden="true">
<i>
</i>
<i>
</i>
<i>
</i>
<i>
</i>
</span>IoT<span class="brand-detail"> / Engineering profile</span></a>
<div class="nav-links">
<a href="{{ profile.username|urlencode }}_profile.html" data-nav-page="overview"{% if current_page == 'overview' %} aria-current="page"{% endif %}>Overview</a>
<a class="nav-capabilities" href="{{ profile.username|urlencode }}_profile.html#capabilities">Capabilities</a>
<a href="repositories.html" data-nav-page="repositories"{% if current_page == 'repositories' %} aria-current="page"{% endif %}>Repositories</a>
<a href="evidence.html" data-nav-page="evidence"{% if current_page == 'evidence' %} aria-current="page"{% endif %}>Evidence</a>
<a class="nav-source" href="https://github.com/{{ profile.username|urlencode }}">GitHub ↗</a>
</div>
<button class="motion-toggle" type="button" data-motion-toggle aria-pressed="false" hidden>Pause motion</button>
</nav>
</header>
<p class="sr-only" id="profile-navigation-status" role="status" aria-live="polite"></p>
<main id="main" class="container" data-profile-version="2" data-profile-page="{{ current_page }}" data-profile-user="{{ profile.username }}" data-profile-generated="{{ profile.generated_at.isoformat() }}">
{% if current_page == 'overview' %}
<section class="hero" aria-labelledby="hero-title">
<div class="hero-content" data-reveal>
<p class="label eyebrow">
<span class="status-dot" aria-hidden="true">
</span>Public repository snapshot · {{ profile.generated_at.strftime('%b %Y') }}</p>
<h1 id="hero-title">Connected systems.<br>
<span>Clear evidence.</span>
</h1>
<p class="hero-copy">A closer look at <a href="https://github.com/{{ profile.username|urlencode }}">
<strong>@{{ profile.username }}</strong>
</a>’s IoT work. Explore the repositories, technical focus and implementation signals behind this profile.</p>
<div class="actions">
<a class="button button-primary" href="repositories.html" data-nav-page="repositories">Explore the work <span aria-hidden="true">↗</span>
</a>
<a class="button button-secondary" href="#capabilities">View capabilities <span aria-hidden="true">↓</span>
</a>
</div>
<p class="hero-note">Generated {{ profile.generated_at.strftime('%B %d, %Y') }} · A dated analysis of public code.</p>
</div>
<div class="system-scene" data-scene data-reveal>
<div class="scene-eyebrow"><span class="label">From code to capability</span><span class="scene-date">{{ profile.generated_at.strftime('%Y.%m.%d') }}</span></div>
<div class="scene-space" data-tilt>
<svg class="scene-orbits" viewBox="0 0 520 500" role="img" aria-labelledby="signal-title signal-description">
<title id="signal-title">From repository evidence to an engineering profile</title>
<desc id="signal-description">{{ profile.total_repos_analyzed }} public repositories scanned, with {{ profile.iot_repos_count }} identified as IoT-related. ESPHome and D-Bus analysis contributes evidence to {{ profile.skills|length }} skill assessments. This illustrates the analysis process, not a deployed system.</desc>
<defs>
<radialGradient id="scene-glow"><stop stop-color="#b5efd7" stop-opacity=".15"/><stop offset="1" stop-color="#b5efd7" stop-opacity="0"/></radialGradient>
<linearGradient id="scene-line"><stop stop-color="#b5efd7" stop-opacity=".6"/><stop offset="1" stop-color="#c6b5ff" stop-opacity=".2"/></linearGradient>
</defs>
<circle cx="260" cy="250" r="245" fill="url(#scene-glow)"/>
<g fill="none" stroke="#b5efd7" stroke-opacity=".12"><ellipse cx="260" cy="250" rx="230" ry="190" transform="rotate(-24 260 250)"/><ellipse cx="260" cy="250" rx="168" ry="220" transform="rotate(35 260 250)"/><circle cx="260" cy="250" r="122"/><path d="M10 250H510M260 10V490" stroke-dasharray="2 8"/></g>
<g fill="none" stroke="url(#scene-line)" stroke-width="1.5"><path class="scene-flow" d="M120 137C240 135 154 244 260 250S368 288 404 286M260 250C255 340 142 305 179 405" stroke-dasharray="5 7"/></g>
<g fill="#b5efd7"><circle cx="118" cy="137" r="4"/><circle cx="405" cy="286" r="4"/><circle cx="180" cy="406" r="4"/></g>
</svg>
<div class="scene-core" aria-hidden="true"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="16" y="16" width="16" height="16" rx="4"/><path d="M24 4V16M24 32V44M4 24H16M32 24H44M10 10L17 17M31 31L38 38M38 10L31 17M17 31L10 38"/><circle cx="24" cy="24" r="3"/></svg></div>
<div class="floating-card card-sources">
<span class="card-index">01 <span> / Sources</span></span>
<div class="floating-value">{{ profile.total_repos_analyzed }}<span>public repositories<br>scanned</span></div>
<div class="card-trace" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
</div>
<div class="floating-card card-signals">
<span class="card-index">02 <span> / Connections</span></span>
<div class="floating-value">{{ profile.iot_repos_count }}<span>IoT-related<br>repositories</span></div>
<div class="card-tags"><span>ESPHome</span><span>D-Bus</span><span>IoT</span></div>
</div>
<div class="floating-card card-profile">
<span class="card-index">03 <span> / The profile</span></span>
<div class="floating-value">{{ profile.skills|length }}<span>skill assessments<br>with source evidence</span></div>
<span class="card-footnote">Patterns, grounded in public code <span aria-hidden="true">↗</span></span>
</div>
</div>
<p class="scene-caption"><span class="status-dot" aria-hidden="true"></span>Analysis pipeline illustration · a dated snapshot</p>
</div>
</section>
<div class="stats" aria-label="Scan totals" data-reveal>
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
<section class="section intro" id="overview" aria-labelledby="overview-title" data-reveal>
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
<section class="section" id="capabilities" aria-labelledby="capabilities-title" data-reveal>
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
{% endif %}
{% if current_page != 'overview' %}
<section class="page-lead" data-reveal aria-labelledby="page-title">
<p class="label eyebrow"><span class="status-dot" aria-hidden="true"></span>@{{ profile.username }} / Public code, in context</p>
<h1 id="page-title">{% if current_page == 'repositories' %}The work.<br><span>In the open.</span>{% else %}Follow<br><span>the evidence.</span>{% endif %}</h1>
<p>{% if current_page == 'repositories' %}Explore the projects behind the profile. Source descriptions and analysis stay tied to their snapshot; public GitHub activity can be checked independently.{% else %}Look inside the configuration and service records that informed the analysis. Every entry below comes from the public code scanned for this profile.{% endif %}</p>
<a class="text-link" href="{{ profile.username|urlencode }}_profile.html" data-nav-page="overview">Back to the full profile <span aria-hidden="true">↗</span></a>
</section>
{% endif %}
{% if current_page in ('overview', 'repositories') %}
<section class="section" id="repositories" aria-labelledby="repositories-title" data-reveal>
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
<article class="repo" data-language="{{ repo.language or '' }}" data-tilt>
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
</div>
<div class="github-metadata" data-github-repo="{{ repo.full_name }}">
<div class="github-counts"><span><strong data-github-stars>{{ repo.stars }}</strong> stars</span><span><strong data-github-forks>{{ repo.forks }}</strong> forks</span><span>Updated <span data-github-updated>{{ repo.updated_at.strftime('%b %d, %Y') }}</span></span></div>
<div class="github-status-row"><p data-github-status role="status">Snapshot · {{ profile.generated_at.strftime('%b %d, %Y') }}. Live GitHub values are checked separately.</p><button type="button" data-github-refresh hidden>Refresh</button></div>
</div>
</article>
{% else %}
<p class="quiet-state">No repositories were retained in this snapshot.</p>
{% endfor %}
</div>
<p class="empty" id="repository-empty" hidden>No repositories match these filters. Try another term or language.</p>
</section>

{% endif %}
{% if current_page == 'overview' and (profile.key_strengths or profile.growth_areas) %}
<section class="section" aria-labelledby="insights-title" data-reveal>
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

{% if current_page in ('overview', 'evidence') %}
<section class="section" id="evidence" aria-labelledby="evidence-title" data-reveal>
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
{% endif %}
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
