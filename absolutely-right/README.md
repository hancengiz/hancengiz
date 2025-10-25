# Absolutely Right!

A fun experiment tracking how confident Claude Code is in my approaches!

Live at: [cc.cengizhan.com](https://cc.cengizhan.com/)

## What's this?

This tracks confidence-affirming phrases that Claude Code uses when reviewing or commenting on my work, like "absolutely right", "perfect", "excellent", etc.

## How it works

- A GitHub Actions workflow runs daily
- It captures a screenshot of the live graph from cc.cengizhan.com
- The screenshot is automatically committed to this repo
- The main README displays the latest graph

## Local Development

### Install dependencies
```bash
npm install
npx playwright install chromium
```

### Capture screenshot
```bash
npm run capture-graph
```

The screenshot will be saved to `assets/claude-code-graph.png`.

## GitHub Actions Workflow

The workflow runs:
- Daily at midnight UTC (scheduled)
- Manually via GitHub Actions UI (workflow_dispatch)

It automatically commits any changes to the screenshot.
