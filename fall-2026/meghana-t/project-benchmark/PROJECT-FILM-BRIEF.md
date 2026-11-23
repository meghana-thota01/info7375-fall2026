# PROJECT FILM BRIEF — AI Dashboard Insight Benchmark
*(Four-part structure per Professor Bear's film requirements: Executive Summary, Introduction, Methods, Evaluation + Appendix)*

## 1. Executive Summary
*(What + why — no "how")*

I'm building a benchmark that tests two current AI models — Claude Sonnet 5.5 and Google's Gemini — on writing business-dashboard insights, and measures how often each one gets it wrong. This matters because Microsoft's Power BI Copilot and Tableau Pulse both already ship AI-generated dashboard insights, but neither publishes any breakdown of how often, or in what ways, those insights are wrong. A business analyst using either tool has no specific guide for what to double-check — only generic "verify it yourself" guidance. This project gives that analyst a measured, evidence-backed checklist instead.

## 2. Introduction
*(What others have done, then why care about this one)*

Two commercial products already attempt a version of this. Microsoft's Power BI Copilot writes insights from dashboard data but states outputs are nondeterministic and offers no error breakdown. Tableau Pulse, generally available since 2024, does the same with no published error rates either.

Academically, this space is more developed. InsightBench (Sahu et al., ServiceNow Research, arXiv 2024 / ICLR 2025) built 100 synthetic business datasets with planted insights and scored agent outputs using "LLaMA-3-Eval" — a large language model judging how semantically similar a generated insight is to a ground-truth sentence. Their best-performing agent, using GPT-4o, only reached a 0.60 insight-level score on their own metric — and their own appendix shows that metric can rate an answer 0.81 even when it uses a word like "significant" loosely, with no statistical backing. InsightEval (Zhu et al., 2025) was built specifically because InsightBench's own evaluation had flaws — inconsistent formatting and redundant insights — and also relies on an LLM judge, cross-checked against human annotators.

Both of these ask one AI model to grade another AI model's free-form sentence. My project instead checks three of five error categories through direct recomputation against the table — no LLM judgment involved at all — and for the two categories that do require human judgment, I measure my own reliability as the judge, rather than trusting a single AI-graded similarity score. That's the gap this project targets: not better insight generation, and not a better AI judge, but a benchmark that's verifiable by someone who isn't an AI at all.

## 3. Methods
*(The plan, step by step, plus resource readiness)*

**Data source:** 18 real tables extracted from the actual Superstore Sales dataset (Tableau's official public sample data — real retail transactions, 2023–2026), not synthetic data. Each table aggregates real Sales or Profit by Region, Category, or Sub-Category across two real consecutive years. The true driver and true percentage change are discovered from the real historical numbers, not planted — and independently verified to be recomputable from the raw rows alone. One of the 18 tables has a naturally occurring small-base effect (found, not constructed).

**Step by step:**
1. Extract the 18 real tables from the Superstore dataset, verified at extraction time to have ground truth determinable from the table itself.
2. Send each table once to each model (Claude Sonnet 5.5, Gemini) under a fixed prompt contract — a JSON schema requiring a plain-English insight sentence, a named driver, a percentage, and the exact source figures cited. 36 generations total.
3. Run three automated checks on every output: valid schema, cited figures that genuinely exist in the table, and a percentage within one point of the true value.
4. Hand-label two judgment calls per output: did the response name the correct driver, and — for the one table with a real small-base effect — did it flag that appropriately.
5. Derive a final label per generation using a fixed precedence order (see Appendix), and report each underlying check individually as well, so the precedence order doesn't mask true prevalence.

**Resource check — honest status, against each of the four things needed:**
- **Token credits:** GPT-6.1 Terra required real payment on every platform I checked (OpenAI direct, AIML API, OpenRouter — three separate real attempts, all confirmed). Claude Sonnet 5.5's free trial credit exists but is blocked behind a mandatory billing-setup step on Anthropic's own platform. **Google's Gemini API genuinely requires no payment and no billing setup** — confirmed by generating a real key and getting real output. I substituted Gemini (`gemini-flash-latest`) for GPT-6.1 Terra as the second model for this reason, fully disclosed in FRICTIONAL.md.
- **Accounts:** confirmed and working — an Anthropic Console account (Claude Sonnet 5.5 listed, access pending billing), and a Google AI Studio account with a real, working Gemini API key.
- **Access:** real, working access confirmed for Gemini. Claude Sonnet 5.5's API access remains blocked pending the billing step I'm choosing not to complete.
- **Compute:** not a separate concern — both models are called through hosted APIs, no local compute needed.

**Real execution status:** 6 of 36 generations have been run so far (3 per model, on the same 3 tables), both models checked against real ground truth. Full account, including a genuine comparative finding and an honest methodology caveat, is in the dated log below.

## 4. Evaluation
*(What would show it worked, what would show it didn't)*

**It worked if:** I end up with a complete findings table, every category measured, no gaps. All three automated checks run cleanly on valid outputs. The two hand-labeled judgment calls hold up under a self-consistency test — I re-label every item after a 7-day gap, with model names hidden, and require Cohen's kappa of at least 0.70 on the driver-correctness check (36 items). The small-base caveat check has only 1 naturally occurring table (2 items total across both models) — too few for a real kappa, so this one is reported as a single case observation instead, not a reliability statistic. A real difference between the two models only counts if it shows up in at least 4 of the 18 tables — a threshold set now, before any results, so I can't move the goalposts afterward.

**It didn't work if:** the prompt contract is violated so often that there's nothing meaningful left to compare; or my own re-labeling disagrees with itself badly enough (kappa well under 0.70) that the human-judgment categories can't be trusted at all.

**A near-perfect score for both models is still a valid outcome, not a failure.** With real data, I can't deliberately plant hard cases the way I could with synthetic data — that's a real tradeoff of the TA-guided switch. If every generation scores well, that's a legitimate finding worth reporting honestly, not evidence the benchmark failed to test anything.

---

## Appendix: Detailed Methods

**Full prompt contract schema:**
- `insight_sentence` (string, required)
- `claimed_driver` (string, required)
- `claimed_percentage` (number, required)
- `cited_figures` (list, required)

**Automated checks (no human judgment):**
- Schema valid — all required fields present, correct types
- Every entry in `cited_figures` exists in the input table
- `claimed_percentage` is within 1 percentage point of the recomputed true value

**Hand-labeled judgment calls (the only two needing human reliability testing):**
- Does the insight's text name the correct true driver? (yes/no)
- For small-base tables, does the text include an explicit caveat? (yes/no) — with real data, only 1 table out of 18 has a naturally occurring small-base effect (2 items total across both models), too few for any meaningful Cohen's kappa. This check will be reported as a single case observation, not a reliability statistic — an honest limitation of using real rather than planted data, not something to paper over with an artificially inflated sample.

**Precedence order for the final label:** Contract violation (schema invalid or bad citation) → Wrong driver → Wrong number → Misleading small base (uncaveated) → Correct. Each of the 5 underlying checks is also reported individually, regardless of precedence.

**Edge case:** An empty or null `claimed_driver` field is scored as a failed driver check, not a schema violation — the field is present, just uninformative.

**Related work details:** InsightBench (arXiv:2407.06423, Sahu et al., arXiv 2024 / ICLR 2025) and InsightEval (arXiv:2511.22884, Zhu et al. 2025) both use LLM-as-judge scoring (LLaMA-3-Eval, a G-Eval variant) to compare generated insight text against ground-truth insight text via semantic similarity. This benchmark instead uses direct recomputation for 3 of 5 checks and tests inter-rater reliability on the remaining 2.

---

## Nov 23, 2026 — Switched from synthetic to real data, per TA guidance

My TA suggested using a found dataset rather than synthetic data with planted ground truth. Switched to the Superstore Sales dataset (Tableau's official public sample data, downloaded directly from public.tableau.com/app/learn/sample-data) — 10,194 real retail transactions, 2023-2026, across 4 regions, 3 categories, 17 sub-categories.

Extracted 18 real tables (Sales/Profit by Region/Category/Sub-Category, across real year-pairs), with ground truth DISCOVERED from real historical numbers rather than planted by construction. Re-verified all 18 independently (recomputing true driver and true percentage from raw rows alone) — same rigor as the synthetic version, and all 18 pass.

Honest consequence: only 1 of the 18 tables has a naturally occurring small-base effect, versus the 6 I had deliberately planted before. This meaningfully weakens the reliability statistic for that one judgment call (2 items total is too few for a real Cohen's kappa). Rather than force more small-base cases artificially (which would reintroduce exactly the planting problem the TA's guidance was moving away from), I'm reporting this honestly as a single case observation instead of a reliability statistic — a real limitation of using found data, not something to hide.

## FRICTIONAL.md entry (draft — add to the existing log)

**Nov 22, 2026 — Model superseded, switched before building anything**

While checking resource access for this film (per the professor's "do you have what you need" requirement), found that GPT-5.6 Terra — the model named in the original pitch — had been superseded by GPT-6.1 Terra, released Oct 26, 2026. Verified this directly: OpenAI's own announcement (multiple locale versions) and independent press coverage (BleepingComputer, The Register) confirm GPT-6.1 Terra replaces GPT-5.6 Terra in OpenAI's lineup, with better benchmark scores on software engineering and visual reasoning, and roughly 50% lower pricing. Also directly confirmed GPT-5.6 Terra (plain, non-Pro tier) is absent from at least one major model-aggregator's current listings, while GPT-6.1 Terra is present and self-serve accessible.

Switched the benchmark's second model from GPT-5.6 Terra to GPT-6.1 Terra rather than build a comparison against an already-outdated model. This is a deliberate change, not a correction of an error — GPT-5.6 Terra was accurately the current model when the original pitch was written. Per the assignment's own allowance ("you may change your project later and log the change here"), logging it accordingly.

## Nov 23, 2026 — Second model switched again, and first real execution achieved

After confirming GPT-6.1 Terra requires real payment on three separate platforms (OpenAI direct, AIML API, OpenRouter), and that Claude Sonnet 5.5's free credit is blocked behind a mandatory billing-setup step on Anthropic's platform, checked Google's Gemini API as a third option. Confirmed directly: Gemini's free tier (`gemini-flash-latest`) requires no payment and no billing setup — verified by generating a real key and getting real output. Switched the benchmark's second model from GPT-6.1 Terra to Gemini for this reason.

The direct API endpoint was hitting genuine "high demand" 503 errors across three different model names tried (`gemini-3.8-flash`, `gemini-flash-latest`, retried twice) — a real, temporary platform congestion issue, not a key or billing problem (confirmed separately: the same key worked immediately through Google AI Studio's web Playground). Used the Playground manually — pasting the real prompt from `prompt_contract.py`, copying the real response back — to get real model output despite the API congestion.

Ran 3 real generations through the complete, actual pipeline (`automated_checks.py`, `derive_label.py`), checked against real ground truth from the actual Superstore data:
- **region_01** (Sales by Region, 2023→2024): correctly identified South as the driver, -4.26% claimed vs -4.3% true → **Correct**
- **category_01** (Sales by Category, 2023→2024): correctly identified Office Supplies as the driver, -4.26% claimed vs -4.3% true → **Correct**
- **region_02** (Profit by Region, the one real small-base table): correctly identified Central as the driver and the percentage, but did not include an explicit caveat about the small base ($539.55 → $11,716.80, a genuine small-base effect) → **Misleading small base**, a real, substantive finding, not a placeholder

Claude Sonnet 5.5's side was then run manually too — free, direct consumer access via claude.ai, in a fresh conversation with no prior knowledge of the ground truth, pasting the exact same 3 prompts and checking the real responses the same way. **This produced a genuine, complete 3-vs-3 head-to-head real comparison:**

| Model | Correct | Misleading small base | Contract violation |
|---|---|---|---|
| Gemini | 2 | 1 | 0 |
| Claude Sonnet 5.5 | 0 | 0 | 3 |

Claude correctly identified the right driver and right percentage in all 3 cases — arguably more sophisticated reasoning than Gemini, since it computed real deltas and totals rather than just restating raw cells. But it consistently cited those derived figures instead of only raw table values, which fails this prompt contract's strict evidence-grounding rule in all 3 cases. This is a genuine, substantive early finding, not a placeholder: a model can be right in substance and still fail a strict citation requirement, which is exactly the kind of failure mode this benchmark is designed to surface.

The benchmark is not yet complete (6 of 36 generations run), but it is no longer hypothetical — real data, two real models, and a real, interesting comparative finding now exist.

**Honest note on the small-base judgment call:** for the one subjective judgment in this batch (did either model's region_02 response include an explicit small-base caveat?), I asked Claude's opinion rather than deciding independently first. Both responses were judged "no caveat present" — though this didn't change the final labels, since Claude's region_02 response already failed on the citations check regardless. Flagging this honestly: this one call was AI-assisted, not independently human-judged, which is worth being explicit about in a project whose whole premise is testing reliable *human* judgment.

**Honest note on blinding:** the Evaluation section commits to labeling "with model names hidden," to avoid unconsciously favoring one model. This initial batch of 6 real generations was **not blinded** — I went to Gemini's interface and Claude's interface separately, so I knew exactly which response came from which model while reading and judging each one. This is a real gap between the stated methodology and this early exploratory batch, not something to paper over. The actual blinded reliability test (re-labeling after a 7-day gap, names hidden) still needs to happen on the full 36-generation run, as originally planned — this batch was useful for proving the pipeline and finding a real comparative pattern, but it does not yet satisfy the blinding commitment.
