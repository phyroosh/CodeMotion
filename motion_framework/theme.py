"""
Theme tokens and visual design systems for Manim Motion Graphics.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    name: str
    bg: str
    card_bg: str
    card_border: str
    accent_primary: str
    accent_secondary: str
    accent_glow: str
    text_primary: str
    text_muted: str
    text_subtle: str


# Palette 1: Onyx Cyber (AI, DevTools, Infrastructure, SaaS)
OnyxCyber = Palette(
    name="Onyx Cyber",
    bg="#0A0B0E",
    card_bg="#13161F",
    card_border="#222838",
    accent_primary="#00F5FF",    # Electric Cyan
    accent_secondary="#7000FF",  # Neon Violet
    accent_glow="#00C8FF",
    text_primary="#F8FAFC",      # Crisp Off-White
    text_muted="#94A3B8",        # Slate
    text_subtle="#475569"        # Dark Slate
)

# Palette 2: Obsidian Emerald (Fintech, Growth, Metrics, Data)
ObsidianEmerald = Palette(
    name="Obsidian Emerald",
    bg="#080D0B",
    card_bg="#101A16",
    card_border="#1C3028",
    accent_primary="#00FFA3",    # High-Voltage Mint
    accent_secondary="#F59E0B",  # Amber
    accent_glow="#059669",
    text_primary="#F1F5F9",
    text_muted="#64748B",
    text_subtle="#334155"
)

# Palette 3: Solar Graphite (Studio, Hardware, Productivity)
SolarGraphite = Palette(
    name="Solar Graphite",
    bg="#0E0E11",
    card_bg="#18181D",
    card_border="#2B2B34",
    accent_primary="#FF553E",    # Coral
    accent_secondary="#FFB800",  # Gold
    accent_glow="#E11D48",
    text_primary="#FFFFFF",
    text_muted="#8E8E9B",
    text_subtle="#52525B"
)

# Typography Specifications
TYPOGRAPHY = {
    "font": "Inter",
    "font_display": "Inter Display",
    "hero_size": 54,
    "h1_size": 42,
    "h2_size": 32,
    "body_size": 22,
    "badge_size": 16,
    "caption_size": 14,
}

# Layout & Geometry Constants
LAYOUT = {
    "corner_radius": 0.16,
    "stroke_hairline": 1.5,
    "stroke_accent": 2.5,
    "card_opacity": 0.65,
    "safe_x": 5.8,
    "safe_y": 3.2,
}
