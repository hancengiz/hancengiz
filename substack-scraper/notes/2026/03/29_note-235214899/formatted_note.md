---
title: Note 235214899
published: Sun, 29 Mar 2026 20:22:16 GMT
author: Cengiz Han
handle: hancengiz
url: https://substack.com/note/c-235214899
type: note
note_id: 235214899
photo_url: https://substackcdn.com/image/fetch/$s_!A8_F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3c9352-78f7-4a7e-ab29-7efd239dd41c_400x400.jpeg
reactions: 0
restacks: 0
replies: 0
---
One thing I’ve become very opinionated about: AI slop is not just bad code. It’s code produced faster than anyone can understand, review, test, or safely maintain.

Vibe coding is when the spec gets replaced by momentum. It feels fast in the moment, but a few weeks later every change turns into archaeology.

That’s where the real cost shows up: maintenance hardness. No clear intent. No durable architecture. No shared model for how the system is supposed to work. Just a pile of generated code that keeps growing while confidence keeps shrinking.

The codebase starts moving faster than comprehension, and that is where teams get trapped.

That’s exactly why I built <http://fabriqa.ai> and <http://Specs.md>.

I built Fabriqa as an AI coding platform for serious engineering, not just code generation. It is built around spec-driven development. The goal is not to get AI to spit out more code. The goal is to make AI-built systems precise, reviewable, and maintainable.

And the important part is this: the leverage did not come from hand-writing code. In fact, not a single line of fabriqa’s production code was hand-written. The production code is AI-generated. The valuable part is the specification layer: the intent, the architecture, the execution plan, the decomposition, the reviews, the constraints, and the tests that make the output reliable.

That philosophy shows up in the repo:

\~160k lines of specs, plans, and architecture docs \~172k lines of production code \~102k lines of tests

That ratio is the point.

I think a lot of the industry is relying on momentum instead of engineering discipline, shipping vibe-coded systems and hoping they hold together later. I don’t think that scales. If AI is going to build real products, the answer is not less engineering. It’s better engineering.

Spec-driven development is how I turn AI from a slot machine into a system.

That’s what I’m building with <https://fabriqa.ai> and <http://Specs.md>.
