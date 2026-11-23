# What's an MCP Server for Bluesky, X, LinkedIn and Mastodon?

> Mima includes a local, read-only MCP server, so Claude Desktop, Codex, Goose and other AI agents on your Mac can search and summarize your posts, mentions and DMs from Bluesky, X, LinkedIn and Mastodon.

Topic: AI agents · Updated: 2026-11-23 · Source: https://www.mima.social/learn/mcp-server-bluesky-x-linkedin-mastodon/

## TL;DR

- [Mima](https://www.mima.social) is a free Mac app that brings Bluesky, X, LinkedIn and Mastodon together. Since version 0.7.0 (22 November 2026) it includes a local MCP server for all four.
- Your agent can read: count unread conversations, search DMs, mentions and posts, open a conversation, and follow a thread. It cannot post, send, like or mark anything read.
- The server is off until you turn it on, and it only accepts connections from your own Mac. What you ask your agent about goes to that agent, and to the company that runs its model.

## What an MCP server does for your social accounts

MCP, the [Model Context Protocol](https://modelcontextprotocol.io), is the standard way to give an AI agent tools. A social media MCP server gives the agent tools for your accounts, so you can ask "who is waiting on a reply from me?" and get an answer from your real messages.

Most servers of this kind cover one network and need a developer key for it. Mima takes a different route. The app already keeps your posts, mentions and DMs from Bluesky, X, LinkedIn and Mastodon in one place on your Mac, so its MCP server gives your agent one set of tools for all four. You sign in to each network once, in Mima, with no API keys to manage.

![The top of Mima's News Wall, with the "Connect Mima to your agent" button in the top right corner](https://www.mima.social/site-assets/app/agent-button.webp "Start from the Connect Mima to your agent button in the top right. People and posts in these pictures are made up.")

## How to connect Claude Desktop, Codex, Goose or another agent

Select **Connect Mima to your agent** in the top right of Mima, or open **Settings > Connectors**. Each app has its own card:

| App | How it connects |
|---|---|
| Claude Desktop | One click: **Connect to Claude Desktop**. |
| Codex in the ChatGPT app | One click: **Connect to ChatGPT**. This also covers the Codex command line and editor extension. |
| Claude Code | Copy a prompt and paste it into Claude Code. |
| Goose and other apps that support local MCP | Copy a prompt for the app's chat or settings, from the **Other AI apps** card. |

To connect Claude Desktop:

1. Open Mima, then **Settings > Connectors**.
2. Select **Connect to Claude Desktop**. Mima turns its server on and adds itself to Claude Desktop's settings.
3. When Mima says it is done, quit Claude Desktop completely (Cmd+Q) and open it again. Mima's tools appear in a new chat.

![Mima Settings, Connectors tab: the Local MCP server switch turned on, Claude Desktop connected, and cards for ChatGPT, Claude Code and other AI apps](https://www.mima.social/site-assets/app/connectors-card.webp "Settings, then Connectors: one card per app, and one switch at the top for all of them.")

Mima has to be open while your agent uses it. Once an agent is connected, the button in the top right changes to say so.

## What you can ask your agent

Your agent gets nine tools. They list your connected accounts, count unread conversations, list and open conversations, search messages and posts, fetch a post, follow a thread, and list one person's recent posts. Posts come with their like, repost and reply counts, so the agent can compare them.

Some things to try:

- "How many unread DMs and replies do I have?"
- "Summarize my unread DMs and say who needs a reply."
- "Find every DM where someone asked me to collaborate."
- "What did people reply to my latest Bluesky post?"
- "Which of my posts this month got the most replies, and what do they have in common?"

The agent sees what Mima has stored as of its last sync. It cannot fetch anything new from the networks, and reading a conversation through an agent does not mark it read in Mima. Accounts you have muted or blocked stay hidden, as they do in the app.

## What stays on your Mac, and what your agent sees

The server runs inside Mima on your Mac. It accepts connections only from that Mac, never from the internet, and every request needs an access token that Mima creates. It makes no network calls of its own.

Your agent is a separate matter. When you ask it about your DMs, the messages it reads become part of that chat. If the agent uses a cloud model, as Claude Desktop and Codex do, that text goes to the company that runs the model. Connect only an agent you would trust with those messages.

The **Local MCP server** switch at the top of Settings > Connectors turns every connection off at once. Each card also has its own **Disconnect** button.

## When another kind of MCP server fits better

Mima's server reads. If you want an agent to publish or schedule posts for you, look for a server built on a network's own API, and expect to supply your own developer key.

It is also local. Chats on claude.ai and ordinary ChatGPT chats run in the cloud and cannot reach a server on your Mac, so they cannot use it. Choose a remote MCP server for those.

## FAQ

**Which AI apps work with Mima?** Claude Desktop, Codex (in the ChatGPT app, the command line and the editor extension), Claude Code, Goose, and other apps that can run a local MCP server.

**Can my agent post or reply for me?** No. Every tool is read-only.

**Is the MCP server on by default?** No. It stays off until you turn it on or connect an app.

**Do I need API keys for Bluesky, X, LinkedIn or Mastodon?** No. The agent reads what Mima already holds for the accounts you connected in the app.

**Does it work with ChatGPT?** With Codex in the ChatGPT desktop app, yes. Ordinary ChatGPT chats cannot reach a server on your Mac.

**Does Mima need to be open?** Yes. If Mima is closed or the server is off, your agent is told that Mima is not reachable.

**Which version of Mima do I need?** Mima 0.7.0 or later, on an Apple Silicon Mac.

## Related guides

- [Private Unified Social Inbox for Mac: Manage Messages and Mentions with Mima](https://www.mima.social/learn/private-unified-social-inbox-mac.md): Mima brings mentions and DMs from Bluesky, X, LinkedIn, and Mastodon into one private inbox on your Mac, where you can filter, reply, pin conversations, set reminders, and catch up with optional Thread Summaries.
- [Can I Read My Bluesky and Mastodon Lists in One App?](https://www.mima.social/learn/bluesky-mastodon-lists-one-app.md): Yes. Mima imports the lists you made on Bluesky and Mastodon and shows them beside its Timeline on your Mac, so one click narrows your feed to the people on a list.

---

About Mima: Connect your AI agent to your posts, mentions and DMs from four networks, through one switch you control. Mima is a free desktop app (beta, Apple Silicon Macs) with one feed of the people you follow on Bluesky, X, LinkedIn and Mastodon, one composer for posting to several networks, and one inbox for conversations. Download: https://www.mima.social/download. More guides: https://www.mima.social/learn/. Overview for AI assistants: https://www.mima.social/llms.txt
