"""
Frontier T Thumbnail Intelligence Verification Script.
Tests creative direction, Manim thumbnail generation, multi-scale optical validation, and RightClips export.
"""

from pathlib import Path
from motion_framework.frontier_t import FrontierTDirector, FrontierTValidator, render_frontier_thumbnail
from motion_framework.metadata import generate_video_metadata
from motion_framework.exporter import export_to_rightclips

TOPIC = "Why Edge AI Changes Everything"
OUTPUT_THUMB = "media/exports/frontier_t_edge_ai_thumbnail.png"

print("=========================================================")
print("🎬 FRONTIER T: THUMBNAIL INTELLIGENCE DIRECTIVE")
print("=========================================================")

# 1. Creative Decision Director
director = FrontierTDirector()
manifest = director.generate_manifest(TOPIC, aspect_ratio="9:16")
chosen = manifest["chosenConcept"]

print(f"🎯 Topic: {TOPIC}")
print(f"💡 Chosen Archetype: {chosen['archetype']} ({chosen['title']})")
print(f"⚡ Punch Hook: '{chosen['punchWord']}' (Words: {manifest['textStrategy']['wordCount']})")
print(f"👁️ Visual Metaphor: {chosen['visualMetaphor']}")
print(f"📐 Complexity Budget: Max words = {manifest['complexityBudget']['maxWords']}, Pill Badges = Banned")

# 2. Render & Multi-Scale Validate
print("\n🎨 Rendering High-Res Frontier T Vector Thumbnail via Manim...")
result = render_frontier_thumbnail(
    topic=TOPIC,
    output_image_path=OUTPUT_THUMB,
    punch_text=chosen["punchWord"],
    aspect_ratio="9:16",
    validate=True,
)

val = result["validation"]
metrics = val.get("metrics", {})
print("\n🔍 Multi-Scale Optical Audit Results:")
print(f"  • Status: {'✅ PASSED' if val.get('passed') else '❌ FAILED'}")
print(f"  • Resolution: {metrics.get('resolution')}")
print(f"  • Mobile RMS Contrast (360x640): {metrics.get('mobileRmsContrast')} (Required: > 30.0)")
print(f"  • Gaussian Blur Contrast (Radius 10): {metrics.get('blurredContrast')} (Required: > 22.0)")

if val.get("errors"):
    for err in val["errors"]:
        print(f"    ❌ Error: {err}")

# 3. Export to RightClips with Certified Frontier T Thumbnail
print("\n🌉 Exporting Certified Thumbnail to RightClips...")
video_file = "media/exports/short_explainer_ava_master.mp4"
if Path(video_file).exists():
    metadata = generate_video_metadata(
        topic=TOPIC,
        script_beats=["Why is modern intelligence moving to the edge? Because speed isn't a feature—it's physics."],
        extra_hashtags=["#FrontierT", "#EdgeAI", "#Shorts"]
    )
    export_res = export_to_rightclips(
        video_path=video_file,
        metadata=metadata,
        custom_video_name="edge_ai_speed_physics_video.mp4",
        thumbnail_path=result["thumbnailPath"]
    )
    print(f"🎉 RightClips Export Complete: {export_res['thumbnail_path']}")
else:
    print(f"ℹ️ Video {video_file} not found for export test, thumbnail saved at {OUTPUT_THUMB}")

print("\n🚀 Frontier T Thumbnail Intelligence Verification Succeeded!")
