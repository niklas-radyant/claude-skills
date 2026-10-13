#!/usr/bin/env node
// Headless screenshots for AFK reviewers: no dependencies (Node >= 22 for the
// global WebSocket), drives an installed Chrome/Chromium over CDP.
//
//   node shoot.mjs --url http://localhost:3314/home --out shots/home-dark.png \
//     [--theme dark|light] [--width 1512] [--height 982] [--full] [--wait 4000] \
//     [--storage key=value ...] [--click "css selector"]
//
// --theme sets localStorage.theme (next-themes) before the page loads.
// --storage sets extra localStorage keys before load.
// --click clicks a selector after load (e.g. to open a modal), then waits 800 ms.
// Exits non-zero with a reason when the page redirects to a login screen.

import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';

const args = process.argv.slice(2);
const opt = { theme: 'light', width: 1512, height: 982, wait: 4000, full: false, storage: [], click: [] };
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--full') opt.full = true;
  else if (a === '--storage') opt.storage.push(args[++i]);
  else if (a === '--click') opt.click.push(args[++i]);
  else if (a.startsWith('--')) opt[a.slice(2)] = args[++i];
}
if (!opt.url || !opt.out) {
  console.error('usage: shoot.mjs --url URL --out FILE.png [--theme dark|light] [--full]');
  process.exit(2);
}

// CHROME_PATH wins; otherwise the usual install locations (macOS app bundles,
// then whatever Chrome/Chromium is on PATH on Linux).
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
const findChrome = () => {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  for (const p of [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  ]) if (existsSync(p)) return p;
  for (const bin of ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']) {
    try { return execFileSync('which', [bin], { encoding: 'utf8' }).trim(); } catch {}
  }
  return null;
};
const CHROME = findChrome();
if (!CHROME) { console.error('No Chrome/Chromium found; set CHROME_PATH'); process.exit(1); }
const port = 9300 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), 'afk-shoot-'));
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), // cloud VMs run as root
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars',
  `--window-size=${opt.width},${opt.height}`, 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// Chrome keeps writing to its profile until it has exited; remove it after.
const cleanup = async () => {
  const exited = new Promise((r) => chrome.once('exit', r));
  chrome.kill();
  await Promise.race([exited, new Promise((r) => setTimeout(r, 3000))]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
};
const fail = async (msg) => { console.error(msg); await cleanup(); process.exit(1); };

let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try {
    const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    target = list.find((t) => t.type === 'page');
  } catch {}
}
if (!target) await fail('Chrome did not start (CHROME_PATH?)');

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let id = 0;
const pending = new Map();
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
};
const send = (method, params = {}) => new Promise((r) => {
  const mid = ++id; pending.set(mid, r); ws.send(JSON.stringify({ id: mid, method, params }));
});

const origin = new URL(opt.url).origin;
const store = { theme: opt.theme, ...Object.fromEntries(opt.storage.map((s) => s.split(/=(.*)/s).slice(0, 2))) };
await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: +opt.width, height: +opt.height, deviceScaleFactor: 1, mobile: +opt.width < 768 });
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: opt.theme }] });
await send('Page.addScriptToEvaluateOnNewDocument', {
  source: `try{if(location.origin===${JSON.stringify(origin)}){const s=${JSON.stringify(store)};for(const k in s)localStorage.setItem(k,s[k]);}}catch(e){}`,
});
await send('Page.navigate', { url: opt.url });

const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).result?.result?.value;
for (let i = 0; i < 100; i++) {
  await sleep(150);
  if ((await evaluate('document.readyState')) === 'complete') break;
}
await sleep(+opt.wait);

const href = await evaluate('location.href');
if (!href || href.startsWith('chrome-error:')) await fail(`page did not load: ${opt.url} (dev server down?)`);
if (/\/(login|signin|auth)\b/.test(new URL(href).pathname)) await fail(`redirected to ${href}: auth bypass not active`);

for (const sel of opt.click) {
  const ok = await evaluate(`(()=>{const el=document.querySelector(${JSON.stringify(sel)});if(!el)return false;el.click();return true})()`);
  if (!ok) await fail(`--click selector not found: ${sel}`);
  await sleep(800);
}

let clip;
if (opt.full) {
  const h = await evaluate('Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)');
  clip = { x: 0, y: 0, width: +opt.width, height: Math.min(h || +opt.height, 12000), scale: 1 };
}
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: !!clip, ...(clip ? { clip } : {}) });
if (!shot.result?.data) await fail('screenshot failed');
mkdirSync(dirname(opt.out), { recursive: true });
writeFileSync(opt.out, Buffer.from(shot.result.data, 'base64'));
console.log(`${opt.out} (${href}, ${opt.theme})`);
ws.close();
await cleanup();
process.exit(0);
