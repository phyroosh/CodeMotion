"""
Reusable, production-grade 2D vector motion design components for Manim.
"""

import numpy as np
from manim import *
from .theme import OnyxCyber, TYPOGRAPHY, LAYOUT
from .easings import snappy_overshoot, ease_out_cubic, ease_in_out_cubic


class BentoCard(VGroup):
    """
    Sleek, rounded container card with hairline border and optional badge.
    """

    def __init__(
        self,
        width: float = 5.0,
        height: float = 3.2,
        corner_radius: float = LAYOUT["corner_radius"],
        bg_color: str = OnyxCyber.card_bg,
        border_color: str = OnyxCyber.card_border,
        bg_opacity: float = LAYOUT["card_opacity"],
        border_width: float = LAYOUT["stroke_hairline"],
        badge_text: str = None,
        badge_color: str = OnyxCyber.accent_primary,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            fill_color=bg_color,
            fill_opacity=bg_opacity,
            stroke_color=border_color,
            stroke_width=border_width,
        )
        self.add(self.card)

        if badge_text:
            badge_label = Text(
                badge_text.upper(),
                font=TYPOGRAPHY["font"],
                font_size=12,
                weight=BOLD,
                color=badge_color,
            )
            badge_box = RoundedRectangle(
                width=badge_label.width + 0.35,
                height=badge_label.height + 0.2,
                corner_radius=0.08,
                fill_color=badge_color,
                fill_opacity=0.15,
                stroke_color=badge_color,
                stroke_width=1.0,
                stroke_opacity=0.6,
            )
            badge_group = VGroup(badge_box, badge_label)
            badge_group.move_to(
                self.card.get_corner(UL) + RIGHT * (badge_box.width / 2 + 0.28) + DOWN * 0.35
            )
            self.badge = badge_group
            self.add(self.badge)


class MetricCounter(VGroup):
    """
    Live numeric counter with ValueTracker, formatted suffixes, and anchored rendering.
    """

    def __init__(
        self,
        start_val: float = 0,
        end_val: float = 100,
        prefix: str = "",
        suffix: str = "",
        decimals: int = 0,
        font: str = TYPOGRAPHY["font"],
        font_size: int = TYPOGRAPHY["hero_size"],
        color: str = OnyxCyber.text_primary,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.tracker = ValueTracker(start_val)
        self.end_val = end_val
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.font = font
        self.font_size = font_size
        self.color = color

        # Invisible anchor to prevent displacement during value updates
        self.anchor = Dot(point=ORIGIN, fill_opacity=0, stroke_opacity=0, radius=0.01)
        self.add(self.anchor)

        self.label = always_redraw(self._create_label)
        self.add(self.label)

    def _create_label(self):
        val = self.tracker.get_value()
        if self.decimals > 0:
            formatted = f"{val:.{self.decimals}f}"
        else:
            formatted = f"{int(round(val))}"
        txt = Text(
            f"{self.prefix}{formatted}{self.suffix}",
            font=self.font,
            font_size=self.font_size,
            weight=BOLD,
            color=self.color,
        )
        txt.move_to(self.anchor.get_center())
        return txt

    def count_to(self, target: float = None, duration: float = 1.8, rate_func=None):
        if target is None:
            target = self.end_val
        if rate_func is None:
            rate_func = ease_out_cubic
        return self.tracker.animate(rate_func=rate_func, run_time=duration).set_value(target)


class KineticText(VGroup):
    """
    Text block split into word vectors for staggered kinetic entrances.
    """

    def __init__(
        self,
        text: str,
        font: str = TYPOGRAPHY["font"],
        font_size: int = TYPOGRAPHY["h1_size"],
        color: str = OnyxCyber.text_primary,
        weight: str = BOLD,
        buff: float = 0.16,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.words = VGroup()
        for w in text.split(" "):
            self.words.add(
                Text(w, font=font, font_size=font_size, weight=weight, color=color)
            )
        self.words.arrange(RIGHT, buff=buff)
        self.add(self.words)

    def reveal_animation(self, lag_ratio: float = 0.08, shift_vector=UP * 0.35, duration: float = 0.9):
        anims = [
            FadeIn(word, shift=shift_vector, rate_func=ease_out_cubic)
            for word in self.words
        ]
        return LaggedStart(*anims, lag_ratio=lag_ratio, run_time=duration)


class PulsingNode(VGroup):
    """
    Vector network node with glowing core and breathing outer halo.
    """

    def __init__(
        self,
        radius: float = 0.22,
        core_color: str = OnyxCyber.accent_primary,
        halo_color: str = OnyxCyber.accent_primary,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.core = Dot(radius=radius, color=core_color)
        self.halo = Circle(
            radius=radius * 1.8,
            stroke_color=halo_color,
            stroke_width=1.5,
            stroke_opacity=0.4,
            fill_color=halo_color,
            fill_opacity=0.08,
        )
        self.add(self.halo, self.core)


class DataWire(VGroup):
    """
    Subtle static wire with a high-voltage traveling packet pulse.
    """

    def __init__(
        self,
        start_pt,
        end_pt,
        control_pt_1=None,
        control_pt_2=None,
        wire_color: str = OnyxCyber.card_border,
        pulse_color: str = OnyxCyber.accent_primary,
        **kwargs
    ):
        super().__init__(**kwargs)
        if control_pt_1 is None:
            control_pt_1 = (start_pt + end_pt) / 2 + UP * 0.5
        if control_pt_2 is None:
            control_pt_2 = (start_pt + end_pt) / 2 + DOWN * 0.5

        self.path = CubicBezier(start_pt, control_pt_1, control_pt_2, end_pt)
        self.static_wire = self.path.copy().set_stroke(
            color=wire_color, width=1.5, opacity=0.4
        )
        self.pulse_color = pulse_color
        self.add(self.static_wire)

    def flash_animation(self, duration: float = 1.4, time_width: float = 0.3):
        return ShowPassingFlash(
            self.path.copy().set_stroke(color=self.pulse_color, width=3.5),
            time_width=time_width,
            run_time=duration,
            rate_func=ease_in_out_cubic,
        )


class RadialMeter(VGroup):
    """
    Circular arc meter with background track and animated progress arc.
    """

    def __init__(
        self,
        radius: float = 1.0,
        stroke_width: float = 6.0,
        track_color: str = OnyxCyber.card_border,
        accent_color: str = OnyxCyber.accent_primary,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.track = Arc(
            radius=radius,
            start_angle=0,
            angle=TAU,
            stroke_color=track_color,
            stroke_width=stroke_width,
            stroke_opacity=0.35,
        )
        self.accent_color = accent_color
        self.stroke_width = stroke_width
        self.progress_tracker = ValueTracker(0.0)

        # Dynamic arc pinned to track center
        self.progress_arc = always_redraw(
            lambda: Arc(
                radius=self.radius,
                start_angle=PI / 2,
                angle=-TAU * np.clip(self.progress_tracker.get_value(), 0.001, 1.0),
                stroke_color=self.accent_color,
                stroke_width=self.stroke_width,
                arc_center=self.track.get_center(),
            )
        )
        self.add(self.track, self.progress_arc)

    def fill_to(self, fraction: float, duration: float = 1.5):
        return self.progress_tracker.animate(
            run_time=duration, rate_func=ease_out_cubic
        ).set_value(fraction)


def create_grid_background(
    width: float = 14.0,
    height: float = 8.0,
    step: float = 1.0,
    dot_color: str = OnyxCyber.card_border,
    dot_radius: float = 0.02,
    opacity: float = 0.35,
) -> VGroup:
    """
    Subtle technical micro-dot matrix background.
    """
    dots = VGroup()
    xs = np.arange(-width / 2, width / 2 + step, step)
    ys = np.arange(-height / 2, height / 2 + step, step)
    for x in xs:
        for y in ys:
            d = Dot(point=[x, y, 0], radius=dot_radius, color=dot_color, fill_opacity=opacity)
            dots.add(d)
    return dots
