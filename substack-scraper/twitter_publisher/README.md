# Twitter Publisher

Automatically publishes Substack notes to Twitter with support for both Free and Premium accounts.

## Files

- **`publish_notes.py`** - Main script that reads unpublished notes and posts them to Twitter
- **`twitter.yaml`** - Configuration file for Twitter Premium mode setting

## Configuration

Edit `twitter.yaml` to configure Twitter Premium mode:

```yaml
twitter:
  premium: true  # Set to false for Twitter Free (280 char limit)
```

### Premium Mode Features
- Posts full note content (up to 4000 characters)
- Uploads images from note folder (up to 4 images per tweet)
- Preserves text formatting (converts Markdown to Twitter-friendly format)

### Free Mode Features
- Truncates content to 280 characters
- Text-only tweets with URL link
- No image uploads

## Usage

### Manual Run (Local Testing)

```bash
# Set environment variables
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"

# Run the script
python3 publish_notes.py
```

### Automated Run (GitHub Actions)

The script is automatically run by the GitHub Actions workflow:
- **Workflow:** `.github/workflows/publish-notes-to-twitter.yml`
- **Trigger:** After notes scraper completes or manual dispatch
- **Credentials:** Stored as GitHub repository secrets

## How It Works

1. Reads unpublished notes from `../notes/` directory
2. Checks for `.published` marker file (skips if exists)
3. Extracts note content and metadata from `original_note.md`
4. Formats content for Twitter (removes Markdown syntax)
5. Uploads images (Premium mode only)
6. Posts tweet with content + link
7. Creates `.published` marker with tweet metadata

## Requirements

```bash
pip install tweepy pyyaml
```

## Debugging

The script provides detailed output:
- Configuration status (Premium/Free mode)
- Twitter client initialization
- Note processing status
- Image upload results
- Tweet posting confirmation
- Error messages with details

## Rate Limiting

- Waits 10 seconds between posts to avoid rate limits
- Twitter Free tier: 1,500 tweets/month (~50/day)
