# Substack Content Scraper

Automatically fetches blog posts and notes from your Substack and saves them as markdown files with downloaded images.

## Structure

```text
substack-scraper/
├── scraper.py              # Main scraper script
├── requirements.txt        # feedparser, html2text
├── posts/                 # Blog posts (from RSS feed)
│   └── YYYY-MM-DD_slug/  # One folder per post
│       ├── original_post.md     # Markdown with remote image URLs
│       ├── formatted_post.md    # Markdown with local image paths (for viewing)
│       ├── .published          # Twitter publish marker (if posted)
│       ├── image1.jpg          # Downloaded images
│       ├── image2.jpg
│       └── ...
└── notes/                 # Short-form notes (from public API)
    └── YYYY-MM-DD_note-{id}/  # One folder per note
        ├── original_note.md     # Markdown with remote image URLs
        ├── formatted_note.md    # Markdown with local image paths (for viewing)
        ├── .published          # Twitter publish marker (if posted)
        ├── image1.jpg          # Downloaded images (if any)
        └── ...
```

## Approach

### Posts

- **Source**: RSS feed (`/feed`) - official, public, stable
- **Method**: Parse with `feedparser` library
- **Why**: RSS is standard and intended for public consumption

### Notes

- **Source**: Public API (`/api/v1/notes`) - undocumented but public
- **Method**: Direct HTTP request, no authentication needed
- **Why**: Faster than HTML scraping, returns structured JSON

Both use official/public endpoints - no authentication, no cookies, no reverse-engineering required.

## Running Locally

```bash
cd substack-scraper
pip install -r requirements.txt
python scraper.py
```

## GitHub Actions

Five separate workflows run independently:

- **Posts Scraper**: Every hour (`.github/workflows/substack-posts.yml`)
- **Notes Scraper**: Every 5 minutes (`.github/workflows/substack-notes.yml`)
- **Twitter Notes**: Auto-posts new notes to Twitter (`.github/workflows/publish-notes-to-twitter.yml`)
- **Twitter Posts**: Auto-posts new blog posts to Twitter (`.github/workflows/publish-posts-to-twitter.yml`)
- **README Update**: Updates README after posts/notes change (`.github/workflows/update-readme.yml`)

Posts and notes scraping run automatically, no setup required. Twitter posting requires API credentials (see below).

## File Format

### Folder Structure

Each post/note is saved in its own folder named `YYYY-MM-DD_slug`:

**Posts**: `2025-10-25_the-ai-native-way-of-building/`
**Notes**: `2025-10-26_note-170317259/`

### Two File Formats

Each folder contains the content in two formats:

1. **original_post.md / original_note.md** - Markdown conversion with remote image URLs preserved
2. **formatted_post.md / formatted_note.md** - Markdown with local image paths for offline viewing

### Downloaded Images

All images are downloaded and saved as `image1.jpg`, `image2.jpg`, etc. in the same folder.

### Frontmatter

All markdown files include YAML frontmatter:

**Posts:**

```yaml
---
title: Post Title
date: Sat, 25 Oct 2025 10:23:50 GMT
author: Cengiz Han
url: https://www.cengizhan.com/p/post-slug
type: post
---
```

**Notes:**

```yaml
---
title: Hey Osman, long time no see!...
date: Sun, 26 Oct 2025 12:42:17 GMT
author: Cengiz Han
handle: hancengiz
url: https://substack.com/note/c-170317259
type: note
note_id: 170317259
photo_url: https://substack-post-media.s3.amazonaws.com/public/images/dd3c9352-78f7-4a7e-ab29-7efd239dd41c_400x400.jpeg
reactions: 0
restacks: 0
replies: 0
# Optional fields (only present if note is a reply to a post):
reply_to_post: The Original Post Title
reply_to_url: https://www.cengizhan.com/p/original-post
---
```

## Configuration

Environment variables (optional):

- `SUBSTACK_BASE_URL` - default: `https://www.cengizhan.com`
- `SUBSTACK_FEED_URL` - default: `https://www.cengizhan.com/feed`
- `POSTS_DIR` - default: `./posts`
- `NOTES_DIR` - default: `./notes`

## Schedule Adjustment

Edit the cron schedule in the respective workflow files:

**Posts** (`.github/workflows/substack-posts.yml`):

```yaml
- cron: '0 * * * *'     # Every hour (current)
- cron: '0 */6 * * *'   # Every 6 hours
- cron: '0 0 * * *'     # Daily
```

**Notes** (`.github/workflows/substack-notes.yml`):

```yaml
- cron: '*/5 * * * *'   # Every 5 minutes (current)
- cron: '*/15 * * * *'  # Every 15 minutes
- cron: '0 * * * *'     # Hourly
```

## Twitter Auto-Posting

Automatically posts new Substack content (both notes and blog posts) to Twitter when scraped.

**Setup:**
1. Get Twitter API credentials from [Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Add 4 secrets to GitHub: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`
3. Workflows run automatically after respective scrapers complete

**Features:**

**Notes Publishing:**
- Posts directly to Twitter (free tier: 1,500 tweets/month)
- Smart truncation (~250 chars + link)
- Uploads up to 4 images (premium tier only)
- Markdown formatting converted to Unicode bold
- Duplicate prevention via `.published` marker files
- Tweet URL saved in each note folder

**Blog Posts Publishing:**
- Posts new blog posts with first paragraph summary
- Smart extraction of meaningful content (skips headers, images, "thanks for reading")
- Truncates to fit Twitter's 280 char limit with smart word breaks
- Includes featured/first image from post (premium tier only)
- Duplicate prevention via `.published` marker files
- Tweet URL saved in each post folder

**See:** [TWITTER_PUBLISH_SETUP.md](TWITTER_PUBLISH_SETUP.md) for detailed setup instructions

---

## Technical Notes for Future Maintenance

### API Discovery

If the notes API changes, here's how to find the new endpoint:

1. Visit `https://www.cengizhan.com` (or your Substack)
2. Open Browser DevTools (F12) → Network tab → Filter by "Fetch/XHR"
3. Browse to where notes appear (usually loaded dynamically)
4. Look for API calls containing "notes" or "api"
5. Click on the request to see:
   - Request URL
   - Response format (JSON structure)
6. Update `scraper.py` line 143 with new endpoint
7. Adjust JSON parsing if response structure changed

**Current endpoint:**

```bash
curl 'https://www.cengizhan.com/api/v1/notes' \
  -H 'accept: application/json'
```

**Response structure:**

```json
{
  "items": [
    {
      "type": "comment",
      "comment": {
        "id": "170317259",
        "body": "...",
        "date": "2025-10-26T12:42:17.540Z",
        "name": "Cengiz Han",
        "handle": "hancengiz",
        "reaction_count": 0,
        "restacks": 0,
        "children_count": 0
      }
    }
  ]
}
```

### Update Detection

The scraper uses **content hash comparison** to detect changes:
- New content → creates new folder with all files
- Changed content → updates existing folder (rewrites all files and re-downloads images)
- Unchanged content → skips folder entirely

This means:
- ✅ Captures edits to posts/notes
- ✅ Updates engagement metrics (reactions, restacks, replies)
- ✅ Doesn't create duplicate folders
- ✅ Only rewrites folders when content actually changes
- ✅ Re-downloads images if content hash changes (ensures image updates are captured)

### Viewing Content Offline

Use the **formatted_post.md** / **formatted_note.md** files to view content with a markdown previewer:

**VS Code**: Open folder and use built-in markdown preview (Cmd+Shift+V)
**Obsidian**: Add `posts/` or `notes/` folder to vault
**Typora / Marked**: Open formatted markdown files directly

All images will display correctly since they use relative paths to local files.

### Why Two Formats?

- **original_*.md** - Human-readable markdown with remote image URLs (preserves original source)
- **formatted_*.md** - Best for offline viewing with all images local

### Why No Authentication?

Both endpoints are public:
- RSS feeds are standard syndication format (always public)
- Notes API is publicly accessible (no cookie/token required)

This makes the scraper:
- ✅ Simple to run (no setup)
- ✅ Reliable (no expired sessions)
- ✅ Fast (direct API access)
- ✅ Maintainable (fewer moving parts)
- ✅ Smart updates (only when content changes)
