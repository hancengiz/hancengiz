---
title: Note 235139298
published: Sun, 29 Mar 2026 17:29:25 GMT
author: Cengiz Han
handle: hancengiz
url: https://substack.com/note/c-235139298
type: note
note_id: 235139298
photo_url: https://substackcdn.com/image/fetch/$s_!A8_F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3c9352-78f7-4a7e-ab29-7efd239dd41c_400x400.jpeg
reactions: 0
restacks: 0
replies: 0
---
Today I re-learned why fabriqa treats worktrees as first-class infrastructure, not as a convenience feature.

I was shipping a breaking fabriqa release that introduced multi-repo workspaces. I needed the release pipeline to finish cleanly, and I needed the database to land in the correct migrated state, so I temporarily used Codex directly from the CLI instead of spawning isolated worktrees for each thread of work.

That shortcut exposed the exact system’s problem fabriqa is meant to solve.

When multiple agents or parallel threads operate against the same repo folder, they share mutable state:

* the same git index

* the same untracked files

* the same generated artifacts and lockfiles

* the same branch checkout and HEAD

* the same partially edited files

At that point, you do not have independent parallel workers. You have concurrent processes mutating the same filesystem surface.

Git worktrees are the isolation primitive. Each agent gets its own checkout, its own branch state, its own side effects, and its own clean diff boundary, while still living inside the same fabriqa workspace.

So the lesson is not just **“be careful with agents.”** The lesson is that **serious multi-agent coding requires filesystem isolation first**, orchestration second.

fabriqa’s multi-repo workspace release made that even clearer for me: one workspace can now hold the real working set for a project, but each agent still needs its own worktree.

One agent, one worktree.
