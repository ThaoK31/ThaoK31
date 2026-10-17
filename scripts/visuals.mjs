// The two pictures of the projects of the GitHub profile, without a card, on a transparent background that takes the
// color of the page of GitHub: the three phones of Sport Extract side by side, and four screenshots of Moss & Mayhem in a
// grid. Usage: node visuals.mjs <sport-extract frontend dir> <phone shots dir> <game shots dir> <assets dir>
import { writeFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [frontend, phones, game, assets] = process.argv.slice(2);
const { chromium } = await import(pathToFileURL(path.join(frontend, 'node_modules', 'playwright-core', 'index.mjs')).href);
const url = file => pathToFileURL(file).href;
const fonts = path.join(frontend, 'src', 'fonts');
const EDGE = '1px solid rgba(128, 128, 128, 0.4)';
const style = `<style>
@font-face { font-family: "Barlow"; font-weight: 400; src: url("${url(path.join(fonts, 'barlow-400.woff2'))}"); }
html, body { margin: 0; background: transparent; }
.phones { display: inline-flex; gap: 32px; padding: 2px; }
.phones img { height: 540px; border-radius: 34px; border: ${EDGE}; display: block; }
.grid { width: 904px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 2px; }
figure { margin: 0; position: relative; aspect-ratio: 16 / 9; border: ${EDGE}; border-radius: 10px; overflow: hidden; }
figure img { width: 100%; height: 100%; object-fit: cover; display: block; }
figcaption { position: absolute; left: 10px; bottom: 10px; font: 400 15px "Barlow"; color: #EFE8E3; background: #160F0C;
  border-radius: 6px; padding: 3px 10px; }
</style>`;
const pictures = {
  'sport-extract.png': ['.phones', `<div class="phones">${['accueil', 'progres', 'plan']
    .map(name => `<img src="${url(path.join(phones, `${name}.png`))}">`).join('')}</div>`],
  // The names of the English version of the game (src/client/i18n/en.ts).
  'moss-and-mayhem.png': ['.grid', `<div class="grid">${[['mm-boss-0.png', 'The Grove'], ['mm-ronce-2.png', 'The Bramble Heart'],
    ['mm-tunnel-0.png', 'Garden Tunnel'], ['mm-jardin-0.png', 'The Garden']]
    .map(([file, name]) => `<figure><img src="${url(path.join(game, file))}"><figcaption>${name}</figcaption></figure>`).join('')}</div>`],
};

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1000, height: 800 }, deviceScaleFactor: 2 });
for (const [name, [selector, body]] of Object.entries(pictures)) {
  // A page of its own on disk: a page made from a string may not read local files (the screenshots, the font).
  const file = path.join(game, `${name}.html`);
  await writeFile(file, `<!doctype html><meta charset="utf-8">${style}${body}`, 'utf-8');
  await page.goto(url(file));
  await page.evaluate(() => document.fonts.ready);
  await page.locator(selector).screenshot({ path: path.join(assets, name), omitBackground: true });
  console.log(name);
}
await browser.close();
