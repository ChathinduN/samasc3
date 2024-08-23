const puppeteer = require('puppeteer');

(async () => {
    const url = process.argv[2];
    const output = process.argv[3];

    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: output, fullPage: true });

    await browser.close();
})();
