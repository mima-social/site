# Making Mima: The QA Story

> [NEEDED: deck, one sentence under the title]

Draft. Not published, and not in the feed, the sitemap or llms.txt.

By David Monk, [NEEDED: role wording] · What shipped: [NEEDED: what shipped] · Category: [NEEDED: category] · Published: 2026-11-23 · Source: https://www.mima.social/labs/drafts/how-a-labs-post-is-built/

![Placeholder picture: the Mima News Wall in Board view](https://www.mima.social/site-assets/app/board.webp)

Stay with me, this story takes weird turns. When I was a kid, I was really into Teenage Mutant Ninja Turtles. Really, really into them. I tore through everything I could find related to them and found some of the more obscure graphic novels that came out way before the turtles reached mainstream awareness. These stories were gritty, hard, and dark. One had a dying ninja master use psychic power to guide them to assault an urban skyscraper that resembled a medieval Japanese Castle (I told you this takes weird turns). The turtles show up, look up at this towering defensive monstrosity, and just shrug, put on their gear, and began climbing. It was springtime of 2026, and I had just started using agentic technologies to enhance the techniques I knew for testing software. I called this Agentic Testing. I did not view AI/LLMs as problems, but rather new tools to use in my toolkit. As luck would have it, I crossed paths with RL Nabors, whom I had known since the late 90’s. They had a codebase and a vision, I had tools I wanted to use to test software, we came to an arrangement. I shrugged, put on my gear, and began climbing.

Traditionally, my approach to testing involves breaking the approach into categories: Safety/Security, Performance, Usability, Localization/Internationalization, Accessibility, and Functionality. For this code base, my focus was primarily on using AI/LLMs to enhance a static code analysis approach to each of these. Rather than the naïve approach (“Hey AI, test everything”) I kept the scope small to start with, and began with a simple workflow: identify the most serious issues with the greatest end-user impact, and propose solutions that were high confidence, low risk, and had a minimal blast-radius. In terms I used Claude and upgraded to the latest Opus models whenever possible. If a straightforward fix could not be quickly identified, I still directed the LLM to record the issues so that the issue list reflected the current state of code.

Next, I stopped to evaluate the automation coverage numbers. At the start the coverage was very low across the board. I directed the LLM to aim for a minimum of 50% block unit test coverage to serve as a backstop to prevent future regressions. As new issues were found and fixed, we developed regression tests that proved that the fixes worked, and that without the fix, the test would fail. The distinction here is critical: we are not just validating correct behavior, we are validating the correction of incorrect behavior, and then additionally preventing backsliding into bad behavior again.

No system is perfect, and refinements were necessary. Github runners were slow and expensive; we migrated to local runners to stop the pain. Developing for all platforms was a distraction, so we focused our efforts on one to start with. At a certain point we realized we were running a full CI/CD pass against documentation updates, so we optimized that path to be a bit more reasonable in terms of resources.

It is a common adage in QA that if you aren’t from QA, it is hard to see the value in it or to understand it. The approach I have taken is to justify it in terms of money, time, and the end user perception of the product. We ended up with one of the smoothest betas I’ve ever seen. We were able to focus on design feedback instead of annoying bugs. We had documentation, unit tests, and defensive security posture. We were able to provide a patched binary to a dependency CVE in under 6 hours the same day it was announced.

What would I have done differently if I had to do it again? Before agentic technologies my primary focus was on simulating the user experience, developing scenarios, black box testing all the way. I admit I may have over-corrected here. RL, being the creator and the visionary behind the project, was left doing most of the manual QA. I became so entrenched in the static analysis and unit coverage that a lot of times I lost focus on what we wanted the project to be rather than how it ran. Ironically, this is something I have raged against previously in my career.

In conclusion, LLM based Agentic Testing has the potential to be a powerful tool, and it is developing rapidly in terms of speed, complexity, and correctness. However, it remains facing a similar challenge that the introduction of Automated Testing did: it cannot tell you what the “feel” of the software it is, and other similar non-quantifiable measurements.

---

About Mima: Mima is a free desktop app (beta, Apple Silicon Macs) with one feed of the people you follow on Bluesky, X, LinkedIn and Mastodon, one composer for posting to several networks, and one inbox for conversations. Download: https://www.mima.social/download. Overview for AI assistants: https://www.mima.social/llms.txt More from Labs: https://www.mima.social/labs/ (feed: https://www.mima.social/labs/feed.xml)
