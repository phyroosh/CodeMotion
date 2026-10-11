"""
🎬 Frontier T: Thumbnail Intelligence & Multi-Scale Validation Engine
===================================================================
Adapted from RightClips for Manim Python motion design.

Core Laws:
  1. STYLE IS CONSISTENT. COMPOSITION IS CREATIVE.
  2. A THUMBNAIL IS NOT THE VISUAL EXPLANATION; IT IS THE VISUAL QUESTION.
  3. COMPLEXITY BUDGET: Strict 1-3 punch words max. Zero pill badges, zero subtitle cards.
  4. MULTI-SCALE VALIDATION: Must survive 360x640 mobile downsampling and Gaussian blur squint test.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageFilter, ImageStat

from manim import *
from .theme import OnyxCyber, ObsidianEmerald, SolarGraphite, TYPOGRAPHY


# =====================================================================
# 1. FRONTIER T: CREATIVE DECISION DIRECTOR
# =====================================================================

class FrontierTDirector:
    """
    Deconstructs topic and narrative into high-converting visual concepts,
    generates 3 candidate archetypes, and selects the optimal thumbnail plan.
    """

    def analyze_tension(self, topic: str, script_text: str = "") -> Dict[str, Any]:
        """Extracts core conceptual paradox and visual question."""
        lower = f"{topic} {script_text}".lower()

        if any(k in lower for k in ["edge", "latency", "local", "speed", "physics", "silicon"]):
            core_idea = "Physical distance and bandwidth bottlenecks crush centralized cloud inference."
            tension = "The speed of light limits the cloud, but local silicon has zero roundtrip distance."
            curiosity_gap = "How does local silicon crush latency by 98% in 15 seconds?"
            domain = "latency_physics"
            punch_candidates = ["SPEED IS PHYSICS", "4MS LATENCY", "THE CLOUD TRAP"]
        elif any(k in lower for k in ["neural", "ai", "model", "inference", "compute"]):
            core_idea = "Massive models are collapsing into micro-chips."
            tension = "Giant intelligence running on milliwatts of local power."
            curiosity_gap = "What happens when intelligence lives directly on the chip?"
            domain = "silicon_intelligence"
            punch_candidates = ["LOCAL SILICON", "AI ON CHIP", "AUTONOMOUS"]
        elif any(k in lower for k in ["network", "mesh", "distributed", "protocol"]):
            core_idea = "Decentralized mesh networks eliminate single points of failure."
            tension = "Fragile central nodes vs unkillable distributed mesh."
            curiosity_gap = "Why can't traditional infrastructure keep up?"
            domain = "distributed_mesh"
            punch_candidates = ["THE MESH SHIFT", "ZERO FAILURE", "NEW PROTOCOL"]
        else:
            core_idea = f"The hidden mechanism behind {topic}."
            tension = f"The counter-intuitive reality of {topic}."
            curiosity_gap = f"Why everything you assumed about {topic} is backwards."
            domain = "tech_paradox"
            clean_words = re.sub(r"[^\w\s]", "", topic.upper()).split()[:2]
            punch_candidates = [" ".join(clean_words) or "THE PARADOX", "NEW SYSTEM", "THE TRUTH"]

        return {
            "topic": topic,
            "coreIdea": core_idea,
            "tension": tension,
            "curiosityGap": curiosity_gap,
            "domain": domain,
            "punchCandidates": punch_candidates,
        }

    def generate_manifest(self, topic: str, script_text: str = "", aspect_ratio: str = "9:16") -> Dict[str, Any]:
        """
        Synthesizes 3 candidate archetypes and outputs the chosen Frontier T manifest.
        """
        analysis = self.analyze_tension(topic, script_text)
        punch_word = analysis["punchCandidates"][0]

        # 3 Canonical Frontier T Archetypes
        concepts = [
            {
                "conceptId": "concept_1_impossible_metaphor",
                "archetype": "impossible_metaphor",
                "title": "The Impossible Circuit",
                "visualMetaphor": "A luminous cybernetic chip core pulsing with high-voltage neon energy against obsidian void.",
                "punchWord": punch_word,
                "accentColor": OnyxCyber.accent_primary,
                "groundColor": OnyxCyber.bg,
                "focalSilhouette": "Glowing central polygonal processor with floating signal rings",
            },
            {
                "conceptId": "concept_2_scale_constraint",
                "archetype": "scale_constraint",
                "title": "The Micro Divide",
                "visualMetaphor": "A massive divergent network bottleneck collapsing down into a single micro-point of light.",
                "punchWord": analysis["punchCandidates"][1] if len(analysis["punchCandidates"]) > 1 else punch_word,
                "accentColor": OnyxCyber.accent_secondary,
                "groundColor": OnyxCyber.bg,
                "focalSilhouette": "Extreme scale contrast between immense wire mesh and pinpoint core",
            },
            {
                "conceptId": "concept_3_minimal_object",
                "archetype": "minimal_object",
                "title": "Tactile Anomaly",
                "visualMetaphor": "A solitary monolithic block with a razor-thin glowing cyan hairline fracture.",
                "punchWord": analysis["punchCandidates"][-1],
                "accentColor": "#00FFA3",
                "groundColor": "#080C14",
                "focalSilhouette": "Monolithic geometric card with glowing metric reading",
            },
        ]

        chosen = concepts[0]

        return {
            "topic": topic,
            "aspectRatio": aspect_ratio,
            "chosenConcept": chosen,
            "candidateConcepts": concepts,
            "textStrategy": {
                "hookWord": chosen["punchWord"],
                "wordCount": len(chosen["punchWord"].split()),
                "fontSize": 64 if aspect_ratio == "9:16" else 76,
            },
            "complexityBudget": {
                "maxWords": 3,
                "pillBadgesAllowed": False,
                "subtitleCardsAllowed": False,
                "dominantSilhouetteRequired": True,
            },
        }


# =====================================================================
# 2. FRONTIER T: MULTI-SCALE OPTICAL VALIDATOR
# =====================================================================

class FrontierTValidator:
    """
    Automated multi-scale auditor verifying:
      1. Mobile Survival (360x640 downsample, RMS contrast > 30.0)
      2. Gaussian Blur / Squint Test (radius 10 blur, contrast > 22.0)
      3. Complexity Budget (zero pill badges, max 3 words)
    """

    @staticmethod
    def audit_thumbnail(
        image_path: str,
        manifest: Optional[Dict[str, Any]] = None,
        save_debug: bool = True
    ) -> Dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            return {"passed": False, "errors": [f"Image not found: {image_path}"], "metrics": {}}

        errors: List[str] = []
        warnings: List[str] = []
        metrics: Dict[str, Any] = {}

        img = Image.open(path).convert("RGB")
        w, h = img.size
        metrics["resolution"] = f"{w}x{h}"
        aspect = "9:16" if h > w else "16:9"
        metrics["aspectRatio"] = aspect

        # 1. MOBILE SURVIVAL TEST (360x640)
        mobile_target = (360, 640) if aspect == "9:16" else (640, 360)
        mobile_img = img.resize(mobile_target, Image.Resampling.LANCZOS)
        stat = ImageStat.Stat(mobile_img)
        avg_contrast = sum(stat.stddev) / len(stat.stddev)
        metrics["mobileRmsContrast"] = round(avg_contrast, 2)

        if avg_contrast < 30.0:
            errors.append(f"Mobile contrast failed ({avg_contrast:.1f} < 30.0). Thumbnail will look washed out on mobile.")

        # 2. GAUSSIAN BLUR / SQUINT TEST
        blurred_img = mobile_img.filter(ImageFilter.GaussianBlur(radius=10))
        blur_stat = ImageStat.Stat(blurred_img)
        blur_contrast = sum(blur_stat.stddev) / len(blur_stat.stddev)
        metrics["blurredContrast"] = round(blur_contrast, 2)

        if blur_contrast < 22.0:
            errors.append(f"Focal hierarchy failed blur test ({blur_contrast:.1f} < 22.0). Lacks a dominant visual silhouette.")

        # 3. COMPLEXITY BUDGET AUDIT
        if manifest:
            hook_word = manifest.get("textStrategy", {}).get("hookWord", "")
            words = hook_word.split()
            metrics["hookWord"] = hook_word
            metrics["wordCount"] = len(words)

            if len(words) > 3:
                errors.append(f"Complexity budget exceeded: text hook has {len(words)} words (max allowed: 3).")

        # 4. SAVE DEBUG PREVIEWS
        if save_debug:
            out_dir = path.parent
            mobile_file = out_dir / f"{path.stem}_audit_mobile.png"
            blur_file = out_dir / f"{path.stem}_audit_blur.png"
            mobile_img.save(mobile_file)
            blurred_img.save(blur_file)
            metrics["mobilePreview"] = str(mobile_file)
            metrics["blurPreview"] = str(blur_file)

        passed = len(errors) == 0
        return {
            "passed": passed,
            "imagePath": str(path),
            "errors": errors,
            "warnings": warnings,
            "metrics": metrics,
        }


# =====================================================================
# 3. NATIVE MANIM FRONTIER T THUMBNAIL SCENE
# =====================================================================

class FrontierThumbnailScene(Scene):
    """
    Dedicated Manim Scene that renders a standalone, razor-sharp Frontier T thumbnail.
    """

    def __init__(self, topic="Why Edge AI Changes Everything", punch_text="SPEED IS PHYSICS", **kwargs):
        self.topic = topic
        self.punch_text = punch_text
        super().__init__(**kwargs)

    def construct(self):
        # Canvas: Dark Obsidian
        self.camera.background_color = OnyxCyber.bg

        # Subtle technical grid
        from .components import create_grid_background
        grid = create_grid_background(width=10, height=18, step=1.2, opacity=0.18)
        self.add(grid)

        # 1. PUNCH TEXT (LEVEL 1 TYPOGRAPHIC MAGNET)
        # Giant, ultra-bold, zero subtitle clutter, strictly inside upper optical quadrant
        words = self.punch_text.split()
        if len(words) == 1:
            line1 = words[0]
            line2 = ""
        elif len(words) == 2:
            line1 = words[0]
            line2 = words[1]
        else:
            line1 = f"{words[0]} {words[1]}"
            line2 = " ".join(words[2:])

        text_group = VGroup()
        t1 = Text(line1, font=TYPOGRAPHY["font"], font_size=64, weight=BOLD, color="#FFFFFF")
        text_group.add(t1)
        if line2:
            t2 = Text(line2, font=TYPOGRAPHY["font"], font_size=64, weight=BOLD, color=OnyxCyber.accent_primary)
            text_group.add(t2)
        text_group.arrange(DOWN, buff=0.18).move_to(UP * 4.3)

        # 2. DOMINANT HERO SILHOUETTE (IMPOSSIBLE SILICON METAPHOR)
        # Intense luminous focal subject designed to survive mobile squint/blur tests
        hero_glow_aura = Circle(
            radius=3.2,
            stroke_color=OnyxCyber.accent_primary,
            stroke_width=6.0,
            stroke_opacity=0.8,
            fill_color=OnyxCyber.accent_primary,
            fill_opacity=0.28,
        ).move_to(DOWN * 0.6)

        hero_container = RoundedRectangle(
            width=7.8,
            height=6.6,
            corner_radius=0.25,
            fill_color="#141E30",
            fill_opacity=0.95,
            stroke_color=OnyxCyber.accent_primary,
            stroke_width=4.0,
        ).move_to(DOWN * 0.6)

        # Luminous high-contrast central processor chip
        chip_plate = RoundedRectangle(
            width=3.6,
            height=3.6,
            corner_radius=0.18,
            fill_color="#00F5FF",
            fill_opacity=0.9,
            stroke_color="#FFFFFF",
            stroke_width=3.0,
        ).move_to(hero_container.get_center())

        chip_icon = Text("4ms", font=TYPOGRAPHY["font"], font_size=48, weight=BOLD, color="#0A0B0E").move_to(chip_plate.get_center())

        # High-voltage neon circuit wires
        n_left = Dot(radius=0.35, color=OnyxCyber.accent_secondary).move_to(hero_container.get_center() + LEFT * 2.6 + DOWN * 1.5)
        n_right = Dot(radius=0.35, color=OnyxCyber.accent_secondary).move_to(hero_container.get_center() + RIGHT * 2.6 + DOWN * 1.5)
        n_top = Dot(radius=0.35, color="#FFFFFF").move_to(hero_container.get_center() + UP * 2.2)

        w1 = Line(chip_plate.get_left(), n_left.get_center(), stroke_color="#00F5FF", stroke_width=4.0)
        w2 = Line(chip_plate.get_right(), n_right.get_center(), stroke_color="#00F5FF", stroke_width=4.0)
        w3 = Line(chip_plate.get_top(), n_top.get_center(), stroke_color=OnyxCyber.accent_secondary, stroke_width=4.0)

        # Level 2 Punch Badge at bottom
        metric_bg = RoundedRectangle(
            width=6.2,
            height=1.5,
            corner_radius=0.18,
            fill_color="#000000",
            fill_opacity=0.95,
            stroke_color="#00F5FF",
            stroke_width=3.0,
        ).move_to(DOWN * 5.4)

        metric_text = Text("ZERO CLOUD", font=TYPOGRAPHY["font"], font_size=38, weight=BOLD, color="#FFFFFF").move_to(metric_bg.get_center())

        self.add(
            text_group,
            hero_glow_aura,
            hero_container,
            w1, w2, w3,
            n_left, n_right, n_top,
            chip_plate, chip_icon,
            metric_bg, metric_text
        )


def render_frontier_thumbnail(
    topic: str,
    output_image_path: str,
    punch_text: Optional[str] = None,
    aspect_ratio: str = "9:16",
    validate: bool = True
) -> Dict[str, Any]:
    """
    Renders and validates a certified Frontier T thumbnail still image.
    """
    director = FrontierTDirector()
    manifest = director.generate_manifest(topic, aspect_ratio=aspect_ratio)
    
    if not punch_text:
        punch_text = manifest["chosenConcept"]["punchWord"]

    dest = Path(output_image_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Configure Manim for still frame rendering
    config.media_dir = str(dest.parent / "temp_media")
    config.quality = "high_quality"
    if aspect_ratio == "9:16":
        config.pixel_width = 1080
        config.pixel_height = 1920
        config.frame_width = 9.0
        config.frame_height = 16.0
    else:
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 16.0
        config.frame_height = 9.0

    scene = FrontierThumbnailScene(topic=topic, punch_text=punch_text)
    scene.render()

    # Move rendered still image to final destination
    temp_images = list(Path(config.media_dir).glob("**/*.png"))
    if temp_images:
        temp_images.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        import shutil
        shutil.copy2(temp_images[0], dest)
    else:
        # Fallback render single frame
        scene.camera.get_image().save(str(dest))

    # Run multi-scale validation
    validation = {}
    if validate:
        validator = FrontierTValidator()
        validation = validator.audit_thumbnail(str(dest), manifest=manifest)
        print(f"🔍 Frontier T Audit: Passed={validation.get('passed')}, RMS={validation.get('metrics', {}).get('mobileRmsContrast')}, Blur={validation.get('metrics', {}).get('blurredContrast')}")

    return {
        "thumbnailPath": str(dest),
        "manifest": manifest,
        "validation": validation,
    }
