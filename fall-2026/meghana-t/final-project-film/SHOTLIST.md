# SHOTLIST.md — AI Dashboard Insight Benchmark pitch

| Beat | Type | What's on screen | Why a card (if applicable) |
|------|------|-------------------|------------------------------|
| BIDEA | Bookend (Remotion, `BrutalistHesitantWriter`) | Naive claim corrected mid-sentence; citation banner with the real Microsoft quote | N/A — bookend pattern |
| BDEFS | Bookend (Remotion, `ClaudeDefinitions`) | Four terms: planted ground truth, prompt contract, cited figures, small base | N/A — bookend pattern |
| B00 | Card (`focus`) | Numbered 5-step chain: Input table → Claude Sonnet 5.5 · GPT-5.6 Terra → JSON output → 5 checks → Findings table | The idea is reading a sequence top to bottom — exactly `focus`'s documented use ("reading a table, finding the one row"), applied here as a numbered pipeline |
| B00B | Card (`focus`) | Findings table, every cell "pending," labeled "Planned, no results yet" | Same reasoning — a row-by-row table read |
| B01 | Card (`focus`) | Prompt contract fields: `claimed_driver`, `claimed_percentage`, `cited_figures` | Switched from `workspace` after repeated text-overflow failures; `focus`'s row layout has real horizontal room for full field names |
| B02 | Card (`tabs`) | "Automated" vs "Judgment" tab switch, 3 scripted checks / 2 hand-labeled calls | The idea is a compare-A-then-B switch between two categories — `tabs`' documented use |
| B03 | Card (`focus`) | Reliability plan: 7-day re-label gap, Cohen's κ ≥ 0.70, % agreement, 12-item caveat check | Row-by-row read of a plan |
| B04 | Card (`focus`) | 18 tables, 6 small-base, 36 generations, 1 run per table per model | Row-by-row read of counts |
| B04B | Card (`masked`) | "4 of 18" — sub-line reads "called a real difference only if this many tables differ. Set before any results." | Single short phrase/number — `masked`'s documented use |
| B05 | Card (`focus`) | "CHECKLIST" heading + the five taxonomy categories | Switched from `masked` after the giant-word rendering clipped "CHECKLIST"; `focus` has real font-size room. Note: `focus` does not render a `sub` prop, so the scope line ("not testing Copilot or Tableau Pulse themselves") is spoken in narration only, not shown on this card. |
| B06 | Drawing (Manim, `B06_ResumeGap`) | A page with scribbled lines; a quill writes one new line; a terracotta dot marks it | Not a card — personal reflection, fails the card test (not an interface/number/word), so drawn per show-tell's own rule. Uses the documented writing-kit (`paper`, `scribble_block`, `quill`, `write_lines`) |
| BHTF | Bookend (Remotion, `ClaudeComposerAsk`) | A real, pasteable prompt for the viewer | N/A — bookend pattern |
| BOUT | Drawing (Manim, `BOUT_TitleCard`) | Title + the speaker's own name, no branding | Custom scene, not the toolkit's default `ClaudeTitleOutro`, since that component is hardcoded to the `@NikBearBrown` channel and cannot be used for a personal submission |

**Note on `focus` appearing on 6 of 13 beats:** this density reflects a genuine content fit (nearly everything in this film is a sequence of facts to read row by row), not a shortcut around drawing. Each use was checked individually against the card test before being chosen, and three kinds (`workspace`, `stack`, `masked`-for-long-words) were tried first and rejected after they produced hardcoded visual defects (fixed-width text overflow, a non-removable decorative checkmark, a 3-card cap, no font-size control) that `focus` does not have.
