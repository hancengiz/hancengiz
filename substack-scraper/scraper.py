#!/usr/bin/env python3
"""
Substack Content Scraper
Fetches both posts (from RSS feed) and notes (from notes page) from Substack.
"""

import feedparser
import os
import re
import json
from datetime import datetime
from html2text import html2text
from pathlib import Path
import hashlib
import urllib.request
from urllib.parse import urljoin


def sanitize_filename(title):
    """Convert title to safe filename."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces and special chars with hyphens
    filename = re.sub(r'[\s\-]+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    # Limit length
    return filename[:100].lower()


def convert_html_to_markdown(html_content):
    """Convert HTML content to markdown."""
    # Use html2text to convert HTML to markdown
    markdown = html2text(html_content)
    return markdown.strip()


def generate_file_hash(title, link):
    """Generate a unique hash for the file based on title and link."""
    content = f"{title}{link}"
    return hashlib.md5(content.encode()).hexdigest()[:8]


def hash_content(content):
    """Generate MD5 hash of content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def extract_content_from_markdown(filepath):
    """Extract content from markdown file (everything after the frontmatter)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the end of frontmatter (second occurrence of ---)
        frontmatter_count = 0
        content_start_idx = 0

        for idx, line in enumerate(lines):
            if line.strip() == '---':
                frontmatter_count += 1
                if frontmatter_count == 2:
                    content_start_idx = idx + 1
                    break

        # Return content after frontmatter
        if content_start_idx > 0:
            return ''.join(lines[content_start_idx:])
        return ''.join(lines)

    except Exception:
        return ''


def should_update_file(filepath, new_content):
    """Check if file should be updated based on content hash comparison."""
    if not os.path.exists(filepath):
        return True, "new"

    # Extract existing content (without frontmatter)
    existing_content = extract_content_from_markdown(filepath)

    # For new content, we need to extract just the content part (after frontmatter)
    # Split by --- and take everything after the second ---
    new_content_lines = new_content.split('\n')
    frontmatter_count = 0
    content_start_idx = 0

    for idx, line in enumerate(new_content_lines):
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count == 2:
                content_start_idx = idx + 1
                break

    new_content_only = '\n'.join(new_content_lines[content_start_idx:])

    # Compare hashes
    existing_hash = hash_content(existing_content)
    new_hash = hash_content(new_content_only)

    if existing_hash != new_hash:
        return True, "updated"

    return False, "unchanged"


def fetch_posts(feed_url, output_dir):
    """Fetch blog posts from RSS feed and save as markdown files."""

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Parse RSS feed
    print(f"Fetching posts from {feed_url}...")
    feed = feedparser.parse(feed_url)

    if feed.bozo:
        print(f"Warning: Feed parsing had issues: {feed.bozo_exception}")

    if not feed.entries:
        print("No posts found in feed")
        return 0

    print(f"Found {len(feed.entries)} posts")

    saved_count = 0

    for entry in feed.entries:
        try:
            # Extract entry data
            title = entry.get('title', 'Untitled')
            link = entry.get('link', '')
            pub_date = entry.get('published', '')
            author = entry.get('author', 'Unknown')

            # Get content (try different fields)
            content_html = entry.get('content', [{}])[0].get('value', '') if 'content' in entry else ''
            if not content_html:
                content_html = entry.get('summary', '')

            # Convert HTML to markdown
            content_md = convert_html_to_markdown(content_html) if content_html else 'No content available'

            # Parse date
            try:
                if pub_date:
                    parsed_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                    date_str = parsed_date.strftime('%Y-%m-%d')
                else:
                    date_str = datetime.now().strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')

            # Extract slug from URL (e.g., /p/slug-here -> slug-here)
            slug = link.split('/')[-1] if link else sanitize_filename(title)

            # Create filename using slug
            filename = f"{date_str}_{slug}.md"
            filepath = os.path.join(output_dir, filename)

            # Create markdown content with frontmatter
            markdown_content = f"""---
title: {title}
date: {pub_date}
author: {author}
url: {link}
type: post
---

# {title}

**Published:** {pub_date}
**Author:** {author}
**Link:** [{link}]({link})

---

{content_md}
"""

            # Check if file should be updated
            should_update, reason = should_update_file(filepath, markdown_content)

            if not should_update:
                print(f"  Skipping (unchanged): {filename}")
                continue

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            if reason == "new":
                print(f"  Saved: {filename}")
            else:
                print(f"  Updated: {filename}")
            saved_count += 1

        except Exception as e:
            print(f"  Error processing post '{entry.get('title', 'Unknown')}': {e}")
            continue

    print(f"Posts: Saved {saved_count} new posts to {output_dir}\n")
    return saved_count


def fetch_notes(base_url, output_dir):
    """Fetch short-form notes from Substack notes API (public, no auth needed)."""

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    notes_url = urljoin(base_url, '/api/v1/notes')

    print(f"Fetching notes from {notes_url}...")

    try:
        # Make request to notes API (public endpoint)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        req = urllib.request.Request(notes_url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

        items = data.get('items', [])

        if not items:
            print("No notes found")
            return 0

        print(f"Found {len(items)} notes")

        saved_count = 0

        for item in items:
            try:
                # Extract note data from comment object
                comment = item.get('comment', {})

                note_id = comment.get('id', '')
                name = comment.get('name', 'Unknown')
                handle = comment.get('handle', '')
                body = comment.get('body', '')
                pub_date_str = comment.get('date', '')
                photo_url = comment.get('photo_url', '')

                # Engagement metrics
                reaction_count = comment.get('reaction_count', 0)
                restacks = comment.get('restacks', 0)
                replies_count = comment.get('children_count', 0)

                # Reply context (if this note is a reply to a post)
                post = item.get('post')
                reply_to_post = None
                reply_to_url = None
                if post:
                    reply_to_post = post.get('title', '')
                    reply_to_url = post.get('canonical_url', '')

                # Build note URL - notes appear as comments in the Notes feed
                # Format: https://substack.com/@handle or publication URL
                if handle:
                    note_url = f"https://substack.com/note/c-{note_id}"
                else:
                    note_url = urljoin(base_url, f'/notes/post/{note_id}')

                # Create a title from body (notes don't have separate titles)
                if body:
                    title = body[:50] + ('...' if len(body) > 50 else '')
                else:
                    title = f'Note {note_id}'

                # Parse date
                try:
                    if pub_date_str:
                        # Substack API returns ISO format dates
                        parsed_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        date_str = parsed_date.strftime('%Y-%m-%d')
                        formatted_date = parsed_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
                    else:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        formatted_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
                except:
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    formatted_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

                # Convert body to markdown if it's HTML
                if body:
                    content_md = convert_html_to_markdown(body)
                else:
                    content_md = 'No content'

                # Create filename using note ID as slug
                slug = f"note-{note_id}"
                filename = f"{date_str}_{slug}.md"
                filepath = os.path.join(output_dir, filename)

                # Build frontmatter with conditional fields
                frontmatter = f"""---
title: {title}
date: {formatted_date}
author: {name}
handle: {handle}
url: {note_url}
type: note
note_id: {note_id}
photo_url: {photo_url}
reactions: {reaction_count}
restacks: {restacks}
replies: {replies_count}"""

                # Add reply context if this is a reply to a post
                if reply_to_post and reply_to_url:
                    frontmatter += f"""
reply_to_post: {reply_to_post}
reply_to_url: {reply_to_url}"""

                frontmatter += "\n---"

                # Build metadata section
                metadata = f"""**Published:** {formatted_date}
**Author:** {name} (@{handle})
**Link:** [{note_url}]({note_url})"""

                # Add engagement metrics if any
                if reaction_count > 0 or restacks > 0 or replies_count > 0:
                    metadata += f"""
**Engagement:** {reaction_count} reactions, {restacks} restacks, {replies_count} replies"""

                # Add reply context if present
                if reply_to_post and reply_to_url:
                    metadata += f"""
**In reply to:** [{reply_to_post}]({reply_to_url})"""

                # Create markdown content
                markdown_content = f"""{frontmatter}

# {title}

{metadata}

---

{content_md}
"""

                # Check if file should be updated
                should_update, reason = should_update_file(filepath, markdown_content)

                if not should_update:
                    print(f"  Skipping (unchanged): {filename}")
                    continue

                # Save to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                if reason == "new":
                    print(f"  Saved: {filename}")
                else:
                    print(f"  Updated: {filename}")
                saved_count += 1

            except Exception as e:
                print(f"  Error processing note '{comment.get('id', 'Unknown')}': {e}")
                continue

        print(f"Notes: Saved {saved_count} new notes to {output_dir}\n")
        return saved_count

    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching notes: {e.code} - {e.reason}")
        return 0
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return 0


def main():
    """Main function."""
    # Configuration
    BASE_URL = "https://www.cengizhan.com"
    FEED_URL = f"{BASE_URL}/feed"
    POSTS_DIR = "./posts"
    NOTES_DIR = "./notes"

    # You can override these with environment variables
    base_url = os.environ.get('SUBSTACK_BASE_URL', BASE_URL)
    feed_url = os.environ.get('SUBSTACK_FEED_URL', FEED_URL)
    posts_dir = os.environ.get('POSTS_DIR', POSTS_DIR)
    notes_dir = os.environ.get('NOTES_DIR', NOTES_DIR)

    print("=" * 60)
    print("Substack Content Scraper")
    print("=" * 60)
    print()

    # Fetch posts
    posts_saved = fetch_posts(feed_url, posts_dir)

    # Fetch notes
    notes_saved = fetch_notes(base_url, notes_dir)

    print("=" * 60)
    print(f"Total: Saved {posts_saved} posts and {notes_saved} notes")
    print("=" * 60)


if __name__ == "__main__":
    main()
