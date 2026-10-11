"""
Custom rate functions and physics curves for Manim.
"""

import numpy as np
from manim import rate_functions


def snappy_overshoot(overshoot: float = 0.15):
    """
    Creates an expressive ease-out-back curve with configurable overshoot.
    Perfect for pop-in elements, badges, metric count settles, and button clicks.
    """
    s = overshoot * 1.70158

    def func(t: float) -> float:
        t = t - 1.0
        return t * t * ((s + 1.0) * t + s) + 1.0

    return func


def fast_out_slow_in(t: float) -> float:
    """
    Quartic ease-out for rapid high-tempo entry with long luxurious settle.
    """
    return 1.0 - (1.0 - t) ** 4


def smooth_drift(t: float) -> float:
    """
    Gentle sine oscillation for breathing and ambient floating.
    """
    return (1.0 - np.cos(t * np.pi)) / 2.0


# Re-export key Manim rate functions for clean framework imports
ease_out_cubic = rate_functions.ease_out_cubic
ease_out_expo = rate_functions.ease_out_expo
ease_in_out_cubic = rate_functions.ease_in_out_cubic
ease_in_out_sine = rate_functions.ease_in_out_sine
