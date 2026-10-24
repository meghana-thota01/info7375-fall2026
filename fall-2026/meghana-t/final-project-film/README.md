# AI Dashboard Insight Benchmark — Project Pitch

**Name:** Meghana Thota
**Target role:** Data / Business Analyst
**Runtime:** 3:29 (208.67 seconds)

## What this is

A pitch film for a benchmark that tests two AI models (Claude Sonnet 5.5, GPT-5.6 Terra) on writing business-dashboard insights, labels each one against planted ground truth, and reports measured error rates. Full details in `PROJECT-BRIEF.md`.

## How to rebuild the film

1. Clone the Brutalist toolkit: `git clone https://github.com/nikbearbrown/brutalist.art`
2. Run `./setup --install` inside the toolkit to install dependencies (Python packages, Remotion/Node, the Kokoro voice model)
3. Place `beat_sheet.json` and `scenes.py` into `youtube/ai-dashboard-insight-benchmark-pitch/` inside the toolkit
4. Apply the one documented font-size fix to `runtime/remotion/src/scenes/ClaudeDefinitions.tsx` (see `BUILD-PROMPT.md`) — without it, Gate T fails on the four-term definitions card
5. Generate narration audio: `python3 runtime/scripts/generate_audio_kokoro.py youtube/ai-dashboard-insight-benchmark-pitch`
6. Render the verified master: `./art final youtube/ai-dashboard-insight-benchmark-pitch --height 2160`
7. The compiled film appears at `renders/ai-dashboard-insight-benchmark-pitch.mp4`

Full prompts and exact commands used are in `BUILD-PROMPT.md`.

## Files in this submission

- `README.md` — this file
- `ai-dashboard-insight-benchmark-pitch.mp4` — the rendered film (the gate-passing final master)
- `PROJECT-BRIEF.md` — the seven required questions, answered
- `beat_sheet.json` — narration and visual plan
- `scenes.py` — custom Manim scene code (two hand-written scenes; all other visuals are parameterized Remotion cards)
- `BUILD-PROMPT.md` — prompts and commands used to build this
- `SOURCES.md` — citations, what I made, what Claude contributed, verified licensing
- `FRICTIONAL.md` — dated log of what was tried, what broke, what changed
- `FACTCHECK.md` — every factual claim in the film, checked against its source
- `SHOTLIST.md` — the typed shot list, updated to match the actual final cards
- `PROMPTS.md` — generation-prompt disclosure (none used; all visuals are code-driven)
- `TYPECHECK.md` — Gate T report (passing)
- `qc-sheet.png`, `layout_audit.md`, `gate-v-report.md` — additional gate reports (all passing)
