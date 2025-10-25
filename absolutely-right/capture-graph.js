#!/usr/bin/env node

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('Launching browser...');
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Set viewport for consistent screenshots
  await page.setViewportSize({ width: 1200, height: 800 });

  console.log('Navigating to cc.cengizhan.com...');
  await page.goto('https://cc.cengizhan.com/', {
    waitUntil: 'networkidle'
  });

  // Wait for content to load and render
  console.log('Waiting for content to load...');
  await page.waitForTimeout(2000);

  // Wait for graph-overlay to have actual height (graph rendered)
  console.log('Waiting for graph to render...');
  try {
    await page.waitForFunction(
      () => {
        const overlay = document.querySelector('.graph-overlay');
        if (!overlay) return false;
        const rect = overlay.getBoundingClientRect();
        return rect.height > 0;
      },
      { timeout: 10000 }
    );
    console.log('Graph rendered successfully!');
  } catch (error) {
    console.log('Graph overlay did not render with height, will use fallback...');
  }

  await page.waitForTimeout(1000); // Extra time for animations

  // Create assets directory if it doesn't exist
  const assetsDir = path.join(__dirname, 'assets');
  if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
  }

  const outputPath = path.join(assetsDir, 'claude-code-graph.png');
  console.log(`Taking screenshot and saving to ${outputPath}...`);

  // Try to find the graph-container element first, then fallback to other selectors
  const selectors = ['.graph-container', '.chart-section', '.graph-overlay', 'main', '.content', '.container', '#app', '#root'];

  let element = null;
  let usedSelector = null;
  for (const selector of selectors) {
    element = await page.$(selector);
    if (element) {
      usedSelector = selector;
      console.log(`Found content using selector: ${selector}`);
      break;
    }
  }

  if (element) {
    // Get the bounding box of the element
    const boundingBox = await element.boundingBox();

    console.log('Bounding box:', boundingBox);

    if (boundingBox && boundingBox.width > 0 && boundingBox.height > 0) {
      // Use clip to screenshot the area
      await page.screenshot({
        path: outputPath,
        clip: {
          x: boundingBox.x,
          y: boundingBox.y,
          width: boundingBox.width,
          height: boundingBox.height
        }
      });
    } else {
      // Element has no dimensions, fall back to next selector
      console.log(`Element ${usedSelector} has no dimensions, trying next selector...`);
      element = null;
    }
  }

  if (!element) {
    // If no container found, try to get bounding box of visible content excluding header/footer
    console.log('No container found, using custom bounds...');

    // Hide header and footer elements
    await page.addStyleTag({
      content: `
        body > *:first-child { display: none !important; }
        body > *:last-child { display: none !important; }
      `
    });

    await page.waitForTimeout(200);

    const bounds = await page.evaluate(() => {
      const allVisible = Array.from(document.querySelectorAll('body > *:not([style*="display: none"])'));
      if (allVisible.length === 0) return null;

      let minX = Infinity, minY = Infinity, maxX = 0, maxY = 0;
      allVisible.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.left < minX) minX = rect.left;
        if (rect.top < minY) minY = rect.top;
        if (rect.right > maxX) maxX = rect.right;
        if (rect.bottom > maxY) maxY = rect.bottom;
      });

      return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
    });

    if (bounds) {
      await page.screenshot({
        path: outputPath,
        clip: {
          x: Math.max(0, bounds.x - 10),
          y: Math.max(0, bounds.y - 10),
          width: bounds.width + 20,
          height: bounds.height + 20
        }
      });
    }
  }

  console.log('Screenshot captured successfully!');
  await browser.close();
})();
