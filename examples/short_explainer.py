"""
Short Explainer: 9:16 Vertical Video with Microsoft Edge Neural Voice Over.
Topic: "Why Edge AI Changes Everything in 15 Seconds"
Default Voice: en-US-AvaMultilingualNeural
"""

import sys
from pathlib import Path
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
from motion_framework.voice import (
    DEFAULT_VOICE,
    VoiceoverBeatSheet,
    mux_video_audio,
)

# -------------------------------------------------------------
# 1. AUDIO SCRIPT & SYNTHESIS (Edge Neural Voice: Ava)
# -------------------------------------------------------------
print("🎙️ Synthesizing Microsoft Edge Neural Voice Over...")
voice_sheet = VoiceoverBeatSheet(voice="en-US-AvaMultilingualNeural", base_dir="media/audio/short_explainer")

# Synthesize narration beats
DUR_HOOK = voice_sheet.add_beat(
    "beat_1_hook",
    "Why is modern intelligence moving to the edge? Because speed isn't a feature—it's physics."
)
DUR_MESH = voice_sheet.add_beat(
    "beat_2_mesh",
    "When neural networks run directly on local silicon, latency plummets from hundreds of milliseconds to single digits."
)
DUR_IMPACT = voice_sheet.add_beat(
    "beat_3_impact",
    "Zero cloud roundtrips. Ninety-nine point nine percent reliability. Pure autonomous scale."
)
MASTER_AUDIO = voice_sheet.build_master_track("media/audio/short_explainer/master_voice.mp3")

print(f"✅ Audio generated! Durations: Hook={DUR_HOOK:.2f}s, Mesh={DUR_MESH:.2f}s, Impact={DUR_IMPACT:.2f}s")


# -------------------------------------------------------------
# 2. MANIM 9:16 VERTICAL SCENE DEFINITION
# -------------------------------------------------------------
class ShortExplainerScene(MovingCameraScene):
    def construct(self):
        # Canvas & Background setup (9:16 Vertical)
        self.camera.background_color = OnyxCyber.bg
        grid = create_grid_background(width=10, height=18, step=1.2, opacity=0.16)
        self.add(grid)

        # ---------------------------------------------------------
        # BEAT 1: KINETIC HOOK (Locked to DUR_HOOK)
        # ---------------------------------------------------------
        badge_text = Text(
            "AUTONOMOUS SILICON",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=OnyxCyber.accent_primary,
        )
        badge_box = RoundedRectangle(
            width=badge_text.width + 0.35,
            height=badge_text.height + 0.2,
            corner_radius=0.08,
            fill_color=OnyxCyber.accent_primary,
            fill_opacity=0.15,
            stroke_color=OnyxCyber.accent_primary,
            stroke_width=1.0,
            stroke_opacity=0.6,
        )
        topic_badge = VGroup(badge_box, badge_text).move_to(UP * 4.6)

        hook_headline = KineticText(
            "SPEED IS PHYSICS",
            font=TYPOGRAPHY["font"],
            font_size=42,
            color=OnyxCyber.text_primary,
            weight=BOLD,
        ).move_to(UP * 2.2)

        hook_sub = Text(
            "The shift from cloud clusters to local edge inference",
            font=TYPOGRAPHY["font"],
            font_size=17,
            color=OnyxCyber.text_muted,
        ).move_to(UP * 1.3)

        # Visual pulse circle in optical center
        pulse_core = PulsingNode(radius=0.35, core_color=OnyxCyber.accent_primary).move_to(DOWN * 1.0)

        # Staggered entrance
        self.play(
            FadeIn(topic_badge, shift=DOWN * 0.2, rate_func=ease_out_cubic),
            hook_headline.reveal_animation(lag_ratio=0.08, duration=0.8),
            FadeIn(hook_sub, shift=UP * 0.15, rate_func=ease_out_cubic),
            FadeIn(pulse_core, shift=UP * 0.3, rate_func=snappy_overshoot(0.12)),
            run_time=min(2.0, DUR_HOOK * 0.4),
        )

        # Remainder of Beat 1: subtle ambient breathing
        remaining_hook = max(0.5, DUR_HOOK - min(2.0, DUR_HOOK * 0.4))
        self.play(
            pulse_core.halo.animate(rate_func=ease_in_out_cubic).scale(1.3).set_opacity(0.15),
            run_time=remaining_hook,
        )

        # ---------------------------------------------------------
        # BEAT 2: VERTICAL BENTO STACK & LATENCY PLUMMET (DUR_MESH)
        # ---------------------------------------------------------
        # Transition out hook elements
        self.play(
            hook_headline.animate(rate_func=ease_out_cubic).shift(UP * 1.5).set_opacity(0),
            hook_sub.animate(rate_func=ease_out_cubic).shift(UP * 1.0).set_opacity(0),
            FadeOut(pulse_core, shift=DOWN * 0.3),
            run_time=0.6,
        )

        # Vertical Bento Cards (Respecting Mobile Safe Zones)
        top_mesh_card = BentoCard(
            width=7.4,
            height=4.6,
            badge_text="NEURAL MESH",
            badge_color=OnyxCyber.accent_primary,
        ).move_to(UP * 1.6)

        bottom_data_card = BentoCard(
            width=7.4,
            height=3.6,
            badge_text="LATENCY CRUSH",
            badge_color=OnyxCyber.accent_secondary,
        ).move_to(DOWN * 2.8)

        # Mesh Nodes inside Top Card
        node_1 = PulsingNode(radius=0.18, core_color=OnyxCyber.accent_primary).move_to(
            top_mesh_card.get_center() + LEFT * 2.0 + DOWN * 0.3
        )
        node_2 = PulsingNode(radius=0.24, core_color=OnyxCyber.accent_secondary).move_to(
            top_mesh_card.get_center() + UP * 0.7
        )
        node_3 = PulsingNode(radius=0.18, core_color=OnyxCyber.accent_primary).move_to(
            top_mesh_card.get_center() + RIGHT * 2.0 + DOWN * 0.3
        )
        wire_12 = DataWire(node_1.get_center(), node_2.get_center())
        wire_23 = DataWire(node_2.get_center(), node_3.get_center())
        wire_13 = DataWire(
            node_1.get_center(),
            node_3.get_center(),
            control_pt_1=top_mesh_card.get_center() + DOWN * 1.1,
        )
        mesh_system = VGroup(wire_12, wire_23, wire_13, node_1, node_2, node_3)

        # Latency Metric in Bottom Card
        latency_counter = MetricCounter(
            start_val=180,
            end_val=4,
            suffix="ms",
            decimals=0,
            font_size=52,
            color=OnyxCyber.accent_primary,
        ).move_to(bottom_data_card.get_center() + LEFT * 1.8 + DOWN * 0.1)

        latency_label = Text(
            "ROUNDTRIP TIME",
            font=TYPOGRAPHY["font"],
            font_size=12,
            weight=BOLD,
            color=OnyxCyber.text_muted,
        ).move_to(bottom_data_card.get_center() + LEFT * 1.8 + UP * 0.6)

        # Sparkline curve in bottom card
        sparkline_pts = [
            bottom_data_card.get_center() + RIGHT * 0.2 + UP * 0.6,
            bottom_data_card.get_center() + RIGHT * 0.8 + UP * 0.2,
            bottom_data_card.get_center() + RIGHT * 1.4 + DOWN * 0.2,
            bottom_data_card.get_center() + RIGHT * 2.0 + DOWN * 0.4,
            bottom_data_card.get_center() + RIGHT * 2.6 + DOWN * 0.5,
        ]
        sparkline = VMobject().set_points_smoothly(sparkline_pts).set_stroke(
            color=OnyxCyber.accent_primary, width=3.0
        )

        bento_group = VGroup(top_mesh_card, bottom_data_card)

        # Bento Reveal
        self.play(
            LaggedStart(
                FadeIn(top_mesh_card, shift=UP * 0.4, rate_func=snappy_overshoot(0.1)),
                FadeIn(bottom_data_card, shift=UP * 0.4, rate_func=snappy_overshoot(0.1)),
                lag_ratio=0.15,
            ),
            FadeIn(mesh_system, shift=UP * 0.2),
            FadeIn(latency_label, shift=UP * 0.1),
            FadeIn(latency_counter),
            Create(sparkline),
            run_time=0.9,
        )

        # Data Surge Animation during Beat 2
        active_mesh_time = max(1.2, DUR_MESH - 1.5)
        self.play(
            latency_counter.count_to(target=4, duration=active_mesh_time),
            wire_12.flash_animation(duration=active_mesh_time * 0.8),
            wire_23.flash_animation(duration=active_mesh_time * 0.9),
            run_time=active_mesh_time,
        )

        # ---------------------------------------------------------
        # BEAT 3: RADIAL RELIABILITY & IMPACT OUTRO (DUR_IMPACT)
        # ---------------------------------------------------------
        # Swap top card content into Radial Reliability Dial
        radial_dial = RadialMeter(
            radius=1.1,
            stroke_width=6.0,
            accent_color=OnyxCyber.accent_secondary,
        ).move_to(top_mesh_card.get_center() + LEFT * 1.5 + DOWN * 0.1)

        efficiency_metric = MetricCounter(
            start_val=0,
            end_val=99.9,
            suffix="%",
            decimals=1,
            font_size=42,
            color=OnyxCyber.text_primary,
        ).move_to(top_mesh_card.get_center() + RIGHT * 1.2 + DOWN * 0.1)

        self.play(
            FadeOut(mesh_system, shift=DOWN * 0.2),
            FadeIn(radial_dial, shift=UP * 0.2),
            FadeIn(efficiency_metric, shift=RIGHT * 0.2),
            run_time=0.8,
        )

        active_impact_time = max(1.2, DUR_IMPACT - 1.2)
        self.play(
            radial_dial.fill_to(0.999, duration=active_impact_time),
            efficiency_metric.count_to(target=99.9, duration=active_impact_time),
            wire_13.flash_animation(duration=active_impact_time * 0.7),
            self.camera.frame.animate(rate_func=ease_in_out_cubic).scale(0.95),
            run_time=active_impact_time,
        )
        self.wait(0.4)


# -------------------------------------------------------------
# 3. DIRECT EXECUTION & AUDIO MUX PIPELINE
# -------------------------------------------------------------
if __name__ == "__main__":
    import os

    # Configure 9:16 Vertical Resolution in Manim
    config.media_dir = "media"
    config.quality = "medium_quality"
    # Ensure vertical dimensions override quality presets
    config.pixel_width = 720
    config.pixel_height = 1280
    config.frame_width = 9.0
    config.frame_height = 16.0

    print("🎬 Rendering Manim 9:16 Vertical Video...")
    scene = ShortExplainerScene()
    scene.render()

    all_videos = [p for p in Path("media").glob("**/ShortExplainerScene.mp4") if "partial_movie_files" not in str(p)]
    if not all_videos:
        raise FileNotFoundError("Rendered ShortExplainerScene.mp4 not found!")
    all_videos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    video_file = str(all_videos[0])
    print(f"📹 Video rendered at: {video_file}")
    output_master = "media/exports/short_explainer_ava_master.mp4"
    print(f"🔊 Muxing video with Edge Neural Voiceover into {output_master}...")
    mux_video_audio(video_file, MASTER_AUDIO, output_master)
    print(f"🎉 Production Master Ready: {output_master}")

    # -------------------------------------------------------------
    # 4. AUTONOMOUS METADATA GENERATION & RIGHTCLIPS EXPORT
    # -------------------------------------------------------------
    print("📝 Generating high-CTR YouTube Shorts metadata...")
    from motion_framework.metadata import generate_video_metadata
    from motion_framework.exporter import export_to_rightclips

    metadata = generate_video_metadata(
        topic="Why Edge AI Changes Everything",
        script_beats=[
            "Why is modern intelligence moving to the edge? Because speed isn't a feature—it's physics.",
            "When neural networks run directly on local silicon, latency plummets from hundreds of milliseconds to single digits.",
            "Zero cloud roundtrips. Ninety-nine point nine percent reliability. Pure autonomous scale."
        ],
        bullet_takeaways=[
            "Running neural networks directly on local hardware drops latency to under 4ms.",
            "Eliminates cloud API roundtrip bottlenecks and bandwidth costs.",
            "Enables true real-time autonomous systems at scale."
        ],
        extra_hashtags=["#EdgeAI", "#Hardware", "#Silicon", "#Latency", "#Coding"]
    )

    print(f"📌 Generated Title: {metadata['title']}")
    print(f"🏷️ Generated Tags: {', '.join(metadata['tags'][:5])}...")

    # Export to RightClips for 1-click YouTube publishing
    print("🌉 Exporting to RightClips Studio...")
    export_result = export_to_rightclips(
        video_path=output_master,
        metadata=metadata,
        custom_video_name="edge_ai_speed_physics_video.mp4"
    )
    print(f"✅ Exported to RightClips: {export_result['video_path']}")
    print(f"✅ RightClips Studio is ready to publish this video to YouTube!")
