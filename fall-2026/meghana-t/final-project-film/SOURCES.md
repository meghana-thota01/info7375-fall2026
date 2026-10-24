# SOURCES.md

## Citations used in the film

**Microsoft Learn**, "Copilot in Power BI tutorial: Discover data and ask questions" (en-US), accessed Oct 22, 2026. Quote used on screen and in narration: "Copilot outputs are nondeterministic." Full quote verified word-for-word against the live page before use.

**TechTarget**, "Tableau launches Pulse, a GenAI-fueled insight generator," by Eric Avidon, published Feb 22, 2024, accessed Oct 24, 2026. Used to support the claim that Tableau Pulse auto-generates insights and has been generally available since 2024 (confirmed directly from the article's own publish date and opening line).

## Model identifiers named in the film

- Claude Sonnet 5.5 (`claude-sonnet-5-5`) — confirmed current via Anthropic's own system documentation.
- GPT-5.6 Terra (`gpt-5.6-terra`) — confirmed current via independent sources (Vercel AI Gateway model listing, LiteLLM provider documentation, AWS Bedrock's own model card), cross-checked Oct 23, 2026. Whether this model accepts a `temperature` parameter has not yet been tested directly; PROJECT-BRIEF.md states this explicitly as unconfirmed rather than assuming it.

## What I made

- `beat_sheet.json` — the narration and visual plan for all 13 beats, written and revised across several rounds based on real review feedback (see FRICTIONAL.md).
- `scenes.py`'s two custom Manim scenes — `B06_ResumeGap` and `BOUT_TitleCard` — designed by me (the resume-reflection concept and the no-branding outro requirement were both mine), with the Manim code itself written with Claude.
- `PROJECT-BRIEF.md`, `README.md`, `BUILD-PROMPT.md`, `SOURCES.md` (this file), and `FRICTIONAL.md`.
- A one-line, well-scoped edit to `runtime/remotion/src/scenes/ClaudeDefinitions.tsx`, increasing two hardcoded font-size constants (`termSize`, `meanSize`) after confirming no prop exists to control this size and that smaller text was failing the toolkit's own Gate T minimum-size check at four terms. Documented in FRICTIONAL.md.

## What Claude (the assistant) contributed

Claude was used throughout this project's development:
- Helping select and scope the project idea against the assignment's "right size" criteria
- Drafting and revising `PROJECT-BRIEF.md` across multiple rounds of adversarial self-review (checking factual claims, exact quote wording, methodology soundness, and consistency with course concepts)
- Verifying every factual/citation claim via live web search before use (both citations above were directly fetched and checked, not assumed from memory)
- Drafting and later rewriting the `beat_sheet.json` narration (the rewrite specifically fixed tense violations — presenting planned work as already done — caught in review)
- Writing both custom Manim scenes in `scenes.py`
- Diagnosing and fixing render/content issues across many iterations: prop-schema mismatches causing placeholder content, duration-sync bugs causing mistimed cuts, a WCAG edge-bleed blocker, and a persistent Gate T text-height failure eventually traced to hardcoded component font sizes

All Claude-assisted drafts were reviewed, and in several cases corrected or pushed back on, by the author before use. See `FRICTIONAL.md` for the dated record.

## Third-party assets and licensing

- **Brutalist toolkit** (`github.com/nikbearbrown/brutalist.art`) — the production pipeline, drawing kit (`iso_kit.py`), and Remotion components (`ShowTellCard`, `ClaudeDefinitions`, `BrutalistHesitantWriter`, `ClaudeComposerAsk`) used to build this film. I checked the repository directly on Oct 24, 2026: GitHub does not detect or display a LICENSE file for this repo, so no open-source license is confirmed for the toolkit itself — it is used here as course-provided shared infrastructure, not redistributed, and only one shared file was edited (noted above and in FRICTIONAL.md).
- **Kokoro TTS voice model** (`af_bella`, via `kokoro-onnx`) — confirmed **Apache License 2.0**, verified against multiple independent sources (the model's own distribution pages) on Oct 24, 2026.

No paid generation, no API keys, and no third-party media accounts were used in producing this film, per the assignment's free-pipeline requirement.
