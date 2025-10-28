---
title: Vibe Coded a PDF Reader MCP Tool for Claude Code - to save my context
date: Mon, 27 Oct 2025 18:33:31 GMT
author: Cengiz Han
url: https://www.cengizhan.com/p/vibe-coded-a-pdf-reader-mcp-tool
type: post
---

# Vibe Coded a PDF Reader MCP Tool for Claude Code - to save my context

**Published:** Mon, 27 Oct 2025 18:33:31 GMT
**Author:** Cengiz Han
**Link:** [https://www.cengizhan.com/p/vibe-coded-a-pdf-reader-mcp-tool](https://www.cengizhan.com/p/vibe-coded-a-pdf-reader-mcp-tool)

---

So I got annoyed and built something. Again. 🤓

Last week I was trying to analyze yet another massive McKinsey report with
Claude, watching my precious context window evaporate, and I thought: "there
has to be a better way."

An hour of vibe-coding with Claude Code later, I had a working MCP server.
Published it to npm. It's called **PDF Reader MCP Server** and it solves my
exact problem.

[![](https://substackcdn.com/image/fetch/$s_!KyGa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F774dbcbf-fa90-4703-a4a4-417b42c598bc_1024x608.png)](https://substackcdn.com/image/fetch/$s_!KyGa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F774dbcbf-fa90-4703-a4a4-417b42c598bc_1024x608.png)

##  **The Problem**

As someone who regularly works with research PDFs from major consulting firms
(think McKinsey, BCG, Deloitte), I was constantly hitting the same frustrating
wall. These documents are gold mines of insights that I use to:

  * Learn about industry trends and best practices

  * Pull context and data for my blog posts

  * Create educational materials for my work

  * Stay current with research in my field

But here's the thing: these PDFs are massive. Not just because of the content,
but because they're packed with formatting, styling, charts, images, and
visual elements. A 26-page research report can easily be 5MB+ with hundreds of
decorative elements. All I want is the text - to search it, understand it, and
extract meaningful insights.

If you've ever tried to analyze these documents with Claude, you know the
pain: you paste in the entire text, it consumes massive amounts of context,
and you're left with fewer tokens for actual analysis. A single consulting
report can eat up your entire context window before you even ask your first
question.

Thanks for reading! Subscribe for free to receive new posts and support my
work.

##  **The Solution (That I Built in Like 45 Minutes)**

Three simple tools. That's it:

###  **🔍 search-pdf - Find What You Need**

Search for specific terms or phrases within a PDF without loading the entire
document. Get results with surrounding context, perfect for quickly locating
relevant sections.

###  **📄 read-pdf - Smart Text Extraction**

Extract text from PDFs with options for cleaning and formatting. Only read
what you need, when you need it.

###  **📊 pdf-metadata - Document Intelligence**

Get instant access to PDF metadata: page count, author, creation date, and
more. Perfect for understanding documents before diving in.

##  **Why This Actually Matters**

Look, I'm not trying to save the world here. I just wanted to stop wasting
context tokens on formatting and images when all I need is to search some text
and pull out insights.

Now I can:

  * Search first, then read only what matters

  * Work with multiple consulting reports in one session

  * Actually have context left for analysis

  * Not lose my mind copying and pasting text

##  **Getting Started (Literally One Command)**

    
    
    claude mcp add pdf-reader npx @fabriqa.ai/pdf-reader-mcp

Restart Claude Code. Done. You now have PDF superpowers.

(No npm install needed - `npx` handles it automatically. Magic.)

##  **Real-World Example: My Actual Use Case**

Here's how I used it just last week with a McKinsey research report on AI
adoption:

 **The old, painful way:**

  * Download the 26-page PDF (5.6MB with all the formatting)

  * Extract text -> massive wall of text with image descriptions and formatting artifacts

  * Paste into Claude -> 150,000+ tokens consumed

  * Context left for my actual questions: barely any

  * Result: Can't even ask follow-up questions or include other sources

 **The new way with PDF Reader MCP:**

    
    
    1. "Search for AI native engineering"
       -> Found 3 matches with surrounding context
       -> Great, this gives me ideas for my current project
    
    2. "Read the section about organizational changes for AI"
       -> Extracts just that section, clean text
       -> Perfect content for what I'm writing about
    
    3. "Search for statistics about AI adoption rates"
       -> Found 12 mentions with data points
       -> Now I can cite actual numbers in my post
    
    Context used: ~8,000 tokens
    Remaining for analysis: 190,000+ tokens!
    

The difference? I can now analyze multiple consulting reports in a single
session, cross-reference findings, and still have plenty of context left to
synthesize everything into a coherent blog post or education document.

##  **The Tech (For Those Who Care)**

MCP SDK + pdf-parse + some quick Node.js glue. Runs locally, talks to Claude
via stdio. Nothing fancy, just works.

It's on npm and GitHub if you want to check it out or improve it:

  *  **npm** : [@fabriqa.ai/pdf-reader-mcp](https://www.npmjs.com/package/@fabriqa.ai/pdf-reader-mcp)

  *  **GitHub** : [hancengiz/read_pdf_as_text_mcp](https://github.com/hancengiz/read_pdf_as_text_mcp)

##  **Should You Use This?**

If you:

  * Analyze research PDFs regularly

  * Write blog posts using consulting reports as sources

  * Create educational materials from various PDF sources

  * Just want to search through PDFs without context pain

Then yeah, try it. It might save you as much frustration as it saved me.

If it doesn't work or you have ideas, hit up the GitHub. PRs welcome.

* * *

 _P.S. Yes, I used Claude Code to build a tool that makes Claude Code better
at PDFs. Meta, I know. 😄_

 _P.P.S. The whole thing took less than an hour. MCP servers are ridiculously
easy to build. You should try making one for your own annoying problem._

 _P.P.P.S. This blog post itself was written with Claude Code in the same
coding session -[9 prompts to get it
right](https://github.com/hancengiz/read_pdf_as_text_mcp/blob/main/blog-post.md). The irony continues._

Thanks for reading! Subscribe for free to receive new posts and support my
work.
