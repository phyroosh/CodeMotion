"""
Rumination & Body Awareness: Break the Loop of Mental Overthinking and Physical Stress
Industry-grade 2D vector motion design animation created with Manim.
"""

from manim import *
import numpy as np

# Framework imports
from motion_framework.theme import Palette, TYPOGRAPHY, LAYOUT
from motion_framework.easings import snappy_overshoot, ease_out_cubic, ease_in_out_cubic
from motion_framework.components import (
    BentoCard,
    MetricCounter,
    KineticText,
    PulsingNode,
    RadialMeter,
    create_grid_background,
)

# Custom Color Palette: Somatic Midnight
SomaticTheme = Palette(
    name="Somatic Midnight",
    bg="#090A0F",
    card_bg="#121520",
    card_border="#1E2436",
    accent_primary="#00FFA3",    # High-Voltage Healing Mint (Body / Vagal Tone)
    accent_secondary="#FF5252",  # Alarm / Stress / Rumination Coral Red
    accent_glow="#00E5FF",       # Electric Cyan (Interoceptive awareness)
    text_primary="#F8FAFC",      # Crisp Off-White
    text_muted="#94A3B8",        # Slate
    text_subtle="#475569",       # Deep Slate
)


class RuminationBodyAwarenessScene(MovingCameraScene):
    def construct(self):
        # -------------------------------------------------------------
        # 0. CANVAS SETUP & BACKGROUND
        # -------------------------------------------------------------
        self.camera.background_color = SomaticTheme.bg
        grid = create_grid_background(
            width=16, height=10, step=1.2,
            dot_color=SomaticTheme.card_border,
            dot_radius=0.018,
            opacity=0.28
        )
        self.add(grid)

        # -------------------------------------------------------------
        # BEAT 1: THE COGNITIVE-SOMATIC TRAP (0:00 - 0:03.5)
        # -------------------------------------------------------------
        badge_text = Text(
            "NEURO-SOMATIC FEEDBACK",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=SomaticTheme.accent_secondary,
        )
        badge_box = RoundedRectangle(
            width=badge_text.width + 0.38,
            height=badge_text.height + 0.22,
            corner_radius=0.09,
            fill_color=SomaticTheme.accent_secondary,
            fill_opacity=0.14,
            stroke_color=SomaticTheme.accent_secondary,
            stroke_width=1.2,
            stroke_opacity=0.6,
        )
        category_badge = VGroup(badge_box, badge_text).move_to(UP * 1.6)

        hero_headline = KineticText(
            "THE RUMINATION TRAP",
            font=TYPOGRAPHY["font"],
            font_size=46,
            color=SomaticTheme.text_primary,
            weight=BOLD,
        ).move_to(UP * 0.7)

        sub_caption = Text(
            "Mental overthinking and physical stress form a closed reinforcing loop",
            font=TYPOGRAPHY["font"],
            font_size=19,
            color=SomaticTheme.text_muted,
        ).move_to(DOWN * 0.2)

        # Entrance
        self.play(
            FadeIn(category_badge, shift=UP * 0.25, rate_func=ease_out_cubic),
            run_time=0.6,
        )
        self.play(
            hero_headline.reveal_animation(lag_ratio=0.08, duration=0.8),
            FadeIn(sub_caption, shift=UP * 0.2, rate_func=ease_out_cubic),
            run_time=0.85,
        )
        self.wait(0.6)

        # -------------------------------------------------------------
        # BEAT 2: THE VICIOUS CYCLE (BENTO GRID EXPANSION) (0:03.5 - 0:08)
        # -------------------------------------------------------------
        # Docked Header aligned in top safe zone (Y = 2.5)
        docked_title = Text(
            "THE EMBODIED FEEDBACK LOOP",
            font=TYPOGRAPHY["font"],
            font_size=17,
            weight=BOLD,
            color=SomaticTheme.text_primary
        )
        docked_sub = Text(
            "HOW THOUGHTS TRAP THE BODY & BODY TRAPS THE MIND",
            font=TYPOGRAPHY["font"],
            font_size=10,
            color=SomaticTheme.text_muted
        )
        docked_header = VGroup(docked_title, docked_sub).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        docked_header.move_to(LEFT * 3.1 + UP * 2.65)

        self.play(
            category_badge.animate(rate_func=ease_out_cubic).shift(UP * 1.5).set_opacity(0),
            sub_caption.animate(rate_func=ease_out_cubic).shift(UP * 1.0).set_opacity(0),
            hero_headline.animate(rate_func=ease_out_cubic).scale(0.5).move_to(docked_header.get_center()).set_opacity(0),
            FadeIn(docked_header, shift=DOWN * 0.2, rate_func=ease_out_cubic),
            run_time=0.75,
        )

        # Bento Containers with aligned top (+1.95) and bottom (-2.45)
        left_card = BentoCard(
            width=6.0,
            height=4.4,
            corner_radius=0.18,
            bg_color=SomaticTheme.card_bg,
            border_color=SomaticTheme.card_border,
            border_width=1.5,
            badge_text="CIRCUIT: LOCKED LOOP",
            badge_color=SomaticTheme.accent_secondary,
        ).move_to(LEFT * 3.0 + DOWN * 0.25)

        right_top_card = BentoCard(
            width=5.6,
            height=2.05,
            corner_radius=0.18,
            bg_color=SomaticTheme.card_bg,
            border_color=SomaticTheme.card_border,
            border_width=1.5,
            badge_text="AUTONOMIC TONE",
            badge_color=SomaticTheme.accent_secondary,
        ).move_to(RIGHT * 3.2 + UP * 0.925)

        right_bot_card = BentoCard(
            width=5.6,
            height=2.05,
            corner_radius=0.18,
            bg_color=SomaticTheme.card_bg,
            border_color=SomaticTheme.card_border,
            border_width=1.5,
            badge_text="HRV COHERENCE",
            badge_color=SomaticTheme.accent_glow,
        ).move_to(RIGHT * 3.2 + DOWN * 1.425)

        self.play(
            LaggedStart(
                FadeIn(left_card, shift=UP * 0.35, rate_func=snappy_overshoot(0.08)),
                FadeIn(right_top_card, shift=RIGHT * 0.35, rate_func=snappy_overshoot(0.08)),
                FadeIn(right_bot_card, shift=RIGHT * 0.35, rate_func=snappy_overshoot(0.08)),
                lag_ratio=0.12,
            ),
            run_time=0.85,
        )

        # -------------------------------------------------------------
        # Left Bento Interior: Dual Nodes & Directed Feedback Wiring
        # -------------------------------------------------------------
        # Vertical placement leaves 0.6 units clearance from badge
        mind_center = left_card.get_center() + UP * 0.9
        body_center = left_card.get_center() + DOWN * 0.9

        # Mind Node (Cognitive Rumination)
        mind_node = PulsingNode(radius=0.20, core_color=SomaticTheme.accent_secondary, halo_color=SomaticTheme.accent_secondary).move_to(mind_center)
        mind_label = Text("MIND: RUMINATION", font=TYPOGRAPHY["font"], font_size=12, weight=BOLD, color=SomaticTheme.text_primary).next_to(mind_node, UP, buff=0.18)
        mind_sub = Text("Catastrophizing • 'What If?'", font=TYPOGRAPHY["font"], font_size=9.5, color=SomaticTheme.text_muted).next_to(mind_label, DOWN, buff=0.05)
        mind_group = VGroup(mind_node, mind_label, mind_sub)

        # Body Node (Somatic Tension)
        body_node = PulsingNode(radius=0.20, core_color=SomaticTheme.accent_secondary, halo_color=SomaticTheme.accent_secondary).move_to(body_center)
        body_label = Text("BODY: CONSTRICTION", font=TYPOGRAPHY["font"], font_size=12, weight=BOLD, color=SomaticTheme.text_primary).next_to(body_node, DOWN, buff=0.18)
        body_sub = Text("Tight Jaw • Elevated Cortisol", font=TYPOGRAPHY["font"], font_size=9.5, color=SomaticTheme.text_muted).next_to(body_label, DOWN, buff=0.05)
        body_group = VGroup(body_node, body_label, body_sub)

        # Directed Feedback Wires (tight radius, completely inside card boundaries)
        w1_start = mind_center + RIGHT * 0.3
        w1_end = body_center + RIGHT * 0.3
        wire_down_path = CubicBezier(
            w1_start,
            w1_start + RIGHT * 1.0 + DOWN * 0.3,
            w1_end + RIGHT * 1.0 + UP * 0.3,
            w1_end
        )
        wire_down = wire_down_path.copy().set_stroke(color=SomaticTheme.card_border, width=1.8, opacity=0.7)
        label_down = Text("Trigger", font=TYPOGRAPHY["font"], font_size=9, color=SomaticTheme.accent_secondary).move_to(
            wire_down_path.point_from_proportion(0.5) + RIGHT * 0.45
        )

        w2_start = body_center + LEFT * 0.3
        w2_end = mind_center + LEFT * 0.3
        wire_up_path = CubicBezier(
            w2_start,
            w2_start + LEFT * 1.0 + UP * 0.3,
            w2_end + LEFT * 1.0 + DOWN * 0.3,
            w2_end
        )
        wire_up = wire_up_path.copy().set_stroke(color=SomaticTheme.card_border, width=1.8, opacity=0.7)
        label_up = Text("Threat", font=TYPOGRAPHY["font"], font_size=9, color=SomaticTheme.accent_secondary).move_to(
            wire_up_path.point_from_proportion(0.5) + LEFT * 0.45
        )

        # -------------------------------------------------------------
        # Right Top Bento: Autonomic Tone Metrics
        # -------------------------------------------------------------
        status_label = Text("STATE: HYPERAROUSAL", font=TYPOGRAPHY["font"], font_size=11, weight=BOLD, color=SomaticTheme.accent_secondary).move_to(
            right_top_card.get_corner(UR) + LEFT * 1.6 + DOWN * 0.32
        )

        stress_metric = MetricCounter(
            start_val=28,
            end_val=94,
            suffix="%",
            decimals=0,
            font_size=38,
            color=SomaticTheme.accent_secondary
        ).move_to(right_top_card.get_center() + LEFT * 1.4 + DOWN * 0.08)

        stress_caption = Text("STRESS LOAD", font=TYPOGRAPHY["font"], font_size=9.5, weight=BOLD, color=SomaticTheme.text_muted).move_to(
            right_top_card.get_center() + LEFT * 1.4 + DOWN * 0.58
        )

        # Radial Gauge on Right
        vagal_meter = RadialMeter(
            radius=0.48,
            stroke_width=4.5,
            track_color=SomaticTheme.card_border,
            accent_color=SomaticTheme.accent_primary,
        ).move_to(right_top_card.get_center() + RIGHT * 1.5 + DOWN * 0.08)

        meter_caption = Text("VAGAL TONE", font=TYPOGRAPHY["font"], font_size=9.5, weight=BOLD, color=SomaticTheme.text_muted).move_to(
            right_top_card.get_center() + RIGHT * 1.5 + DOWN * 0.58
        )

        # -------------------------------------------------------------
        # Right Bottom Bento: HRV Autonomic Waveform
        # -------------------------------------------------------------
        hrv_label = Text("HRV: 24 ms", font=TYPOGRAPHY["font"], font_size=11.5, weight=BOLD, color=SomaticTheme.accent_secondary).move_to(
            right_bot_card.get_corner(UR) + LEFT * 1.1 + DOWN * 0.32
        )

        wave_center_x = right_bot_card.get_center()[0]
        wave_center_y = right_bot_card.get_center()[1] - 0.2
        wave_half_w = 2.1

        jagged_coords = [
            [wave_center_x - wave_half_w + 0.0, wave_center_y, 0],
            [wave_center_x - wave_half_w + 0.4, wave_center_y + 0.16, 0],
            [wave_center_x - wave_half_w + 0.7, wave_center_y - 0.42, 0],
            [wave_center_x - wave_half_w + 1.0, wave_center_y + 0.48, 0],
            [wave_center_x - wave_half_w + 1.3, wave_center_y - 0.30, 0],
            [wave_center_x - wave_half_w + 1.7, wave_center_y + 0.54, 0],
            [wave_center_x - wave_half_w + 2.1, wave_center_y - 0.44, 0],
            [wave_center_x - wave_half_w + 2.6, wave_center_y + 0.36, 0],
            [wave_center_x - wave_half_w + 3.1, wave_center_y - 0.26, 0],
            [wave_center_x - wave_half_w + 3.6, wave_center_y + 0.44, 0],
            [wave_center_x + wave_half_w, wave_center_y, 0],
        ]
        jagged_wave = VMobject().set_points_as_corners(jagged_coords).set_stroke(
            color=SomaticTheme.accent_secondary, width=2.4
        )

        # Entrance of internal widgets
        self.play(
            FadeIn(mind_group, shift=UP * 0.2, rate_func=ease_out_cubic),
            FadeIn(body_group, shift=DOWN * 0.2, rate_func=ease_out_cubic),
            Create(wire_down, rate_func=ease_out_cubic),
            Create(wire_up, rate_func=ease_out_cubic),
            FadeIn(label_down, shift=LEFT * 0.1),
            FadeIn(label_up, shift=RIGHT * 0.1),
            FadeIn(status_label, shift=LEFT * 0.1),
            FadeIn(stress_metric, shift=RIGHT * 0.1),
            FadeIn(stress_caption, shift=UP * 0.1),
            FadeIn(vagal_meter, shift=LEFT * 0.1),
            FadeIn(meter_caption, shift=UP * 0.1),
            FadeIn(hrv_label, shift=LEFT * 0.1),
            Create(jagged_wave, rate_func=ease_out_cubic),
            run_time=0.9,
        )

        # Stress pulses racing around the loop
        pulse_down = ShowPassingFlash(
            wire_down_path.copy().set_stroke(color=SomaticTheme.accent_secondary, width=4.0),
            time_width=0.35,
            run_time=1.2,
            rate_func=ease_in_out_cubic,
        )
        pulse_up = ShowPassingFlash(
            wire_up_path.copy().set_stroke(color=SomaticTheme.accent_secondary, width=4.0),
            time_width=0.35,
            run_time=1.2,
            rate_func=ease_in_out_cubic,
        )

        self.play(
            stress_metric.count_to(94, duration=1.5),
            pulse_down,
            run_time=1.4,
        )
        self.play(
            pulse_up,
            run_time=1.2,
        )

        # -------------------------------------------------------------
        # BEAT 3: THE INTERVENTION — SOMATOSENSORY AWARENESS (0:08 - 0:13)
        # -------------------------------------------------------------
        # Cinematic Camera punch
        self.play(
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(0.96).shift(LEFT * 0.15),
            run_time=0.9,
        )

        # Central Grounding Breathing Pacer
        center_anchor_pos = left_card.get_center()
        pacer_circle = Circle(
            radius=0.38,
            stroke_color=SomaticTheme.accent_primary,
            stroke_width=2.5,
            fill_color=SomaticTheme.accent_primary,
            fill_opacity=0.15,
        ).move_to(center_anchor_pos)

        pacer_ripple = Circle(
            radius=0.72,
            stroke_color=SomaticTheme.accent_glow,
            stroke_width=1.2,
            stroke_opacity=0.4,
        ).move_to(center_anchor_pos)

        pacer_text = Text(
            "INTEROCEPTIVE\nANCHOR",
            font=TYPOGRAPHY["font"],
            font_size=8.5,
            weight=BOLD,
            color=SomaticTheme.accent_primary,
            line_spacing=0.85,
        ).move_to(center_anchor_pos)

        pacer_group = VGroup(pacer_ripple, pacer_circle, pacer_text)

        # Dynamic Badge morph on Left Card: LOCKED LOOP -> BODY AWARENESS
        new_left_badge_text = Text(
            "BODY AWARENESS",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=SomaticTheme.accent_primary,
        )
        new_left_badge_box = RoundedRectangle(
            width=new_left_badge_text.width + 0.35,
            height=new_left_badge_text.height + 0.2,
            corner_radius=0.08,
            fill_color=SomaticTheme.accent_primary,
            fill_opacity=0.15,
            stroke_color=SomaticTheme.accent_primary,
            stroke_width=1.0,
            stroke_opacity=0.6,
        )
        new_left_badge = VGroup(new_left_badge_box, new_left_badge_text).move_to(left_card.badge.get_center())

        break_flash = Dot(point=w2_start + LEFT * 0.6 + UP * 0.8, radius=0.14, color=SomaticTheme.accent_primary)

        self.play(
            FadeIn(pacer_group, scale=0.6, rate_func=snappy_overshoot(0.15)),
            ReplacementTransform(left_card.badge, new_left_badge),
            run_time=0.8,
        )

        # BREAKING THE CIRCUIT
        severed_wire_top = CubicBezier(
            w2_start + LEFT * 0.8 + UP * 0.5,
            w2_start + LEFT * 1.1 + UP * 0.4,
            w2_end + LEFT * 1.1 + DOWN * 0.3,
            w2_end
        ).set_stroke(color=SomaticTheme.text_subtle, width=1.0, opacity=0.25)

        self.play(
            FadeIn(break_flash, rate_func=ease_out_cubic),
            wire_up.animate.set_stroke(color=SomaticTheme.accent_primary, width=3.0),
            run_time=0.35,
        )
        self.play(
            FadeOut(break_flash, scale=2.5),
            ReplacementTransform(wire_up, severed_wire_top),
            label_up.animate.set_opacity(0.15).set_color(SomaticTheme.text_subtle),
            # Shift body node to grounded mint
            body_node.core.animate.set_color(SomaticTheme.accent_primary),
            body_node.halo.animate.set_color(SomaticTheme.accent_primary),
            body_label.animate.set_color(SomaticTheme.accent_primary),
            run_time=0.85,
        )

        # Rhythmic Breathing Cycle (Inhale / Exhale)
        self.play(
            pacer_circle.animate(rate_func=ease_in_out_cubic).scale(1.35).set_fill(opacity=0.25),
            pacer_ripple.animate(rate_func=ease_in_out_cubic).scale(1.25).set_stroke(opacity=0.7),
            run_time=1.3,
        )
        self.play(
            pacer_circle.animate(rate_func=ease_in_out_cubic).scale(1 / 1.35).set_fill(opacity=0.15),
            pacer_ripple.animate(rate_func=ease_in_out_cubic).scale(1 / 1.25).set_stroke(opacity=0.3),
            # Mind node quiets down
            mind_node.core.animate.set_color(SomaticTheme.accent_glow),
            mind_node.halo.animate.set_color(SomaticTheme.accent_glow),
            mind_label.animate.set_color(SomaticTheme.text_muted),
            mind_sub.animate.set_opacity(0.25),
            run_time=1.3,
        )

        # -------------------------------------------------------------
        # BEAT 4: VAGAL COHERENCE & RESTORED EQUILIBRIUM (0:13 - 0:18)
        # -------------------------------------------------------------
        # Reset camera
        self.play(
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(1.0 / 0.96).move_to(ORIGIN),
            run_time=0.75,
        )

        # Morph Right Top: State Hyperarousal -> Regulated
        coherent_status = Text("STATE: REGULATED", font=TYPOGRAPHY["font"], font_size=11, weight=BOLD, color=SomaticTheme.accent_primary).move_to(
            status_label.get_center()
        )

        # Morph Right Top Badge to Mint
        new_right_top_badge_text = Text(
            "PARASYMPATHETIC TONE",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=SomaticTheme.accent_primary,
        )
        new_right_top_badge_box = RoundedRectangle(
            width=new_right_top_badge_text.width + 0.35,
            height=new_right_top_badge_text.height + 0.2,
            corner_radius=0.08,
            fill_color=SomaticTheme.accent_primary,
            fill_opacity=0.15,
            stroke_color=SomaticTheme.accent_primary,
            stroke_width=1.0,
            stroke_opacity=0.6,
        )
        new_right_top_badge = VGroup(new_right_top_badge_box, new_right_top_badge_text).move_to(right_top_card.badge.get_center())

        # Transform Right Bottom: Chaotic waveform into silky harmonic sine wave
        harmonic_points = []
        for x_val in np.linspace(-wave_half_w, wave_half_w, 90):
            y_val = 0.30 * np.sin(4.2 * x_val)
            harmonic_points.append([wave_center_x + x_val, wave_center_y + y_val, 0])

        harmonic_wave = VMobject().set_points_smoothly(harmonic_points).set_stroke(
            color=SomaticTheme.accent_primary, width=2.6
        )

        coherent_hrv_label = Text("HRV: 86 ms (HIGH)", font=TYPOGRAPHY["font"], font_size=11.5, weight=BOLD, color=SomaticTheme.accent_primary).move_to(
            hrv_label.get_center() + LEFT * 0.3
        )

        # Labels for Regulated Equilibrium State
        coherent_body_label = Text("BODY: REGULATION", font=TYPOGRAPHY["font"], font_size=12, weight=BOLD, color=SomaticTheme.accent_primary).next_to(body_node, DOWN, buff=0.18)
        coherent_body_sub = Text("Somatic Release • Deep Respiration", font=TYPOGRAPHY["font"], font_size=9.5, color=SomaticTheme.text_muted).next_to(coherent_body_label, DOWN, buff=0.05)

        coherent_mind_label = Text("MIND: CLARITY", font=TYPOGRAPHY["font"], font_size=12, weight=BOLD, color=SomaticTheme.accent_glow).next_to(mind_node, UP, buff=0.18)
        coherent_mind_sub = Text("Cognitive Stillness • Present", font=TYPOGRAPHY["font"], font_size=9.5, color=SomaticTheme.text_muted).next_to(coherent_mind_label, DOWN, buff=0.05)

        # Transform metrics simultaneously
        self.play(
            ReplacementTransform(status_label, coherent_status),
            ReplacementTransform(right_top_card.badge, new_right_top_badge),
            stress_metric.count_to(14, duration=1.5),
            vagal_meter.fill_to(0.94, duration=1.5),
            ReplacementTransform(jagged_wave, harmonic_wave),
            ReplacementTransform(hrv_label, coherent_hrv_label),
            ReplacementTransform(body_label, coherent_body_label),
            ReplacementTransform(body_sub, coherent_body_sub),
            ReplacementTransform(mind_label, coherent_mind_label),
            ReplacementTransform(mind_sub, coherent_mind_sub),
            label_down.animate.set_opacity(0.15).set_color(SomaticTheme.text_subtle),
            run_time=1.5,
        )

        # Coherence Pulse passing through the harmonic wave
        coherent_pulse = ShowPassingFlash(
            harmonic_wave.copy().set_stroke(color=SomaticTheme.accent_glow, width=4.5),
            time_width=0.35,
            run_time=1.3,
            rate_func=ease_in_out_cubic,
        )
        self.play(coherent_pulse, run_time=1.3)

        # Final Key Takeaway Hero Badge safely placed inside 85% safe zone
        final_takeaway_bg = RoundedRectangle(
            width=7.2,
            height=0.54,
            corner_radius=0.14,
            fill_color=SomaticTheme.card_bg,
            fill_opacity=0.94,
            stroke_color=SomaticTheme.accent_primary,
            stroke_width=1.4,
        ).move_to(DOWN * 3.1)

        final_takeaway_text = Text(
            "BODY AWARENESS DISSOLVES THE RUMINATION LOOP",
            font=TYPOGRAPHY["font"],
            font_size=13,
            weight=BOLD,
            color=SomaticTheme.text_primary,
        ).move_to(final_takeaway_bg.get_center())

        final_takeaway = VGroup(final_takeaway_bg, final_takeaway_text)

        self.play(
            FadeIn(final_takeaway, shift=UP * 0.25, rate_func=snappy_overshoot(0.1)),
            run_time=0.75,
        )

        # Ambient life hold: breathing pacer keeps gently breathing until scene finish
        self.play(
            pacer_circle.animate(rate_func=ease_in_out_cubic).scale(1.15),
            pacer_ripple.animate(rate_func=ease_in_out_cubic).scale(1.15),
            run_time=0.9,
        )
        self.wait(0.5)
