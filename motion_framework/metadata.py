"""
Autonomous YouTube Shorts Viral Metadata & Tag Synthesizer.
Generates high-CTR titles, structured descriptions with algorithmic hashtags, and SEO tags.
"""

import re
from typing import Dict, List, Any


def clean_topic_slug(topic: str) -> str:
    """Creates a filesystem-safe topic slug."""
    clean = re.sub(r"[^\w\s-]", "", topic.lower()).strip()
    return re.sub(r"[\s_-]+", "_", clean)


def synthesize_yt_title(topic: str, hook_line: str = "") -> str:
    """
    Transforms topic and hook into a high-CTR YouTube Shorts title.
    Enforces curiosity gaps, punchy length (<60 chars), and #Shorts suffix.
    """
    lower = topic.lower().strip()

    # Pattern mappings for tech/AI/science topics
    if "edge" in lower and ("ai" in lower or "infer" in lower):
        title = "Why Edge AI Changes Everything ⚡"
    elif "latency" in lower:
        title = "How to Crush Latency in 15 Seconds ⏱️"
    elif "neural" in lower or "silicon" in lower:
        title = "The Secret Power of Local Silicon 🧠"
    elif "autonomous" in lower:
        title = "The Architecture of Autonomous Systems 🚀"
    elif lower.startswith("why "):
        title = f"{topic.title()} 💡"
    elif lower.startswith("how to "):
        action = topic[7:].strip().title()
        title = f"The Secret to {action} ⚡"
    else:
        title = f"{topic.title()} (Explained) 🧠"

    # Ensure length with #Shorts is optimal
    if not title.endswith("#Shorts"):
        title = f"{title} #Shorts"

    return title


def synthesize_yt_description(
    topic: str,
    script_beats: List[str] = None,
    bullet_takeaways: List[str] = None,
    hashtags: List[str] = None,
) -> str:
    """
    Generates a structured, algorithmic YouTube Shorts description.
    """
    if script_beats is None:
        script_beats = []
    if bullet_takeaways is None:
        bullet_takeaways = [
            "Local neural inference slashes roundtrip latency to single-digit milliseconds.",
            "Eliminates cloud overhead and guarantees offline privacy.",
            "Pure autonomous velocity at enterprise scale."
        ]

    # Default tech/AI hashtags
    default_hashtags = [
        "#Shorts",
        "#ArtificialIntelligence",
        "#Tech",
        "#Coding",
        "#SoftwareEngineering",
        "#EdgeAI",
        "#MachineLearning",
        "#Developer",
        "#ComputerScience"
    ]
    if hashtags:
        combined_tags = list(dict.fromkeys(["#Shorts"] + hashtags + default_hashtags))
    else:
        combined_tags = default_hashtags

    hook_section = script_beats[0] if script_beats else f"Why is modern computing moving away from centralized cloud clusters? Here is the real physics behind it."
    
    body_lines = [
        hook_section,
        "",
        "Key takeaways:",
        *[f"• {point}" for point in bullet_takeaways],
        "",
        "Built with Manim Community Edition & Python motion graphics.",
        "",
        " ".join(combined_tags[:10])
    ]

    return "\n".join(body_lines)


def synthesize_yt_tags(topic: str, extra_tags: List[str] = None) -> List[str]:
    """
    Returns search query tags for YouTube SEO ranking.
    """
    base_tags = [
        "Shorts",
        "YouTube Shorts",
        "AI",
        "Artificial Intelligence",
        "Machine Learning",
        "Edge Computing",
        "Software Architecture",
        "Tech Explained",
        "Data in Motion",
        "Programming",
        "Computer Science",
        "Manim Python"
    ]
    if extra_tags:
        for t in extra_tags:
            if t not in base_tags:
                base_tags.append(t)
    return base_tags[:15]


def generate_video_metadata(
    topic: str,
    script_beats: List[str] = None,
    bullet_takeaways: List[str] = None,
    extra_hashtags: List[str] = None,
    category_id: str = "28",  # 28 = Science & Technology
    privacy_status: str = "public",
) -> Dict[str, Any]:
    """
    Master metadata generator returning ready-to-publish metadata package.
    """
    clean_topic = clean_topic_slug(topic)
    title = synthesize_yt_title(topic, script_beats[0] if script_beats else "")
    description = synthesize_yt_description(topic, script_beats, bullet_takeaways, extra_hashtags)
    tags = synthesize_yt_tags(topic)
    pinned_comment = (
        "⚡ The Protocol: Local compute beats centralized latency every single time. "
        "What edge model are you deploying this year? Tell us below 👇"
    )

    return {
        "topic": clean_topic,
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": category_id,
        "privacyStatus": privacy_status,
        "pinnedComment": pinned_comment
    }
