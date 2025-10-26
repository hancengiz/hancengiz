#!/usr/bin/env python3
"""
Update README.md with latest Substack posts.
Reads posts from substack-scraper/posts/ and updates the Latest Blog Posts section.
"""

import os
import re
from datetime import datetime
from pathlib import Path


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

        # Clean up and truncate
        clean = para.replace('\n', ' ').strip()

        # Remove any remaining markdown bold/italic
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)  # bold
        clean = re.sub(r'_([^_]+)_', r'\1', clean)  # italic

        if len(clean) > 250:
            clean = clean[:250].rsplit(' ', 1)[0] + '...'

        return clean

    return "Read the full post for more details."


def get_latest_posts(posts_dir, count=3):
    """Get the latest N posts from the posts directory."""
    posts = []

    if not os.path.exists(posts_dir):
        print(f"Posts directory not found: {posts_dir}")
        return []

    # Iterate through all post folders
    for folder in sorted(Path(posts_dir).iterdir(), reverse=True):
        if not folder.is_dir():
            continue

        # Read original_post.md
        post_file = folder / 'original_post.md'
        if not post_file.exists():
            continue

        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)

            # Parse date
            date_str = frontmatter.get('date', '')
            try:
                parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                parsed_date = datetime.now()

            posts.append({
                'title': frontmatter.get('title', 'Untitled'),
                'url': frontmatter.get('url', ''),
                'date': parsed_date,
                'date_str': parsed_date.strftime('%B %d, %Y'),
                'description': extract_first_paragraph(content)
            })
        except Exception as e:
            print(f"Error processing {folder.name}: {e}")
            continue

    # Sort by date (most recent first) and return top N
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts[:count]


def generate_blog_section(posts):
    """Generate the Latest Blog Posts markdown section."""
    if not posts:
        return """## Latest Blog Posts

No posts available yet. Check back soon!

➡️ [Read more on my blog](https://www.cengizhan.com)
"""

    lines = ["## Latest Blog Posts", ""]

    for post in posts:
        lines.append(f"### [{post['title']}]({post['url']})")
        lines.append(f"*{post['date_str']}*")
        lines.append("")
        lines.append(post['description'])
        lines.append("")

    lines.append("➡️ [Read more on my blog](https://www.cengizhan.com)")

    return '\n'.join(lines)


def update_readme(readme_path, posts_dir, num_posts=3):
    """Update the README.md file with latest posts."""

    # Get latest posts
    posts = get_latest_posts(posts_dir, num_posts)

    if not posts:
        print("No posts found to update README")
        return False

    # Generate new section
    new_section = generate_blog_section(posts)

    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"README not found at {readme_path}")
        return False

    # Find and replace the Latest Blog Posts section
    # Pattern matches from "## Latest Blog Posts" to the next "## " section
    pattern = r'## Latest Blog Posts\n.*?(?=\n## |\n---\n|\Z)'

    if not re.search(pattern, readme_content, re.DOTALL):
        print("Could not find 'Latest Blog Posts' section in README")
        return False

    # Replace the section
    updated_content = re.sub(
        pattern,
        new_section,
        readme_content,
        flags=re.DOTALL
    )

    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✓ Updated README with {len(posts)} latest posts")
    for post in posts:
        print(f"  - {post['title']} ({post['date_str']})")

    return True


def main():
    """Main function."""
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    posts_dir = script_dir / 'posts'
    readme_path = repo_root / 'README.md'

    print(f"Posts directory: {posts_dir}")
    print(f"README path: {readme_path}")
    print()

    # Update README
    success = update_readme(readme_path, posts_dir, num_posts=3)

    if success:
        print("\n✓ README updated successfully!")
    else:
        print("\n✗ Failed to update README")
        exit(1)


if __name__ == "__main__":
    main()
