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

from src.visualization.renderer import create_hud_texts, draw_bars, update_hud

logger = logging.getLogger(__name__)

Frame = tuple[list[float], list[int], dict[str, Any]]


class FFmpegNotFoundError(RuntimeError):
    """Raised when ffmpeg is not available for MP4 export."""


def _check_ffmpeg() -> None:
    """Raise FFmpegNotFoundError if ffmpeg is not in PATH."""
    if shutil.which("ffmpeg") is None:
        msg = (
            "ffmpeg not found. Install ffmpeg to export MP4.\n"
            "Windows: choco install ffmpeg or download from ffmpeg.org\n"
            "macOS: brew install ffmpeg\n"
            "Linux: sudo apt install ffmpeg"
        )
        raise FFmpegNotFoundError(msg)


def _generator_to_frames(gen: Generator[Frame, None, None]) -> list[Frame]:
    """Exhaust the generator and return all frames."""
    frames: list[Frame] = []
    try:
        while True:
            frames.append(next(gen))
    except StopIteration:
        pass
    return frames


def filter_key_frames(
    frames: list[Frame],
) -> list[Frame]:
    """Return only frames where the array changed from previous key frame."""
    if not frames:
        return []
    key: list[Frame] = [frames[0]]
    for frame in frames[1:]:
        if frame[0] != key[-1][0]:
            key.append(frame)
    return key


def export_csv(
    frames: list[Frame],
    filename: str,
) -> None:
    """Save trace as CSV with columns: index, array, highlights, stats."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "array", "highlights", "stats"])
        for i, (arr, hl, st) in enumerate(frames):
            writer.writerow([i, arr, hl, st])
    logger.info("Exported %d frames to CSV: %s", len(frames), filename)


def export_json(
    frames: list[Frame],
    filename: str,
) -> None:
    """Save trace as JSON array of objects."""
    data = []
    for arr, hl, st in frames:
        data.append({"array": arr, "highlights": hl, "stats": st})
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    logger.info("Exported %d frames to JSON: %s", len(frames), filename)


def export_gif(
    gen: Generator[Frame, None, None],
    filename: str,
    interval: int = 50,
) -> None:
    """Save the sorting animation as a GIF file."""
    frames = _generator_to_frames(gen)
    if not frames:
        logger.error("No frames to export GIF.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    def animate(frame_data: Frame) -> list[Any]:
        ax.clear()
        arr, hl, st = frame_data
        draw_bars(ax, arr, hl)
        hud_texts = create_hud_texts(ax)
        update_hud(
            hud_texts,
            st["comparisons"],
            st["swaps"],
            st["aux_elements"],
            st["elapsed_time"],
        )
        return []

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
    """Save the sorting animation as an MP4 file."""
    _check_ffmpeg()
    frames = _generator_to_frames(gen)
    if not frames:
        logger.error("No frames to export MP4.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    def animate(frame_data: Frame) -> list[Any]:
        ax.clear()
        arr, hl, st = frame_data
        draw_bars(ax, arr, hl)
        hud_texts = create_hud_texts(ax)
        update_hud(
            hud_texts,
            st["comparisons"],
            st["swaps"],
            st["aux_elements"],
            st["elapsed_time"],
        )
        return []

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
