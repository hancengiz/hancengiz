---
title: fabriqa.ai: turning scattered AI coding tools into one coordinated, spec-driven workspace
date: Sun, 29 Mar 2026 15:08:42 GMT
author: Cengiz Han
url: https://www.cengizhan.com/p/fabriqaai-turning-scattered-ai-coding
type: post
---

# fabriqa.ai: turning scattered AI coding tools into one coordinated, spec-driven workspace

**Published:** Sun, 29 Mar 2026 15:08:42 GMT
**Author:** Cengiz Han
**Link:** [https://www.cengizhan.com/p/fabriqaai-turning-scattered-ai-coding](https://www.cengizhan.com/p/fabriqaai-turning-scattered-ai-coding)

---

[![](https://substackcdn.com/image/fetch/$s_!N4Le!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9f91b03-24b8-45f8-a95e-b4cb3f750595_2312x2154.png)](https://substackcdn.com/image/fetch/$s_!N4Le!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9f91b03-24b8-45f8-a95e-b4cb3f750595_2312x2154.png)

The AI coding tools spectrum itself is actually a good way of working. Each
tool brings its own strengths for different contexts, and using multiple tools
across a project is natural. The problem is what happens in between. I was
working on a spec-driven development project recently and found myself
reaching for Codex when I wanted autonomous execution against my
specifications. Codex is genuinely good at following structured specs and
running through implementation tasks without hand-holding. But when the
implementation introduced an edge case bug, I tried troubleshooting with Codex
multiple times and it could not find the issue it had created. The bug was
subtle enough that the same model that wrote the code kept missing it on
review.

So I switched to Claude Code CLI. But I needed to give it the full context of
what had been built, what the specs were, and where things had gone wrong. I
actually asked Codex to write me a handover prompt first, a summary of the
current state, the implementation decisions, and the specific failure. I
copied that prompt into Claude Code, and as I expected, it identified the edge
case almost immediately. That entire workflow, using one tool's strength to
compensate for another's blind spot, with a manual copy-paste handover in
between, is something I do constantly. It works, but it is held together with
clipboard and memory.

That is the problem fabriqa solves. fabriqa is not another editor. It is an AI
Development Orchestration Layer: a coordinated, spec-driven workspace for the
tools you already use.

* * *

##  **Why You Should Use It**

There are three big reasons to use fabriqa.

First, the unified worktree experience is already useful today. If you are
already paying for tools like Claude Code, Codex, Cursor, OpenCode, Gemini
CLI, or Kiro CLI, fabriqa gives them one shared place to work. You can switch
tools without losing the thread, keep the same project history visible,
inspect diffs and git changes in one place, and avoid the usual copy-paste
handoff mess. The broader ACP lineup already works too:

  * Amp

  * Auggie CLI

  * Autohand Code

  * Claude Agent

  * Cline

  * Codebuddy Code

  * Corust Agent

  * crow-cli

  * DimCode

  * Factory Droid

  * GitHub Copilot

  * goose

  * Junie

  * Kilo

  * Kimi CLI

  * Minion Code

  * Mistral Vibe

  * pi ACP

  * Qoder CLI

  * Qwen Code

  * Stakpak

fabriqa fetches the ACP registry and hot-swaps new entries into the catalog,
so this list keeps growing without me having to ship a release every time a
new tool shows up.

Second, specs are the real point. That is the part I care about most, and it
is the reason I think fabriqa can become much more than a tool switcher. The
specs module is coming in April 2026, in a couple of weeks. That is what I am
focused on getting right now. I believe spec-driven development is a
fundamental skill everyone needs to learn if they want agents to work like
real teammates instead of glorified autocomplete. If you cannot define the
work clearly, you cannot expect autonomous agents to execute it well.

Third, multi-agent orchestration is where this goes next. That part is phased
right now. Today, worktrees plus manual prompts already let you do a practical
version of multi-agent work inside fabriqa. But that is not the final goal.
The real goal is: define specs, define dependencies and execution order, then
fire up multi-agent profiles that can run those tasks fully autonomously. I
want that layer to sit on top of a best-in-class specs system, not on top of
vague prompts. That is why I am pushing specs first and the deeper
orchestration layer after that.

fabriqa is in alpha, and it is free right now. When I start charging, it will
be a small platform fee. I am not going to charge for tokens or meter your LLM
usage. The model side is BYOK, bring your own keys. The agent side is BYOS,
bring your own subscriptions. Native LLM integrations through API keys are
already there, but they are still limited. The full agentic loop on that side
is not fully where I want it yet.

It runs as a desktop application on macOS, Windows, and Linux. I initially
started by maintaining a CLI TUI and the desktop app together, but for now I
have stopped trying to keep the TUI at parity with desktop. That is
intentional. I think the popularity of CLIs is decreasing, so the desktop
experience is the primary focus. If there is real demand, I will continue
investing in the TUI more seriously.

A session in fabriqa is not just a chat thread. It is a full execution context
backed by a database that tracks what actually happened.

* * *

##  **What Is Coming**

This alpha focuses on the foundation: coordinated execution across the tools
you already pay for, plus a user experience that feels like a real
application, not a weekend side project. Since releasing fabriqa on March 3,
2026, I have been using it as my main daily driver. Until mid-February 2026 I
was using Claude Code more heavily. Around the GPT-5.3 release, Codex became
my main subscription inside fabriqa. I still keep a Claude Code subscription
and use it where I find it better, especially for more interactive
troubleshooting sessions and a lot of UI design work, but not only that.

But the main unique value proposition of fabriqa is not just putting existing
tools into one window. It is spec-driven execution. That layer is under active
development now and is planned for release in April 2026. I am already testing
these workflows myself with a limited number of early testers. If you want to
get into the specs testing group and do not want to wait another month, reach
out.

After that, multi-agent orchestration builds on top of those specs. The goal
is not random agent swarms. The goal is coordinated execution against explicit
intent, structured artifacts, and clear workflow state, with git worktree
isolation and conflict detection where that makes sense.

* * *

##  **The Details That Matter**

Global hotkeys bring fabriqa to the front and send it to the background
instantly. In the chat view, pressing the right and left arrow keys acts as
page up and page down. Command-up takes you to the top of the conversation.
There is a strict sticky scroll behavior that always keeps your last message
to the AI visible at the top of the viewport. If you are a multitasker like I
am and you switch back to a fabriqa chat after working on something else, you
do not have to wonder what you were doing. Your last message is right there,
and you immediately have context on where you left off. When you scroll up,
your previous message stays anchored and visible.

There is light mode, dark mode, and a bunch of themes. Git changes are visible
directly in the interface. If you are curious about how I implemented ACP, I
actually kept the ACP debug logs that I used during development open as a
feature. You can open the ACP debug panel and see the raw protocol messages
going back and forth between fabriqa and the agents. The settings page, the
command palette, and the keyboard shortcuts have a bunch of things in them
that are not common in tools like this yet. I am prioritizing features over
documentation right now, so some of these are things you discover by exploring
the application itself.

* * *

##  **Where This Is Going**

I have been writing about spec-driven development and the [Explore-Specify-
Engineer workflow](https://www.cengizhan.com/p/the-ai-native-way-of-building)
for a while. fabriqa is where those ideas become tooling. Mark my word: if you
are not working with specs yet, you are missing where this is going. Making
specs a first-class part of how you build should be a top priority.

The specs-driven system in fabriqa is being built to be generic, not hardcoded
to one opinionated flow. It will include my own [specs.md](http://specs.md/)
FIRE flow, AWS AI-DLC flows as implemented in [specs.md](https://specs.md/),
and commonly used patterns like BMAD-METHOD as built-in fabriqa workflows. I
am also working on a meta-workflow for fabriqa itself, where you can talk to
fabriqa agents to design your own workflows around your own needs, with those
agents being aware of fabriqa's workflow DSL instead of treating workflows
like raw text.

The release planned for May 2026 adds a marketplace so fabriqa users can share
their own workflows with each other. That matters because the long-term goal
is not just to ship my workflows. It is to make fabriqa a system where good
workflows can be created, evolved, reused, and shared.

fabriqa is also architected in a way that lets me run it as a hosted web
application later. I plan to offer that as fabriqa.cloud with the exact same
core experience. That is possible because the frontend is React-based and the
server-side architecture is cleanly separated, more like Slack than like a
one-off desktop app. The hosted version will run in cloud sandboxes, but that
is not the only future I care about.

I also want a mobile app that can connect to your fabriqa instance on
fabriqa.cloud, on your own machine, or on your own premises. I am planning
around private-network approaches like Tailscale so fabriqa.cloud does not
have to be mandatory for mobile. I want fabriqa to be something you can keep
building with while you are on the go, not something that traps you into one
deployment model.

* * *

##  **What You Get Today**

If you use fabriqa today, you get a real desktop workspace for coordinating
the AI coding tools you already pay for.

  * One place to switch between tools like Claude Code, Codex, Gemini CLI, OpenCode, Cursor, and more without losing context

  * A unified worktree and git-aware workflow where chats, diffs, progress, and handoffs live together

  * A practical path to multi-agent execution today through worktrees and manual prompt coordination, with the specs layer landing in April

  * Access to the ACP ecosystem without vendor lock-in, plus occasional free-model opportunities that come through platforms like OpenCode and Kilo

The desktop builds are available at **[fabriqa.ai](https://fabriqa.ai/). Go
download fabriqa for free** and start using it with your own subscriptions
like Claude Code and Codex. You can also benefit from free model offers that
show up through platforms like OpenCode and Kilo. For example, OpenCode is
currently hosting Xiaomi MiMo-V2-Pro free for OpenCode users for a limited
time, and those kinds of campaign models are useful inside fabriqa too.

fabriqa itself is free during the alpha. I am not asking anyone to sign up
right now. Just download fabriqa and start using it. Later, when I have user
accounts or email capture in place, the people who helped me make fabriqa
better during this alpha will get free fabriqa access and should not need to
pay that small platform fee. I have not really settled the pricing model yet,
and I want to be honest about that. My instinct is that it should cost less
than a Starbucks coffee, not something meaningful compared to what you already
spend on the tools around it. My main goal right now is to get fabriqa into
the hands of agentic AI developers and teams so they can help me make fabriqa
the best AI Development Orchestration Layer for software development in the
world. If you want early access to the specs workflows, reach out. fabriqa is
still early, but amazing things are in plan. It will be nothing like what
already exists.
