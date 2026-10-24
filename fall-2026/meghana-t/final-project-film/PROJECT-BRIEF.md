# PROJECT BRIEF — AI Dashboard Insight Benchmark

## 1. What is it?

A benchmark testing Claude Sonnet 5.5 and GPT-5.6 Terra on writing business-dashboard insights from the same data, labeling each one against planted ground truth — data where I secretly know the right answer — and reporting measured error rates.

Will exist: 18 distinct synthetic input tables across 3 business domains, each sent once to each model under a fixed prompt contract (36 generations total), every generation scored on independent pass/fail checks, a reliability check on the genuine judgment calls, and a written findings report. Repository on GitHub.

## 2. Why would anyone care?

Microsoft's own Power BI Copilot documentation says "Copilot outputs are nondeterministic" (Microsoft Learn, "Copilot in Power BI tutorial: Discover data and ask questions," accessed October 22, 2026) — and says users should know how they can "evaluate or validate these outputs, for themselves." Tableau Pulse, generally available since 2024 (TechTarget, "Tableau launches Pulse, a GenAI-fueled insight generator," published Feb 22, 2024, accessed October 24, 2026), auto-surfaces similar insights. I found no published breakdown of specific error types or rates for either.

What this saves a BI analyst is the guesswork of which numbers to double-check, by giving them a measured, specific checklist — where the vendors currently offer only generic "validate it yourself" guidance.

## 3. Who opens it, and what do they do with it?

Reader: a hiring manager or recruiter for a Data/Business Analyst or BI Analyst role.

First sixty seconds: opens the README, sees the findings table (counts and rates by model and category) at the top, clicks a row, and is linked to a per-example file showing the input table, the model's raw structured output, the recorded checks, and the final label.

## 4. What does it prove about you?

**Evaluation:** an error taxonomy built from independently recorded checks, not one collapsed label (see Appendix). **Verification:** recomputing true values from planted ground truth. **Prompt contract:** a fixed JSON schema every generation must follow, so outputs can be checked by script. **Source grounding:** that contract requires a `cited_figures` field, checked automatically against the input table.

There's no agent here on purpose — the point is measuring, not building. What this should show: I can tell which checks a script can do and which need a human, and I test whether my own judgment is actually consistent instead of assuming it.

## 5. What is in, out, and first?

One thing I deliberately won't build: an automatic correction tool — that's a natural next step, not part of this. Also out: testing Tableau Pulse or Copilot's actual products, more than 2 models or 18 tables, and run-to-run consistency — this measures how often a single generation gets something wrong, not whether a model is consistent with itself across repeats.

**Scope-defining choice:** each model receives an aggregated summary table, not raw rows or a chart image. Every planted driver is verified, at construction time, to be determinable from the table itself.

**First thing that runs:** one table sent to both models under the fixed contract; both outputs run through the three automated checks (see Appendix); result logged with model name (`claude-sonnet-5-5`, `gpt-5.6-terra`), the settings used — temperature fixed at 0 for Claude; for GPT-5.6 Terra, a reasoning-tier model, whether it accepts a temperature setting at all is not yet confirmed, so this will use temperature 0 if accepted or that model's default settings otherwise — and timestamp.

**How you'd know it ran:** a log row with both models' output and their automated check results.

## 6. What could sink it?

**Sample size.** 18 distinct tables, each worth about 5.6 percentage points. I'm pre-committing now, before seeing results: I'll only call a difference between models meaningful if it's at least 4 of 18 tables — not an after-the-fact judgment call. The paired design could support a McNemar's test, but 18 pairs gives it limited power, and I'll say so rather than overstate the comparison.

**Both models could just ace it.** If my planted errors are too easy, error rates go near zero and there's nothing to report. So 6 of the 18 tables are built deliberately hard, each with a small-base effect a careless insight would miss. I'll also hand-label with the model's identity hidden, so I can't unconsciously favor one.

**Reliability of the genuine judgment calls.** Schema validity, citation-matching, and number-tolerance are scriptable — no human judgment, no kappa needed. The real judgment calls are which driver the text names, and whether a small-base caveat is present. I'll hand-label only these two, re-label after a 7-day gap, and report both Cohen's kappa (target ≥ 0.70) and raw percent agreement.

**Reproducibility.** Even at temperature 0 where accepted, output isn't guaranteed identical. What I can promise is that every generation is logged and traceable to its exact model, version, and timestamp.

## 7. Why this project?

I'm applying for Data/Business Analyst roles right now. I reread my resume and noticed every AI line said I'd used AI. None said I'd checked it. That's backwards for an analyst job. I'd originally planned to build an auto-correction tool; my TA pointed out this course rewards the analysis itself more than a polished build, which reframed the format — but closing that resume gap with real evidence is the actual reason I'm doing this.

Existing skills, with evidence: hypothesis-driven analysis and business-facing reporting, demonstrated in my churn, CLV, and airline-satisfaction projects — course projects, reports and notebooks available on request.

New skill: telling apart what a script can check and what needs a human, and testing whether my own judgment holds up a second time.

---

## Exists today
This brief. Verified research in SOURCES.md (exact Microsoft quote, dated; Tableau Pulse source, with its real publish date). The pitch film itself (`ai-dashboard-insight-benchmark-pitch.mp4`), its `beat_sheet.json`, and its passing gate reports (Gate V, Gate T). No benchmark code written yet — the 18 tables, the prompt contract, the generation scripts, and the findings report below are all still planned.

## Will exist
18 synthetic tables with planted, table-visible ground truth (6 of the 18 include a small-base case) · fixed prompt contract (JSON schema, `claimed_driver` required, `claimed_percentage` as a specific field, `cited_figures` list) · generation scripts (Claude Sonnet 5.5 + GPT-5.6 Terra, temperature 0 where accepted) · 36 generations, each scored on 3 automated checks + 2 hand-labeled judgment calls · a reliability pass (κ and percent agreement) on the judgment calls · a written findings report · the full benchmark repository.

---

## Appendix: Scoring methodology

**Automated checks (scripted, run on every generation, no human judgment):**
- Schema valid (all required fields present, correct types)
- Every entry in `cited_figures` exists in the input table
- `claimed_percentage` is within 1 percentage point of the recomputed true value

**Hand-labeled judgment calls (the only two requiring human reliability testing):**
- Does the insight's text name the correct planted driver? (yes/no)
- For small-base tables, does the text include an explicit caveat about the small base? (yes/no) — this check only applies to 6 tables × 2 models = 12 items, so a single disagreement can swing kappa sharply. I'll treat kappa here as a rough signal and lean on raw percent agreement for this specific check.

**Deriving the report-level label**, in this precedence order: Contract violation (schema invalid or bad citation) → Wrong driver → Wrong number → Misleading small base (uncaveated) → Correct.

Each of the 5 underlying checks is also reported individually, so precedence does not mask true prevalence — e.g., "wrong driver" is reported both as a precedence-ordered label count and as the raw rate across all generations regardless of what else was also wrong.

An empty or null `claimed_driver` field is automatically scored as a failed driver check, not a schema violation — the field is present, just uninformative.

Of the 18 input tables, 6 are constructed with a planted small-base effect specifically to populate the small-base category; the other 12 do not.
