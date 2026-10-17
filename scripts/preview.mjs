// Two previews of the GitHub profile, dark and light, from its README as it is: a page that imitates the profile of GitHub.
// Usage: node preview.mjs <sport-extract frontend dir> <profile repo dir> <out dir>
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [frontend, repo, out] = process.argv.slice(2);
const { chromium } = await import(pathToFileURL(path.join(frontend, 'node_modules', 'playwright-core', 'index.mjs')).href);
const readme = (await readFile(path.join(repo, 'README.md'), 'utf-8'))
  .replace(/(src|srcset)="assets\//g, (_, attribute) => `${attribute}="${pathToFileURL(path.join(repo, 'assets')).href}/`);
const page = theme => {
  const c = theme === 'dark'
    ? { bg: '#0d1117', line: '#30363d', text: '#e6edf3', muted: '#8d96a0', link: '#4493f8', avatar: '#21262d' }
    : { bg: '#ffffff', line: '#d0d7de', text: '#1f2328', muted: '#59636e', link: '#0969da', avatar: '#eaeef2' };
  return `<!doctype html><meta charset="utf-8"><style>
body { margin: 0; background: ${c.bg}; color: ${c.text}; font: 16px/1.5 -apple-system, "Segoe UI", Arial, sans-serif; }
.wrap { display: flex; gap: 24px; padding: 32px; width: 1232px; }
aside { width: 296px; flex: none; font-size: 14px; }
.avatar { width: 296px; height: 296px; border-radius: 50%; background: ${c.avatar}; border: 1px solid ${c.line}; }
aside h1 { font-size: 24px; margin: 16px 0 0; } aside .login { color: ${c.muted}; font-size: 20px; font-weight: 300; }
main { flex: 1; min-width: 0; }
.box { border: 1px solid ${c.line}; border-radius: 6px; padding: 16px 32px 24px; }
.file { font: 12px ui-monospace, Consolas, monospace; color: ${c.muted}; margin-bottom: 16px; }
.box img { max-width: 100%; box-sizing: content-box; }
.box p { margin: 0 0 16px; } .box h3 { font-size: 20px; font-weight: 600; line-height: 1.25; margin: 24px 0 16px; } .box a { color: ${c.link}; text-decoration: none; }
</style><div class="wrap"><aside><div class="avatar"></div><h1>Lucas Remery</h1><div class="login">ThaoK31</div>
<p>Full-stack developer · Master's student at Ynov · Work-study at SII</p></aside>
<main><div class="box"><div class="file">ThaoK31 / README.md</div>${readme}</div></main></div>`;
};

const browser = await chromium.launch({ channel: 'chrome' });
const tab = await browser.newPage({ viewport: { width: 1296, height: 900 } });
for (const theme of ['dark', 'light']) {
  // A page of its own on disk: a page made from a string may not read local files (the images).
  const file = path.join(out, `preview-${theme}.html`);
  await writeFile(file, page(theme), 'utf-8');
  await tab.emulateMedia({ colorScheme: theme });
  await tab.goto(pathToFileURL(file).href);
  await tab.waitForTimeout(6500); // the curve of the header has drawn itself
  await tab.screenshot({ path: path.join(out, `preview-${theme}.png`), fullPage: true });
}
await tab.setViewportSize({ width: 390, height: 844 });
await tab.emulateMedia({ colorScheme: 'dark' });
await tab.goto(pathToFileURL(path.join(out, 'preview-dark.html')).href);
await tab.addStyleTag({ content: '.wrap { display: block; width: auto; padding: 16px; } aside { display: none; } .box { padding: 16px; }' });
await tab.waitForTimeout(6500);
await tab.screenshot({ path: path.join(out, 'preview-mobile.png'), fullPage: true });
await browser.close();
console.log('previews done');
