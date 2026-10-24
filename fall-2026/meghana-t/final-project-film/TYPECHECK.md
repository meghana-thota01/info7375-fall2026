# TYPECHECK.md — GATE T

Reel: `ai-dashboard-insight-benchmark-pitch`  |  Checked: 2026-10-24T18:35  |  Overall: PASS  |  Beats checked: 13  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B00 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B00B | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04B | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 45px >= floor 41px | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 84px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 9 | 0 |
| min-size §8.1 | 13 | 0 |
| overflow §8.2 | 13 | 0 |
| contrast §8.3 | 13 | 0 |
| contrast-local §8.3b | 13 | 0 |
| bbox-overlap §8.6b | 13 | 0 |
| card-clip §8.13 | 13 | 0 |
| kerning §8.4 | 2 | 0 |
| redundancy §8.10 (advisory) | 7 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
