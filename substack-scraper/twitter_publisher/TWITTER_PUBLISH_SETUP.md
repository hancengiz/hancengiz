# Twitter Auto-Publishing Setup

This guide explains how to automatically publish your Substack notes to Twitter using GitHub Actions and Twitter API v2.

**What you need:**
- ✅ Twitter Developer Account (you already have this)
- ✅ Twitter App with Read & Write permissions
- ✅ 4 API credentials (API Key, API Secret, Access Token, Access Token Secret)
- ✅ GitHub repository secrets configured

**Cost:** Free (Twitter API v2 Free Tier: 1,500 tweets/month)

## Overview

```
Substack Notes → GitHub (every 5 min) → Twitter API v2 → Twitter
```

## How It Works

1. **Substack Notes Scraper** runs every 5 minutes and saves notes to `substack-scraper/notes/`
2. **Publish Notes to Twitter** workflow detects new notes (those without `.published` marker file)
3. For each new note, it posts directly to Twitter using the Twitter API v2
4. Tweet is formatted with content (truncated to ~250 chars) + link
5. A `.published` marker file is created in the note folder to prevent duplicates

## Setup Instructions

### 1. Get Twitter API Credentials

You already have a Twitter Developer account, so:

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Select your app (or create a new one)
3. Go to **"Keys and tokens"** tab
4. Generate/copy these credentials:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Access Token**
   - **Access Token Secret**

**Important:** Make sure your app has **Read and Write** permissions:
- Go to **"Settings"** tab
- Under "User authentication settings"
- Ensure "Read and write" is enabled

### 2. Add Twitter Credentials to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add **four secrets** (click "New repository secret" for each):

| Secret Name | Value from Twitter |
|-------------|-------------------|
| `TWITTER_API_KEY` | API Key (Consumer Key) |
| `TWITTER_API_SECRET` | API Secret (Consumer Secret) |
| `TWITTER_ACCESS_TOKEN` | Access Token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Access Token Secret |

### 3. Test the Workflow

#### Option 1: Manual Trigger
1. Go to **Actions** tab in your GitHub repository
2. Select **"Publish Notes to Twitter"** workflow
3. Click **"Run workflow"** button
4. Check the logs to see if notes were published

#### Option 2: Wait for Automatic Trigger
- The workflow automatically runs after the Notes Scraper completes
- Check **Actions** tab to see when it runs next

## Tweet Format

The workflow automatically formats tweets like this:

```
{note content - truncated to ~250 chars if needed}...

👉 {note URL}
```

**Character Limits:**
- Maximum tweet length: 280 characters
- Content is truncated at word boundaries (no mid-word cuts)
- URLs count as 23 characters (Twitter's t.co shortening)

## Example Tweet

For a note with content:
> "Even when I work alone, I still follow the BMAD Method or a similar approach I've designed. I usually start by 'vibing'—exploring ideas, testing possibilities..."

**Posted tweet:**
```
Even when I work alone, I still follow the BMAD Method or a similar approach I've designed. I usually start by 'vibing'—exploring ideas, testing possibilities, and clarifying what I want to accomplish. Even at this early stage, I open...

👉 https://substack.com/note/c-170317259
```

## Tracking Published Notes

- Each published note gets a `.published` marker file in its folder
- Example: `substack-scraper/notes/2025-10-26_note-170317259/.published`
- Contains timestamp: `published_at: 2025-10-26T17:45:00Z`

### To Republish a Note

1. Delete the `.published` file from the note folder
2. The workflow will pick it up on next run
3. Commit and push the deletion

### To Stop Publishing

1. Disable the workflow in GitHub Actions
2. Or remove the Twitter API secrets from GitHub

## Rate Limiting

- The workflow waits 10 seconds between each note
- This prevents Twitter rate limiting
- Multiple notes will be published sequentially

## Troubleshooting

### Notes Not Being Published

1. Check if `.published` marker already exists
2. Verify all 4 Twitter API secrets are set correctly
3. Check GitHub Actions logs for errors
4. Verify Twitter app has Read and Write permissions

### Twitter API Errors

Common errors and solutions:

**"403 Forbidden"**
- Your app doesn't have write permissions
- Go to Developer Portal → App Settings → Enable "Read and Write"
- Regenerate Access Token and Access Token Secret

**"401 Unauthorized"**
- Credentials are incorrect
- Regenerate all keys in Developer Portal
- Update GitHub secrets with new values

**"429 Too Many Requests"**
- Hit rate limits (1,500 tweets/month on free tier)
- Wait for rate limit to reset
- Reduce posting frequency

### Tweets Not Appearing

1. Check Twitter API response in GitHub Actions logs
2. Look for tweet ID in logs (confirms successful post)
3. Check your Twitter profile

## Files Structure

```
substack-scraper/
├── notes/
│   └── 2025-10-26_note-170317259/
│       ├── original_note.md       # Source data
│       ├── formatted_note.md      # Formatted version
│       └── .published             # Marker (auto-created)
└── TWITTER_PUBLISH_SETUP.md       # This file
```

## GitHub Actions Workflow

Location: `.github/workflows/publish-notes-to-twitter.yml`

**Triggers:**
- After "Substack Notes Scraper" completes successfully
- Manual dispatch (via Actions UI)

**Permissions:**
- `contents: write` (to commit `.published` markers)

## Support

If you encounter issues:
1. Check GitHub Actions logs for detailed error messages
2. Verify all 4 Twitter secrets are set correctly
3. Check Twitter app permissions (Read and Write required)
4. Monitor rate limits (1,500 tweets/month on free tier)
5. Test manually by triggering workflow in Actions tab

## API Rate Limits

**Twitter API v2 Free Tier:**
- 1,500 tweets per month (~50 per day)
- If you post 10 notes/day = ~300/month ✅ Well within limit
- Rate limit resets monthly
