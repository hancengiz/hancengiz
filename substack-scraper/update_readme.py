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


def get_latest_notes(notes_dir, count=3):
    """Get the latest N notes from the notes directory."""
    notes = []

    if not os.path.exists(notes_dir):
        print(f"Notes directory not found: {notes_dir}")
        return []

    # Recursively find all original_note.md files
    note_files = sorted(Path(notes_dir).rglob('*/original_note.md'), reverse=True)

    for note_file in note_files:
        note_folder = note_file.parent

        try:
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)

            # Parse date
            date_str = frontmatter.get('date', '')
            try:
                parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                parsed_date = datetime.now()

            # Extract note content (after frontmatter and metadata)
            note_content = extract_first_paragraph(content)

            notes.append({
                'title': frontmatter.get('title', 'Untitled'),
                'url': frontmatter.get('url', ''),
                'date': parsed_date,
                'date_str': parsed_date.strftime('%B %d, %Y'),
                'content': note_content,
                'reactions': frontmatter.get('reactions', '0'),
                'restacks': frontmatter.get('restacks', '0')
            })
        except Exception as e:
            # Show relative path from notes_dir
            rel_path = note_folder.relative_to(Path(notes_dir))
            print(f"Error processing {rel_path}: {e}")
            continue

    # Sort by date (most recent first) and return top N
    notes.sort(key=lambda x: x['date'], reverse=True)
    return notes[:count]


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


def generate_notes_section(notes):
    """Generate the Latest Notes markdown section."""
    if not notes:
        return """## Latest Notes

No notes available yet. Check back soon!

➡️ [See all notes](https://www.cengizhan.com/notes)
"""

    lines = ["## Latest Notes", ""]

    for note in notes:
        # Truncate title if too long
        title = note['title']
        if len(title) > 60:
            title = title[:60] + '...'

        lines.append(f"**[{title}]({note['url']})** · *{note['date_str']}*")
        lines.append("")
        lines.append(note['content'])

        # Add engagement metrics if present
        reactions = int(note.get('reactions', 0))
        restacks = int(note.get('restacks', 0))
        if reactions > 0 or restacks > 0:
            metrics = []
            if reactions > 0:
                metrics.append(f"❤️ {reactions}")
            if restacks > 0:
                metrics.append(f"🔄 {restacks}")
            lines.append("")
            lines.append(f"*{' · '.join(metrics)}*")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Remove trailing separator
    if lines[-1] == "" and lines[-2] == "---":
        lines = lines[:-2]

    lines.append("")
    lines.append("➡️ [See all notes](https://www.cengizhan.com/notes)")

    return '\n'.join(lines)


def update_readme(readme_path, posts_dir, notes_dir, num_posts=3, num_notes=3):
    """Update the README.md file with latest posts and notes."""

    # Get latest posts and notes
    posts = get_latest_posts(posts_dir, num_posts)
    notes = get_latest_notes(notes_dir, num_notes)

    if not posts and not notes:
        print("No posts or notes found to update README")
        return False

    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"README not found at {readme_path}")
        return False

    updated_content = readme_content

    # Update posts section if we have posts
    if posts:
        new_posts_section = generate_blog_section(posts)
        posts_pattern = r'## Latest Blog Posts\n.*?(?=\n## |\Z)'

        if re.search(posts_pattern, updated_content, re.DOTALL):
            updated_content = re.sub(
                posts_pattern,
                new_posts_section,
                updated_content,
                flags=re.DOTALL
            )
            print(f"✓ Updated README with {len(posts)} latest posts")
            for post in posts:
                print(f"  - {post['title']} ({post['date_str']})")
        else:
            print("Could not find 'Latest Blog Posts' section in README")

    # Update notes section if we have notes
    if notes:
        new_notes_section = generate_notes_section(notes)
        notes_pattern = r'## Latest Notes\n.*?(?=\n## |\Z)'

        if re.search(notes_pattern, updated_content, re.DOTALL):
            updated_content = re.sub(
                notes_pattern,
                new_notes_section,
                updated_content,
                flags=re.DOTALL
            )
            print(f"✓ Updated README with {len(notes)} latest notes")
            for note in notes:
                print(f"  - {note['title']} ({note['date_str']})")
        else:
            print("Could not find 'Latest Notes' section in README")

    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return True


def main():
    """Main function."""
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    posts_dir = script_dir / 'posts'
    notes_dir = script_dir / 'notes'
    readme_path = repo_root / 'README.md'

    print(f"Posts directory: {posts_dir}")
    print(f"Notes directory: {notes_dir}")
    print(f"README path: {readme_path}")
    print()

    # Update README
    success = update_readme(readme_path, posts_dir, notes_dir, num_posts=3, num_notes=3)

    if success:
        print("\n✓ README updated successfully!")
    else:
        print("\n✗ Failed to update README")
        exit(1)


if __name__ == "__main__":
    main()
