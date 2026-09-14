const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });

  for (let i = 1; i <= 5; i++) {
    const filePath = `file://${path.resolve(__dirname, `carousel-${i}.html`)}`;
    await page.goto(filePath, { waitUntil: 'networkidle2', timeout: 15000 });
    // Wait for fonts & images to load
    await new Promise(r => setTimeout(r, 3000));

    const card = await page.$('.card');
    await card.screenshot({
      path: path.resolve(__dirname, `carousel-${i}.png`),
      type: 'png'
    });
    console.log(`✓ carousel-${i}.png saved`);
  }

  await browser.close();
  console.log('\nГотово! 5 PNG файлов сохранены.');
})();
