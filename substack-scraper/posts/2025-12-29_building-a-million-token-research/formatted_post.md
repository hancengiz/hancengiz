---
title: Building a Million-Token Research Agent for Claude Code
date: Mon, 29 Dec 2025 11:10:58 GMT
author: Cengiz Han
url: https://www.cengizhan.com/p/building-a-million-token-research
type: post
---

# Building a Million-Token Research Agent for Claude Code

**Published:** Mon, 29 Dec 2025 11:10:58 GMT
**Author:** Cengiz Han
**Link:** [https://www.cengizhan.com/p/building-a-million-token-research](https://www.cengizhan.com/p/building-a-million-token-research)

---

# **Building a Million-Token Research Agent for Claude Code**

 **TL;DR:** Claude Code's extensible agent system lets you create custom sub-
agents that leverage different AI models for specialized tasks. I built a
Gemini research specialist that uses Google's 1 million token context window
for research--and it's transformed how I gather information during coding
sessions.

* * *

![](image1.png)

##  **The Research Problem Every Developer Knows**

You're deep in a coding session. The flow state is perfect. Then you hit a
wall: you need to understand how a library handles edge cases, compare
authentication approaches, or research best practices for a pattern you've
never implemented.

What happens next? You open a browser. Start Googling. Open fifteen tabs. Lose
your flow state. Spend 45 minutes reading documentation, Stack Overflow
answers, and blog posts. Try to hold all that context in your head while
switching back to code.

The mental cost is brutal. Context switching alone can cost 23 minutes to
regain focus, according to productivity research. But the bigger problem is
synthesis--turning scattered information into actionable knowledge while
keeping your coding context intact.

What if your coding assistant could delegate research to a specialized agent
that processes a million tokens of context and returns synthesized insights
without you ever leaving your terminal?

* * *

##  **Why Build a Custom Research Agent?**

Claude Code is powerful for coding tasks. But research has different
requirements:

  *  **Web access** : Need current information, not just training data

  *  **Massive context** : Processing entire documentation sets, not snippets

  *  **Synthesis focus** : Connecting dots across multiple sources

  *  **Background execution** : Research while you continue coding

Claude's context window is substantial, but Gemini offers something different:
a 1 million token context window. That's not just "bigger"--it's a different
category of capability for research tasks.

The insight: **use the right model for the right job**. Claude for code
understanding and editing. Gemini for web research and massive context
synthesis.

* * *

Thanks for reading cengizhan.com! Subscribe for free to receive new posts and
support my work.

##  **The Gemini Research Specialist Agent**

I created a custom agent called `gemini-research-specialist` that Claude Code
can delegate to for research tasks. Here's what it does:

  * Leverages Gemini's web search capabilities

  * Processes research using the 1 million token context window

  * Synthesizes findings into actionable developer-focused insights

  * Returns results directly into my Claude Code session

Think of it as adding a research department to your coding assistant.

###  **How It Works in Practice**

When I'm in Claude Code and need research, the system recognizes research-
oriented requests and spawns the Gemini agent:

    
    
    You: I'm building a recommendation system. Can you research
         best practices for collaborative filtering?
    
    Claude Code: Let me use the gemini-research-specialist agent
                 to research best practices for collaborative
                 filtering in recommendation systems.
    
    [Agent runs in background, processing web sources]
    
    Claude Code: Based on the research, here are the key findings...
    

The agent runs asynchronously. I can continue other work while it gathers and
synthesizes information. When it returns, the insights integrate directly into
my conversation context.

* * *

##  **The 1 Million Token Context Window: Why It Matters**

Here's where things get interesting. Gemini's context window isn't just
"bigger"--it's categorically different.

 **Traditional research with smaller context windows:**

  * Retrieve a document chunk

  * Summarize and discard

  * Retrieve next chunk

  * Try to connect insights across lossy summaries

  * Lose nuance, miss connections, make errors

 **Research with a 1 million token context window:**

  * Load entire documentation sets simultaneously

  * Process complete technical specifications

  * Hold multiple full research papers at once

  * See connections across sources that smaller windows miss

  * Synthesize without information loss

To put this in perspective: 1 million tokens is roughly 750,000 words. That's
approximately:

  * 4-5 complete technical books

  * Hundreds of documentation pages

  * Dozens of research papers

  * Thousands of Stack Overflow answers

All held in working memory. Simultaneously. While looking for patterns and
connections.

###  **The Mental Model: Research Synthesis at Scale**

Think of traditional AI research like looking through a keyhole--you see one
thing at a time and try to remember what you saw before. A million-token
context window is like having the entire wall removed. You see everything at
once and can trace connections that keyhole viewing would never reveal.

For developers, this means research that actually captures:

  * How library X's approach compares to library Y's across their full documentation

  * The evolution of best practices from 2020 recommendations to current consensus

  * Edge cases mentioned in GitHub issues that contradict documentation claims

  * The "why" behind decisions, not just the "what"

* * *

##  **Building the Agent: Key Design Decisions**

Creating an effective research agent required several deliberate choices:

###  **1\. Clear Agent Description**

Claude Code needs to know when to delegate. The agent description explicitly
defines the trigger conditions:

    
    
    Use this agent when the user needs to research information,
    gather data from the web, investigate topics, find current
    information, or explore subjects that require internet
    search capabilities.
    

This ensures Claude recognizes research requests and routes them
appropriately.

###  **2\. Prompt Engineering for Research Quality**

The agent's system prompt shapes how Gemini approaches research tasks:

  * Focus on synthesizing, not just retrieving

  * Prioritize actionable insights over exhaustive listings

  * Consider recency and source credibility

  * Structure output for developer consumption

###  **3\. Asynchronous Execution**

Research takes time. The agent runs in the background so you're not blocked
waiting for results. This preserves your flow state--you can continue coding
other parts while research completes.

###  **4\. Context Integration**

When the agent returns, its findings integrate into your Claude Code
conversation. You're not switching tools or copying information. The research
becomes part of your working context.

* * *

##  **Real-World Use Cases**

###  **1\. Learning New Protocols and Technologies**

This goes far beyond searching for library docs. I used this approach to learn
the Agent Commerce Protocol (ACP). Instead of bouncing between websites,
reading scattered documentation, and trying to piece together understanding, I
used the research agent as a learning partner:

    
    
    "Explain the Agent Commerce Protocol architecture. What are
    the core concepts, how do agents discover each other, and
    what's the payment flow?"
    

Then I asked follow-up questions, drilling deeper into areas I didn't
understand. Once I had clarity, I asked the agent to synthesize everything
into step-by-step tutorials that my entire team could use to learn the
protocol.

The workflow becomes:

  1.  **Ask questions** \- Use the agent to explore and understand

  2.  **Drill deeper** \- Follow up on confusing parts

  3.  **Create artifacts** \- Turn your learning into tutorials, guides, documentation

  4.  **Share knowledge** \- Now your whole team benefits from your learning session

This transforms the agent from a search tool into a **learning accelerator**.
You're not just finding information--you're building understanding and
creating reusable knowledge assets.

###  **2\. Technology Evaluation**

You're choosing between vector databases for your AI application. Instead of
opening tabs for Pinecone, Weaviate, Milvus, Qdrant, and Chroma documentation:

    
    
    "Compare the performance characteristics of different vector
    databases for a use case with 10M embeddings, focusing on
    query latency, scalability, and operational complexity"
    

The agent processes documentation, benchmarks, and community experiences
simultaneously, returning a synthesis that would take hours to compile
manually.

###  **3\. Library Deep Dives**

You need to understand how a framework handles a specific scenario:

    
    
    "Research how Next.js App Router handles streaming,
    error boundaries, and suspense in server components,
    including known edge cases and workarounds"
    

The agent can process the full Next.js documentation, relevant GitHub issues,
and developer discussions to provide a comprehensive answer.

###  **4\. Current State of the Art**

Technology moves fast. Staying current is exhausting:

    
    
    "What are the latest developments in local LLM inference
    optimization as of late 2025?"
    

The agent researches current information, giving you a snapshot of the
landscape without context-switching to browser research.

###  **5\. Academic Research and Whitepaper Discovery**

Staying current with academic research is nearly impossible manually. New
papers drop daily on arXiv, and finding the ones relevant to your work
requires constant vigilance. The research agent changes this:

    
    
    "Find recent whitepapers and academic research on AI-native
    software engineering methodologies. Focus on papers from
    arxiv.org discussing agentic development, LLM-assisted
    coding workflows, and human-AI collaboration in software
    development. Summarize the key approaches and findings."
    

The agent can surface papers you'd never find through casual browsing,
synthesize their key contributions, and help you understand how academic
research connects to practical engineering. This is how I stay current on AI-
native engineering approaches--not by manually checking arXiv every day, but
by periodically asking the agent to find what's new and explain what matters.

For practitioners, this bridges the gap between academic innovation and real-
world application. You get the insights without the hours of reading dense
papers.

###  **6\. Implementation Pattern Research**

Before building, understand what works:

    
    
    "Research production patterns for implementing rate limiting
    in distributed systems, focusing on Redis-based approaches
    versus token bucket implementations"
    

* * *

## **The Workflow Integration Advantage**

Here's what makes this powerful: the research happens inside your coding
session. The insights feed directly into your context. You don't lose your
mental model of the code you're writing.

 **Before: Fragmented Research**

  1. Code -> encounter unknown

  2. Switch to browser

  3. Research (lose coding context)

  4. Return to code

  5. Try to remember insights

  6. Repeat

 **After: Integrated Research**

  1. Code -> encounter unknown

  2. Request research (stay in terminal)

  3. Continue coding other parts

  4. Receive synthesized insights

  5. Apply directly to your code

The agent system also handles something subtle but important: it knows what
format of answer you need. It's not returning raw search results or document
dumps. It's synthesizing research into developer-focused insights because it
understands you're in a coding context.

* * *

##  **Practical Tips for Effective Research Prompts**

Not all research requests are equal. Here's how to get the most from the
agent:

###  **Be Specific About Your Context**

 **Weak:** "Research authentication"  
 **Strong:** "Research OAuth 2.0 best practices for SPAs in 2025, focusing on
token storage security and refresh token rotation"

###  **Specify What You Need to Know**

 **Weak:** "Tell me about React Server Components"  
 **Strong:** "Research React Server Components focusing on data fetching
patterns, when to use them vs client components, and common migration pitfalls
from Pages Router"

###  **Request Comparisons Explicitly**

 **Weak:** "Research state management"  
 **Strong:** "Compare Zustand vs Jotai vs Redux Toolkit for a medium-sized
React application, focusing on bundle size, learning curve, and TypeScript
support"

###  **Ask for Current Information When It Matters**

 **Weak:** "How does Kubernetes handle autoscaling?"  
 **Strong:** "What are the latest best practices for Kubernetes pod
autoscaling in 2025, including HPA, VPA, and KEDA approaches?"

* * *

##  **The Bigger Picture: Multi-Model Agent Architectures**

This research agent illustrates a larger pattern in AI-native development:
**using specialized models for specialized tasks**.

Claude excels at code understanding, reasoning about complex systems, and
careful editing. Gemini excels at processing massive context and web search.
Why choose one when you can orchestrate both?

This mirrors how effective development teams work. You don't ask your backend
specialist to also handle UX research. You leverage expertise where it
matters.

The architecture becomes:

  *  **Primary agent (Claude)** : Code understanding, editing, problem-solving

  *  **Research specialist (Gemini)** : Web research, information synthesis, current data

  *  **Task delegation** : The right model for the right job

As AI development tools mature, expect this pattern to deepen. Specialized
agents for security analysis, performance optimization, documentation
generation--each leveraging their unique strengths.

* * *

##  **Limitations and Considerations**

Let's be honest about the constraints:

 **Research latency** : Deep research takes time. The agent may run for 30-60
seconds on complex queries. This is a feature, not a bug--thorough research
isn't instant.

 **Information currency** : While the agent accesses current web information,
it's still subject to what's indexed and available. Cutting-edge developments
from yesterday might not surface.

 **Synthesis quality** : Large context windows enable better synthesis, but
they don't guarantee perfect interpretation. Verify critical findings.

 **Token costs** : Million-token operations aren't cheap. Use targeted
research requests rather than "tell me everything about X" approaches.

 **Setup complexity** : Building custom agents requires understanding Claude
Code's agent delegation system. The initial investment pays off in workflow
efficiency.

* * *

##  **The Complete Source Code**

Here's the full implementation. Create this file at `~/.claude/agents/gemini-
research-specialist.md`:

    
    
    ---
    name: gemini-research-specialist
    description: Use this agent when the user needs to research information, gather data from the web, investigate topics, find current information, or explore subjects that require internet search capabilities. Examples:\n\n<example>\nContext: User needs current information about a technology.\nuser: "What are the latest developments in quantum computing?"\nassistant: "I'll use the gemini-research-specialist agent to research the latest developments in quantum computing for you."\n<commentary>The user is asking for current information that requires web research, so launch the gemini-research-specialist agent.</commentary>\n</example>\n\n<example>\nContext: User is working on a project and needs background information.\nuser: "I'm building a recommendation system. Can you research best practices for collaborative filtering?"\nassistant: "Let me use the gemini-research-specialist agent to research best practices for collaborative filtering in recommendation systems."\n<commentary>The user needs research on a specific technical topic, so use the gemini-research-specialist agent to gather comprehensive information.</commentary>\n</example>\n\n<example>\nContext: User needs comparative analysis requiring research.\nuser: "Compare the performance characteristics of different vector databases"\nassistant: "I'll deploy the gemini-research-specialist agent to research and compare performance characteristics across different vector databases."\n<commentary>This requires gathering current information from multiple sources, making it ideal for the research specialist agent.</commentary>\n</example>
    model: sonnet
    ---
    
    You are an elite Research Specialist with expertise in conducting thorough, efficient, and accurate research using the Gemini AI model in headless mode. Your primary tool is the command `gemini -p "prompt"` which you will use to gather information from the web and synthesize findings.
    
    ## Core Responsibilities
    
    1. **Execute Targeted Research**: When given a research task, formulate precise, well-structured prompts for Gemini that will yield the most relevant and comprehensive information.
    
    2. **Strategic Prompt Design**: Craft your Gemini prompts to:
       - Be specific and focused on the exact information needed
       - Request current, factual information when timeliness matters
       - Ask for multiple perspectives or sources when appropriate
       - Include requests for examples, data, or evidence to support findings
       - Specify the desired format or structure of the response when helpful
    
    3. **Synthesize and Present Findings**: After receiving results from Gemini:
       - Organize information logically and coherently
       - Highlight key findings and insights
       - Identify any gaps or limitations in the research
       - Present information in a clear, actionable format
       - Cite or reference the nature of sources when relevant
    
    ## Operational Guidelines
    
    **Research Process**:
    - Begin by clarifying the research objective and scope
    - Break complex research questions into focused sub-queries if needed
    - Execute Gemini searches using the exact format: `gemini -p "your precise prompt here"`
    - Evaluate the quality and relevance of returned information
    - Conduct follow-up searches if initial results are incomplete or require deeper investigation
    
    **Quality Assurance**:
    - Cross-reference information when making critical claims
    - Note when information may be time-sensitive or subject to change
    - Distinguish between factual information, expert opinions, and speculation
    - Acknowledge uncertainty when sources conflict or information is limited
    
    **Prompt Engineering Best Practices**:
    - Use clear, unambiguous language in your Gemini prompts
    - Include relevant context that helps narrow the search scope
    - Request specific types of information (statistics, examples, comparisons, etc.)
    - Ask for recent or current information when timeliness is important
    - Frame questions to elicit comprehensive yet focused responses
    
    **Output Standards**:
    - Present research findings in a well-structured format (use headings, bullet points, or numbered lists as appropriate)
    - Lead with the most important or directly relevant information
    - Provide context and background when it aids understanding
    - Include actionable insights or recommendations when applicable
    - Clearly indicate if additional research would be beneficial
    
    ## Edge Cases and Special Situations
    
    - **Insufficient Results**: If initial research yields limited information, reformulate your prompt with different angles or broader/narrower scope
    - **Conflicting Information**: When sources disagree, present multiple perspectives and note the discrepancy
    - **Rapidly Evolving Topics**: Explicitly note that information may change quickly and recommend follow-up research timelines
    - **Highly Technical Topics**: Break down complex findings into accessible explanations while maintaining accuracy
    - **Ambiguous Requests**: Proactively ask clarifying questions before conducting research to ensure you're investigating the right topic
    
    ## Self-Verification
    
    Before presenting findings, ask yourself:
    - Does this information directly address the research question?
    - Have I provided sufficient depth and breadth of coverage?
    - Are there obvious gaps or follow-up questions that should be addressed?
    - Is the information presented in a clear, actionable format?
    - Have I noted any important caveats or limitations?
    
    Your goal is to be a reliable, efficient research partner that delivers high-quality, relevant information through strategic use of Gemini's capabilities. Always prioritize accuracy, clarity, and usefulness in your research outputs.
    

### **Prerequisites**

Before the agent works, you need Gemini CLI installed and configured:

    
    
    # Install Gemini CLI (choose one)
    npm install -g @google/gemini-cli    # npm
    brew install gemini-cli               # Homebrew (macOS/Linux)
    npx https://github.com/google-gemini/gemini-cli  # Run without installing
    
    # First run - authenticate with Google (recommended, free tier)
    gemini
    # Select "Login with Google" when prompted
    # This gives you 60 requests/min and 1,000 requests/day for free
    
    # Alternative: Use API key instead
    export GEMINI_API_KEY="your-api-key-here"  # from https://aistudio.google.com/apikey
    
    # Test it works
    gemini "What is the current date?"
    

The Google login option is recommended for most users since it's simpler and
includes a generous free tier.

###  **Key Design Elements**

 **The frontmatter** tells Claude Code when and how to use this agent:

  * `name`: The identifier Claude uses when delegating

  * `description`: Rich examples help Claude recognize when to delegate (the `\n\n<example>` pattern is intentional)

  * `model`: The Claude model the agent itself uses for orchestration (sonnet for speed)

 **The system prompt** shapes the research behavior:

  * Instructs the agent to use `gemini -p "prompt"` for actual research

  * Defines quality standards for synthesis

  * Handles edge cases like conflicting sources

  * Ensures output is developer-friendly

###  **How It Works Under the Hood**

The core pattern is simple: **a Claude Code agent that invokes another CLI
tool**.

    
    
    ┌─────────────────────────────────────────────────────────┐
    │  Claude Code (your terminal session)                    │
    │                                                         │
    │  You: "Research best practices for rate limiting"       │
    │           │                                             │
    │           ▼                                             │
    │  ┌─────────────────────────────────────────────────┐   │
    │  │  Task Tool spawns gemini-research-specialist    │   │
    │  │  (Claude Sonnet agent)                          │   │
    │  │                                                 │   │
    │  │  Agent runs: gemini "rate limiting patterns..." │   │
    │  │              ───────────────────────────────────│───┼──► Gemini CLI
    │  │                        │                        │   │    (web search,
    │  │                        ▼                        │   │     1M context)
    │  │  Agent synthesizes Gemini's response            │   │
    │  │  Returns findings to Claude Code                │   │
    │  └─────────────────────────────────────────────────┘   │
    │           │                                             │
    │           ▼                                             │
    │  Claude Code: "Based on the research, here are..."      │
    └─────────────────────────────────────────────────────────┘
    

The flow:

  1. You ask Claude Code a research question

  2. Claude recognizes the pattern and spawns a sub-agent using the Task tool

  3. The sub-agent (Claude Sonnet) executes `gemini "..."` via Bash

  4. Gemini CLI performs web searches with its 1M token context window

  5. The sub-agent synthesizes Gemini's response

  6. Results return to your main Claude Code session

 **This is the key insight: Claude Code agents can invoke any CLI tool.** The
agent is just a markdown file that defines when to trigger and what
instructions to give Claude. The actual research happens through the Gemini
CLI, which Claude calls like any other command-line tool.

You could use this same pattern to integrate:

  * `perplexity` CLI for search

  * `llm` CLI for other models

  * `gh` for GitHub operations

  * Any tool with a command-line interface

* * *

##  **Getting Started: Step by Step**

  1.  **Create the agents directory** (if it doesn't exist):

    
    
    mkdir -p ~/.claude/agents
    

  1. **Create the agent file** :

    
    
    # Copy the source code above into this file
    nano ~/.claude/agents/gemini-research-specialist.md
    

  1. **Install and configure Gemini CLI** :

    
    
    npm install -g @google/generative-ai-cli
    export GEMINI_API_KEY="your-key-here"
    

  1. **Test the agent** : In Claude Code, try:

    
    
    Research the latest best practices for TypeScript monorepo tooling in 2025
    

  1. **Iterate** : Adjust the system prompt based on the quality of research you receive

* * *

##  **The Future of AI-Augmented Research**

We're watching the research workflow transform in real-time. The pattern--
specialized agents with massive context windows handling domain-specific tasks
--will only accelerate.

What this means for developers:

  * Less context switching, more flow state

  * Research quality that matches the breadth you'd never have time for

  * Insights synthesized for your specific context

  * Knowledge work that scales with AI rather than competing with it

The million-token context window isn't just a bigger number. It's a
qualitative shift in what's possible when researching during development.
Combined with Claude Code's extensible agent architecture, it represents a
glimpse of how AI-native development tools will actually work.

Not AI replacing developers. Not developers ignoring AI. Instead: specialized
AI agents as force multipliers, each excelling at specific tasks, orchestrated
together in an integrated environment.

Your research assistant is ready to be built. It can live in your terminal.
And it can hold more context in memory than you could read in a week.

* * *

##  **Further Reading**

  * Claude Code documentation on custom agents and task delegation

  * Google's technical deep dive on Gemini's context window architecture

  * Context engineering principles for effective AI tool usage

Building a Million-Token Research Agent for Claude Code

The Research Problem Every Developer Knows

Why Build a Custom Research Agent?

The Gemini Research Specialist Agent

How It Works in Practice

The 1 Million Token Context Window: Why It Matters

The Mental Model: Research Synthesis at Scale

Building the Agent: Key Design Decisions

  1. Clear Agent Description

  2. Prompt Engineering for Research Quality

  3. Asynchronous Execution

  4. Context Integration

Real-World Use Cases

  1. Learning New Protocols and Technologies

  2. Technology Evaluation

  3. Library Deep Dives

  4. Current State of the Art

  5. Academic Research and Whitepaper Discovery

  6. Implementation Pattern Research

The Workflow Integration Advantage

Practical Tips for Effective Research Prompts

Be Specific About Your Context

Specify What You Need to Know

Request Comparisons Explicitly

Ask for Current Information When It Matters

The Bigger Picture: Multi-Model Agent Architectures

Limitations and Considerations

The Complete Source Code

Prerequisites

Key Design Elements

How It Works Under the Hood

Getting Started: Step by Step

The Future of AI-Augmented Research

Further Reading

imgursm.msqiniu

Thanks for reading cengizhan.com! Subscribe for free to receive new posts and
support my work.
