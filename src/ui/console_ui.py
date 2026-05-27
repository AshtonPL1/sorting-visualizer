"""Console interface: argument parsing, batch and interactive modes."""

from __future__ import annotations

import argparse
import logging
import sys

from src.algorithms import (
    ALGORITHM_REGISTRY,
    get_algorithm_class,
    get_available_algorithms,
)
from src.algorithms.base import AlgorithmIncompatibleError
from src.config import MAX_ARRAY_SIZE
from src.data.generator import generate_random_array
from src.visualization.exporter import (
    FFmpegNotFoundError,
    _generator_to_frames,
    export_csv,
    export_gif,
    export_json,
    export_mp4,
    filter_key_frames,
)

logger = logging.getLogger(__name__)


def parse_array_input(
    user_input: str,
) -> list[int | float] | None:
    """
    Parse a string of numbers separated by spaces or commas.
    Returns list of int/float or None if invalid.
    """
    if not user_input.strip():
        return None
    parts = user_input.replace(",", " ").split()
    numbers: list[int | float] = []
    for part in parts:
        try:
            numbers.append(int(part))
        except ValueError:
            try:
                numbers.append(float(part))
            except ValueError:
                return None
    return numbers


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Sorting Algorithm Visualizer"
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        help="Sorting algorithm to use",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help="Size of random array to generate",
    )
    parser.add_argument(
        "--array",
        type=str,
        default=None,
        help="Comma/space-separated list of numbers",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=50,
        help="Animation interval in milliseconds (default: 50)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch interactive mode (ignores other arguments)",
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("ALGO1", "ALGO2"),
        help="Compare two algorithms",
    )
    parser.add_argument("--export-csv", type=str, help="Export to CSV")
    parser.add_argument("--export-json", type=str, help="Export to JSON")
    parser.add_argument("--export-gif", type=str, help="Export to GIF")
    parser.add_argument("--export-mp4", type=str, help="Export to MP4")
    parser.add_argument(
        "--trace-step",
        choices=["all", "key"],
        default="key",
        help="Trace granularity (default: key)",
    )
    return parser


def run_pipeline(args: argparse.Namespace) -> None:
    """Execute batch mode: generate/load array, run animation or export."""
    from src.visualization.animator import SortAnimator

    # --- Algorithm ---
    if not args.algorithm:
        print(
            "Error: --algorithm is required in batch mode.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        algo_cls = get_algorithm_class(args.algorithm)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Array ---
    if args.array is not None:
        raw_array = parse_array_input(args.array)
        if raw_array is None:
            print("Error: invalid --array value.", file=sys.stderr)
            sys.exit(1)
        if len(raw_array) > MAX_ARRAY_SIZE:
            print(
                f"Error: array length {len(raw_array)} exceeds "
                f"maximum {MAX_ARRAY_SIZE}.",
                file=sys.stderr,
            )
            sys.exit(1)
        array: list[float] | list[int] = raw_array
    elif args.size is not None:
        if args.size <= 0 or args.size > MAX_ARRAY_SIZE:
            print(
                f"Error: --size must be between 1 and {MAX_ARRAY_SIZE}.",
                file=sys.stderr,
            )
            sys.exit(1)
        array = generate_random_array(args.size)
    else:
        array = generate_random_array(32)

    # --- Compatibility ---
    try:
        if hasattr(algo_cls, "check_compatibility"):
            algo_cls.check_compatibility(array)
    except AlgorithmIncompatibleError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Interval ---
    interval = args.interval
    if interval <= 0:
        print("Error: --interval must be positive.", file=sys.stderr)
        sys.exit(1)

    # --- Export CSV/JSON ---
    if args.export_csv or args.export_json:
        sorter = algo_cls()
        gen = sorter.sort(array)
        frames = _generator_to_frames(gen)
        if args.trace_step == "key":
            frames = filter_key_frames(frames)
        if args.export_csv:
            export_csv(frames, args.export_csv)
        if args.export_json:
            export_json(frames, args.export_json)
        return

    # --- Export GIF/MP4 ---
    if args.export_gif:
        sorter = algo_cls()
        gen = sorter.sort(array)
        export_gif(gen, args.export_gif, interval=interval)
        return
    if args.export_mp4:
        sorter = algo_cls()
        gen = sorter.sort(array)
        try:
            export_mp4(gen, args.export_mp4, interval=interval)
        except FFmpegNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # --- Normal animation ---
    sorter = algo_cls()
    gen = sorter.sort(array)
    animator = SortAnimator(gen, interval=interval, blit=False)
    try:
        animator.start()
    except Exception as e:
        logger.exception("Animation failed.")
        print(f"Animation error: {e}", file=sys.stderr)
        sys.exit(1)


def interactive_loop() -> None:
    """Main interactive session with user prompts and animation."""
    from src.config_io import load_settings, save_settings
    from src.visualization.animator import SortAnimator

    settings = load_settings()
    available = get_available_algorithms()
    if not available:
        print("No algorithms registered. Exiting.")
        return

    while True:
        print("\nAvailable algorithms:")
        for name in available:
            print(f"  {name}")
        algo_name = input(
            f"Algorithm [default: {settings['last_algorithm']}]: "
        ).strip()
        if not algo_name:
            algo_name = str(settings["last_algorithm"])
        if algo_name not in ALGORITHM_REGISTRY:
            print(f"Unknown algorithm '{algo_name}'. Try again.")
            continue

        # --- Get array ---
        choice = (
            input("Generate random array (r) or enter manually (m)? [r]: ")
            .strip()
            .lower()
        )
        if choice == "m":
            array: list[int | float] = []
            while array is None:
                raw = input("Enter numbers (space/comma-separated): ")
                array = parse_array_input(raw)
                if array is None:
                    print("Invalid input. Use numbers only.")
                elif len(array) > MAX_ARRAY_SIZE:
                    print(
                        f"Length {len(array)} exceeds limit "
                        f"{MAX_ARRAY_SIZE}."
                    )
                    ans = (
                        input("Keep first 512 (k) or re-enter (r)? [k]: ")
                        .strip()
                        .lower()
                    )
                    if ans == "r":
                        array = None
                    else:
                        array = array[:MAX_ARRAY_SIZE]
        else:
            size_str = input(
                f"Array size [default: {settings['array_size']}]: "
            ).strip()
            try:
                size = (
                    int(size_str) if size_str else int(settings["array_size"])
                )
                if size > MAX_ARRAY_SIZE:
                    print(
                        f"Max size is {MAX_ARRAY_SIZE}, " "using that instead."
                    )
                    size = MAX_ARRAY_SIZE
                data = generate_random_array(size)
            except ValueError:
                print("Invalid number, using default size.")
                data = generate_random_array(int(settings["array_size"]))
            array = data

        # --- Check compatibility ---
        algo_cls = get_algorithm_class(algo_name)
        try:
            if hasattr(algo_cls, "check_compatibility"):
                algo_cls.check_compatibility(array)
        except AlgorithmIncompatibleError as e:
            print(f"Incompatible: {e}")
            continue

        # --- Speed ---
        interval_str = input(
            f"Interval ms [default: {settings['speed_interval']}]: "
        ).strip()
        try:
            interval = (
                int(interval_str)
                if interval_str
                else int(settings["speed_interval"])
            )
            if interval <= 0:
                raise ValueError
        except ValueError:
            print("Invalid interval, using default 50 ms.")
            interval = 50

        # --- Run animation ---
        sorter = algo_cls()
        gen = sorter.sort(array)
        animator = SortAnimator(gen, interval=interval, blit=False)
        try:
            animator.start()
        except Exception as e:
            logger.exception("Animation failed.")
            print(f"Animation error: {e}")

        # --- Ask to repeat ---
        again = input("Run again? (y/n) [n]: ").strip().lower()
        if again != "y":
            settings["last_algorithm"] = algo_name
            settings["array_size"] = len(array)
            settings["speed_interval"] = interval
            save_settings(settings)
            print("Settings saved. Bye!")
            break


def main() -> None:
    """Entry point: parse arguments and branch to mode."""
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    )

    if args.interactive:
        ignored = {
            k: v
            for k, v in vars(args).items()
            if v not in (None, False, []) and k != "interactive"
        }
        if ignored:
            logger.warning(
                "Ignored arguments due to --interactive: %s", ignored
            )
            print(
                "Warning: other arguments are ignored " "in interactive mode.",
                file=sys.stderr,
            )
        interactive_loop()
        return

    if args.compare and (
        args.export_csv
        or args.export_json
        or args.export_gif
        or args.export_mp4
    ):
        print(
            "Error: --compare cannot be used with --export-*.",
            file=sys.stderr,
        )
        sys.exit(1)

    any_action = any(
        [
            args.algorithm,
            args.size,
            args.array,
            args.compare,
            args.export_csv,
            args.export_json,
            args.export_gif,
            args.export_mp4,
        ]
    )
    if any_action:
        run_pipeline(args)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
