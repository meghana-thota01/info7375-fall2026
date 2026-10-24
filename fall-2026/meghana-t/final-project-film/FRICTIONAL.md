# FRICTIONAL.md

Dated log of what was tried, what broke, and what changed.

## Oct 22, 2026 — Project selection

Considered and rejected several directions before landing on this one, including a generic dashboard-checker tool and a synthetic-data generation project. Rejected the synthetic-data idea specifically after research showed it would be a weaker clone of an existing free tool (SDV). Settled on the AI Dashboard Insight Benchmark after my TA pointed out that the course rewards rigorous analysis more than a polished build — this reframed the project from "build a correction tool" to "build a benchmark that measures the problem," which also happened to be a better-scoped, more finishable idea for one person.

## Oct 22–23, 2026 — Building and stress-testing PROJECT-BRIEF.md

Went through four full rounds of adversarial review before the brief held up:
- **Round 1:** caught a model-name/version error (cited an outdated Claude model and GPT-4o instead of current models) and a sample-design flaw (repeated runs of 3 tables measures variance, not model behavior across inputs).
- **Round 2:** caught that my "wrong driver" category had no real ground truth (I'd have been grading the model against my own opinion) — fixed by committing to planted, table-visible drivers in synthetic data.
- **Round 3:** caught that my labeling precedence rule would mask the true prevalence of each error type — fixed by scripting the mechanical checks separately from the two genuine human-judgment calls.
- **Round 4:** caught a fabricated-sounding quote (I'd paraphrased Microsoft's wording and put it in quotes) — fixed by fetching the live page and using the exact wording, with the real access date.

## Oct 23, 2026 — Environment setup friction

`./setup --install` failed on `pycairo` (missing `cairo`/`pkg-config` system libraries) and separately on `npm` (a stale, root-owned cache from a previous Homebrew bug). Fixed by installing Homebrew, then `brew install cairo pkg-config pango`, then `pip install kokoro-onnx` directly, then `sudo chown -R` on the npm cache. Confirmed via `./help` that `/v0` genuinely isn't a Gru-equivalent command in this toolkit either — a different course's Gru tool had the same gap, so didn't fight it; used `/problemstatement`-equivalent synthesis instead where relevant.

## Oct 23, 2026 — First beat sheet build, major content bug

Built the first `beat_sheet.json` and rendered successfully, but the compiled film showed generic marketing placeholder content (email open rates, product prices in £, social media tabs) instead of my actual project content on five different cards. Root cause, found by reading the actual `ShowTellCard.tsx` component source: several card "kinds" (`workspace`, `stack`, `paths`, `masked`) silently fall back to their own built-in demo data when the specific props they expect (`items` with a minimum count, `labels`, `word`) aren't supplied exactly right. This was not a one-time fix — it took several rounds to find the right props for each kind.

## Oct 23–24, 2026 — Repeated bugs across multiple render rounds

Several specific bugs survived 4–5 separate fix attempts before being correctly diagnosed:
- **"CHECKLIST" text clipping:** turned out the `masked` card kind has no font-size control prop — longer words are simply too wide for its fixed giant font size. Fixed by switching that beat to the `focus` kind instead, which has real layout room.
- **Overlapping/cut-off field-name text** (`claimed_percentage` running into `cited_figures`): the `workspace` kind uses fixed-width pill chips regardless of text length. Fixed the same way — switched to `focus`.
- **A hardcoded orange decorative ball** on `workspace` and `stack` cards, and a **hardcoded checkmark** on `stack`'s first card: confirmed these are not prop-controllable at all by reading the component source directly. Switching away from those kinds was the only real fix. (One smaller decorative dot remains on `focus` cards — confirmed this is intentional, consistent styling, not a placeholder, per an independent reviewer's assessment.)
- **Long static holds and mid-sentence cuts:** caused by card `durationSeconds` props not matching the real measured audio length for each beat. Fixed by syncing every card's duration to its actual Kokoro-measured audio length plus a ~0.3s tail, after every narration change.

## Oct 24, 2026 — Gate-level failures

- Adding a second citation (Tableau Pulse) to the opening banner caused a Gate V `edge-bleed` blocker — the combined two-citation text overflowed the safe frame. Reverted to a single citation on screen; moved the Tableau Pulse citation to `SOURCES.md` instead, since adding it as spoken narration plus a written citation elsewhere still satisfies the sourcing requirement without breaking the render.
- `./art final` consistently failed its Gate T (text-height) check on one specific element in the `BDEFS` beat, even after two different attempted fixes (removing a 4th term card; clearing a hardcoded 32px caption field). The exact failing element was never conclusively identified even after reading the component source — the measurement tool reported the same 40px value across unrelated changes, suggesting either a genuinely small text run I couldn't isolate, or a quirk in the measurement itself. Given the extensive, otherwise-clean passing record of the standard `./art run` pipeline (Gate V: 0 blockers, 0 majors, confirmed by direct frame inspection against the full checklist), I used the `./art run` review-cut output as the final submitted film rather than continue chasing this one Gate T issue indefinitely. **(Superseded by the entry below — Gate T was later fixed, and `./art final`'s output is what's actually submitted.)**

## Oct 24, 2026 — File-transfer friction (process note, not project content)

Several rounds of corrupted/incomplete `beat_sheet.json` transfers between this conversation and the local machine, caused by terminal paste buffering and heredoc issues with a large JSON file. Eventually resolved using `pbpaste > file.json` directly from the clipboard, which proved reliable where `nano` and inline heredocs were not.

## Oct 24, 2026 — Honesty-rule violation caught in review, and a real Gate T fix

A review against the full assignment rubric (not just visual/factual accuracy) caught that my narration violated the assignment's own tense rule in several places — lines like "I send," "I relabel," and "what this produces" presented planned, not-yet-run work in the present tense, when the rule is explicit: past tense only for what exists, "will" for everything else. The same review caught that three of the seven required questions (who opens it and the first 60 seconds; the first thing to run and how you'd know; which skills are new versus existing, with evidence) were answered in `PROJECT-BRIEF.md` but never actually appeared in the film — and the film, not the brief, is what's graded. Rewrote all 13 narration lines to fix tense and fold in the missing answers, re-generated audio, re-synced every duration, and re-rendered. Verified directly against the file (not from memory) before treating the fix as done.

Separately, the Gate T failure (a 40px text run against a 41px floor) that had resisted two earlier prop-based fixes was finally resolved by reading the component source closely enough to find the actual hardcoded values (`termSize`, `meanSize`) and bumping them directly, since no prop exists to control this. This is a one-line, narrowly-scoped edit to a shared toolkit file, made only after confirming no other option existed, and documented here and in `SOURCES.md` rather than left unmentioned. `./art final` now passes Gate T cleanly and also turned out to remove the corner debug labels that `./art run`'s review cut always carried — something I'd previously given up on finding a toggle for.

## Oct 24, 2026 — One remaining tense slip

A final review caught one more honesty-rule slip that survived the larger rewrite: B00 said "against the answer I planted," past tense for a table that doesn't exist yet. Changed to "against the planted answer," regenerated B00's audio only, re-synced its duration, and re-rendered.

## What changed from the original plan

- No scope change to the core project (benchmark design, taxonomy, methodology all as originally briefed).
- Did add two beats not in the original plan (`B00B`: a "pending" findings-table mockup; `B04B`: the pre-committed comparison-rule card) after review feedback pointed out these directly cover two of the seven required questions (Q3 and Q6) that weren't otherwise visible on screen.
- Did not pursue restructuring the beat sheet into finer, per-sentence beats to land every cut on every narration pause — confirmed with a reviewer that one-beat-per-chunk cuts are acceptable as long as each beat's visual duration matches its own audio exactly, which was implemented instead.
