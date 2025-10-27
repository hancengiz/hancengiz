#!/usr/bin/env python3
"""
Publish Substack blog posts to Twitter.

Reads unpublished blog posts from the posts directory and posts them to Twitter
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


def extract_first_paragraph(content):
    """Extract first meaningful paragraph from markdown content."""
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove title heading
    content = re.sub(r'^#\s+.*?\n', '', content, flags=re.DOTALL)

    # Remove metadata section (**Published:** ... **Link:** ... \n---)
    content = re.sub(r'^\*\*Published:.*?^---\n', '', content, flags=re.DOTALL | re.MULTILINE)

    # Split into paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

    # Find first substantial paragraph (not headings, images, or very short)
    for para in paragraphs:
        # Skip headings
        if para.startswith('#'):
            continue
        # Skip images (both markdown and clickable images)
        if para.startswith('![') or para.startswith('[!['):
            continue
        # Skip horizontal rules
        if para.startswith('* * *') or para.startswith('---'):
            continue
        # Skip "Thanks for reading" type paragraphs
        if 'Thanks for reading' in para or 'Subscribe' in para:
            continue
        # Skip very short paragraphs
        if len(para) < 50:
            continue

        # Clean up and return
        clean = para.replace('\n', ' ').strip()

        # Remove any remaining markdown bold/italic
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)  # bold
        clean = re.sub(r'_([^_]+)_', r'\1', clean)  # italic

        return clean

    return "Read the full post for more details."


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


def post_to_twitter(twitter_client, title, content, url, premium_mode=False, post_folder=None):
    """Post blog post to Twitter using tweepy. Returns tweet_id on success, None on failure."""
    if not twitter_client:
        print("⚠️  Twitter credentials not set, skipping post")
        return None

    try:
        media_ids = []

        # Handle images in premium mode
        if premium_mode and post_folder:
            print("🖼️  Checking for images to include...")
            # Look for image files in the post folder
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_files = []

            for ext in image_extensions:
                image_files.extend(list(post_folder.glob(f'*{ext}')))
                image_files.extend(list(post_folder.glob(f'*{ext.upper()}')))

            # Twitter allows up to 4 images per tweet, but for blog posts we'll just use the first one
            image_files = sorted(image_files)[:1]

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
                print("  No images found in post folder")

        # Format tweet based on premium mode
        if premium_mode:
            # Premium mode: Post formatted content with title
            print("📱 Using Twitter Premium mode - posting with formatting")
            # Leave room for URL (23 chars) + title + formatting
            formatted_content = format_for_twitter(content)

            # Calculate available space for content
            # Tweet format: "Title\n\n[content]\n\n👉 [url]"
            url_part = f'\n\n👉 {url}'
            title_part = f'{title}\n\n'
            available_space = 280 - len(url_part) - len(title_part)

            if len(formatted_content) > available_space:
                truncated_content = formatted_content[:available_space].rsplit(' ', 1)[0] + '...'
            else:
                truncated_content = formatted_content

            tweet_text = title_part + truncated_content + url_part
        else:
            # Free mode: Truncate to fit in 280 chars
            print("📱 Using Twitter Free mode - truncating to 280 chars")
            # Leave room for URL (23 chars) + formatting
            url_part = f'\n\n👉 {url}'
            max_content_length = 280 - len(url_part) - 3  # -3 for "..."

            if len(content) > max_content_length:
                tweet_text = content[:max_content_length].rsplit(' ', 1)[0] + '...'
            else:
                tweet_text = content

            tweet_text += url_part

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
    """Main function to publish blog posts to Twitter."""
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    posts_dir = project_root / 'substack-scraper' / 'posts'

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

    if not posts_dir.exists():
        print(f"Posts directory not found: {posts_dir}")
        sys.exit(0)

    published_count = 0

    # Find all post folders
    post_folders = sorted([f for f in posts_dir.iterdir() if f.is_dir()], reverse=True)

    for post_folder in post_folders:
        # Check if original_post.md exists
        post_file = post_folder / 'original_post.md'
        if not post_file.exists():
            continue

        # Check if already published
        published_marker = post_folder / '.published'
        if published_marker.exists():
            print(f"⏭️  Skipping {post_folder.name} (already published)")
            continue

        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter and extract summary
            frontmatter = parse_frontmatter(content)
            summary = extract_first_paragraph(content)

            title = frontmatter.get('title', 'Untitled')
            post_url = frontmatter.get('url', '')

            print(f"\n📝 Publishing post: {post_folder.name}")
            print(f"   Title: {title}")
            print(f"   URL: {post_url}")
            print(f"   Summary length: {len(summary)} chars")

            # Post to Twitter
            tweet_id = post_to_twitter(twitter_client, title, summary, post_url, twitter_premium, post_folder)

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
            print(f"✗ Error processing {post_folder.name}: {e}")
            continue

    print(f"\n{'='*50}")
    print(f"Published {published_count} new post(s) to Twitter")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
