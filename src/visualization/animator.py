"""SortAnimator: drives the step-by-step animation using a generator."""

from __future__ import annotations

import itertools
import logging
from collections.abc import Generator
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.container import BarContainer

from src.visualization.renderer import (
    create_hud_texts,
    draw_bars,
    update_hud,
)

logger = logging.getLogger(__name__)

Frame = tuple[list[float], list[int], dict[str, Any]]


class SortAnimator:
    """Manages animation of a single sorting algorithm.

    Stores all generated frames in a cache, supports pause/step.
    """

    def __init__(
        self,
        algorithm_generator: Generator[Frame, None, None],
        interval: int = 50,
        blit: bool = True,
    ) -> None:
        """Initialise the animator.

        Args:
            algorithm_generator: Generator yielding
                (array, highlights, stats) tuples.
            interval: Milliseconds between frames.
            blit: Whether to use blitting for performance.
        """
        self._generator = algorithm_generator
        self._interval = interval
        self._blit = blit

        self._frames: list[Frame] = []
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self._bars: BarContainer | None = None
        self._hud_texts = create_hud_texts(self.ax)

        self._anim_finished = False
        self._window_closed = False
        self.ani: FuncAnimation | None = None

        self._load_first_frame()

        self.fig.canvas.mpl_connect("close_event", self._on_window_close)
        self.fig.canvas.mpl_connect("key_press_event", self._on_key_press)

    def _load_first_frame(self) -> None:
        """Extract initial frame from generator and cache it."""
        try:
            first_frame = next(self._generator)
            self._frames.append(first_frame)
        except StopIteration:
            logger.error("Generator yielded no frames (empty).")
            raise RuntimeError("Algorithm must yield at least one frame.")

    def _on_window_close(self, event: Any) -> None:
        """Handle figure close event: stop animation, mark closed."""
        self._window_closed = True
        if self.ani is not None:
            self.ani.event_source.stop()

    def _on_key_press(self, event: Any) -> None:
        """Handle key presses: Space for pause/resume, Right for step."""
        if event.key == " ":
            self._toggle_pause()
        elif event.key == "right":
            self._step_forward()

    def _toggle_pause(self) -> None:
        """Pause or resume the animation."""
        if self.ani is None or self.ani.event_source is None:
            return
        if self.ani.event_source.running():
            self.ani.event_source.stop()
            logger.debug("Animation paused.")
        else:
            self.ani.event_source.start()
            logger.debug("Animation resumed.")

    def _step_forward(self) -> None:
        """Advance by one frame, stopping if necessary."""
        if self._anim_finished:
            return
        if self.ani is not None and self.ani.event_source.running():
            self.ani.event_source.stop()
        self._add_frame(len(self._frames))
        self.fig.canvas.draw_idle()

    def init_func(self) -> list[Any]:
        """Initialize the plot with the first cached frame."""
        array, highlights, stats = self._frames[0]
        self._bars = draw_bars(self.ax, array, highlights)
        update_hud(
            self._hud_texts,
            stats["comparisons"],
            stats["swaps"],
            stats["aux_elements"],
            stats["elapsed_time"],
        )
        if self._blit:
            return [self._bars] + list(self._hud_texts)
        return []

    def update(self, frame_index: int) -> list[Any]:
        """Animation update function.

        Args:
            frame_index: Sequential frame number.

        Returns:
            Iterable of changed artists for blitting.
        """
        if self._anim_finished or self._window_closed:
            return []
        self._add_frame(frame_index)
        return self._draw_current_frame()

    def _add_frame(self, frame_index: int) -> None:
        """Ensure cache has frame at given index."""
        while len(self._frames) <= frame_index:
            try:
                new_frame = next(self._generator)
                self._frames.append(new_frame)
            except StopIteration:
                self._anim_finished = True
                if self.ani is not None:
                    self.ani.event_source.stop()
                last_array = self._frames[-1][0]
                if not all(
                    last_array[i] <= last_array[i + 1]
                    for i in range(len(last_array) - 1)
                ):
                    logger.error("Algorithm did not sort correctly!")
                else:
                    logger.info("Sorting completed successfully.")
                return

    def _draw_current_frame(self) -> list[Any]:
        """Redraw the last frame in cache and return artists."""
        array, highlights, stats = self._frames[-1]
        self._bars = draw_bars(self.ax, array, highlights)
        update_hud(
            self._hud_texts,
            stats["comparisons"],
            stats["swaps"],
            stats["aux_elements"],
            stats["elapsed_time"],
        )
        if self._blit:
            return [self._bars] + list(self._hud_texts)
        return []

    def start(self) -> None:
        """Create FuncAnimation and show the plot."""
        self.ani = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init_func,
            frames=itertools.count(start=1),
            interval=self._interval,
            blit=self._blit,
            repeat=False,
            cache_frame_data=False,
        )
        plt.show()

        if not self._window_closed:
            self._window_closed = True
            if self.ani is not None:
                self.ani.event_source.stop()
        plt.close(self.fig)
        logger.debug("Animation window closed.")
