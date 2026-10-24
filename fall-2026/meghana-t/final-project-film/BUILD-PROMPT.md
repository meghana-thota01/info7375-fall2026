# BUILD-PROMPT.md

Exact commands and prompts used to build this film, in order.

## 1. Setup

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
./setup --install
```

If `pycairo`/`manim` fail to install (common on macOS without Homebrew's cairo), run:

```bash
brew install cairo pkg-config pango
pip install kokoro-onnx
pip install -r requirements.txt
```

If npm reports a cache permissions error:

```bash
sudo chown -R 501:20 "$HOME/.npm"
cd runtime/remotion && npm install && cd ../..
```

## 2. Place project files

Put `beat_sheet.json` and `scenes.py` (both included in this submission) into:

```
youtube/ai-dashboard-insight-benchmark-pitch/
```

Also place `FACTCHECK.md`, `SHOTLIST.md`, and `PROMPTS.md` (included) in the same folder — Gate F in the toolkit refuses to render without this paperwork present.

## 3. Generate narration (audio is the master clock)

```bash
python3 runtime/scripts/generate_audio_kokoro.py youtube/ai-dashboard-insight-benchmark-pitch
```

This writes real measured durations (`actual_duration_s`) back into `beat_sheet.json`. If you edit any narration text, re-run this before rendering, then re-sync each card's `durationSeconds` prop to match the new `actual_duration_s` (plus a ~0.3s tail) — mismatched durations cause mid-sentence cuts and awkward long holds.

## 4. Render the verified master

```bash
./art final youtube/ai-dashboard-insight-benchmark-pitch --height 2160
```

Output: `renders/ai-dashboard-insight-benchmark-pitch.mp4` — this is the gate-passing final cut actually submitted (it also removes the corner debug labels that `./art run`'s review cut always carries).

Gate reports are written to `TYPECHECK.md`, `layout_audit.md`, and `qc-sheet.png` inside `youtube/ai-dashboard-insight-benchmark-pitch/`.

If you only want a quick review cut while iterating (not the final submission), `./art run youtube/ai-dashboard-insight-benchmark-pitch --height 2160 --force` produces a faster `-slate.mp4` preview in the same project folder, but it keeps the corner labels and does not run Gate T.

## 5. The Manim scene

One beat (`B06`) uses hand-written Manim code instead of a parameterized card, since it's a personal reflection, not an interface/number/word (per the toolkit's own "card test"). It's built entirely from the toolkit's documented `iso_kit.py` writing-kit primitives:

```python
class B06_ResumeGap(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        page = paper(-1.4, 0.2, w=3.4, h=3.8)
        self.play(FadeIn(page), run_time=0.6)
        existing = scribble_block(page.cx - 1.3, page.cy + 1.3, 2.6, n=3, gap=0.55)
        self.play(Create(existing), run_time=1.3)
        q = quill(page.cx - 1.3, page.cy - 1.1, s=0.85)
        self.play(FadeIn(q), run_time=0.5)
        new_line = scribble(page.cx - 1.3, page.cy - 1.5, 2.3)
        write_lines(self, q, [new_line])
        mark = Dot(new_line.get_end(), radius=0.09, color=TERRA)
        self.play(FadeIn(mark), run_time=0.4)
        label = T("the one line missing", size=32, color=INK).next_to(page, RIGHT, buff=0.7)
        self.play(Write(label), run_time=0.9)
        finish(self)
```

## 6. The outro scene

A custom title card was used instead of the toolkit's default `ClaudeTitleOutro`, since that component is hardcoded to the `@NikBearBrown` channel handle and cannot be used for a personal, non-branded submission:

```python
class BOUT_TitleCard(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        title = T("AI Dashboard Insight Benchmark", size=52, bold=True).move_to(ORIGIN + UP * 0.3)
        name = T("Meghana Thota", size=36, color=DIM).next_to(title, DOWN, buff=0.6)
        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(name), run_time=0.3)
        underline = Line(name.get_left() + DOWN * 0.25, name.get_right() + DOWN * 0.25, color=TERRA, stroke_width=3)
        self.play(Create(underline), run_time=0.2)
        finish(self)
```

## Required font-size fix (for Gate T)

The toolkit's `ClaudeDefinitions` component has no prop controlling its term/definition text size. At four terms, its default sizes (50px/48px) failed Gate T's 41px minimum. Fixed with this one-line edit (the `sed -i ''` syntax below is macOS-specific; on Linux, drop the empty quotes: `sed -i 's/.../.../' file`):

```bash
sed -i '' 's/const termSize = n <= 3 ? 54 : 50;/const termSize = n <= 3 ? 56 : 56;/' runtime/remotion/src/scenes/ClaudeDefinitions.tsx
sed -i '' 's/const meanSize = 48;/const meanSize = 54;/' runtime/remotion/src/scenes/ClaudeDefinitions.tsx
```

## Key prompts used with Claude during development

These are paraphrased summaries of the actual back-and-forth, not verbatim quotes of either side:

- *(paraphrased)* Help design the seven pitch answers for a benchmark project comparing two AI models on dashboard-insight generation, with planted ground truth and a reliability check.
- *(paraphrased)* Check every factual claim in this brief against a live source before using it — don't assume from memory.
- *(paraphrased)* The rendered cards are showing placeholder content instead of my real data — find the actual component source and tell me what props it really reads.
- *(paraphrased)* Write one Manim scene for a personal reflection beat, using the toolkit's own documented writing-kit functions, not generic primitives.
- *(paraphrased)* The narration uses present tense for work that hasn't happened yet — rewrite every line to use correct tense per the assignment's honesty rule, and fold in the three required questions missing from the film.
