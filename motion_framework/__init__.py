"""
Manim Motion Design Framework
High-end, minimalist 2D vector animation, kinetic typography, and data-in-motion.
"""

from .theme import OnyxCyber, ObsidianEmerald, SolarGraphite, TYPOGRAPHY
from .easings import snappy_overshoot, smooth_drift, fast_out_slow_in
from .components import (
    BentoCard,
    MetricCounter,
    KineticText,
    PulsingNode,
    DataWire,
    RadialMeter,
    create_grid_background,
)
from .voice import (
    DEFAULT_VOICE,
    generate_voiceover,
    get_audio_duration,
    mux_video_audio,
    concatenate_audio_files,
    VoiceoverBeatSheet,
)
from .metadata import (
    generate_video_metadata,
    synthesize_yt_title,
    synthesize_yt_description,
    synthesize_yt_tags,
)
from .exporter import export_to_rightclips
from .publisher import upload_to_youtube
from .frontier_t import (
    FrontierTDirector,
    FrontierTValidator,
    FrontierThumbnailScene,
    render_frontier_thumbnail,
)
from .script_engine import (
    HookArchetype,
    BeatType,
    ScriptBeat,
    ValidationReport,
    ScriptValidator,
    VeteranScript,
    VeteranScriptDirector,
)

__all__ = [
    "OnyxCyber",
    "ObsidianEmerald",
    "SolarGraphite",
    "TYPOGRAPHY",
    "snappy_overshoot",
    "smooth_drift",
    "fast_out_slow_in",
    "BentoCard",
    "MetricCounter",
    "KineticText",
    "PulsingNode",
    "DataWire",
    "RadialMeter",
    "create_grid_background",
    "DEFAULT_VOICE",
    "generate_voiceover",
    "get_audio_duration",
    "mux_video_audio",
    "concatenate_audio_files",
    "VoiceoverBeatSheet",
    "generate_video_metadata",
    "synthesize_yt_title",
    "synthesize_yt_description",
    "synthesize_yt_tags",
    "export_to_rightclips",
    "upload_to_youtube",
    "FrontierTDirector",
    "FrontierTValidator",
    "FrontierThumbnailScene",
    "render_frontier_thumbnail",
    "HookArchetype",
    "BeatType",
    "ScriptBeat",
    "ValidationReport",
    "ScriptValidator",
    "VeteranScript",
    "VeteranScriptDirector",
]

