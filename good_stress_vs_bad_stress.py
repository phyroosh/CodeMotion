"""
Good Stress vs Bad Stress (Eustress vs Distress)
9:16 Vertical Short-Form Motion Design Video for YouTube Shorts / Instagram Reels.
Powered by Manim Community Edition, Microsoft Edge Neural Voice, and modern kinetic motion design.
"""

import sys
from pathlib import Path
from manim import *
import numpy as np

# Framework imports
from motion_framework.theme import Palette, TYPOGRAPHY, LAYOUT
from motion_framework.easings import snappy_overshoot, ease_out_cubic, ease_in_out_cubic, smooth_drift
from motion_framework.components import (
    BentoCard,
    MetricCounter,
    KineticText,
    PulsingNode,
    RadialMeter,
    create_grid_background,
)
from motion_framework.voice import (
    DEFAULT_VOICE,
    VoiceoverBeatSheet,
    mux_video_audio,
)

# -----------------------------------------------------------------------------
# 1. COLOR PALETTE: NEURO DUAL-TONE (Eustress Mint vs Distress Coral)
# -----------------------------------------------------------------------------
NeuroTheme = Palette(
    name="Neuro Dual-Tone",
    bg="#090A0F",             # Deep Slate Void
    card_bg="#121522",        # Glassy Slate Card
    card_border="#1E2538",    # Hairline Border
    accent_primary="#00FFA3", # High-Voltage Mint (Eustress / Flow State)
    accent_secondary="#FF4757",# Neon Coral (Distress / Alarm / Burnout)
    accent_glow="#00E5FF",    # Electric Cyan (Focus / Arousal)
    text_primary="#F8FAFC",   # Crisp Off-White
    text_muted="#94A3B8",     # Slate Muted
    text_subtle="#475569",    # Deep Slate
)

# -----------------------------------------------------------------------------
# 2. VOICE SYNTHESIS & TIMING LOCK
# -----------------------------------------------------------------------------
AUDIO_DIR = "media/audio/stress_explainer"
MASTER_AUDIO = f"{AUDIO_DIR}/master_voice.mp3"

# Beat Sheet timings from Edge Neural Voice (Ava)
voice_sheet = VoiceoverBeatSheet(voice="en-US-AvaMultilingualNeural", base_dir=AUDIO_DIR)
DUR_1_HOOK = voice_sheet.add_beat(
    "beat_1_hook",
    "Stress isn't your enemy. Without it, your brain lacks the biological trigger to focus, adapt, or perform."
)
DUR_2_EUSTRESS = voice_sheet.add_beat(
    "beat_2_eustress",
    "This is the Yerkes-Dodson Law. Up to an optimal threshold, acute stress—or Eustress—fuels peak cognitive focus and flow state."
)
DUR_3_DISTRESS = voice_sheet.add_beat(
    "beat_3_distress",
    "Cross that threshold without recovery, and it turns into Distress: chronic cortisol flood, heart rate spikes, and cognitive burnout."
)
DUR_4_SYNTHESIS = voice_sheet.add_beat(
    "beat_4_synthesis",
    "The secret isn't eliminating pressure. It's balancing acute intensity with deep, deliberate recovery."
)
voice_sheet.build_master_track(MASTER_AUDIO)

print(f"Loaded Voiceover: Beat 1={DUR_1_HOOK:.2f}s | Beat 2={DUR_2_EUSTRESS:.2f}s | Beat 3={DUR_3_DISTRESS:.2f}s | Beat 4={DUR_4_SYNTHESIS:.2f}s")


# -----------------------------------------------------------------------------
# 3. CUSTOM MOTION COMPONENTS
# -----------------------------------------------------------------------------
def create_topic_pill(text: str, color: str = NeuroTheme.accent_primary) -> VGroup:
    """Creates a high-end tracked uppercase category pill."""
    lbl = Text(
        text.upper(),
        font=TYPOGRAPHY["font"],
        font_size=11,
        weight=BOLD,
        color=color,
    )
    box = RoundedRectangle(
        width=lbl.width + 0.36,
        height=lbl.height + 0.22,
        corner_radius=0.08,
        fill_color=color,
        fill_opacity=0.14,
        stroke_color=color,
        stroke_width=1.1,
        stroke_opacity=0.6,
    )
    return VGroup(box, lbl)


class YerkesDodsonCurve(VGroup):
    """
    Parametric Inverted-U Bell Curve representing Performance vs Stress / Arousal.
    Includes baseline axis, optimal zone gradient highlight, and tracer dot.
    """
    def __init__(self, width: float = 6.2, height: float = 2.8, **kwargs):
        super().__init__(**kwargs)
        self.curve_w = width
        self.curve_h = height

        # Horizontal baseline axis
        self.axis_line = Line(
            LEFT * (width / 2),
            RIGHT * (width / 2),
            stroke_color=NeuroTheme.card_border,
            stroke_width=1.5,
            stroke_opacity=0.7,
        )

        # Baseline ticks & labels
        low_lbl = Text("LOW AROUSAL", font=TYPOGRAPHY["font"], font_size=9, color=NeuroTheme.text_subtle, weight=BOLD)
        low_lbl.move_to(self.axis_line.get_left() + DOWN * 0.25 + RIGHT * 0.6)
        
        opt_lbl = Text("OPTIMAL ZONE", font=TYPOGRAPHY["font"], font_size=9, color=NeuroTheme.accent_primary, weight=BOLD)
        opt_lbl.move_to(self.axis_line.get_center() + DOWN * 0.25)

        high_lbl = Text("EXHAUSTION", font=TYPOGRAPHY["font"], font_size=9, color=NeuroTheme.accent_secondary, weight=BOLD)
        high_lbl.move_to(self.axis_line.get_right() + DOWN * 0.25 + LEFT * 0.6)

        self.labels = VGroup(low_lbl, opt_lbl, high_lbl)

        # Parametric Bell Curve: y = height * exp(- (x)^2 / (2 * sigma^2))
        x_min, x_max = -width / 2 + 0.2, width / 2 - 0.2
        sigma = width / 4.4
        
        def bell_point(t):
            x = x_min + t * (x_max - x_min)
            raw_y = np.exp(-(x**2) / (2 * sigma**2))
            base_val = np.exp(-((width/2)**2) / (2 * sigma**2))
            y = self.curve_h * (raw_y - base_val) / (1.0 - base_val)
            return np.array([x, y, 0])

        # Sample points for curve
        pts = [bell_point(t) for t in np.linspace(0, 1, 60)]
        self.curve = VMobject()
        self.curve.set_points_smoothly(pts)
        self.curve.set_stroke(
            color=NeuroTheme.accent_glow,
            width=2.8,
            opacity=0.9,
        )

        # Peak marker line
        peak_pt = bell_point(0.5)
        self.peak_pt = peak_pt
        self.peak_line = DashedLine(
            np.array([0, 0, 0]),
            peak_pt,
            dash_length=0.08,
            stroke_color=NeuroTheme.accent_primary,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )

        # Tracer dot for animation along the curve
        self.tracer = PulsingNode(radius=0.14, core_color=NeuroTheme.accent_primary)
        self.tracer.move_to(pts[0])

        self.add(self.axis_line, self.labels, self.peak_line, self.curve, self.tracer)


class CoherentWaveform(VMobject):
    """Smooth rhythmic harmonic wave indicating regulated acute arousal (Eustress)."""
    def __init__(self, width: float = 6.2, amplitude: float = 0.35, freq: float = 3.0, color=NeuroTheme.accent_primary, **kwargs):
        super().__init__(**kwargs)
        pts = []
        for x in np.linspace(-width / 2, width / 2, 70):
            y = amplitude * np.sin(x * freq)
            pts.append(np.array([x, y, 0]))
        self.set_points_smoothly(pts)
        self.set_stroke(color=color, width=2.4, opacity=0.85)


class ErraticWaveform(VMobject):
    """Jagged, erratic waveform with sharp abnormal spikes indicating chronic distress."""
    def __init__(self, width: float = 6.2, color=NeuroTheme.accent_secondary, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(42)
        pts = []
        xs = np.linspace(-width / 2, width / 2, 60)
        for i, x in enumerate(xs):
            if 15 <= i <= 22 or 38 <= i <= 46:
                y = 0.55 * np.sin(x * 12.0) + (0.35 if i % 2 == 0 else -0.35)
            else:
                y = 0.12 * np.sin(x * 4.0) + np.random.uniform(-0.06, 0.06)
            pts.append(np.array([x, y, 0]))
        self.set_points_as_corners(pts)
        self.set_stroke(color=color, width=2.4, opacity=0.9)


# -----------------------------------------------------------------------------
# 4. MAIN MANIM SCENE (9:16 VERTICAL ARCHITECTURE)
# -----------------------------------------------------------------------------
class GoodStressVsBadStressScene(MovingCameraScene):
    def construct(self):
        # 0. Setup Canvas & Ambient Background
        self.camera.background_color = NeuroTheme.bg
        grid = create_grid_background(
            width=10,
            height=18,
            step=1.2,
            dot_color=NeuroTheme.card_border,
            dot_radius=0.018,
            opacity=0.22,
        )
        self.add(grid)

        # =====================================================================
        # BEAT 1: THE HOOK (0:00 - 0:07.63s)
        # "Stress isn't your enemy. Without it, your brain lacks the biological trigger to focus, adapt, or perform."
        # =====================================================================
        topic_pill = create_topic_pill("NEURO-BIOLOGY", NeuroTheme.accent_primary).move_to(UP * 4.8)

        hook_line1 = KineticText(
            "STRESS IS NOT",
            font=TYPOGRAPHY["font"],
            font_size=40,
            color=NeuroTheme.text_primary,
            weight=BOLD,
        ).move_to(UP * 3.4)

        hook_line2 = KineticText(
            "YOUR ENEMY",
            font=TYPOGRAPHY["font"],
            font_size=44,
            color=NeuroTheme.accent_primary,
            weight=BOLD,
        ).move_to(UP * 2.6)

        hook_sub = Text(
            "Without acute activation, the brain cannot focus or adapt",
            font=TYPOGRAPHY["font"],
            font_size=15,
            color=NeuroTheme.text_muted,
        ).move_to(UP * 1.8)

        # Central Biometric Activation Bento Card
        card_hero = BentoCard(
            width=7.6,
            height=4.8,
            badge_text="BIOLOGICAL READINESS",
            badge_color=NeuroTheme.accent_glow,
        ).move_to(DOWN * 1.2)

        # Internal Bio-Core in Card
        bio_core = PulsingNode(radius=0.32, core_color=NeuroTheme.accent_glow).move_to(card_hero.get_center() + UP * 0.4)
        
        # Dual Orbit Rings around Core
        ring_1 = Circle(radius=0.85, stroke_color=NeuroTheme.accent_glow, stroke_width=1.0, stroke_opacity=0.35).move_to(bio_core.get_center())
        ring_2 = Circle(radius=1.35, stroke_color=NeuroTheme.card_border, stroke_width=1.0, stroke_opacity=0.45).move_to(bio_core.get_center())
        
        # Live Metric Counter inside Card
        readiness_counter = MetricCounter(
            start_val=0,
            end_val=88,
            suffix="%",
            prefix="READINESS: ",
            decimals=0,
            font_size=24,
            color=NeuroTheme.accent_primary,
        ).move_to(card_hero.get_center() + DOWN * 1.4)

        # Animation Beat 1 Entrance
        self.play(
            FadeIn(topic_pill, shift=DOWN * 0.25, rate_func=ease_out_cubic),
            hook_line1.reveal_animation(lag_ratio=0.08, duration=0.7),
            hook_line2.reveal_animation(lag_ratio=0.08, duration=0.8),
            FadeIn(hook_sub, shift=UP * 0.15, rate_func=ease_out_cubic),
            FadeIn(card_hero, shift=UP * 0.4, rate_func=snappy_overshoot(0.08)),
            FadeIn(bio_core, shift=UP * 0.2),
            Create(ring_1),
            Create(ring_2),
            FadeIn(readiness_counter),
            run_time=1.8,
        )

        # Active Data-in-Motion Counter & Ambient Pulse during Voiceover
        beat1_remaining = max(1.0, DUR_1_HOOK - 1.8)
        self.play(
            readiness_counter.count_to(target=88, duration=beat1_remaining * 0.7),
            bio_core.halo.animate(rate_func=ease_in_out_cubic).scale(1.4).set_opacity(0.18),
            ring_1.animate.rotate(PI / 2),
            ring_2.animate.rotate(-PI / 3),
            run_time=beat1_remaining,
        )

        # =====================================================================
        # BEAT 2: THE MECHANISM — YERKES-DODSON LAW & EUSTRESS (DUR_2_EUSTRESS = ~9.50s)
        # "This is the Yerkes-Dodson Law. Up to an optimal threshold, acute stress—or Eustress—fuels peak cognitive focus and flow state."
        # =====================================================================
        pill_beat2 = create_topic_pill("YERKES-DODSON LAW", NeuroTheme.accent_primary).move_to(UP * 4.8)

        headline_beat2 = KineticText(
            "THE SWEET SPOT",
            font=TYPOGRAPHY["font"],
            font_size=42,
            color=NeuroTheme.accent_primary,
            weight=BOLD,
        ).move_to(UP * 3.4)

        sub_beat2 = Text(
            "Optimal acute arousal maximizes cognitive throughput",
            font=TYPOGRAPHY["font"],
            font_size=15,
            color=NeuroTheme.text_muted,
        ).move_to(UP * 2.6)

        # New Bento Card for Curve with generous breathing room
        curve_card = BentoCard(
            width=7.6,
            height=6.2,
            badge_text="HUMAN PERFORMANCE CURVE",
            badge_color=NeuroTheme.accent_primary,
        ).move_to(DOWN * 1.1)

        # Build Bell Curve with controlled height (height=1.9)
        curve_viz = YerkesDodsonCurve(width=5.8, height=1.9).move_to(curve_card.get_center() + DOWN * 0.7)

        # Performance metric positioned cleanly at top of card
        flow_metric = MetricCounter(
            start_val=22,
            end_val=98,
            suffix="%",
            prefix="FLOW STATE: ",
            decimals=0,
            font_size=23,
            color=NeuroTheme.accent_primary,
        ).move_to(curve_card.get_center() + UP * 2.3)

        peak_badge = Text(
            "EUSTRESS (PEAK COGNITION)",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=NeuroTheme.accent_primary,
        ).move_to(curve_card.get_center() + UP * 1.7)

        # Execute smooth morphing transition (60/40 overlap)
        self.play(
            ReplacementTransform(topic_pill, pill_beat2),
            FadeOut(hook_line1, shift=UP * 0.4),
            FadeOut(hook_line2, shift=UP * 0.3),
            FadeOut(hook_sub, shift=UP * 0.2),
            FadeOut(bio_core),
            FadeOut(ring_1),
            FadeOut(ring_2),
            FadeOut(readiness_counter),
            ReplacementTransform(card_hero, curve_card),
            FadeIn(headline_beat2, shift=DOWN * 0.2),
            FadeIn(sub_beat2, shift=UP * 0.1),
            run_time=0.9,
        )

        # Draw the curve and reveal labels
        self.play(
            Create(curve_viz.axis_line),
            FadeIn(curve_viz.labels, shift=UP * 0.1),
            Create(curve_viz.curve, run_time=1.4),
            FadeIn(flow_metric),
            run_time=1.5,
        )

        climb_time = min(3.8, DUR_2_EUSTRESS * 0.45)
        self.play(
            flow_metric.count_to(target=98, duration=climb_time),
            curve_viz.tracer.animate(rate_func=ease_out_cubic).move_to(curve_viz.peak_pt + curve_viz.get_center()),
            Create(curve_viz.peak_line),
            FadeIn(peak_badge, shift=UP * 0.15, rate_func=snappy_overshoot(0.1)),
            run_time=climb_time,
        )

        # Ambient hold at peak: glowing pulse and camera slight push
        beat2_remaining = max(1.0, DUR_2_EUSTRESS - (0.9 + 1.5 + climb_time))
        self.play(
            curve_viz.tracer.halo.animate(rate_func=ease_in_out_cubic).scale(1.5).set_opacity(0.2),
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(0.98),
            run_time=beat2_remaining,
        )

        # =====================================================================
        # BEAT 3: THE TIPPING POINT & DISTRESS (DUR_3_DISTRESS = ~8.33s)
        # "Cross that threshold without recovery, and it turns into Distress: chronic cortisol flood, heart rate spikes, and cognitive burnout."
        # =====================================================================
        pill_beat3 = create_topic_pill("CHRONIC OVERLOAD", NeuroTheme.accent_secondary).move_to(UP * 4.8)

        headline_beat3 = KineticText(
            "THE BURNOUT CRASH",
            font=TYPOGRAPHY["font"],
            font_size=40,
            color=NeuroTheme.accent_secondary,
            weight=BOLD,
        ).move_to(UP * 3.4)

        sub_beat3 = Text(
            "Unrecovered stress causes neuro-endocrine exhaustion",
            font=TYPOGRAPHY["font"],
            font_size=15,
            color=NeuroTheme.text_muted,
        ).move_to(UP * 2.6)

        # Plunge tracer off the right cliff
        right_crash_pt = curve_viz.axis_line.get_right() + UP * 0.25
        
        # Split Bento Comparison Cards:
        # Top: EUSTRESS (Coherent Rhythmic Wave)
        eustress_card = BentoCard(
            width=7.6,
            height=3.1,
            badge_text="EUSTRESS (ACUTE + RECOVERED)",
            badge_color=NeuroTheme.accent_primary,
        ).move_to(UP * 0.9)

        wave_eustress = CoherentWaveform(width=5.8, amplitude=0.28, freq=3.2, color=NeuroTheme.accent_primary).move_to(eustress_card.get_center() + DOWN * 0.15)
        eustress_sub = Text("Coherent Vagal Rhythm • Growth Signaled", font=TYPOGRAPHY["font"], font_size=12, color=NeuroTheme.text_muted).move_to(eustress_card.get_center() + DOWN * 0.95)

        # Bottom: DISTRESS (Erratic Cortisol Surge)
        distress_card = BentoCard(
            width=7.6,
            height=3.6,
            badge_text="DISTRESS (CHRONIC / UNCHECKED)",
            badge_color=NeuroTheme.accent_secondary,
        ).move_to(DOWN * 2.7)

        wave_distress = ErraticWaveform(width=5.8, color=NeuroTheme.accent_secondary).move_to(distress_card.get_center() + UP * 0.45)
        
        cortisol_ticker = MetricCounter(
            start_val=100,
            end_val=440,
            prefix="CORTISOL SPIKE: +",
            suffix="%",
            decimals=0,
            font_size=20,
            color=NeuroTheme.accent_secondary,
        ).move_to(distress_card.get_center() + DOWN * 0.65)

        distress_warning = Text("Systemic Inflammation • Prefrontal Shutdown", font=TYPOGRAPHY["font"], font_size=12, color=NeuroTheme.accent_secondary).move_to(distress_card.get_center() + DOWN * 1.25)

        # First: Tracer plunge animation over the threshold
        self.play(
            curve_viz.tracer.animate(rate_func=ease_in_out_cubic).move_to(right_crash_pt),
            curve_viz.curve.animate.set_stroke(color=NeuroTheme.accent_secondary),
            FadeOut(peak_badge),
            FadeOut(flow_metric),
            ReplacementTransform(pill_beat2, pill_beat3),
            FadeOut(headline_beat2, shift=UP * 0.3),
            FadeOut(sub_beat2, shift=UP * 0.2),
            FadeIn(headline_beat3, shift=DOWN * 0.2),
            FadeIn(sub_beat3, shift=UP * 0.1),
            run_time=1.1,
        )

        # Morph curve into the Dual Bento Stack
        self.play(
            FadeOut(curve_viz),
            ReplacementTransform(curve_card, eustress_card),
            FadeIn(distress_card, shift=UP * 0.3, rate_func=snappy_overshoot(0.1)),
            Create(wave_eustress),
            FadeIn(eustress_sub),
            Create(wave_distress),
            FadeIn(cortisol_ticker),
            FadeIn(distress_warning),
            run_time=1.1,
        )

        # Active data surge during Beat 3
        beat3_remaining = max(1.2, DUR_3_DISTRESS - 2.2)
        self.play(
            cortisol_ticker.count_to(target=440, duration=beat3_remaining * 0.8),
            wave_distress.animate(rate_func=ease_in_out_cubic).shift(UP * 0.04),
            run_time=beat3_remaining,
        )

        # =====================================================================
        # BEAT 4: THE MASTER SYNTHESIS & EQUILIBRIUM RULE (DUR_4_SYNTHESIS = ~7.01s)
        # "The secret isn't eliminating pressure. It's balancing acute intensity with deep, deliberate recovery."
        # =====================================================================
        pill_beat4 = create_topic_pill("THE NEURAL PROTOCOL", NeuroTheme.accent_glow).move_to(UP * 4.8)

        headline_beat4 = KineticText(
            "PRESSURE + RECOVERY",
            font=TYPOGRAPHY["font"],
            font_size=38,
            color=NeuroTheme.text_primary,
            weight=BOLD,
        ).move_to(UP * 3.4)

        sub_beat4 = Text(
            "Stress expands capacity • Recovery locks in adaptation",
            font=TYPOGRAPHY["font"],
            font_size=15,
            color=NeuroTheme.accent_primary,
            weight=BOLD,
        ).move_to(UP * 2.6)

        # Master Equilibrium Dial Card
        master_card = BentoCard(
            width=7.6,
            height=5.6,
            badge_text="DYNAMIC EQUILIBRIUM",
            badge_color=NeuroTheme.accent_glow,
        ).move_to(DOWN * 1.0)

        # Radial Dual-Meter
        radial_balance = RadialMeter(
            radius=1.3,
            stroke_width=7.0,
            accent_color=NeuroTheme.accent_primary,
        ).move_to(master_card.get_center() + UP * 0.3)

        arc_intensity = Arc(
            radius=1.3,
            start_angle=-PI / 2,
            angle=PI,
            stroke_color=NeuroTheme.accent_glow,
            stroke_width=7.0,
            arc_center=radial_balance.get_center(),
        )

        arc_recovery = Arc(
            radius=1.3,
            start_angle=PI / 2,
            angle=PI,
            stroke_color=NeuroTheme.accent_primary,
            stroke_width=7.0,
            arc_center=radial_balance.get_center(),
        )

        core_balance = PulsingNode(radius=0.28, core_color=NeuroTheme.accent_primary).move_to(radial_balance.get_center())

        label_intensity = Text("INTENSITY", font=TYPOGRAPHY["font"], font_size=12, color=NeuroTheme.accent_glow, weight=BOLD).move_to(radial_balance.get_center() + LEFT * 2.1)
        label_recovery = Text("RECOVERY", font=TYPOGRAPHY["font"], font_size=12, color=NeuroTheme.accent_primary, weight=BOLD).move_to(radial_balance.get_center() + RIGHT * 2.1)

        rule_metric = MetricCounter(
            start_val=0,
            end_val=100,
            prefix="ADAPTIVE CAPACITY: ",
            suffix="%",
            decimals=0,
            font_size=22,
            color=NeuroTheme.text_primary,
        ).move_to(master_card.get_center() + DOWN * 1.6)

        # Transition into Final Master Synthesis
        self.play(
            ReplacementTransform(pill_beat3, pill_beat4),
            FadeOut(headline_beat3, shift=UP * 0.3),
            FadeOut(sub_beat3, shift=UP * 0.2),
            FadeIn(headline_beat4, shift=DOWN * 0.2),
            FadeIn(sub_beat4, shift=UP * 0.1),
            ReplacementTransform(eustress_card, master_card),
            FadeOut(distress_card, shift=DOWN * 0.4),
            FadeOut(wave_eustress),
            FadeOut(eustress_sub),
            FadeOut(wave_distress),
            FadeOut(cortisol_ticker),
            FadeOut(distress_warning),
            FadeIn(core_balance),
            Create(arc_intensity),
            Create(arc_recovery),
            FadeIn(label_intensity, shift=RIGHT * 0.2),
            FadeIn(label_recovery, shift=LEFT * 0.2),
            FadeIn(rule_metric),
            run_time=1.2,
        )

        # Animate radial dial settle and final metric growth
        beat4_remaining = max(1.0, DUR_4_SYNTHESIS - 1.2)
        self.play(
            rule_metric.count_to(target=100, duration=beat4_remaining * 0.7),
            core_balance.halo.animate(rate_func=ease_in_out_cubic).scale(1.4).set_opacity(0.18),
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(1.02),
            run_time=beat4_remaining,
        )

        # Subtle clean final hold
        self.wait(0.3)


# -----------------------------------------------------------------------------
# 5. EXECUTION & PIPELINE ENTRYPOINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Configure Manim for 9:16 Vertical Video Output (Full 1080x1920 60fps)
    config.media_dir = "media"
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_width = 9.0
    config.frame_height = 16.0
    config.frame_rate = 60

    print("🎬 Rendering Master 1080p 60fps Manim 9:16 Vertical Video: GoodStressVsBadStressScene...")
    scene = GoodStressVsBadStressScene()
    scene.render()

    # Find the rendered video
    all_videos = [
        p for p in Path("media").glob("**/GoodStressVsBadStressScene.mp4")
        if "partial_movie_files" not in str(p)
    ]
    if not all_videos:
        raise FileNotFoundError("Rendered GoodStressVsBadStressScene.mp4 not found!")
    all_videos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    video_file = str(all_videos[0])

    print(f"📹 Video rendered at: {video_file}")
    output_master = "media/exports/good_stress_vs_bad_stress_master.mp4"
    print(f"🔊 Muxing video with Edge Neural Voiceover into {output_master}...")
    mux_video_audio(video_file, MASTER_AUDIO, output_master)
    print(f"🎉 Production Master Ready: {output_master}")
