"""
Golden Showcase Example: Industry-Level Manim Motion Design
Demonstrating Minimalist 2D Vector Animation, Kinetic Typography, and Data-in-Motion.
"""

from manim import *
import numpy as np

# Framework imports
from motion_framework.theme import OnyxCyber, TYPOGRAPHY
from motion_framework.easings import snappy_overshoot, ease_out_cubic, ease_in_out_cubic
from motion_framework.components import (
    BentoCard,
    MetricCounter,
    KineticText,
    PulsingNode,
    DataWire,
    RadialMeter,
    create_grid_background,
)


class ShowcaseScene(MovingCameraScene):
    def construct(self):
        # 1. Canvas Setup
        self.camera.background_color = OnyxCyber.bg
        grid = create_grid_background(width=16, height=10, step=1.2, opacity=0.18)
        self.add(grid)

        # ---------------------------------------------------------
        # BEAT 1: KINETIC TYPOGRAPHY INTRO (0:00 - 0:03)
        # ---------------------------------------------------------
        badge_text = Text(
            "INTELLIGENT WORKSPACE",
            font=TYPOGRAPHY["font"],
            font_size=13,
            weight=BOLD,
            color=OnyxCyber.accent_primary,
        )
        badge_box = RoundedRectangle(
            width=badge_text.width + 0.4,
            height=badge_text.height + 0.22,
            corner_radius=0.1,
            fill_color=OnyxCyber.accent_primary,
            fill_opacity=0.12,
            stroke_color=OnyxCyber.accent_primary,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )
        category_badge = VGroup(badge_box, badge_text).move_to(UP * 1.5)

        hero_headline = KineticText(
            "VELOCITY AT SCALE",
            font=TYPOGRAPHY["font"],
            font_size=TYPOGRAPHY["hero_size"],
            color=OnyxCyber.text_primary,
            weight=BOLD,
        ).move_to(UP * 0.5)

        sub_caption = Text(
            "Deterministic performance architecture for mission-critical systems",
            font=TYPOGRAPHY["font"],
            font_size=TYPOGRAPHY["body_size"],
            color=OnyxCyber.text_muted,
        ).move_to(DOWN * 0.4)

        # Entrance with physical ease and staggered overlap
        self.play(
            FadeIn(category_badge, shift=UP * 0.2, rate_func=ease_out_cubic),
            run_time=0.6,
        )
        self.play(
            hero_headline.reveal_animation(lag_ratio=0.07, duration=0.8),
            FadeIn(sub_caption, shift=UP * 0.15, rate_func=ease_out_cubic),
            run_time=0.9,
        )
        self.wait(0.6)

        # ---------------------------------------------------------
        # BEAT 2: MORPH INTO BENTO GRID (0:03 - 0:07)
        # ---------------------------------------------------------
        # Shift intro elements upward/out
        self.play(
            category_badge.animate(rate_func=ease_out_cubic).shift(UP * 2.0).set_opacity(0),
            sub_caption.animate(rate_func=ease_out_cubic).shift(UP * 1.5).set_opacity(0),
            hero_headline.animate(rate_func=ease_out_cubic).scale(0.55).to_corner(UL, buff=0.8),
            run_time=0.8,
        )

        # Bento Cards Setup
        left_card = BentoCard(
            width=6.0,
            height=4.6,
            badge_text="NETWORK MESH",
            badge_color=OnyxCyber.accent_primary,
        ).move_to(LEFT * 3.3 + DOWN * 0.5)

        right_top_card = BentoCard(
            width=5.4,
            height=2.15,
            badge_text="EFFICIENCY",
            badge_color=OnyxCyber.accent_secondary,
        ).move_to(RIGHT * 3.3 + UP * 0.75)

        right_bot_card = BentoCard(
            width=5.4,
            height=2.15,
            badge_text="REALTIME LATENCY",
            badge_color=OnyxCyber.accent_primary,
        ).move_to(RIGHT * 3.3 + DOWN * 1.7)

        # Staggered Bento Entrance with subtle tactile overshoot
        self.play(
            LaggedStart(
                FadeIn(left_card, shift=UP * 0.4, rate_func=snappy_overshoot(0.1)),
                FadeIn(right_top_card, shift=RIGHT * 0.4, rate_func=snappy_overshoot(0.1)),
                FadeIn(right_bot_card, shift=RIGHT * 0.4, rate_func=snappy_overshoot(0.1)),
                lag_ratio=0.14,
            ),
            run_time=1.0,
        )

        # ---------------------------------------------------------
        # BEAT 3: DATA-IN-MOTION (TOPOLOGY + METRICS) (0:07 - 0:10)
        # ---------------------------------------------------------
        # Left Card: Network Nodes
        node_a = PulsingNode(radius=0.18, core_color=OnyxCyber.accent_primary).move_to(
            left_card.get_center() + LEFT * 1.6 + DOWN * 0.4
        )
        node_b = PulsingNode(radius=0.22, core_color=OnyxCyber.accent_secondary).move_to(
            left_card.get_center() + UP * 0.6
        )
        node_c = PulsingNode(radius=0.18, core_color=OnyxCyber.accent_primary).move_to(
            left_card.get_center() + RIGHT * 1.6 + DOWN * 0.4
        )

        wire_ab = DataWire(node_a.get_center(), node_b.get_center())
        wire_bc = DataWire(node_b.get_center(), node_c.get_center())
        wire_ac = DataWire(node_a.get_center(), node_c.get_center(), control_pt_1=left_card.get_center() + DOWN * 1.2)

        network_group = VGroup(wire_ab, wire_bc, wire_ac, node_a, node_b, node_c)

        # Right Top: Radial Meter + Metric Counter
        radial = RadialMeter(radius=0.68, stroke_width=5.0, accent_color=OnyxCyber.accent_secondary).move_to(
            right_top_card.get_center() + LEFT * 1.5 + DOWN * 0.1
        )
        efficiency_metric = MetricCounter(
            start_val=0,
            end_val=99.8,
            suffix="%",
            decimals=1,
            font_size=38,
            color=OnyxCyber.text_primary,
        ).move_to(right_top_card.get_center() + RIGHT * 1.0 + DOWN * 0.1)

        # Right Bottom: Latency Counter + Sparkline
        latency_metric = MetricCounter(
            start_val=120,
            end_val=4,
            suffix="ms",
            decimals=0,
            font_size=38,
            color=OnyxCyber.accent_primary,
        ).move_to(right_bot_card.get_center() + LEFT * 1.4 + DOWN * 0.1)

        # Mini Sparkline Curve
        sparkline_points = [
            right_bot_card.get_center() + RIGHT * 0.3 + DOWN * 0.4,
            right_bot_card.get_center() + RIGHT * 0.8 + DOWN * 0.1,
            right_bot_card.get_center() + RIGHT * 1.3 + DOWN * 0.3,
            right_bot_card.get_center() + RIGHT * 1.8 + UP * 0.2,
            right_bot_card.get_center() + RIGHT * 2.3 + UP * 0.1,
        ]
        sparkline = VMobject().set_points_smoothly(sparkline_points).set_stroke(
            color=OnyxCyber.accent_primary, width=2.5
        )

        # Entrance of internal widgets
        self.play(
            FadeIn(network_group, shift=UP * 0.2, rate_func=ease_out_cubic),
            FadeIn(radial, shift=LEFT * 0.2, rate_func=ease_out_cubic),
            FadeIn(efficiency_metric, shift=RIGHT * 0.2, rate_func=ease_out_cubic),
            FadeIn(latency_metric, shift=LEFT * 0.2, rate_func=ease_out_cubic),
            Create(sparkline, rate_func=ease_out_cubic),
            run_time=0.8,
        )

        # ---------------------------------------------------------
        # BEAT 4: CINEMATIC DATA SURGE & CAMERA PAN (0:10 - 0:13)
        # ---------------------------------------------------------
        # Trigger counts, radial fill, data wire flashes, and subtle camera punch
        self.play(
            efficiency_metric.count_to(target=99.8, duration=1.6),
            radial.fill_to(0.998, duration=1.6),
            latency_metric.count_to(target=4, duration=1.4),
            wire_ab.flash_animation(duration=1.2),
            wire_bc.flash_animation(duration=1.4),
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(0.94).shift(LEFT * 0.3 + DOWN * 0.1),
            run_time=1.8,
        )

        # Final secondary flash and settle
        self.play(
            wire_ac.flash_animation(duration=1.2),
            run_time=1.2,
        )
        self.wait(0.5)
