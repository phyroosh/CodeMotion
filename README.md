# CodeMotion ⚡

**CodeMotion** is an autonomous, industry-level motion design engine built with **Manim Community Edition** and **Python**. It crafts high-conversion, minimalist 2D vector animations, kinetic typography, and data-in-motion with frame-accurate neural voiceover synchronization.

---

## 🎨 Visual Philosophy

CodeMotion replaces academic blackboard slides with modern digital design inspired by **Linear**, **Stripe**, **Apple Keynotes**, and top-tier studios like **Buck** and **Kurzgesagt**:

- **Minimalist 2D Vector Animation**: Deep obsidian/graphite canvases (`#0A0B0E`), hairline strokes (`1.5px`), rounded Bento containers (`corner_radius=0.16`), and micro-dot matrix backgrounds.
- **Kinetic Typography**: Modern grotesque sans-serif (`Inter`, `Inter Display`), strict typographic scale contrast, tracked uppercase category tags, and staggered word-by-word reveals.
- **Data-in-Motion**: Continuous rolling metric counters (`ValueTracker`), live radial dial meters, reactive topological mesh networks, and glowing Bezier data streams (`ShowPassingFlash`).
- **Physical Easing**: Strict ban on robotic linear interpolation; tactile rate functions (`ease_out_cubic`, `snappy_overshoot` spring physics, `fast_out_slow_in`).

---

## 🧠 The 20-Year Veteran Script Engine

Every video starts with high-tension, zero-fluff storytelling built on a 3-phase veteran blueprint:

1. **Phase 1: The Zero-Second Hook Engine (Seconds 0 – 3)**:
   - Halts scroll momentum with immediate cognitive friction.
   - 4 High-Conversion Archetypes: `Inverted Truth`, `In Media Res`, `Negative Constraint`, and `Sensory Micro-Specificity`.
   - **Banned**: Rhetorical questions (`?`), topic announcements, contextual throat-clearing, and platitudes.
2. **Phase 2: The Lock-In Phase (Seconds 3 – 45)**:
   - **Cadence Calibration**: 3-to-14 word rule with jagged alternating sentence lengths.
   - **The "And Then" Ban**: Replaces chronological sequencing with causal opposition (`Therefore`, `However`).
   - **Open-Loop Stacking**: Resolves the premise by second 15, introducing an unexpected variable at second 16.
   - **Tactile Verbs**: Mechanical verbs carry weight over subjective adverbs.
3. **Phase 3: The Payoff and Seamless Infinite Audio Loop**:
   - Zero-fluff payoff without legacy outro fluff (*"like & subscribe"* is strictly banned).
   - Infinite Audio Loop bridge where the final spoken line syntactically connects straight back into the opening hook.
   - Optional polarizing binary dilemma for comment section engagement.

### 🛡️ Automated 8-Gate Script Verification (`ScriptValidator`)
Mechanically tests scripts across 8 gates before synthesizing voiceover or generating Manim scenes:
- Zero-Second Hook Gate
- Legacy Outro Ban Gate
- Causal Opposition Gate
- Anti-Hedging Gate
- 18-Word Monologue Cap & Visual Cues Gate
- Pacing Budget Gate (130–160 words / 60s; 2.2–2.5 words/sec)
- Cadence Calibration Gate ($\sigma > 1.5$)
- Infinite Loop & Dilemma Gate

---

## 🎙️ Microsoft Edge Neural Voice Over

Narration is driven by **Microsoft Edge Neural Voice**, defaulting to:
- **Primary Default**: **`en-US-AvaMultilingualNeural`** (Expressive, clear, warm, modern explainer voice).
- **Alternative (Documentary)**: `en-US-ChristopherNeural`.
- **Alternative (Conversational SaaS)**: `en-US-AndrewMultilingualNeural`.

Animations never guess durations at random—spoken audio clip lengths are measured with millisecond precision to drive visual play and wait durations. Final MP4 and AAC audio are muxed losslessly via FFmpeg.

---

## 📱 Short-Form Architecture (9:16 Vertical)

Engineered for YouTube Shorts, Instagram Reels, and TikTok:
- **Canvas Resolution**: `720x1280` (preview) or `1080x1920` (master), `frame_width=9.0`, `frame_height=16.0`.
- **Mobile Safe Zones**: Keeps all critical graphics within $Y \in [-4.5, 5.2]$ to avoid top app headers, bottom subtitle discs, and the right interactive rail.
- **Vertical Bento Stack**: Categorical pill badge at $Y = 4.6$, Top Hero Card at $Y = 1.6$, Bottom Data Card at $Y = -2.8$.

---

## 🖼️ Frontier T: Thumbnail Intelligence

Ported directly from companion project **RightClips**, Frontier T creates click-worthy thumbnails through creative direction and automated optical validation:
- **Complexity Budget**: Strictly **1 to 3 punch words** in massive typography (bans pill badges, subtitle cards, and clutter).
- **Level 1 Silhouette**: 60% visual weight given to one unmistakable focal hero with minimum 7:1 luminance contrast.
- **Mobile Survival Test**: Downscales to a 360x640 mobile preview to verify RMS contrast ($> 30.0$).
- **Gaussian Blur Squint Test**: Applies 10px blur simulation to evaluate feed scroll retention ($> 22.0$).

---

## 🚀 Autonomous Publishing & RightClips Studio Bridge

1. **Autonomous Metadata**: Generates high-CTR title, structured description with hashtags, algorithmic tags, and pinned comment.
2. **RightClips Bridge**: Automatically exports final MP4 and certified Frontier T thumbnail to `/home/phyroosh/TopProducts/RightClips/out/` and registers metadata in `RightClips/studio/metadata.json` for 1-click publishing.
3. **Standalone Direct YouTube API**: Direct upload via YouTube Data API v3 (`motion_framework.publisher`).

---

## 📂 Project Structure

```
CodeMotion/
├── SKILL.md                  # Master AI agent instruction manual & design tokens
├── .agent/skills/            # Native AI skill discovery mirror
├── motion_framework/         # Core Python framework
│   ├── theme.py              # Dark-mode palettes (OnyxCyber, ObsidianEmerald, SolarGraphite)
│   ├── easings.py            # Custom tactile rate functions & spring curves
│   ├── components.py         # BentoCard, MetricCounter, KineticText, DataWire, RadialMeter
│   ├── script_engine.py      # 20-Year Veteran Script Engine & 8-Gate Validator
│   ├── voice.py              # Edge TTS integration (en-US-AvaMultilingualNeural) & FFmpeg muxer
│   ├── frontier_t.py         # Thumbnail intelligence director & optical multi-scale validator
│   ├── metadata.py           # YouTube Shorts autonomous metadata synthesizer
│   ├── exporter.py           # RightClips Studio automated export bridge
│   └── publisher.py          # Direct YouTube Data API v3 publisher
├── examples/
│   ├── showcase.py           # 16:9 Landscape master showcase
│   ├── short_explainer.py    # 9:16 Vertical explainer with voiceover & RightClips export
│   ├── test_frontier_t.py    # Frontier T optical verification suite
│   └── test_script_engine.py # Veteran script engine & Edge TTS verification
└── pyproject.toml            # Project configuration & uv dependencies
```

---

## ⚡ Quickstart & Usage

### 1. Installation
This project uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic dependency management:

```bash
# Clone the repository
git clone https://github.com/phyroosh/CodeMotion.git
cd CodeMotion

# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 2. Run Test & Verification Suites
```bash
# Verify the 20-Year Veteran Script Engine & Edge TTS audio synthesis
uv run python examples/test_script_engine.py

# Verify Frontier T Thumbnail Intelligence & Optical Multi-Scale Validation
uv run python examples/test_frontier_t.py
```

### 3. Render Videos
```bash
# Full 9:16 Short Explainer (Script + Voiceover + Render + Mux + RightClips Export)
uv run python examples/short_explainer.py

# Landscape 16:9 Showcase Preview (720p 30fps)
uv run manim -pqm examples/showcase.py ShowcaseScene

# Production 1080p 60fps Master Render
uv run manim -pqh --fps 60 examples/showcase.py ShowcaseScene
```

---

## 📄 License
MIT License. Crafted with precision for high-impact visual storytelling.
