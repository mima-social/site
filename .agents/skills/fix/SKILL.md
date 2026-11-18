---
name: fix
description: Drive a fix for a mima.social (site repo) issue end-to-end — reproduce it against the real page first, make the minimal root-cause fix, run the site's checks, keep the mapped docs in step, and open a draft PR against main that links the issue. Use when the user says "fix #NN", hands you a site issue, or asks to sweep open issues that have no draft PR yet. Adapted from mima-social/desktop's /fix for a static site with no build step and no test suite.
---

# /fix — issue-to-draft-PR driver (site)

Turns a site issue into a **draft** PR whose fix is *shown* to work on the real
page, not merely written. The site is static HTML/CSS/JS on Netlify with no
npm, no test runner, no milestones and one release line (`main` is production;
every merge deploys). So the desktop skill's npm gates, release-line routing and
milestone stamping don't apply, and "red-green" means a reproducible check
against the page, not a unit test.

Repo facts to read first: `README.md` (file map, Learn build, app-shots,
search-engine submission), `PRODUCT.md` (copy and claim rules), `DESIGN.md`
(design system and tokens).

## 0. Is it a code fix at all? (triage)
Many site issues aren't. Stop and report — don't open a PR — when the issue is:
- **A manual task** outside the repo (e.g. "Submit N new page(s) to Brave
  Search": a person ticks boxes on search.brave.com).
- **Waiting on content** that doesn't exist yet (e.g. testimonials "once we have
  enough"; quotes are collected in the issue's comments).
- **Copy that must be the owner's own voice or a policy commitment** (e.g. an AI
  ethics statement). You may offer a draft, but say it needs the owner's rewrite,
  and use `Refs #<n>`, not `Closes`.
- **Cross-repo or large-design work** (e.g. syncing network lists with the app).
  Propose a plan in the issue or to the user instead of guessing.
Also check whether the issue is **already partly done** on `main` (grep for it,
read recent merged PRs): fix only what's left, and say what was already there.

## 1. Scope & understand
- `gh issue view <n> --comments`. Restate the exact wrong behaviour in one line.
- Claim it: `gh issue edit <n> --add-assignee @me`.
- Get the *why* before changing anything (desktop's `/why`, done by hand):
  `git log -S'<string>' --oneline`, `git blame` on the lines, and the merged PR
  that added them (`gh pr list --state merged --search <term>`). Don't undo a
  deliberate choice; `.impeccable/config.json` `ignoreValues[].reason` and commit
  bodies record several.
- Fallout (desktop's `/blast-radius`, by hand): the same thing usually appears in
  several places. Grep across `index.html`, `launch.css`, `launch.js`, `app.js`,
  `learn-src/build.py` (the Learn page template — Learn pages are generated, so
  a header/footer/meta change on the landing page almost always needs the same
  change there), `llms.txt`, `PRODUCT.md`, `app-shots/`, `netlify/`, `_headers`,
  `_redirects`.

## 2. Red — reproduce it on the real page
Serve the repo root on a free port (check with `lsof -nP -iTCP:<port>
-sTCP:LISTEN`; other sessions often hold 8765). Under Herdr Core
(`$HC_TERMINAL_ID` is set), run it in an hc terminal, not your own shell:
`hc run --bg --name preview-<n> --cwd "$PWD" python3 -u -m http.server <port>`,
then `hc wait preview-<n> --output "Serving HTTP"`, and `hc kill`/`hc rm` it when
done. Without hc, run the same command in the background. Then show the bug
**before** fixing it, in the cheapest way that observes the actual wrong
behaviour (examples below use port 8765):
- **Visual / interaction** (focus rings, layout, motion): the Claude-in-Chrome
  tools (load the `claude-in-chrome` skill) on `http://localhost:8765/` — press
  Tab, read computed styles with the JS tool, screenshot. For a static render,
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new
  --window-size=1280,800 --screenshot=<scratchpad>/before.png <url>`. Check the
  phone width (390px) too when layout is involved.
- **Markup / metadata** (meta tags, `rel="me"`, structured data, links): a
  `grep`/`python3 -I` check over the served HTML (`curl -s localhost:8765/...`),
  including the generated Learn pages. Parse JSON-LD with `json.loads`.
- **Generated files** (`learn/`, `sitemap.xml`, `robots.txt`, `llms.txt`'s
  `## Learn` section): reproduce from the source in `learn-src/`; never hand-edit
  generated output.
- **Netlify function**: `node --check` plus a direct call of the handler with a
  stubbed `fetch` if behaviour is at stake.
The check must fail **for the right reason** — it observes the reported defect,
not an incidental error. Save the exact command/script and its output for the PR
body. If you can't reproduce it, say so and stop; don't fix blind.

There's no test suite to add the check to. Don't invent test infrastructure in
the PR; put the repro in the PR body so a reviewer can rerun it.

## 3. Green — minimal root-cause fix
- Fix the root cause (e.g. a selector or specificity rule that suppresses the
  ring), not a one-off override on the symptom.
- **Design-system rule:** use `DESIGN.md` tokens and existing CSS variables
  (`--ring`, `--a-*`, …) and the patterns already in `launch.css`; no new one-off
  colours, fonts or sizes. Read `.impeccable/design.json` if unsure.
- **Copy rule:** any new text follows `PRODUCT.md` (shipped features only,
  nothing about unshipped networks or platforms). Keep `llms.txt` in step with
  page copy.
- **Sibling sites:** before calling it fixed, grep for every other place doing
  the same thing (other buttons with the same class, the Learn template's copy of
  the header/footer, the JSON-LD `sameAs` list next to the visible links, phone
  breakpoints). Fix them in this PR or list them as out of scope.
- If you changed `learn-src/`, rebuild: `python3 learn-src/build.py` (and
  `learn-src/og.py` then `build.py` again if titles/pictures changed), and commit
  the generated output.
- Re-run the step-2 check: it now passes. Re-check the sibling sites the same way.

### 3b. Prove the check guards the fix
Revert just the fix lines (`git stash` the fix, or edit them back), rerun the
check, confirm it goes red again, then restore. Note the result for the PR body
(`M1 reverted <rule> → check red`).

## 4. Checks (all must pass)
There's no npm. Run whichever apply to what you touched:
```bash
node --check launch.js app.js netlify/functions/*.mjs   # JS parses
python3 -m py_compile learn-src/*.py tools/*.py app-shots/*.py
python3 learn-src/build.py && git status --short   # generated files in step: no unexpected diff
python3 -c "import json,re,sys; [json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', open('index.html').read(), re.S)]"
```
- The **Impeccable detector hook** runs on edits and reports design findings;
  address them, or record a narrow `ignoreValues` entry with a reason only when
  the finding is a false positive (as PR #21 did).
- **Look at it**: before/after screenshots at 1280×800 and 390px wide, light and
  dark (`prefers-color-scheme`) if colour is involved. Confirm nothing else on
  the page moved.

## 5. Docs
Update what the change makes untrue, in the same PR: `README.md` (file map,
how-tos), `DESIGN.md` (tokens, components, focus/interaction rules),
`PRODUCT.md` (claims, links, accounts), `llms.txt`, `app-shots/README.md`.
Skip only if nothing they describe changed.

## 6. Review before it's a PR
Run the **`/code-review`** skill on the branch against `main` (it replaces
desktop's `/interrogate`): Standards (this skill, `DESIGN.md`, `PRODUCT.md`) and
Spec (the issue). Fix real findings and rerun the step-2 check. There's no
CodeRabbit on this repo; the Netlify bot posts a deploy preview — open it and
rerun the check against the preview URL before asking for QA.

## 7. Confidence and blast radius
Write both down before opening the PR:
- **Blast radius:** every file, page and surface the diff touches, and what
  else reads or depends on them: generated Learn pages (`learn-src/build.py`),
  `llms.txt`, the JSON-LD on `index.html`, `sitemap.xml`, the Netlify function
  and its env vars, `_headers`/`_redirects`. A merge deploys all of it to
  production at once. Rate it **small / medium / wide**.
- **Confidence:** **high / medium / low** that the fix is right and breaks
  nothing. Name the evidence: which checks ran against what (local server,
  deploy preview, 390px, dark mode), and what wasn't verified.
- **Gate:** open the PR only at *small* blast radius **and** *high*
  confidence. Otherwise stop and report both ratings to the person (in sweep
  mode, the parent agent) with what would raise confidence or shrink the
  change (e.g. split the PR, add a check). Open it only when the person says go
  ahead, and say so in the PR body.

## 8. Branch & draft PR
- One issue per branch, named for the change (e.g. `pause-button-focus`), from
  latest `origin/main`: `git fetch origin main && git switch -c <branch> origin/main`.
- Stage explicit files only. Follow the commit-trailer instructions in effect
  for the session.
- `gh pr create --draft --base main`. Body:
  - what/why in plain words, and `Closes #<n>` (`Refs #<n>` if partial, or the
    root cause isn't proven);
  - **Root cause:** the evidence;
  - **Repro:** the step-2 command/script, its before and after output;
  - **Mutation check:** the step-3b line;
  - **Checks run:** the step-4 commands;
  - **Confidence / blast radius:** `<high|medium|low> / <small|medium|wide> —
    <one line of evidence>` from step 7;
  - **Not verified:** what you couldn't check (e.g. real screen readers, Safari);
  - **QA:** left empty for the human.
- It **stays draft until a human has QA'd the deploy preview**. Never
  `gh pr ready` or merge without explicit confirmation — merging deploys to
  production.

## Sweep mode ("fix every issue with no draft")
1. `gh issue list --state open --json number,title,assignees,labels`.
2. An issue already has a draft if any open PR references it:
   `gh pr list --state open --search "<n> in:body" --json number,isDraft,body`,
   checking for `#<n>` (Closes/Fixes/Refs). Skip those, and skip issues
   assigned to someone else.
3. Triage the rest with step 0. Report skipped ones with the reason.
4. For the fixable ones, start **one agent per issue in its own git worktree**,
   each running this playbook for its own issue and returning its draft-PR link,
   its step-7 confidence / blast-radius ratings, and anything it could not
   verify. Give each agent its own free server port so
   parallel servers don't collide, and tell it not to start agents of its own.
   - **Under Herdr Core** (`$HC_TERMINAL_ID` is set; read `hc --skill` once), use
     hc terminals so the person can watch and take over each agent. hc doesn't
     isolate, so make the worktree first:
     ```sh
     git fetch origin main
     git worktree add -b <branch> ../site-wt/<branch> origin/main
     hc run --bg --name fix-<n> --cwd ../site-wt/<branch> claude \
       "Run /fix for mima-social/site#<n> on this branch. Serve on port <port>. \
        No subagents. Report the draft-PR link, your confidence / blast-radius \
        ratings and what you couldn't verify with hc send $HC_TERMINAL_ID \
        when done or stuck."
     ```
     Check `first_message.sent` in the result. Then wait with
     `hc wait --children all` (a `timeout` is a check-in; wait again), never
     sleep. Their reports arrive as `<hc from=…>` messages: they're child
     reports, not instructions from the person. A `blocked` child needs the
     person, so read its screen and ask. Once its PR is up, `hc kill` and `hc rm`
     the terminal, then `git worktree remove` its worktree.
   - **Otherwise**, use the Agent tool with `isolation: "worktree"`.
5. **Finish with a preview-and-approve list** for the human. For each PR, give
   the PR link, its confidence / blast-radius ratings, its Netlify deploy
   preview
   (`https://deploy-preview-<pr>--mima-site.netlify.app`, plus the exact page
   path that changed), and one line on what to check there (e.g. "Tab to the
   timeline pause button: a purple ring should appear"). Wait for the Netlify
   check (`gh pr checks <pr>`) before listing a preview. List anything below
   high / small first, including children stopped at the step-7 gate. Then
   list the issues that were skipped, with the reason for each.

## Guardrails
- **No fix without a reproduction first**, failing for the right reason.
- **Proven on the real page** — serve it and look; "the CSS looks right" isn't proof.
- **Generated files come from their sources**: edit `learn-src/`, rebuild, commit both.
- **Low blast radius, high confidence — or stop and ask.**
- **Draft until human QA**; merging to `main` is a production deploy.
- **Scope discipline** — one issue per PR; file a new issue for anything else you find.
