const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('--- Converting RetailIQ Proposal Deck to High-Resolution PDF ---');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  const htmlPath = path.resolve(__dirname, 'RetailIQ_Proposal_Deck.html');
  console.log('Loading HTML deck:', htmlPath);
  await page.goto('file:///' + htmlPath.replace(/\\/g, '/'), { waitUntil: 'networkidle' });

  // Wait for web fonts (Plus Jakarta Sans & JetBrains Mono) to render
  await page.waitForTimeout(2000);

  const pdfPath = path.resolve(__dirname, 'RetailIQ_Proposal_Deck.pdf');
  console.log('Printing to PDF with 16:9 widescreen layout...');
  await page.pdf({
    path: pdfPath,
    width: '16in',
    height: '9in',
    printBackground: true,
    margin: { top: '0in', right: '0in', bottom: '0in', left: '0in' },
    preferCSSPageSize: true
  });

  const stats = fs.statSync(pdfPath);
  console.log(`✓ PDF Generated Successfully! Size: ${stats.size} bytes (${(stats.size / 1024 / 1024).toFixed(2)} MB)`);
  console.log(`✓ Output file: ${pdfPath}`);

  // Also copy to root folder for instant access
  const rootPdfPath = path.resolve(__dirname, '..', 'RetailIQ_Proposal_Deck.pdf');
  fs.copyFileSync(pdfPath, rootPdfPath);
  console.log(`✓ Copied to root: ${rootPdfPath}`);

  await browser.close();
})();
