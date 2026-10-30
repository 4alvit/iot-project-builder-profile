/** Real-browser controller regressions; local documents and mocked public API only. */
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { mkdtemp, readFile, rm, writeFile, mkdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const engines = require(process.env.CI_PLAYWRIGHT_MODULE || process.env.PROFILE_PLAYWRIGHT_MODULE || 'playwright');
const root = fileURLToPath(new URL('../../', import.meta.url));
const fixtureDir = await mkdtemp(path.join(tmpdir(), 'profile-experience-'));
const localPython = path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const python = process.env.PROFILE_PYTHON || (existsSync(localPython) ? localPython : 'python');
execFileSync(python, ['-c', `
from datetime import datetime, timezone
from pathlib import Path
import sys
from iot_profile_builder.models import EngineeringProfile, RepositoryMetrics, ComplexityLevel, FocusArea, SkillAssessment
from iot_profile_builder.output.renderer import ProfileRenderer
stamp = datetime(2026, 1, 2, tzinfo=timezone.utc)
def repo(name, language):
    return RepositoryMetrics(name=name, full_name='example/' + name, description='Synthetic public project for browser checks.', stars=7, forks=3, language=language, topics=['mqtt'], is_fork=False, created_at=stamp, updated_at=stamp, size_kb=10, complexity=ComplexityLevel.LOW, focus_areas=[FocusArea.HOME_AUTOMATION], iot_score=0.7)
profile = EngineeringProfile(username='fixture', generated_at=stamp, total_repos_analyzed=7, iot_repos_count=4, top_repositories=[repo('alpha','Python'),repo('beta','Rust'),repo('gamma','Go'),repo('alpha','Python')], skills=[SkillAssessment('Home automation','automation',7,['alpha'],0.8)], focus_areas={FocusArea.HOME_AUTOMATION:0.8}, complexity_distribution={ComplexityLevel.LOW:3}, narrative_summary='A synthetic profile for browser acceptance checks.', key_strengths=['Public source evidence'], growth_areas=['More fixtures'])
renderer = ProfileRenderer()
for name in ('overview','repositories','evidence'):
    renderer.render_html(profile, Path(sys.argv[1]) / (name + '.html'), page_kind=name)
`, fixtureDir], { cwd: root, stdio: 'pipe' });
const pages = new Map(await Promise.all(['overview', 'repositories', 'evidence'].map(async name => [name, await readFile(path.join(fixtureDir, name + '.html'), 'utf8')])));
function html(page, extra = '', version = '2', user = 'fixture') {
  // The production renderer supplies all markup, styling, CSP and executable code.
  // Only test links and adversarial imported content are inserted into its result.
  return pages.get(page).replace('data-profile-version="2"', `data-profile-version="${version}"`).replace('data-profile-user="fixture"', `data-profile-user="${user}"`)
    .replace('</header>', '</header><a id="native" href="native.html">Native</a>')
    .replace('</main>', `<a href="#browser-bottom" id="jump">Bottom</a>${extra}<h2 id="browser-bottom" tabindex="-1" style="margin-top:1400px">Bottom heading</h2><details id="browser-details"><summary>Browser evidence details</summary>Details</details></main>`);
}
let overrides = new Map(), loads = [];
const server = createServer(async (request, response) => {
  const url = new URL(request.url, 'http://localhost'); loads.push(url.pathname);
  const value = overrides.get(url.pathname);
  if (value?.delay && (!value.onlyFetch || request.headers['sec-fetch-dest'] !== 'document')) await new Promise(resolve => setTimeout(resolve, value.delay));
  response.statusCode = value?.status || 200; response.setHeader('Content-Type', value?.type || 'text/html');
  const page = url.pathname.endsWith('repositories.html') ? 'repositories' : url.pathname.endsWith('evidence.html') ? 'evidence' : 'overview';
  response.end(value?.body ?? html(page));
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const browsers = (process.env.CI_BROWSER_ENGINE || process.env.PROFILE_BROWSERS || 'chromium,firefox,webkit').split(',');
const api = repo => ({ full_name: `example/${repo}`, private: false, html_url: `https://github.com/example/${repo}`, stargazers_count: 31, forks_count: 5, updated_at: '2026-10-29T12:00:00Z' });
let passed = 0;
const scenarios = [];
let runtimeIdentity;
async function check(name, browser, run) {
  overrides = new Map(); loads = [];
  const context = await browser.newContext({ viewport: { width: 1150, height: 900 } });
  if (process.env.CI_BROWSER_DIAGNOSTICS) await mkdir(process.env.CI_BROWSER_DIAGNOSTICS, { recursive: true });
  const page = await context.newPage(), errors = [], consoleErrors = [], requests = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  await context.route('https://api.github.com/**', async route => { requests.push(route.request()); await route.fulfill({ json: api(route.request().url().split('/').at(-1)) }); });
  try { await run({ page, context, requests }); assert.deepEqual(errors, [], 'No uncaught browser errors');
    if (process.env.CI_BROWSER_DIAGNOSTICS && consoleErrors.length) {
      await mkdir(process.env.CI_BROWSER_DIAGNOSTICS, { recursive: true });
      await writeFile(path.join(process.env.CI_BROWSER_DIAGNOSTICS, 'profile-console-' + passed + '.json'), JSON.stringify({ name, errors: consoleErrors }));
    }
    assert.deepEqual(consoleErrors.filter(error => !/Failed to load resource|429|403/.test(error) && !(name.includes('sanitization') && /inline event handler.*Content Security Policy|inline event handler.*script-src|inline event handler because it violates/.test(error))), [], 'No unexpected console errors'); passed++; scenarios.push(name); console.log(`PASS ${name}`); }
  catch (error) {
    if (process.env.CI_BROWSER_DIAGNOSTICS) {
      await mkdir(process.env.CI_BROWSER_DIAGNOSTICS, { recursive: true });
      await page.screenshot({ path: path.join(process.env.CI_BROWSER_DIAGNOSTICS, 'profile-failure.png'), fullPage: true }).catch(() => {});
      await writeFile(path.join(process.env.CI_BROWSER_DIAGNOSTICS, 'profile-failure.txt'), String(error));
    }
    throw error;
  } finally { await context.close(); }
}
try {
  for (const engine of browsers) {
    const browser = await engines[engine].launch({ headless: true, ...(process.env.CI_BROWSER_CHANNEL ? { channel: process.env.CI_BROWSER_CHANNEL } : {}) });
    runtimeIdentity = { engine: browser.browserType().name(), browserVersion: browser.version() };
    try {
      await check(`${engine}: transitions, history, filters and print`, browser, async ({ page, requests }) => {
        await page.goto(`${origin}/profile/index.html`);
        await page.evaluate(() => { window.documentToken = 'preserved'; window.headerToken = document.querySelector('.topbar'); });
        await page.click('.topbar [data-nav-page="repositories"]'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'repositories');
        assert.equal(await page.evaluate(() => window.documentToken === 'preserved' && window.headerToken === document.querySelector('.topbar')), true);
        await page.locator('[data-github-repo]').first().scrollIntoViewIfNeeded();
        await page.waitForFunction(() => document.querySelector('[data-github-stars]').textContent === '31');
        assert.equal(await page.locator('[data-github-updated]').first().textContent(), await page.evaluate(() => new Date('2026-10-29T12:00:00Z').toLocaleDateString()));
        assert.ok(requests.length >= 1); assert.equal(requests[0].headers().authorization, undefined); assert.equal(requests[0].headers().referer, undefined);
        assert.match(await page.title(), /repositor/i); assert.equal(await page.locator('.topbar [data-nav-page="repositories"]').getAttribute('aria-current'), 'page');
        assert.match(await page.locator('meta[name="description"]').getAttribute('content'), /fixture/); assert.ok(['H1', 'MAIN'].includes(await page.evaluate(() => document.activeElement.tagName)));
        await page.fill('#repository-search', 'beta'); assert.equal(await page.locator('.repo:visible').count(), 1);
        await page.fill('#repository-search', ''); await page.selectOption('#repository-language', 'Rust'); assert.equal(await page.locator('.repo:visible').count(), 1);
        await page.selectOption('#repository-language', 'Python'); assert.equal(await page.locator('.repo:visible').count(), 2);
        await page.evaluate(() => dispatchEvent(new Event('beforeprint'))); assert.equal(await page.locator('#browser-details').getAttribute('open'), '');
        await page.evaluate(() => dispatchEvent(new Event('afterprint'))); assert.equal(await page.locator('#browser-details').getAttribute('open'), null);
        await page.click('#jump'); await page.waitForFunction(() => location.hash === '#browser-bottom'); assert.equal(await page.evaluate(() => document.activeElement.id), 'browser-bottom');
        await page.goBack(); await page.waitForFunction(() => !location.hash); await page.goBack(); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'overview');
        assert.equal(await page.evaluate(() => window.documentToken), 'preserved');
      });
      await check(`${engine}: storage denied, duplicates, private response and rate limit`, browser, async ({ page, context }) => {
        await context.addInitScript(() => { Object.defineProperty(window, 'sessionStorage', { get() { throw new Error('Storage unavailable'); } }); });
        await context.unroute('https://api.github.com/**'); const hits = [];
        await context.route('https://api.github.com/**', async route => { const repo = route.request().url().split('/').at(-1); hits.push(repo); await route.fulfill({ json: repo === 'alpha' ? { ...api(repo), private: true } : api(repo) }); });
        await page.goto(`${origin}/profile/repositories.html`); await page.locator('[data-github-repo]').first().scrollIntoViewIfNeeded(); await page.waitForFunction(() => document.querySelector('[data-github-status]').textContent.includes('unavailable'));
        assert.equal(hits.filter(repo => repo === 'alpha').length, 1); assert.equal(await page.locator('[data-github-repo="example/alpha"] [data-github-stars]').first().textContent(), '7');
        await context.unroute('https://api.github.com/**'); let limited = 0;
        await context.route('https://api.github.com/**', async route => { limited++; await route.fulfill({ status: 429, headers: { 'Retry-After': '3600' }, json: {} }); });
        await page.locator('[data-github-repo="example/alpha"] [data-github-refresh]').first().click(); await page.waitForFunction(() => document.querySelector('[data-github-status]').textContent.includes('rate limit'));
        await page.locator('[data-github-repo="example/alpha"] [data-github-refresh]').first().click(); assert.equal(limited, 1);
        assert.equal(await page.locator('[data-github-repo="example/alpha"] [data-github-stars]').first().textContent(), '7');
      });
      await check(`${engine}: reduced motion, pause persistence and sanitization`, browser, async ({ page }) => {
        overrides.set('/profile/evidence.html', { body: html('evidence', '<button id="unsafe" onclick="window.untrusted=true">Unsafe handler</button><a id="bad-link" href="javascript:alert(1)">unsafe</a><script>window.untrusted=true</script><p id="styled" style="background-image:url(https://invalid.example/a);width:50%">Bar</p>') });
        await page.emulateMedia({ reducedMotion: 'reduce' }); await page.goto(`${origin}/profile/index.html`);
        assert.equal(await page.locator('html').getAttribute('data-motion'), 'paused'); assert.equal(await page.locator('[data-motion-toggle]').isDisabled(), true); assert.equal(await page.locator('[data-reveal]:not(.is-visible)').count(), 0);
        await page.emulateMedia({ reducedMotion: 'no-preference' }); await page.locator('[data-motion-toggle]').click();
        await page.click('.topbar [data-nav-page="evidence"]'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'evidence');
        assert.equal(await page.locator('html').getAttribute('data-motion'), 'paused'); assert.equal(await page.evaluate(() => window.untrusted), undefined);
        assert.equal(await page.locator('#main script').count(), 0); assert.equal(await page.locator('#unsafe').getAttribute('onclick'), null); assert.equal(await page.locator('#unsafe').getAttribute('src'), null);
        assert.equal(await page.locator('#bad-link').getAttribute('href'), null); assert.equal(await page.locator('#styled').getAttribute('style'), 'width: 50%;');
      });
      await check(`${engine}: racing navigation and native exit cancellation`, browser, async ({ page }) => {
        overrides.set('/profile/repositories.html', { delay: 450, body: html('repositories') });
        await page.goto(`${origin}/profile/index.html`); await page.evaluate(() => { window.documentToken = 'original'; });
        await page.click('.topbar [data-nav-page="repositories"]'); await page.click('.topbar [data-nav-page="evidence"]'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'evidence'); await page.waitForTimeout(500);
        assert.match(await page.title(), /evidence/i); assert.equal(await page.evaluate(() => window.documentToken), 'original');
        await page.click('.topbar [data-nav-page="repositories"]'); await page.click('#native'); await page.waitForURL('**/native.html');
        assert.equal(await page.evaluate(() => window.documentToken), undefined); assert.equal(await page.locator('#main').getAttribute('data-profile-page'), 'overview');
      });
      await check(`${engine}: mismatched template falls back to normal navigation`, browser, async ({ page }) => {
        overrides.set('/profile/evidence.html', { body: html('evidence', '', '3') });
        await page.goto(`${origin}/profile/index.html`); await page.evaluate(() => { window.documentToken = 'original'; });
        await page.click('.topbar [data-nav-page="evidence"]'); await page.waitForURL('**/evidence.html'); await page.waitForFunction(() => document.querySelector('#main').dataset.profileVersion === '3');
        assert.equal(await page.evaluate(() => window.documentToken), undefined); assert.equal(loads.filter(path => path === '/profile/evidence.html').length, 2);
      });
      await check(`${engine}: cached metadata, concurrency cap and pointer reset`, browser, async ({ page, context }) => {
        await context.unroute('https://api.github.com/**');
        let active = 0, peak = 0, hits = 0;
        await page.setViewportSize({ width: 1150, height: 2600 });
        await context.route('https://api.github.com/**', async route => {
          hits++; active++; peak = Math.max(peak, active);
          await new Promise(resolve => setTimeout(resolve, 120));
          active--; await route.fulfill({ json: api(route.request().url().split('/').at(-1)) });
        });
        await page.goto(`${origin}/profile/repositories.html`);
        await page.locator('[data-github-repo]').first().scrollIntoViewIfNeeded();
        await page.waitForFunction(() => document.querySelector('[data-github-stars]').textContent === '31');
        await page.locator('[data-github-repo="example/beta"]').scrollIntoViewIfNeeded();
        await page.waitForFunction(() => document.querySelector('[data-github-repo="example/beta"] [data-github-stars]').textContent === '31');
        await page.locator('[data-github-repo="example/gamma"]').scrollIntoViewIfNeeded();
        await page.waitForFunction(() => document.querySelector('[data-github-repo="example/gamma"] [data-github-stars]').textContent === '31');
        assert.equal(peak, 2); assert.equal(hits, 3);
        const tile = page.locator('.repo[data-tilt]').first(); await tile.scrollIntoViewIfNeeded();
        await page.waitForTimeout(100); const box = await tile.boundingBox();
        await page.mouse.move(box.x + box.width * 0.8, box.y + box.height * 0.4);
        await page.waitForFunction(() => Boolean(document.querySelector('.repo[data-tilt]').style.getPropertyValue('--tilt-x')));
        await page.mouse.move(0, 0); await page.waitForFunction(() => !document.querySelector('.repo[data-tilt]').style.getPropertyValue('--tilt-x'));
        await page.click('.topbar [data-nav-page="evidence"]'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'evidence');
        await page.click('.topbar [data-nav-page="repositories"]'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'repositories');
        await page.locator('[data-github-repo]').first().scrollIntoViewIfNeeded();
        await page.waitForFunction(() => document.querySelector('[data-github-stars]').textContent === '31'); assert.equal(hits, 3);
      });
      await check(`${engine}: timeout returns to normal navigation`, browser, async ({ page }) => {
        overrides.set('/profile/evidence.html', { delay: 9000, onlyFetch: true, body: html('evidence') });
        await page.goto(`${origin}/profile/index.html`); await page.evaluate(() => { window.documentToken = 'before-timeout'; });
        const started = Date.now(); await page.click('.topbar [data-nav-page="evidence"]');
        await page.waitForURL('**/evidence.html'); await page.waitForFunction(() => document.querySelector('#main').dataset.profilePage === 'evidence');
        assert.ok(Date.now() - started >= 7500, 'The timeout path, not immediate fallback, ran');
        assert.equal(await page.evaluate(() => window.documentToken), undefined);
        assert.equal(loads.filter(route => route === '/profile/evidence.html').length, 2);
      });
      await check(`${engine}: same-page fragment and reload restore scroll`, browser, async ({ page }) => {
        await page.goto(`${origin}/profile/index.html`); await page.click('#jump');
        await page.waitForFunction(() => location.hash === '#browser-bottom');
        const position = await page.evaluate(() => scrollY); assert.ok(position > 500);
        await page.reload(); await page.waitForFunction(position => Math.abs(scrollY - position) < 5, position);
        assert.equal(await page.evaluate(() => location.hash), '#browser-bottom');
      });
      await check(`${engine}: narrow screens preserve every page without horizontal overflow`, browser, async ({ page }) => {
        await page.emulateMedia({ reducedMotion: 'reduce' });
        for (const width of [320, 390]) {
          await page.setViewportSize({ width, height: 844 });
          for (const route of ['index.html', 'repositories.html', 'evidence.html']) {
            await page.goto(`${origin}/profile/${route}`);
            await page.locator('#main').waitFor();
            const overflow = await page.evaluate(() => ({ width: document.documentElement.scrollWidth, viewport: innerWidth, nodes: [...document.querySelectorAll('body *')].filter(n => n.getBoundingClientRect().right > innerWidth + 1).slice(0, 12).map(n => ({ tag: n.tagName, id: n.id, class: typeof n.className === 'string' ? n.className : '', right: n.getBoundingClientRect().right })) }));
            assert.ok(overflow.width <= overflow.viewport, `${route} overflows at ${width}px: ${JSON.stringify(overflow)}`);
            assert.equal(await page.locator('.topbar').isVisible(), true);
            if (process.env.CI_BROWSER_DIAGNOSTICS && width === 390) await page.screenshot({ path: path.join(process.env.CI_BROWSER_DIAGNOSTICS, `${engine}-${route}.png`), fullPage: true });
          }
        }
      });
      await check(`${engine}: no JavaScript keeps snapshot and navigation`, browser, async () => {
        const context = await browser.newContext({ javaScriptEnabled: false });
        try { const page = await context.newPage(); await page.goto(`${origin}/profile/repositories.html`); assert.equal(await page.locator('.repo:visible').count(), 4); assert.equal(await page.locator('#repository-filters').isVisible(), false); await page.click('.topbar [data-nav-page="evidence"]'); assert.match(await page.title(), /evidence/i); }
        finally { await context.close(); }
      });
    } finally { await browser.close(); }
  }
  console.log(JSON.stringify({ passed, browsers }));
  if (process.env.CI_BROWSER_EVIDENCE) {
    assert.equal(browsers.length, 1, 'A matrix target must report exactly one real browser');
    const runtime = JSON.parse(await readFile(path.join(process.env.CI_BROWSER_DIAGNOSTICS, 'runtime.json'), 'utf8'));
    await writeFile(process.env.CI_BROWSER_EVIDENCE, JSON.stringify({ ...runtime, ...runtimeIdentity, testsPassed: scenarios.length, testsFailed: 0, scenarios }));
  }
} finally { await new Promise(resolve => server.close(resolve)); await rm(fixtureDir, { recursive: true, force: true }); }
