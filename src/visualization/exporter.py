"""Export animation to GIF/MP4 and trace states to CSV/JSON."""

from __future__ import annotations

import csv
import json
import logging
import os
import shutil
from collections.abc import Generator
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.container import BarContainer

from src.config import INACTIVE_COLOR
from src.visualization.renderer import (
    HIGHLIGHT_COLORS,
    create_hud_texts,
    update_hud,
)

logger = logging.getLogger(__name__)

Frame = tuple[list[float], list[int], dict[str, Any]]


class FFmpegNotFoundError(RuntimeError):
    """Raised when ffmpeg is not available for MP4 export."""


def _check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        msg = (
            "ffmpeg not found. Install ffmpeg to export MP4.\n"
            "Windows: choco install ffmpeg or download from ffmpeg.org\n"
            "macOS: brew install ffmpeg\n"
            "Linux: sudo apt install ffmpeg"
        )
        raise FFmpegNotFoundError(msg)


def _generator_to_frames(gen: Generator[Frame, None, None]) -> list[Frame]:
    frames: list[Frame] = []
    try:
        while True:
            frames.append(next(gen))
    except StopIteration:
        pass
    return frames


def filter_key_frames(frames: list[Frame]) -> list[Frame]:
    if not frames:
        return []
    key: list[Frame] = [frames[0]]
    for frame in frames[1:]:
        if frame[0] != key[-1][0]:
            key.append(frame)
    return key


def export_csv(frames: list[Frame], filename: str) -> None:
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "array", "highlights", "stats"])
        for i, (arr, hl, st) in enumerate(frames):
            writer.writerow([i, arr, hl, st])
    logger.info("Exported %d frames to CSV: %s", len(frames), filename)


def export_json(frames: list[Frame], filename: str) -> None:
    data = []
    for arr, hl, st in frames:
        data.append({"array": arr, "highlights": hl, "stats": st})
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    logger.info("Exported %d frames to JSON: %s", len(frames), filename)


def _setup_fixed_axes(ax: Any, n: int, max_val: float) -> Any:
    """Draw initial bars and configure axes without clearing later."""
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max_val * 1.1 if max_val > 0 else 1)
    if n <= 50:
        ax.set_xticks(range(n))
        ax.set_xticklabels([str(i) for i in range(n)])
    else:
        step = max(1, n // 50)
        ax.set_xticks(range(0, n, step))
        ax.set_xticklabels([str(i) for i in range(0, n, step)])
    bars = ax.bar(range(n), [0] * n, color=INACTIVE_COLOR, width=0.8)
    return bars


def _update_bars(
    bars: BarContainer, array: list[float], highlights: list[int]
) -> None:
    """Update bar heights and colors without recreating axes."""
    for i, bar in enumerate(bars):
        bar.set_height(array[i])
        if i in highlights:
            idx = highlights.index(i)
            bar.set_facecolor(HIGHLIGHT_COLORS[idx % len(HIGHLIGHT_COLORS)])
        else:
            bar.set_facecolor(INACTIVE_COLOR)


def export_gif(
    gen: Generator[Frame, None, None],
    filename: str,
    interval: int = 50,
) -> None:
    frames = _generator_to_frames(gen)
    if not frames:
        logger.error("No frames to export GIF.")
        return

    arr0, _, _ = frames[0]
    n = len(arr0)
    max_val = max(arr0) if arr0 else 1.0

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = _setup_fixed_axes(ax, n, max_val)
    hud_texts = create_hud_texts(ax)

    def animate(frame_data: Frame) -> list[Any]:
        arr, hl, st = frame_data
        _update_bars(bars, arr, hl)
        update_hud(
            hud_texts,
            st["comparisons"],
            st["swaps"],
            st["aux_elements"],
            st["elapsed_time"],
        )
        return [bars] + list(hud_texts)

    try:
        anim = FuncAnimation(
            fig,
            animate,
            frames=frames,
            interval=interval,
            blit=False,
            repeat=False,
            cache_frame_data=False,
        )
        anim.save(filename, writer="pillow", fps=int(1000 / interval))
        logger.info("GIF exported to %s", filename)
    except Exception as e:
        logger.exception("GIF export failed.")
        if os.path.exists(filename):
            os.remove(filename)
        raise e
    finally:
        plt.close(fig)


def export_mp4(
    gen: Generator[Frame, None, None],
    filename: str,
    interval: int = 50,
) -> None:
    _check_ffmpeg()
    frames = _generator_to_frames(gen)
    if not frames:
        logger.error("No frames to export MP4.")
        return

    arr0, _, _ = frames[0]
    n = len(arr0)
    max_val = max(arr0) if arr0 else 1.0

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = _setup_fixed_axes(ax, n, max_val)
    hud_texts = create_hud_texts(ax)

    def animate(frame_data: Frame) -> list[Any]:
        arr, hl, st = frame_data
        _update_bars(bars, arr, hl)
        update_hud(
            hud_texts,
            st["comparisons"],
            st["swaps"],
            st["aux_elements"],
            st["elapsed_time"],
        )
        return [bars] + list(hud_texts)

    try:
        anim = FuncAnimation(
            fig,
            animate,
            frames=frames,
            interval=interval,
            blit=False,
            repeat=False,
            cache_frame_data=False,
        )
        anim.save(filename, writer="ffmpeg", fps=int(1000 / interval))
        logger.info("MP4 exported to %s", filename)
    except Exception as e:
        logger.exception("MP4 export failed.")
        if os.path.exists(filename):
            os.remove(filename)
        raise e
    finally:
        plt.close(fig)
