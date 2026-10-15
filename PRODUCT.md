# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: people overwhelmed by keeping up across several social networks. Their friends, news and conversations are scattered across Bluesky, X, LinkedIn and Mastodon, each app competing for their attention with its own algorithmic feed. They want to keep up with their people without the noise, and without opening a dozen apps.

The landing page's job (tracking issue mima-social/desktop#1348): answer "what does Mima do, and why should I download it?", get them to download, and keep the rest in touch via newsletter and Discord.

## Product Purpose

Mima is a free desktop app (macOS, Apple Silicon) that brings a person's social networks into one calm place: one feed of the people they follow, one composer to post to several networks, and one place for their conversations. Success: a visitor understands that in seconds, downloads it, and connects their accounts.

## Positioning

Lead with (user-confirmed):

- **Calm, no algorithm.** Your feed is your people; Mima does not rank for engagement or show ads.
- **Everything in one place.** Reading, posting and conversations across networks in one app, not just scheduling posts.

Privacy and local-first architecture are true and supporting, explained earnestly for those who care, not the headline.

## Operating Context

- Desktop app, installed from a .dmg (signed and notarized, auto-updating). One account per network at launch.
- Connecting: Bluesky and Mastodon sign in through the browser (OAuth; Mima never sees the password). X and LinkedIn (Beta) sign in inside a Mima window; the user is warned this is experimental and may violate those platforms' terms.
- In-app copy and onboarding are the canonical value proposition; the site must stay in sync with the onboarding welcome.

## Capabilities and Constraints

Shipped (code on `next`, latest release v0.1.3):

- **Networks:** Bluesky, Mastodon (full read, post, reply, like, repost, DMs); X and LinkedIn (Beta: read timeline, mentions and DMs; posting and replying are *assisted*: Mima opens the platform's composer pre-filled and the user clicks Post there; LinkedIn assisted posts are text and links only).
- **News Wall:** unified Timeline and Board views; duplicate cross-posts collapse into one card.
- **Omnibox:** one composer posting to several networks at once (direct to Bluesky/Mastodon; assisted to X/LinkedIn).
- **Conversations:** messages, mentions and DMs from all connected networks, unread badge, pin, reminders to resurface, optional AI thread summaries.
- **Filters:** hide reposts, mute accounts (local-only unless synced to platforms); respects Bluesky/Mastodon mute and block lists.
- **AI (optional):** Thread Summaries via a local model (Llama 3.2 3B, ~2GB, offline) or the user's own OpenAI/Anthropic/Google key, or off.

Copy decisions (user, 2026-10-14): X and LinkedIn may be presented alongside Bluesky and Mastodon without Beta labels or assisted-posting caveats on the website ("People care about capability, not minutiae"); "Compose once … post it to every network" stays.

Not shipped (do not claim): Windows/Linux/Intel builds, Telegram, RSS, newsletters, WhatsApp, Signal, topic clustering, hate/toxicity screening, multiple accounts per network, direct posting or DMing on X/LinkedIn, open source.

Undecided: public download URL (repo is private; placeholder until hosted), demo video, future pricing ("free at launch", paid features possible later).

## Brand Commitments

- Name: Mima (Mima Labs LTD, England & Wales). Brand guide: `~/Dropbox/2 Areas/Mima/MimaStyleGuide` (Mima.pdf, styles.css, icons, logo, squiggles, marketing backgrounds) is binding.
- Voice: friendly, calm, a little playful with a mature tone. Sentence case; no em dashes in UI copy; AI-generated text set in serif italic.
- In-app line: "Mima collects all your social feeds and friends in one calm place."
- Logo: looping M "looping you in, no matter where you are coming from." Animated M draw-on is approved for the heading.

## Evidence on Hand

- Real app (can be screenshotted by the founders); onboarding copy; brand guide; marketing backgrounds; app icons.
- Absent, do not fabricate: testimonials, user counts, press, benchmarks, reviews, real app screenshots in this repo, the demo video.

## Product Principles

1. Your people, not the platform's priorities: chronology and choice over engagement ranking.
2. One place, honestly: say exactly what each network supports, including Beta limits.
3. Calm by default: nothing in the product or page should feel like it is fighting for attention.
4. Private because of how it is built: data and accounts live on the user's Mac, and we explain the mechanism plainly, including its limits.

## Privacy and Security Facts (for earnest explanation)

- No Mima backend for user content: sync, storage and AI run on the user's Mac; network calls go from the Mac to each platform. Content is "processed locally on your device and is not received or stored by us"; never used for ads, analytics or AI training.
- Account credentials and tokens encrypted with macOS Keychain (Electron safeStorage). Bluesky/Mastodon sign in via OAuth in the default browser, so Mima never sees those passwords.
- X/LinkedIn sign in on the platform's own login page inside a sandboxed Mima window with no Mima script on it; network capture starts only after the session cookie appears, and no code reads password fields or submitted form data (verified against `next`, 2026-10-14). Mima keeps only the signed-in session cookies locally (and X request auth headers in memory). Claim to use: "We never store your passwords", never "we never see" for X/LinkedIn.
- Website copy rule (user, 2026-10-14): mention Mac only in download contexts; elsewhere say "your computer(s)". Don't call telemetry "opt-in" while the app's consent toggles default to on; "You choose what to share before anything is sent" is accurate.
- Local database is a SQLite file on the Mac and is **not** encrypted at rest (rely on macOS FileVault); do not claim an encrypted database.
- Telemetry (PostHog EU): crash reports, network names, feature taps, launch ping; excludes post/message content, credentials and contact names; shown before anything is sent, toggles default on (opt-out). Do not claim "nothing ever leaves your device".
- AI summaries are fully local only with the local model; bring-your-own-key sends content to that provider.
- App is sandboxed, signed with Developer ID, hardened runtime, notarized by Apple.
- The website (not the app) runs Google Analytics (G-GHJGZHDR95) without a consent prompt; the user chose to keep it as is (2026-10-14).
