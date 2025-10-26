#!/usr/bin/env node
/**
 * Convert ProseMirror JSON to Markdown
 *
 * Reads ProseMirror JSON from stdin and outputs Markdown to stdout.
 * Uses the official prosemirror-markdown library.
 */

const { schema } = require('prosemirror-markdown');
const { Node } = require('prosemirror-model');
const { MarkdownSerializer, defaultMarkdownSerializer } = require('prosemirror-markdown');

// Read JSON from stdin
let inputData = '';

process.stdin.on('data', (chunk) => {
  inputData += chunk;
});

/**
 * Convert Substack's ProseMirror format to standard ProseMirror format
 * Substack uses: bold, italic, orderedList, bulletList
 * Standard uses: strong, em, ordered_list, bullet_list
 */
function normalizeSubstackFormat(node) {
  if (!node || typeof node !== 'object') {
    return node;
  }

  // Clone the node to avoid mutation
  const normalized = Array.isArray(node) ? [...node] : { ...node };

  // Normalize node type
  if (normalized.type) {
    const typeMap = {
      'orderedList': 'ordered_list',
      'bulletList': 'bullet_list',
      'listItem': 'list_item',
      'hardBreak': 'hard_break',
      'codeBlock': 'code_block',
      'horizontalRule': 'horizontal_rule',
    };
    if (typeMap[normalized.type]) {
      normalized.type = typeMap[normalized.type];
    }
  }

  // Normalize marks
  if (normalized.marks && Array.isArray(normalized.marks)) {
    normalized.marks = normalized.marks.map(mark => {
      const markMap = {
        'bold': 'strong',
        'italic': 'em',
      };
      return {
        ...mark,
        type: markMap[mark.type] || mark.type
      };
    });
  }

  // Recursively normalize content
  if (normalized.content && Array.isArray(normalized.content)) {
    normalized.content = normalized.content.map(normalizeSubstackFormat);
  }

  return normalized;
}

process.stdin.on('end', () => {
  try {
    // Parse the ProseMirror JSON
    const prosemirrorDoc = JSON.parse(inputData);

    // Normalize Substack format to standard ProseMirror format
    const normalizedDoc = normalizeSubstackFormat(prosemirrorDoc);

    // Create a ProseMirror node from the JSON
    const doc = Node.fromJSON(schema, normalizedDoc);

    // Serialize to Markdown
    const markdown = defaultMarkdownSerializer.serialize(doc);

    // Output the markdown
    process.stdout.write(markdown);
    process.exit(0);
  } catch (error) {
    process.stderr.write(`Error: ${error.message}\n`);
    process.exit(1);
  }
});
