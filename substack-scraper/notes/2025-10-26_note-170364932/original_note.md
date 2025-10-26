---
title: I automated my Substack notes to Twitter (complete...
date: Sun, 26 Oct 2025 15:28:28 GMT
author: Cengiz Han
handle: hancengiz
url: https://substack.com/note/c-170364932
type: note
note_id: 170364932
photo_url: https://substack-post-media.s3.amazonaws.com/public/images/dd3c9352-78f7-4a7e-ab29-7efd239dd41c_400x400.jpeg
reactions: 0
restacks: 0
replies: 0
---

# I automated my Substack notes to Twitter (complete...

**Published:** Sun, 26 Oct 2025 15:28:28 GMT
**Author:** Cengiz Han (@hancengiz)
**Link:** [https://substack.com/note/c-170364932](https://substack.com/note/c-170364932)

---

I automated my Substack notes to Twitter (completely free) Every time I
publish a note here on Substack, it automatically posts to Twitter within 5
minutes. No Zapier, no Buffer, no manual copying. Just pure automation. How it
works: 1\. GitHub Actions scrapes my Substack notes API every 5 minutes 2\.
When a new note appears, another workflow kicks in 3\. It posts directly to
Twitter using the API v2 (free tier: 1,500 tweets/month) 4\. A .published
marker file tracks which notes have been tweeted Why I built this: I decided
to use Substack more actively for my quick thoughts and updates. But I didn't
want to completely ignore Twitter in the process. I looked at Zapier ($20/mo)
and Buffer ($6/mo) - both felt like overkill for "just post this text to
Twitter." So I spent an afternoon with Claude Code building a free
alternative. Now I can write once on Substack and my thoughts automatically
flow to Twitter. No friction, no double-posting. The tech stack: \- GitHub
Actions (cron: every 5 minutes) \- Twitter API v2 (free tier, no credit card)
\- Python + tweepy \- Marker files for duplicate prevention What I like about
it: \- ✅ Completely free (within Twitter's 1,500 tweets/month) \- ✅ No third-
party dependencies \- ✅ Tweet URLs saved in each note folder \- ✅ Smart
truncation at word boundaries \- ✅ Open source, easy to modify The whole setup
is here if you want to clone it:
https://github.com/hancengiz/hancengiz/tree/main/substack-scraper Built with
Claude Code in one afternoon. AI-native development is wild. Let’s see if this
gets automatically posted to twitter(yeah I know know it is called x) ;)
