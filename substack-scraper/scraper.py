#!/usr/bin/env python3
"""
Substack Content Scraper
Fetches both posts (from RSS feed) and notes (from notes page) from Substack.
Creates folders with original and formatted markdown files, plus downloaded images.
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
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class ImageExtractor(HTMLParser):
    """Extract image URLs from HTML."""
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'src' in attrs_dict:
                self.images.append(attrs_dict['src'])


def sanitize_filename(title):
    """Convert title to safe filename."""
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = re.sub(r'[\s\-]+', '-', filename)
    filename = filename.strip('-')
    return filename[:100].lower()


def clean_markdown_urls(markdown_content):
    """Remove newlines and extra whitespace from URLs in markdown syntax."""
    # First, handle clickable images: [![](url1)](url2)
    # This pattern has two URLs that both need cleaning
    markdown_content = re.sub(
        r'\[!\[(.*?)\]\(([^)]+)\)\]\(([^)]+)\)',
        lambda m: f'[![{m.group(1)}]({clean_url(m.group(2))})]({clean_url(m.group(3))})',
        markdown_content,
        flags=re.DOTALL
    )

    # Then handle standalone images: ![alt](url)
    markdown_content = re.sub(
        r'!\[(.*?)\]\(([^)]+)\)',
        lambda m: f'![{m.group(1)}]({clean_url(m.group(2))})',
        markdown_content,
        flags=re.DOTALL
    )

    # Finally handle regular links: [text](url)
    markdown_content = re.sub(
        r'\[(.*?)\]\(([^)]+)\)',
        lambda m: f'[{m.group(1)}]({clean_url(m.group(2))})',
        markdown_content,
        flags=re.DOTALL
    )

    return markdown_content


def convert_html_to_markdown(html_content):
    """Convert HTML content to markdown."""
    markdown = html2text(html_content)
    # Clean up URLs by removing newlines from within parentheses
    markdown = clean_markdown_urls(markdown)
    return markdown.strip()


def apply_marks(text, marks):
    """Apply ProseMirror marks (bold, italic, links, code) to text."""
    if not marks:
        return text

    # Sort marks by type to ensure consistent nesting
    # Links should be applied last to wrap other formatting
    mark_order = {'code': 0, 'bold': 1, 'italic': 2, 'link': 3}
    sorted_marks = sorted(marks, key=lambda m: mark_order.get(m.get('type', ''), 99))

    result = text
    for mark in sorted_marks:
        mark_type = mark.get('type')
        if mark_type == 'bold':
            result = f"**{result}**"
        elif mark_type == 'italic':
            result = f"*{result}*"
        elif mark_type == 'link':
            href = mark.get('attrs', {}).get('href', '')
            result = f"[{result}]({href})"
        elif mark_type == 'code':
            result = f"`{result}`"

    return result


def parse_paragraph_node(node):
    """Parse a paragraph node from ProseMirror JSON."""
    content = node.get('content', [])
    parts = []

    for item in content:
        if item.get('type') == 'text':
            text = item.get('text', '')
            marks = item.get('marks', [])
            parts.append(apply_marks(text, marks))

    return ''.join(parts)


def parse_list_item_node(node):
    """Parse a list item node from ProseMirror JSON."""
    content = node.get('content', [])
    parts = []

    for item in content:
        if item.get('type') == 'paragraph':
            parts.append(parse_paragraph_node(item))
        elif item.get('type') == 'orderedList':
            # Nested ordered list
            parts.append('\n' + parse_ordered_list_node(item, indent_level=1))
        elif item.get('type') == 'bulletList':
            # Nested bullet list
            parts.append('\n' + parse_bullet_list_node(item, indent_level=1))

    return ' '.join(parts)


def parse_ordered_list_node(node, indent_level=0):
    """Parse an ordered list node from ProseMirror JSON."""
    content = node.get('content', [])
    lines = []
    indent = '  ' * indent_level

    for idx, item in enumerate(content, 1):
        if item.get('type') == 'listItem':
            item_text = parse_list_item_node(item)
            lines.append(f"{indent}{idx}. {item_text}")

    return '\n'.join(lines)


def parse_bullet_list_node(node, indent_level=0):
    """Parse a bullet list node from ProseMirror JSON."""
    content = node.get('content', [])
    lines = []
    indent = '  ' * indent_level

    for item in content:
        if item.get('type') == 'listItem':
            item_text = parse_list_item_node(item)
            lines.append(f"{indent}- {item_text}")

    return '\n'.join(lines)


def parse_body_json_to_markdown_custom(body_json):
    """Parse Substack's ProseMirror-style body_json to markdown using custom parser."""
    if not body_json or not isinstance(body_json, dict):
        return ""

    content = body_json.get('content', [])
    if not content:
        return ""

    paragraphs = []
    for node in content:
        node_type = node.get('type')

        if node_type == 'paragraph':
            para_text = parse_paragraph_node(node)
            if para_text:  # Only add non-empty paragraphs
                paragraphs.append(para_text)
        elif node_type == 'orderedList':
            list_text = parse_ordered_list_node(node)
            if list_text:
                paragraphs.append(list_text)
        elif node_type == 'bulletList':
            list_text = parse_bullet_list_node(node)
            if list_text:
                paragraphs.append(list_text)

    return '\n\n'.join(paragraphs)


def parse_body_json_to_markdown(body_json):
    """
    Parse Substack's ProseMirror-style body_json to markdown.

    Uses the official prosemirror-markdown Node.js library via subprocess.
    Falls back to custom parser if Node.js is not available.
    """
    if not body_json or not isinstance(body_json, dict):
        return ""

    try:
        import subprocess

        # Get the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        converter_script = os.path.join(script_dir, 'prosemirror-to-markdown.js')

        # Call Node.js script with JSON input
        result = subprocess.run(
            ['node', converter_script],
            input=json.dumps(body_json),
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Warning: Node.js converter failed: {result.stderr}")
            print(f"  Falling back to custom parser...")
            return parse_body_json_to_markdown_custom(body_json)

    except FileNotFoundError:
        print(f"Warning: Node.js not found, falling back to custom parser...")
        return parse_body_json_to_markdown_custom(body_json)
    except Exception as e:
        print(f"Warning: Failed to parse body_json with Node.js: {e}")
        print(f"  Falling back to custom parser...")
        return parse_body_json_to_markdown_custom(body_json)


def extract_images_from_html(html_content):
    """Extract all image URLs from HTML content."""
    parser = ImageExtractor()
    parser.feed(html_content)
    return parser.images


def extract_images_from_markdown(markdown_content):
    """Extract image URLs from markdown content."""
    # Match markdown image syntax: ![alt](url)
    # Allow newlines within URLs to handle wrapped text
    pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    return re.findall(pattern, markdown_content, re.DOTALL)


def download_image(url, filepath):
    """Download an image from URL to filepath."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    Failed to download {url}: {e}")
        return False


def clean_url(url):
    """Remove newlines and extra whitespace from URLs."""
    return re.sub(r'\s+', '', url)


def replace_image_urls_with_local(markdown_content, url_to_filename_map):
    """Replace remote image URLs with local file paths in markdown."""
    result = markdown_content
    for url, filename in url_to_filename_map.items():
        # Replace in markdown image syntax and bare URLs
        # URL may contain newlines from text wrapping
        result = result.replace(f']({url})', f']({filename})')
        result = result.replace(url, filename)

    # Remove clickable image wrappers that link to Substack CDN
    # Convert [![](local_image)](https://substackcdn...) to just ![](local_image)
    result = re.sub(
        r'\[!\[(.*?)\]\((image\d+\.[^)]+)\)\]\(https?://substackcdn\.com/[^)]+\)',
        r'![\1](\2)',
        result,
        flags=re.DOTALL
    )

    return result


def hash_content(content):
    """Generate MD5 hash of content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def should_update_folder(folder_path, new_content_hash):
    """Check if folder content should be updated."""
    original_file = os.path.join(folder_path, 'original_post.md')
    if not os.path.exists(folder_path):
        return True, "new"

    if not os.path.exists(original_file):
        original_file = os.path.join(folder_path, 'original_note.md')

    if not os.path.exists(original_file):
        return True, "new"

    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        existing_hash = hash_content(existing_content)

        if existing_hash != new_content_hash:
            return True, "updated"
        return False, "unchanged"
    except:
        return True, "new"


def download_images_to_folder(image_urls, folder_path, url_variants=None):
    """
    Download images to a folder and return URL-to-filename mapping.

    Args:
        image_urls: List of clean image URLs to download
        folder_path: Destination folder path
        url_variants: Optional dict mapping clean URLs to list of URL variants (for posts)

    Returns:
        dict: Mapping from URL (and variants) to local filename
    """
    url_to_filename = {}

    for idx, img_url in enumerate(image_urls, 1):
        # Determine file extension
        parsed_url = urlparse(img_url)
        path = parsed_url.path

        # Try to extract extension from URL
        ext = os.path.splitext(path)[1].lower()
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            ext = '.jpg'  # default extension

        # Use sequential numbering
        img_filename = f"image{idx}{ext}"
        img_path = os.path.join(folder_path, img_filename)

        # Download image
        if download_image(img_url, img_path):
            # If url_variants provided (for posts), map all variants
            if url_variants:
                for variant in url_variants.get(img_url, [img_url]):
                    url_to_filename[variant] = img_filename
            else:
                # For notes, just map the clean URL
                url_to_filename[img_url] = img_filename

    return url_to_filename


def build_post_frontmatter(title, pub_date, author, link):
    """Build YAML frontmatter for a post."""
    return f"""---
title: {title}
date: {pub_date}
author: {author}
url: {link}
type: post
---"""


def build_note_frontmatter(title, formatted_date, name, handle, note_url, note_id,
                          photo_url, reaction_count, restacks, replies_count,
                          reply_to_post=None, reply_to_url=None):
    """Build YAML frontmatter for a note."""
    frontmatter = f"""---
title: {title}
published: {formatted_date}
author: {name}
handle: {handle}
url: {note_url}
type: note
note_id: {note_id}
photo_url: {photo_url}
reactions: {reaction_count}
restacks: {restacks}
replies: {replies_count}"""

    if reply_to_post and reply_to_url:
        frontmatter += f"""
reply_to_post: {reply_to_post}
reply_to_url: {reply_to_url}"""

    frontmatter += "\n---"
    return frontmatter


def build_post_metadata(title, pub_date, author, link):
    """Build metadata section for a post."""
    return f"""# {title}

**Published:** {pub_date}
**Author:** {author}
**Link:** [{link}]({link})

---"""


def build_note_metadata(title, formatted_date, name, handle, note_url,
                       reaction_count, restacks, replies_count,
                       reply_to_post=None, reply_to_url=None):
    """Build metadata section for a note."""
    metadata = f"""**Published:** {formatted_date}
**Author:** {name} (@{handle})
**Link:** [{note_url}]({note_url})"""

    if reaction_count > 0 or restacks > 0 or replies_count > 0:
        metadata += f"""
**Engagement:** {reaction_count} reactions, {restacks} restacks, {replies_count} replies"""

    if reply_to_post and reply_to_url:
        metadata += f"""
**In reply to:** [{reply_to_post}]({reply_to_url})"""

    metadata += "\n\n---"
    return metadata


def fetch_posts(feed_url, output_dir):
    """Fetch blog posts from RSS feed and save as folders with markdown and images."""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

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

            # Get content HTML
            content_html = entry.get('content', [{}])[0].get('value', '') if 'content' in entry else ''
            if not content_html:
                content_html = entry.get('summary', '')

            # Convert HTML to markdown first
            content_md = convert_html_to_markdown(content_html) if content_html else 'No content available'

            # Extract images from both HTML and markdown to catch all image URLs
            html_image_urls = extract_images_from_html(content_html)
            markdown_image_urls_raw = extract_images_from_markdown(content_md)

            # Build mapping from clean URLs to original URLs (preserving newlines for replacement)
            url_variants = {}  # clean_url -> list of original variants
            for url in html_image_urls + markdown_image_urls_raw:
                clean = clean_url(url)
                if clean not in url_variants:
                    url_variants[clean] = []
                if url not in url_variants[clean]:
                    url_variants[clean].append(url)

            # Use clean URLs for downloading
            image_urls = list(url_variants.keys())

            # Parse date
            try:
                if pub_date:
                    parsed_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                    date_str = parsed_date.strftime('%Y-%m-%d')
                else:
                    date_str = datetime.now().strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')

            # Extract slug from URL
            slug = link.split('/')[-1] if link else sanitize_filename(title)

            # Create folder name
            folder_name = f"{date_str}_{slug}"
            folder_path = os.path.join(output_dir, folder_name)

            # Build markdown content
            frontmatter = build_post_frontmatter(title, pub_date, author, link)
            metadata = build_post_metadata(title, pub_date, author, link)
            original_markdown = f"""{frontmatter}

{metadata}

{content_md}
"""

            # Check if update is needed
            content_hash = hash_content(original_markdown)
            should_update, reason = should_update_folder(folder_path, content_hash)

            if not should_update:
                print(f"  Skipping (unchanged): {folder_name}")
                continue

            # Create folder
            Path(folder_path).mkdir(parents=True, exist_ok=True)

            # Save original markdown (with remote URLs)
            original_path = os.path.join(folder_path, 'original_post.md')
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write(original_markdown)

            # Download images and build URL mapping
            url_to_filename = download_images_to_folder(image_urls, folder_path, url_variants)

            # Create formatted markdown with local image paths
            formatted_markdown = replace_image_urls_with_local(original_markdown, url_to_filename)
            formatted_path = os.path.join(folder_path, 'formatted_post.md')
            with open(formatted_path, 'w', encoding='utf-8') as f:
                f.write(formatted_markdown)

            if reason == "new":
                print(f"  Saved: {folder_name} ({len(url_to_filename)} images)")
            else:
                print(f"  Updated: {folder_name} ({len(url_to_filename)} images)")
            saved_count += 1

        except Exception as e:
            print(f"  Error processing post '{entry.get('title', 'Unknown')}': {e}")
            continue

    print(f"Posts: Saved {saved_count} new posts to {output_dir}\n")
    return saved_count


def fetch_notes(base_url, output_dir):
    """Fetch short-form notes from Substack notes API and save as folders with markdown and images."""

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    notes_url = urljoin(base_url, '/api/v1/notes')

    print(f"Fetching notes from {notes_url}...")

    try:
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
                # Skip restacks - only save original notes
                context = item.get('context', {})
                if context.get('type') == 'comment_restack':
                    continue

                comment = item.get('comment', {})

                note_id = comment.get('id', '')

                # Skip items without a valid note_id (e.g., likes on other posts)
                if not note_id:
                    continue

                name = comment.get('name', 'Unknown')
                handle = comment.get('handle', '')
                body = comment.get('body', '')
                body_json = comment.get('body_json', {})
                pub_date_str = comment.get('date', '')
                photo_url = comment.get('photo_url', '')

                # Engagement metrics
                reaction_count = comment.get('reaction_count', 0)
                restacks = comment.get('restacks', 0)
                replies_count = comment.get('children_count', 0)

                # Extract attachment images (separate from body content)
                attachments = comment.get('attachments', [])
                attachment_image_urls = []
                for attachment in attachments:
                    if attachment.get('type') == 'image':
                        img_url = attachment.get('imageUrl', '')
                        if img_url:
                            attachment_image_urls.append(img_url)

                # Reply context
                post = item.get('post')
                reply_to_post = None
                reply_to_url = None
                if post:
                    reply_to_post = post.get('title', '')
                    reply_to_url = post.get('canonical_url', '')

                # Build note URL
                if handle:
                    note_url = f"https://substack.com/note/c-{note_id}"
                else:
                    note_url = urljoin(base_url, f'/notes/post/{note_id}')

                # Substack notes don't have titles, just use note ID as identifier
                title = f'Note {note_id}'

                # Parse date
                try:
                    if pub_date_str:
                        parsed_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        year = parsed_date.strftime('%Y')
                        month = parsed_date.strftime('%m')
                        day = parsed_date.strftime('%d')
                        formatted_date = parsed_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
                    else:
                        now = datetime.now()
                        year = now.strftime('%Y')
                        month = now.strftime('%m')
                        day = now.strftime('%d')
                        formatted_date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
                except:
                    now = datetime.now()
                    year = now.strftime('%Y')
                    month = now.strftime('%m')
                    day = now.strftime('%d')
                    formatted_date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

                # Convert body_json to markdown (with fallback to plain body)
                if body_json and isinstance(body_json, dict) and body_json.get('content'):
                    # Parse structured JSON format with formatting preserved
                    content_md = parse_body_json_to_markdown(body_json)
                elif body:
                    # Fallback to plain text body (legacy support)
                    content_md = body
                else:
                    content_md = 'No content'

                # Append attachment images to markdown content
                if attachment_image_urls:
                    content_md += '\n\n'
                    for idx, img_url in enumerate(attachment_image_urls):
                        content_md += f'![Image]({img_url})'
                        # Add newline between images, but not after the last one
                        if idx < len(attachment_image_urls) - 1:
                            content_md += '\n\n'

                # Extract images from markdown and clean URLs (remove newlines from wrapped text)
                markdown_image_urls = extract_images_from_markdown(content_md)
                image_urls = list(set(clean_url(url) for url in markdown_image_urls))

                # Add attachment images to the list
                for att_url in attachment_image_urls:
                    clean_att_url = clean_url(att_url)
                    if clean_att_url not in image_urls:
                        image_urls.append(clean_att_url)

                # Create folder structure: notes/YYYY/MM/DD_note-ID
                slug = f"note-{note_id}"
                folder_name = f"{day}_{slug}"
                year_month_dir = os.path.join(output_dir, year, month)
                folder_path = os.path.join(year_month_dir, folder_name)

                # Build markdown content
                frontmatter = build_note_frontmatter(
                    title, formatted_date, name, handle, note_url, note_id,
                    photo_url, reaction_count, restacks, replies_count,
                    reply_to_post, reply_to_url
                )
                original_markdown = f"""{frontmatter}
{content_md}
"""

                # Check if update is needed
                content_hash = hash_content(original_markdown)
                should_update, reason = should_update_folder(folder_path, content_hash)

                if not should_update:
                    print(f"  Skipping (unchanged): {year}/{month}/{folder_name}")
                    continue

                # Create year/month directories and note folder
                Path(folder_path).mkdir(parents=True, exist_ok=True)

                # Save original markdown (with remote URLs)
                original_path = os.path.join(folder_path, 'original_note.md')
                with open(original_path, 'w', encoding='utf-8') as f:
                    f.write(original_markdown)

                # Download images and build URL mapping
                url_to_filename = download_images_to_folder(image_urls, folder_path)

                # Create formatted markdown with local image paths
                formatted_markdown = replace_image_urls_with_local(original_markdown, url_to_filename)
                formatted_path = os.path.join(folder_path, 'formatted_note.md')
                with open(formatted_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_markdown)

                if reason == "new":
                    print(f"  Saved: {year}/{month}/{folder_name} ({len(url_to_filename)} images)")
                else:
                    print(f"  Updated: {year}/{month}/{folder_name} ({len(url_to_filename)} images)")
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
    BASE_URL = "https://www.cengizhan.com"
    FEED_URL = f"{BASE_URL}/feed"
    POSTS_DIR = "./posts"
    NOTES_DIR = "./notes"

    base_url = os.environ.get('SUBSTACK_BASE_URL', BASE_URL)
    feed_url = os.environ.get('SUBSTACK_FEED_URL', FEED_URL)
    posts_dir = os.environ.get('POSTS_DIR', POSTS_DIR)
    notes_dir = os.environ.get('NOTES_DIR', NOTES_DIR)

    print("=" * 60)
    print("Substack Content Scraper")
    print("=" * 60)
    print()

    posts_saved = fetch_posts(feed_url, posts_dir)
    notes_saved = fetch_notes(base_url, notes_dir)

    print("=" * 60)
    print(f"Total: Saved {posts_saved} posts and {notes_saved} notes")
    print("=" * 60)


if __name__ == "__main__":
    main()
