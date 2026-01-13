---
title: A new Simple Flow added to SPECS.MD : for solo devs and small teams
date: Tue, 13 Jan 2026 07:21:02 GMT
author: Cengiz Han
url: https://www.cengizhan.com/p/simple-flow-lightweight-specs-for
type: post
---

# A new Simple Flow added to SPECS.MD : for solo devs and small teams

**Published:** Tue, 13 Jan 2026 07:21:02 GMT
**Author:** Cengiz Han
**Link:** [https://www.cengizhan.com/p/simple-flow-lightweight-specs-for](https://www.cengizhan.com/p/simple-flow-lightweight-specs-for)

---

[specs.md](http://specs.md/) has now a new flow; simple flow.

It's spec-driven development stripped down to three phases and one agent.

Imagine Kiro specs in any AI coding tool you like.

[![](https://substackcdn.com/image/fetch/$s_!9Dhf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305b9953-efe1-4952-8e5c-f7462c23cddb_2816x1504.png)](https://substackcdn.com/image/fetch/$s_!9Dhf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305b9953-efe1-4952-8e5c-f7462c23cddb_2816x1504.png)

##  **What It Is**

 **Requirements** -> **Design** -> **Tasks**

One agent (`/specsmd-agent`) guides you through all three. No context
switching between specialized agents. No complex handoffs. You describe what
you want to build, and the agent generates documents at each phase, waiting
for your approval before continuing.

Install it:

    
    
    npx specsmd@latest install

Select "Simple" when prompted. Done.

Works with all major agentic coding tools:

  * Claude Code

  * Cursor

  * Kiro (Amazon)

  * Windsurf

  * GitHub Copilot

  * Cline

  * Roo

  * Gemini

  * Codex (OpenAI)

  * Antigravity (Google)

  * OpenCode

The installer auto-detects which tools you have. For Kiro, it creates a
symlink so the editor detects your specs automatically.

##  **How It Works**

Invoke the agent with your feature idea:

    
    
    /specsmd-agent Create a user authentication system with email login

The agent:

  1. Derives a feature name (`user-auth`)

  2. Generates a requirements document with user stories and [EARS](https://alistairmavin.com/ears/) acceptance criteria

  3.  **Waits for your approval**

  4. Generates a technical design with architecture and data models

  5.  **Waits for your approval**

  6. Generates numbered implementation tasks

  7.  **Waits for your approval**

  8. Executes tasks one at a time, pausing after each

The pattern is generate, then ask. Every phase requires explicit approval. Say
"yes," "approved," or "looks good" to continue. Say anything else to trigger
revision.

##  **The Pause Is Intentional**

By default, Simple Flow executes one task, then stops.

This is deliberate. You review what was built. You understand the changes.
Then you decide whether to continue.

If you're in flow and trust the direction, tell the agent: "continue until
done" or "go yolo." The guardrails are there. You choose when to lower them.

##  **What Gets Generated**

After completing the phases:

    
    
    specs/
    └── user-auth/
        ├── requirements.md    # What to build
        ├── design.md          # How to build it
        └── tasks.md           # Step-by-step plan

These documents persist. When you return to the project (or start a new
session), the agent reads these files to understand context. The spec becomes
the source of truth.

##  **EARS Format for Requirements**

Acceptance criteria use [EARS](https://alistairmavin.com/ears/) (Easy Approach
to Requirements Syntax):

    
    
    Event-driven: WHEN [trigger], THE [system] SHALL [response]
    State-driven: WHILE [condition], THE [system] SHALL [response]
    Unwanted behavior: IF [condition], THEN THE [system] SHALL [response]

Example:

    
    
    WHEN user submits login form, THE Auth_System SHALL validate credentials
    IF password is invalid, THEN THE Auth_System SHALL display error message

This format makes requirements unambiguous and testable.

##  **Simple Flow vs AI-DLC**

They're independent flows for different project types. Not a progression.

 **Simple Flow:**

  * Solo developers and small teams

  * Prototypes and MVPs

  * Features where you want structure without ceremony

  * One agent, three phases

 **AI-DLC:**

  * Production systems with multiple stakeholders

  * Teams needing coordination across phases

  * Complex domains requiring Domain-Driven Design

  * Four agents, full methodology

Choose based on your context. Install one or the other.

##  **Commands Reference**

 **Create new spec:** `/specsmd-agent Create a [feature idea]`

 **Continue existing:** `/specsmd-agent`

 **Resume specific spec:** `/specsmd-agent --spec="user-auth"`

 **Execute next task:** `/specsmd-agent What's the next task?`

 **Execute specific task:** `/specsmd-agent Execute task 2.1`

##  **Getting Started**

    
    
    npx specsmd@latest install

Select Simple. Invoke the agent with your feature idea. Review and approve
each phase.

That's it. Structure without the overhead.

* * *

 **Resources:**

  * [specs.md Documentation](https://specs.md/)

  * [Simple Flow Quick Start](https://specs.md/simple-flow/quick-start)

  * [Three Phases Deep Dive](https://specs.md/simple-flow/three-phases)

Thanks for reading my blog!
