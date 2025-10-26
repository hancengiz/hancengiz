# Twitter Auto-Publishing Setup

This guide explains how to automatically publish your Substack notes to Twitter using GitHub Actions and Zapier.

## Overview

```
Substack Notes → GitHub (every 5 min) → Zapier Webhook → Buffer → Twitter
```

## How It Works

1. **Substack Notes Scraper** runs every 5 minutes and saves notes to `substack-scraper/notes/`
2. **Publish Notes to Twitter** workflow detects new notes (those without `.published` marker file)
3. For each new note, it sends JSON data to Zapier webhook
4. Zapier formats the data and posts to Buffer/Twitter
5. A `.published` marker file is created in the note folder to prevent duplicates

## Setup Instructions

### 1. Set Up Zapier Zap

Create a Zap with these steps:

#### Step 1: Webhooks by Zapier (Catch Hook)
- **Trigger:** Catch Hook
- **Action:** Wait for webhook data
- Copy the webhook URL (you'll need this for GitHub)

#### Step 2: Formatter by Zapier (Optional)
- **Action:** Text → Truncate
- **Input:** `{{content}}` from Step 1
- **Length:** 250 characters
- This ensures tweet doesn't exceed character limits

#### Step 3: Formatter by Zapier (Format Tweet)
- **Action:** Text → Custom
- **Template Example:**
  ```
  {{1__content}}

  👉 Read more: {{1__url}}
  ```
- Or with truncation:
  ```
  {{2__output}}...

  Continue reading: {{1__url}}
  ```

#### Step 4: Buffer (or Twitter API)
- **Action:** Create Post
- **Account:** Connect your Twitter account via Buffer
- **Text:** Use the formatted text from Step 3

### 2. Add Zapier Webhook URL to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ZAPIER_WEBHOOK_URL`
5. Value: Paste the webhook URL from Zapier Step 1
6. Click **Add secret**

### 3. Test the Workflow

#### Option 1: Manual Trigger
1. Go to **Actions** tab in your GitHub repository
2. Select **"Publish Notes to Twitter"** workflow
3. Click **"Run workflow"** button
4. Check the logs to see if notes were published

#### Option 2: Wait for Automatic Trigger
- The workflow automatically runs after the Notes Scraper completes
- Check **Actions** tab to see when it runs next

## JSON Payload Structure

The workflow sends this data to Zapier:

```json
{
  "note_id": "170317259",
  "content": "Full note content without frontmatter or metadata...",
  "url": "https://substack.com/note/c-170317259",
  "author": "Cengiz Han",
  "handle": "hancengiz",
  "published_date": "Sun, 26 Oct 2025 12:42:17 GMT",
  "reactions": "0",
  "restacks": "0",
  "replies": "0"
}
```

### Available Fields in Zapier

- `{{note_id}}` - Note ID number
- `{{content}}` - Full note text
- `{{url}}` - Substack note URL
- `{{author}}` - Author name
- `{{handle}}` - Substack handle
- `{{published_date}}` - Original publish date
- `{{reactions}}` - Number of reactions
- `{{restacks}}` - Number of restacks
- `{{replies}}` - Number of replies

## Tweet Format Examples

### Simple
```
{{content}}

{{url}}
```

### With Emoji
```
{{content}}

🔗 {{url}}

#AI #TechLeadership
```

### With Engagement
```
{{content}}

❤️ {{reactions}} | 🔄 {{restacks}}

{{url}}
```

### Truncated
```
{{content|truncate:250}}...

Continue reading: {{url}}
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

1. Remove the `ZAPIER_WEBHOOK_URL` secret from GitHub
2. The workflow will skip webhook calls but still create markers

## Rate Limiting

- The workflow waits 10 seconds between each note
- This prevents Twitter rate limiting
- Multiple notes will be published sequentially

## Troubleshooting

### Notes Not Being Published

1. Check if `.published` marker already exists
2. Verify `ZAPIER_WEBHOOK_URL` secret is set
3. Check GitHub Actions logs for errors
4. Test Zapier webhook manually with sample data

### Zapier Not Receiving Data

1. Check webhook URL is correct
2. Test webhook in Zapier using "Test trigger"
3. Check GitHub Actions logs for HTTP response codes

### Tweets Not Posting

1. Check Buffer/Twitter connection in Zapier
2. Verify tweet format doesn't exceed 280 characters
3. Check Buffer posting schedule

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
1. Check GitHub Actions logs
2. Test Zapier zap with sample data
3. Verify all secrets are set correctly
4. Check rate limits on Twitter/Buffer
