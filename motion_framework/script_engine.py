"""
The 20-Year Veteran Script Engine for High-Conversion Short-Form Motion Design.
Implements the 3-phase operational blueprint:
1. Phase 1: The Zero-Second Hook Engine (Inverted Truth, In Media Res, Negative Constraint, Sensory Specificity)
2. Phase 2: The Lock-In Phase (Cadence Calibration 3-to-14 words, "And Then" Ban, Open-Loop Stacking, Tactile Verbs)
3. Phase 3: The Payoff and Seamless Infinite Audio Loop (Zero-fluff payoff, legacy outro ban, polarizing dilemma)
"""

import re
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path

from motion_framework.voice import VoiceoverBeatSheet, DEFAULT_VOICE, get_audio_duration


class HookArchetype(str, Enum):
    INVERTED_TRUTH = "inverted_truth"
    IN_MEDIA_RES = "in_media_res"
    NEGATIVE_CONSTRAINT = "negative_constraint"
    SENSORY_MICRO_SPECIFICITY = "sensory_micro_specificity"


class BeatType(str, Enum):
    HOOK = "hook"
    LOCK_IN_PREMISE = "lock_in_premise"
    OPEN_LOOP_VARIABLE = "open_loop_variable"
    PAYOFF = "payoff"
    DILEMMA = "dilemma"
    LOOP_BRIDGE = "loop_bridge"


@dataclass
class ScriptBeat:
    """
    A single beat of spoken dialogue locked with visual Manim choreography.
    Strict rule: Spoken dialogue block MUST NOT exceed 18 words.
    """
    id: str
    text: str
    visual_cue: str  # Bracketed Manim direction e.g. "[Camera pushes on neon red counter at Y=1.5]"
    beat_type: BeatType = BeatType.LOCK_IN_PREMISE
    target_duration_sec: Optional[float] = None

    @property
    def word_count(self) -> int:
        return len(self.text.strip().split())

    def clean_text(self) -> str:
        # Strip any extraneous brackets from spoken text if accidentally placed
        return re.sub(r"\[.*?\]", "", self.text).strip()


@dataclass
class ValidationReport:
    is_valid: bool
    score: float  # 0 to 100
    gate_results: Dict[str, bool]
    violations: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]

    def summary(self) -> str:
        status = "PASSED (10/10 Standard)" if self.is_valid else "FAILED"
        lines = [
            f"=== Veteran Script Validation Audit: {status} (Score: {self.score:.1f}/100) ===",
            "Validation Gates:",
        ]
        for gate, passed in self.gate_results.items():
            icon = "✅" if passed else "❌"
            lines.append(f"  {icon} {gate}: {'PASS' if passed else 'FAIL'}")
        if self.violations:
            lines.append("\nViolations (Hard Fails):")
            for v in self.violations:
                lines.append(f"  🚨 {v}")
        if self.warnings:
            lines.append("\nWarnings:")
            for w in self.warnings:
                lines.append(f"  ⚠️  {w}")
        lines.append(f"\nMetrics: Words={self.metrics.get('word_count')}, Est. Duration={self.metrics.get('est_duration_sec')}s, Words/Sec={self.metrics.get('words_per_sec')}, Cadence StdDev={self.metrics.get('cadence_std_dev'):.2f}")
        return "\n".join(lines)


class ScriptValidator:
    """
    Automated verification engine enforcing the 20-Year Veteran Script standards.
    Guarantees strict compliance against banned patterns, pacing budgets, and cadence.
    """

    # Banned Hook Opening Patterns
    BANNED_HOOK_PATTERNS = [
        (r"^(have you ever wondered|did you ever wonder)", "Rhetorical Question hook opening"),
        (r"^(today,? we(’re| are) going to|in this video|let(’s| us) talk about)", "Topic Announcement hook opening"),
        (r"^(in a world where|with attention spans|throughout history)", "Contextual Throat-Clear opening"),
        (r"^(success is all about|discipline is key|consistency is everything)", "Platitude opening"),
        (r"^(let me tell you about|here is why|here are \d+)", "Generic passive explainer opening"),
    ]

    # Banned Legacy Outro Expressions
    BANNED_OUTRO_PATTERNS = [
        (r"comment below", "Banned legacy CTA: 'comment below'"),
        (r"let me know (what you think|in the comments)", "Banned legacy CTA: 'let me know in comments'"),
        (r"(don't forget to |remember to )?(like( and|,) subscribe)", "Banned legacy CTA: 'like & subscribe'"),
        (r"thanks for watching", "Banned legacy CTA: 'thanks for watching'"),
        (r"see you in the next (one|video)", "Banned legacy CTA: 'see you in the next one'"),
        (r"hit that follow button", "Banned legacy CTA: 'hit that follow button'"),
        (r"share this with", "Banned legacy CTA: 'share this with'"),
    ]

    # Banned Chronological Chaining (The "And Then" Ban)
    BANNED_CHRONOLOGICAL = [
        (r"\band then\b", "Banned chronological linker: 'and then' (Use 'therefore' or 'however')"),
        (r"\bafter that\b", "Banned chronological linker: 'after that'"),
        (r"\bthe next step is\b", "Banned chronological linker: 'the next step is'"),
    ]

    # Banned Hedging / Safe Language
    BANNED_HEDGING = [
        (r"\bmaybe\b", "Hedging language: 'maybe' (State observations as absolute reality)"),
        (r"\bperhaps\b", "Hedging language: 'perhaps'"),
        (r"\boften\b", "Hedging language: 'often'"),
        (r"\busually\b", "Hedging language: 'usually'"),
        (r"\bsomewhat\b", "Hedging language: 'somewhat'"),
        (r"\bcould possibly\b", "Hedging language: 'could possibly'"),
    ]

    @classmethod
    def validate(cls, script: "VeteranScript") -> ValidationReport:
        violations: List[str] = []
        warnings: List[str] = []
        gate_results: Dict[str, bool] = {}

        full_text = " ".join([b.clean_text() for b in script.beats]).lower()
        first_beat = script.beats[0].clean_text() if script.beats else ""
        first_beat_lower = first_beat.lower()
        last_beat = script.beats[-1].clean_text() if script.beats else ""
        last_beat_lower = last_beat.lower()

        # Gate 1: Zero-Second Hook Audit
        gate_1_pass = True
        if first_beat.endswith("?") and not any(k in first_beat_lower for k in ["how", "why"]):
            violations.append(f"Hook ends with question mark: '{first_beat}'. Rhetorical questions are banned.")
            gate_1_pass = False

        for pattern, desc in cls.BANNED_HOOK_PATTERNS:
            if re.search(pattern, first_beat_lower):
                violations.append(f"Hook violates constraint: {desc} -> '{first_beat}'")
                gate_1_pass = False

        if script.beats and script.beats[0].word_count > 16:
            warnings.append(f"Hook contains {script.beats[0].word_count} words; veteran hooks should land within 6-12 words.")

        gate_results["Zero-Second Hook Gate"] = gate_1_pass

        # Gate 2: Legacy Outro Ban Audit
        gate_2_pass = True
        for pattern, desc in cls.BANNED_OUTRO_PATTERNS:
            if re.search(pattern, full_text):
                violations.append(f"Legacy outro detected: {desc}")
                gate_2_pass = False
        gate_results["Legacy Outro Ban Gate"] = gate_2_pass

        # Gate 3: The 'And Then' Ban (Causal Opposition Check)
        gate_3_pass = True
        for pattern, desc in cls.BANNED_CHRONOLOGICAL:
            matches = re.findall(pattern, full_text)
            if matches:
                violations.append(f"Chronological sequencing found: {desc} (count: {len(matches)})")
                gate_3_pass = False
        gate_results["Causal Opposition ('And Then' Ban) Gate"] = gate_3_pass

        # Gate 4: Anti-Hedging (Safe Language Ban)
        gate_4_pass = True
        for pattern, desc in cls.BANNED_HEDGING:
            if re.search(pattern, full_text):
                violations.append(f"Hedging detected: {desc}")
                gate_4_pass = False
        gate_results["Anti-Hedging (Absolute Reality) Gate"] = gate_4_pass

        # Gate 5: 18-Word Monologue Cap & Visual Prompts Presence
        gate_5_pass = True
        for idx, beat in enumerate(script.beats):
            # Check monologue cap
            if beat.word_count > 18:
                violations.append(f"Beat '{beat.id}' exceeds 18-word limit ({beat.word_count} words): '{beat.text}'")
                gate_5_pass = False

            # Check paired visual prompt
            if not beat.visual_cue or not (beat.visual_cue.strip().startswith("[") and beat.visual_cue.strip().endswith("]")):
                violations.append(f"Beat '{beat.id}' missing paired visual cue in brackets '[...]'")
                gate_5_pass = False
        gate_results["18-Word Cap & Visual Cues Gate"] = gate_5_pass

        # Gate 6: Word Count Budget (130-160 words / 60s -> 2.2 to 2.5 words/sec)
        total_words = script.total_words
        est_duration = total_words / 2.35  # target median 2.35 words/sec
        words_per_sec = total_words / est_duration if est_duration > 0 else 0

        gate_6_pass = True
        if total_words > 175:
            violations.append(f"Total word count ({total_words}) exceeds 60s hard budget (max 170). Pacing will be rushed.")
            gate_6_pass = False
        elif total_words < 40 and script.target_duration_sec and script.target_duration_sec > 25:
            warnings.append(f"Word count ({total_words}) is quite brief for target duration.")
        gate_results["Pacing Budget Gate"] = gate_6_pass

        # Gate 7: Cadence Calibration (3-to-14 Word Variance)
        # Verify jagged alternating rhythm rather than monotonous sentence lengths
        sentence_lengths = [b.word_count for b in script.beats]
        if len(sentence_lengths) > 2:
            mean_len = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((x - mean_len) ** 2 for x in sentence_lengths) / len(sentence_lengths)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0.0

        gate_7_pass = True
        if std_dev < 1.5 and len(sentence_lengths) >= 4:
            warnings.append(f"Cadence variation is low (std dev: {std_dev:.2f}). Alternate between punchy (3-6 words) and extended (10-14 words) sentences.")
        gate_results["Cadence Calibration Gate"] = gate_7_pass

        # Gate 8: Infinite Audio Loop or Friction Dilemma
        gate_8_pass = True
        has_loop_bridge = bool(script.loop_bridge_line and script.loop_bridge_line.strip())
        has_dilemma = bool(script.polarizing_dilemma and script.polarizing_dilemma.strip())

        if not has_loop_bridge and not has_dilemma:
            warnings.append("Script lacks an explicit Infinite Audio Loop bridge line or Polarizing Dilemma outro.")
            gate_8_pass = False
        gate_results["Infinite Loop & Dilemma Gate"] = gate_8_pass

        # Calculate final score
        passed_gates = sum(1 for p in gate_results.values() if p)
        base_score = (passed_gates / len(gate_results)) * 100.0
        deductions = len(violations) * 10.0 + len(warnings) * 3.0
        final_score = max(0.0, min(100.0, base_score - deductions if not violations else base_score * 0.75))

        is_valid = len(violations) == 0 and final_score >= 80.0

        metrics = {
            "word_count": total_words,
            "est_duration_sec": round(est_duration, 1),
            "words_per_sec": round(words_per_sec, 2),
            "sentence_lengths": sentence_lengths,
            "cadence_std_dev": round(std_dev, 2),
            "beat_count": len(script.beats),
        }

        return ValidationReport(
            is_valid=is_valid,
            score=final_score,
            gate_results=gate_results,
            violations=violations,
            warnings=warnings,
            metrics=metrics,
        )


@dataclass
class VeteranScript:
    """
    Production-grade script container adhering to the 20-Year Veteran Standard.
    """
    topic: str
    hook_archetype: HookArchetype
    beats: List[ScriptBeat] = field(default_factory=list)
    target_duration_sec: float = 30.0
    loop_bridge_line: Optional[str] = None
    polarizing_dilemma: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    @property
    def total_words(self) -> int:
        return sum(b.word_count for b in self.beats)

    @property
    def estimated_duration_sec(self) -> float:
        # Standard natural delivery: 2.35 words/second
        return round(self.total_words / 2.35, 1)

    def add_beat(self, beat_id: str, text: str, visual_cue: str, beat_type: BeatType = BeatType.LOCK_IN_PREMISE) -> "VeteranScript":
        self.beats.append(ScriptBeat(id=beat_id, text=text, visual_cue=visual_cue, beat_type=beat_type))
        return self

    def validate(self) -> ValidationReport:
        return ScriptValidator.validate(self)

    def to_beat_sheet(self, voice: str = DEFAULT_VOICE, base_dir: str = "media/audio") -> VoiceoverBeatSheet:
        """
        Synthesizes the script beats into Edge TTS neural voiceover files,
        returning an initialized VoiceoverBeatSheet ready for Manim timeline locking.
        """
        sheet = VoiceoverBeatSheet(voice=voice, base_dir=base_dir)
        for beat in self.beats:
            sheet.add_beat(beat.id, beat.clean_text())
        return sheet

    def to_markdown(self) -> str:
        lines = [
            f"# Veteran Script: {self.topic}",
            f"- **Hook Archetype**: `{self.hook_archetype.value}`",
            f"- **Word Count**: {self.total_words} words (Est. Duration: {self.estimated_duration_sec}s)",
            f"- **Target Pacing**: 2.35 words/second",
            "",
            "## Beat Sheet & Visual Choreography",
            "",
        ]
        for b in self.beats:
            lines.append(f"### Beat: `{b.id}` [{b.beat_type.value}] ({b.word_count} words)")
            lines.append(f"**Narration**: \"{b.text}\"")
            lines.append(f"**Visual Cue**: `{b.visual_cue}`")
            lines.append("")

        if self.loop_bridge_line:
            lines.append(f"**Seamless Loop Bridge**: \"{self.loop_bridge_line}\" -> Links back to Hook: \"{self.beats[0].text if self.beats else ''}\"")
            lines.append("")
        if self.polarizing_dilemma:
            lines.append(f"**Polarizing Dilemma**: \"{self.polarizing_dilemma}\"")
            lines.append("")

        return "\n".join(lines)


class VeteranScriptDirector:
    """
    AI Script Director: Generates, guides, and procedurally validates 10/10 veteran scripts.
    """

    @classmethod
    def get_system_prompt_blueprint(cls) -> str:
        """
        Returns the operational prompt to feed any language model to ensure 10/10 script output.
        """
        return """
YOU ARE A 20-YEAR VETERAN SHORT-FORM SCRIPTWRITER & CHIEF MOTION DESIGNER.
You discard all amateur explainer exposition. You write scripts that stop thumbs within 0.5s, lock attention with jagged cadence, and force infinite loops.

PHASE 1: THE ZERO-SECOND HOOK ENGINE (Seconds 0 - 3)
Pick exactly one of these 4 high-conversion veteran archetypes:
1. THE INVERTED TRUTH: Invert a widely held belief violently in <= 6 words.
   Example: "Breakfast isn't the most important meal; it was an ad campaign run in 1944."
2. IN MEDIA RES: Drop directly into the moment of highest consequence. Zero backstory.
   Example: "At 2:14 PM, a junior developer pressed Enter and erased $400 million in six keystrokes."
3. THE NEGATIVE CONSTRAINT: Warn against an everyday action.
   Example: "If you drink coffee before 10 AM, you chemically guarantee a 2 PM crash."
4. SENSORY MICRO-SPECIFICITY: Ultra-specific numbers, textures, mechanical objects.
   Example: "This rusted 1968 steel stopwatch just sold for more than a three-bedroom house in Austin."

BANNED HOOKS:
- Never ask a rhetorical question ("Have you ever wondered...?").
- Never announce the topic ("Today we are going to discuss...").
- Never throat-clear ("In a fast-paced world...").
- Never open with platitudes ("Discipline is everything...").

PHASE 2: THE LOCK-IN PHASE (Seconds 3 - 45)
- CADENCE CALIBRATION: Alternate sentence lengths continuously (3-word to 14-word rule). Monotony kills attention.
- THE "AND THEN" BAN: Never chain chronologically. Chain with causal opposition ("Therefore", "However", "But").
- OPEN-LOOP STACKING: Resolve the initial premise by second 15, then drop an unexpected variable at second 16 that carries to second 45.
- TACTILE VERBS OVER ADJECTIVES: Strip subjective modifiers ("amazingly", "huge"). Use mechanical physical verbs.

PHASE 3: THE PAYOFF & SEAMLESS LOOP (Seconds 45 - 60)
- ZERO-FLUFF PAYOFF: Deliver the final bottom-line revelation cleanly in one punchy sentence. Never summarize what was just said.
- KILL THE LEGACY OUTRO: Strictly ban "like and subscribe", "comment below", "thanks for watching".
- INFINITE AUDIO LOOP: The final spoken line must grammatically or conceptually bridge directly into the opening hook line.
- FRICTION-BASED DILEMMA: If prompting engagement, force a zero-friction binary split dilemma ("Are you taking the 20% pay cut or going back on Monday?").

HARD NEGATIVE CONSTRAINTS:
1. Target Word Count: 130 - 160 words per 60s (~2.2 to 2.5 words/sec). For 20-30s shorts, 50 - 75 words.
2. Visual Prompts: Every single beat MUST have a paired visual cue in brackets [like this] specifying Manim motion/layout.
3. No Monologues: Spoken blocks cannot exceed 18 words without an edit or visual cut.
4. No Safe Language: Zero hedging ("maybe", "perhaps", "usually", "often"). Everything is absolute, immediate reality.
"""

    @classmethod
    def craft_knight_capital_script(cls) -> VeteranScript:
        """
        Reference 10/10 Veteran Script on the Knight Capital $400M algorithmic disaster.
        Archetype: IN_MEDIA_RES
        """
        script = VeteranScript(
            topic="The $400 Million Keystroke",
            hook_archetype=HookArchetype.IN_MEDIA_RES,
            target_duration_sec=25.0,
            loop_bridge_line="...all triggered when...",
            polarizing_dilemma="Would you keep your money in an algorithm you didn't personally audit?",
        )
        script.add_beat(
            beat_id="beat_hook",
            text="At 9:30 AM, an untested script went live on Wall Street.",
            visual_cue="[Camera snaps to high-contrast obsidian clock flashing 09:30:00 with red glitch border]",
            beat_type=BeatType.HOOK,
        )
        script.add_beat(
            beat_id="beat_consequence",
            text="In forty-five minutes, it executed four million accidental trades.",
            visual_cue="[Rapid rolling counter surges from 0 to 4,000,000 with blazing cyan data wires]",
            beat_type=BeatType.LOCK_IN_PREMISE,
        )
        script.add_beat(
            beat_id="beat_cadence_short",
            text="Total carnage.",
            visual_cue="[Monochrome flash. Screen desaturates to matte graphite]",
            beat_type=BeatType.LOCK_IN_PREMISE,
        )
        script.add_beat(
            beat_id="beat_variable",
            text="However, the server wasn't hacked. An engineer simply forgot one deployment flag.",
            visual_cue="[Bento Card splits open revealing glowing terminal line with missing boolean parameter]",
            beat_type=BeatType.OPEN_LOOP_VARIABLE,
        )
        script.add_beat(
            beat_id="beat_payoff",
            text="Four hundred and forty million dollars evaporated. Knight Capital ceased to exist.",
            visual_cue="[Radial efficiency ring plummets from 100% to 0% with seismic camera shake]",
            beat_type=BeatType.PAYOFF,
        )
        script.add_beat(
            beat_id="beat_loop",
            text="And that catastrophic wipeout...",
            visual_cue="[Camera tracks inward toward black void origin point]",
            beat_type=BeatType.LOOP_BRIDGE,
        )
        return script

    @classmethod
    def craft_coffee_adenosine_script(cls) -> VeteranScript:
        """
        Reference 10/10 Veteran Script on morning coffee timing.
        Archetype: NEGATIVE_CONSTRAINT
        """
        script = VeteranScript(
            topic="Why Morning Coffee Before 10 AM Backfires",
            hook_archetype=HookArchetype.NEGATIVE_CONSTRAINT,
            target_duration_sec=24.0,
            loop_bridge_line="...which is guaranteed whenever...",
            polarizing_dilemma="Are you waiting 90 minutes tomorrow, or drinking your espresso the moment you wake up?",
        )
        script.add_beat(
            beat_id="beat_hook",
            text="Drinking coffee before 10 AM chemically guarantees your 2 PM brain fog.",
            visual_cue="[High-contrast split card: Golden mug on left vs Red battery depleted at 14:00 on right]",
            beat_type=BeatType.HOOK,
        )
        script.add_beat(
            beat_id="beat_mechanism",
            text="When you wake up, your brain is drowning in residual adenosine.",
            visual_cue="[Vector neural mesh fills with floating dark violet molecules]",
            beat_type=BeatType.LOCK_IN_PREMISE,
        )
        script.add_beat(
            beat_id="beat_cadence_short",
            text="Caffeine doesn't clear it.",
            visual_cue="[Sharp red barrier snaps down across receptor node]",
            beat_type=BeatType.LOCK_IN_PREMISE,
        )
        script.add_beat(
            beat_id="beat_variable",
            text="Therefore, it only plugs the receptor until noon, when the dam breaks.",
            visual_cue="[Barricade cracks under accumulated violet particle pressure]",
            beat_type=BeatType.OPEN_LOOP_VARIABLE,
        )
        script.add_beat(
            beat_id="beat_payoff",
            text="Delay your first cup ninety minutes, and the fog vanishes.",
            visual_cue="[Metric counter sets to +90m; violet particles dissolve into clean emerald glow]",
            beat_type=BeatType.PAYOFF,
        )
        script.add_beat(
            beat_id="beat_loop",
            text="Preventing the afternoon crash...",
            visual_cue="[Cyan glow contracts back to central circular silhouette]",
            beat_type=BeatType.LOOP_BRIDGE,
        )
        return script
