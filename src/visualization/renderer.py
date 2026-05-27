"""Rendering functions for the sorting visualizer."""

from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.text import Text

from src.config import INACTIVE_COLOR

# Palette of distinct colors for highlighted bars (tab10 subset).
HIGHLIGHT_COLORS = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
    "#7f7f7f",  # gray
    "#bcbd22",  # olive
    "#17becf",  # cyan
]


def draw_bars(
    ax: Axes, array: list[float], highlights: list[int]
) -> BarContainer:
    """
    Draw (or update) vertical bars on the given axes.

    Args:
        ax: matplotlib Axes to draw on.
        array: current values (heights).
        highlights: indices of bars to color specially.

    Returns:
        BarContainer of all bars (needed for blit).
    """
    ax.clear()
    n = len(array)
    colors = [INACTIVE_COLOR] * n
    for idx, bar_idx in enumerate(highlights):
        if bar_idx < n:
            colors[bar_idx] = HIGHLIGHT_COLORS[idx % len(HIGHLIGHT_COLORS)]

    bars = ax.bar(range(n), array, color=colors, width=0.8)

    # Configure axes
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max(array) * 1.1 if array else 1)
    ax.set_xticks(range(n))
    # Show all indices if small array, otherwise sparse
    if n <= 50:
        ax.set_xticklabels([str(i) for i in range(n)])
    else:
        step = max(1, n // 50)
        ax.set_xticks(range(0, n, step))
        ax.set_xticklabels([str(i) for i in range(0, n, step)])

    return bars


def create_hud_texts(ax: Axes) -> list[Text]:
    """
    Create persistent Text objects for HUD (comparisons, swaps,
    aux_elements, elapsed time). They will be updated in-place.

    Args:
        ax: matplotlib Axes to place HUD on.

    Returns:
        List of Text objects to be returned as artists for blit.
    """
    texts = []
    # Position in top-left of axes coordinates
    y_start = 0.95
    dy = 0.05

    for label in ["Comparisons", "Swaps", "Aux Mem", "Time"]:
        t = ax.text(
            0.02,
            y_start,
            f"{label}: 0",
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )
        texts.append(t)
        y_start -= dy

    return texts


def update_hud(
    hud_texts: list[Text],
    comparisons: int,
    swaps: int,
    aux_elements: int,
    elapsed_time: float,
) -> None:
    """Update the text objects with current statistics."""
    hud_texts[0].set_text(f"Comparisons: {comparisons}")
    hud_texts[1].set_text(f"Swaps: {swaps}")
    hud_texts[2].set_text(f"Aux Mem: {aux_elements}")
    hud_texts[3].set_text(f"Time: {elapsed_time:.4f}s")
