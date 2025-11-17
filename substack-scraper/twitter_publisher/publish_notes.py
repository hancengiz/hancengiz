#!/usr/bin/env python3
"""
Publish Substack notes to Twitter.

Reads unpublished notes from the notes directory and posts them to Twitter
using the Twitter API. Supports both Free and Premium Twitter accounts with
image uploads for Premium users.
"""

import os
import re
import sys
import time
import yaml
from pathlib import Path
from datetime import datetime
import tweepy


def parse_frontmatter(content):
    """Extract frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_content(content):
    """Extract main content from note (after frontmatter)."""
    # Remove frontmatter (handles both with and without blank line after ---)
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    return content.strip()


def text_to_unicode_bold(text):
    """Convert text to Unicode bold characters."""
    bold_map = {}

    # A-Z: 𝗔-𝗭 (U+1D5D4 - U+1D5ED)
    for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        bold_map[char] = chr(0x1D5D4 + i)

    # a-z: 𝗮-𝘇 (U+1D5EE - U+1D607)
    for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
        bold_map[char] = chr(0x1D5EE + i)

    # 0-9: 𝟬-𝟵 (U+1D7EC - U+1D7F5)
    for i, char in enumerate('0123456789'):
        bold_map[char] = chr(0x1D7EC + i)

    # Convert each character to bold if mapping exists, otherwise keep as-is
    return ''.join(bold_map.get(c, c) for c in text)


def format_for_twitter(content):
    """Convert Markdown formatting to Twitter-friendly text."""
    # Preserve the content but clean up markdown syntax for Twitter
    # Twitter doesn't support Markdown, so we'll keep basic formatting

    # Remove markdown images ![alt](url) - images will be attached via media_ids
    content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)

    # Convert bold (**text** or __text__) to Unicode bold characters
    content = re.sub(r'\*\*([^*]+)\*\*', lambda m: text_to_unicode_bold(m.group(1)), content)
    content = re.sub(r'__([^_]+)__', lambda m: text_to_unicode_bold(m.group(1)), content)

    # Convert italic (*text* or _text_) - just keep the text
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)

    # Convert inline code (`code`) - just keep the text
    content = re.sub(r'`([^`]+)`', r'\1', content)

    # Convert markdown links [text](url) to Twitter-friendly format
    # If link text is the same as URL, just show URL once (Twitter auto-links)
    # Otherwise show "text: url"
    def convert_link(match):
        text = match.group(1)
        url = match.group(2)
        # If text is the same as URL (or a shortened version), just return the URL
        if text == url or text.startswith('http') and url.startswith(text):
            return url
        # Otherwise return "text: url"
        return f"{text}: {url}"

    content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', convert_link, content)

    # Remove heading markers (# ## ###)
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

    # Remove horizontal rules (---, ___, ***)
    content = re.sub(r'^[\-_*]{3,}$', '', content, flags=re.MULTILINE)

    # Clean up multiple newlines (keep max 2 for paragraph breaks)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def post_to_twitter(twitter_client, content, url, premium_mode=False, note_folder=None):
    """Post note to Twitter using tweepy. Returns tweet_id on success, None on failure."""
    if not twitter_client:
        print("⚠️  Twitter credentials not set, skipping post")
        return None

    try:
        media_ids = []

        # Handle images in premium mode
        if premium_mode and note_folder:
            print("🖼️  Checking for images to include...")
            # Look for image files in the note folder
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_files = []

            for ext in image_extensions:
                image_files.extend(list(note_folder.glob(f'*{ext}')))
                image_files.extend(list(note_folder.glob(f'*{ext.upper()}')))

            # Twitter allows up to 4 images per tweet
            image_files = sorted(image_files)[:4]

            if image_files:
                print(f"📸 Found {len(image_files)} image(s) to upload")
                # Upload images to Twitter
                api_key = os.environ.get('TWITTER_API_KEY')
                api_secret = os.environ.get('TWITTER_API_SECRET')
                access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
                access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

                # Use tweepy API v1.1 for media upload
                auth = tweepy.OAuth1UserHandler(
                    api_key, api_secret, access_token, access_token_secret
                )
                api_v1 = tweepy.API(auth)

                for img_file in image_files:
                    try:
                        media = api_v1.media_upload(filename=str(img_file))
                        media_ids.append(media.media_id)
                        print(f"  ✓ Uploaded: {img_file.name}")
                    except Exception as e:
                        print(f"  ✗ Failed to upload {img_file.name}: {e}")
            else:
                print("  No images found in note folder")

        # Format tweet based on premium mode
        if premium_mode:
            # Premium mode: Post full content with formatting preserved
            print("📱 Using Twitter Premium mode - posting full content with formatting")
            formatted_content = format_for_twitter(content)
            tweet_text = formatted_content + f'\n\n👉 {url}'
        else:
            # Free mode: Use current truncation logic (280 char limit)
            print("📱 Using Twitter Free mode - truncating to 280 chars")
            # Leave room for URL (23 chars) + formatting
            max_content_length = 250

            if len(content) > max_content_length:
                tweet_text = content[:max_content_length].rsplit(' ', 1)[0] + '...\n\n'
            else:
                tweet_text = content + '\n\n'

            tweet_text += f"👉 {url}"

            # Ensure tweet doesn't exceed 280 characters
            if len(tweet_text) > 280:
                # Recalculate with smaller content
                max_content_length = 280 - len(f"\n\n👉 {url}") - 3  # -3 for "..."
                tweet_text = content[:max_content_length].rsplit(' ', 1)[0] + f'...\n\n👉 {url}'

        # Post tweet with media if available
        if media_ids:
            response = twitter_client.create_tweet(text=tweet_text, media_ids=media_ids)
            print(f"  📎 Attached {len(media_ids)} image(s)")
        else:
            response = twitter_client.create_tweet(text=tweet_text)

        tweet_id = response.data['id']

        print(f"✓ Successfully posted to Twitter")
        print(f"  Tweet ID: {tweet_id}")
        print(f"  Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
        print(f"  Length: {len(tweet_text)} chars")
        print(f"  Preview: {tweet_text[:100]}...")

        return tweet_id

    except tweepy.TweepyException as e:
        print(f"✗ Twitter API error: {e}")
        return None
    except Exception as e:
        print(f"✗ Error posting to Twitter: {e}")
        return None


def main():
    """Main function to publish notes to Twitter."""
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    notes_dir = project_root / 'substack-scraper' / 'notes'

    # Read Twitter Premium setting from config file
    config_path = script_dir / 'twitter.yaml'
    twitter_premium = False  # Default to free mode

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                twitter_premium = config.get('twitter', {}).get('premium', False)
            print(f"🔧 Twitter Premium Mode: {'Enabled' if twitter_premium else 'Disabled'}")
        except Exception as e:
            print(f"⚠️  Error reading twitter.yaml: {e}")
            print(f"🔧 Defaulting to Twitter Free Mode")
    else:
        print(f"⚠️  twitter.yaml not found at {config_path}")
        print(f"🔧 Defaulting to Twitter Free Mode")

    # Initialize Twitter client
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    twitter_client = None
    if api_key and api_secret and access_token and access_token_secret:
        try:
            twitter_client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            print("✓ Twitter client initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Twitter client: {e}")
            sys.exit(1)
    else:
        print("✗ Twitter credentials not set. Please add secrets:")
        print("  - TWITTER_API_KEY")
        print("  - TWITTER_API_SECRET")
        print("  - TWITTER_ACCESS_TOKEN")
        print("  - TWITTER_ACCESS_TOKEN_SECRET")
        sys.exit(1)

    if not notes_dir.exists():
        print(f"Notes directory not found: {notes_dir}")
        sys.exit(0)

    published_count = 0

    # Recursively find all original_note.md files
    note_files = sorted(notes_dir.rglob('*/original_note.md'))

    for note_file in note_files:
        note_folder = note_file.parent

        # Check if already published
        published_marker = note_folder / '.published'
        if published_marker.exists():
            # Show relative path from notes_dir
            rel_path = note_folder.relative_to(notes_dir)
            print(f"⏭️  Skipping {rel_path} (already published)")
            continue

        try:
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter and content
            frontmatter = parse_frontmatter(content)
            main_content = extract_content(content)

            note_id = frontmatter.get('note_id', '')
            note_url = frontmatter.get('url', '')

            # Show relative path from notes_dir
            rel_path = note_folder.relative_to(notes_dir)
            print(f"\n📝 Publishing note: {rel_path}")
            print(f"   Note ID: {note_id}")
            print(f"   URL: {note_url}")
            print(f"   Content length: {len(main_content)} chars")

            # Post to Twitter
            tweet_id = post_to_twitter(twitter_client, main_content, note_url, twitter_premium, note_folder)

            if tweet_id:
                # Mark as published with tweet metadata
                tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
                with open(published_marker, 'w') as f:
                    f.write(f"published_at: {datetime.utcnow().isoformat()}Z\n")
                    f.write(f"tweet_id: {tweet_id}\n")
                    f.write(f"tweet_url: {tweet_url}\n")

                published_count += 1
                print(f"✓ Marked as published")

                # Rate limiting - wait 10 seconds before next post
                time.sleep(10)
            else:
                print(f"✗ Failed to publish, will retry next run")

        except Exception as e:
            rel_path = note_folder.relative_to(notes_dir)
            print(f"✗ Error processing {rel_path}: {e}")
            continue

    print(f"\n{'='*50}")
    print(f"Published {published_count} new note(s) to Twitter")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
