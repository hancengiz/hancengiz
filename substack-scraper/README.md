# Substack Content Scraper

Automatically fetches blog posts and notes from your Substack and saves them as markdown files.

## Structure

```text
substack-scraper/
├── scraper.py          # Main scraper script
├── requirements.txt    # feedparser, html2text
├── posts/             # Blog posts (from RSS feed)
└── notes/             # Short-form notes (from public API)
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

Two separate workflows run independently:

- **Posts**: Every 6 hours (`.github/workflows/substack-posts.yml`)
- **Notes**: Every 5 minutes (`.github/workflows/substack-notes.yml`)

Both run automatically, no setup required.

## File Format

Files saved as `YYYY-MM-DD_slug.md` using Substack's URL slugs:

**Posts**: `2025-10-25_the-ai-native-way-of-building.md`
**Notes**: `2025-10-26_note-170317259.md`

All files include YAML frontmatter:

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
- cron: '0 */6 * * *'   # Every 6 hours (current)
- cron: '0 0 * * *'     # Daily
- cron: '0 0,12 * * *'  # Twice daily
```

**Notes** (`.github/workflows/substack-notes.yml`):

```yaml
- cron: '*/5 * * * *'   # Every 5 minutes (current)
- cron: '*/15 * * * *'  # Every 15 minutes
- cron: '0 * * * *'     # Hourly
```

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
- New content → saved
- Changed content → updated
- Unchanged content → skipped

This means:
- ✅ Captures edits to posts/notes
- ✅ Updates engagement metrics (reactions, restacks, replies)
- ✅ Doesn't create duplicate files
- ✅ Only rewrites files when content actually changes

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
