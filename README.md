# Sorting Visualizer

An educational tool that visualizes six classic sorting algorithms with
step‑by‑step animation and real‑time metrics.

![Demo Animation](quick_sort.gif)

## Features

- **Six algorithms**: [Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort), [Insertion Sort](https://en.wikipedia.org/wiki/Insertion_sort), [Merge Sort](https://en.wikipedia.org/wiki/Merge_sort), [Quick Sort](https://en.wikipedia.org/wiki/Quicksort),
  [Heap Sort](https://en.wikipedia.org/wiki/Heapsort), [Counting Sort](https://en.wikipedia.org/wiki/Counting_sort).
- **Step‑by‑step animation** with highlighted comparisons and swaps.
- **Real‑time HUD**: comparisons, swaps, auxiliary memory used, and elapsed
  time (pauses excluded).
- **Two operating modes**:
  - *Interactive*: guided console prompts to choose algorithm, array, and speed.
  - *Batch*: command‑line arguments (e.g. `--algorithm bubble --size 50 --interval 50`).
- **Playback controls**: pause/resume (`Space`) and frame‑by‑frame step (`→`).
- **Export**:
  - Save animation as **GIF** or **MP4**.
  - Save trace states as **CSV** or **JSON** (all frames or key frames only).
- **Algorithm comparison** (upcoming) – side‑by‑side synchronized animation.
- **User settings persistence** between interactive sessions.
- **Cross‑platform**: Windows, macOS, Linux.

## Quick start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sorting-visualizer.git
   cd sorting-visualizer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Launch interactive mode:
   ```bash
   python -m src.ui.console_ui --interactive
   ```
   or run in batch mode:
   ```bash
   python -m src.ui.console_ui --algorithm bubble --size 20 --interval 100
   ```

5. Export an animation:
   ```bash
   python -m src.ui.console_ui --algorithm quick --size 30 --export-gif quick_sort.gif
   ```

## Available algorithms

| Algorithm      | Average complexity | Extra memory | Notes                                    |
|----------------|--------------------|--------------|------------------------------------------|
| Bubble Sort    | O(n²)              | O(1)         | Simple comparison‑based                   |
| Insertion Sort | O(n²)              | O(1)         | Efficient on partially sorted data       |
| Merge Sort     | O(n log n)         | O(n)         | Iterative bottom‑up implementation       |
| Quick Sort     | O(n log n)         | O(log n)*    | 3‑way partition, median‑of‑three pivot   |
| Heap Sort      | O(n log n)         | O(1)         | In‑place heap construction               |
| Counting Sort  | O(n + k)           | O(n + k)     | Non‑negative integers only               |

## Technologies

- Python 3.10+
- matplotlib (animation and drawing)
- numpy
- Pillow (GIF export)
- pytest (testing)
- black, ruff, mypy (code style and type checking)

## Educational value

This project was created to help students and developers **understand sorting
algorithms through direct visualisation**. Instead of dry theoretical
explanations or static diagrams, every comparison, swap, and memory allocation
is displayed in real time. You can slow down the animation, pause it, or step
through frame by frame – perfect for classrooms, self‑study, or workshops.

The source code itself is written to be a **learning resource**:
- Each algorithm is a **generator** that yields array snapshots, not a
  black‑box function.
- Clean separation of concerns: algorithm logic, rendering, animation control,
  and user interface live in independent modules.
- Full **type annotations** and rigorous linting (`ruff`, `black`, `mypy`)
  make the code predictable and easy to explore.
- Comprehensive **unit tests** ensure correctness and demonstrate how to
  validate generators.

## How it works (under the hood)

### 1. Algorithms as generators
Each sorting algorithm is implemented as a **class with a generator method**.
Instead of returning a sorted array once, the method `sort()` yields a tuple
after every *significant action* (swap, insertion, pivot selection):
```python
yield (array_copy, highlighted_indices, statistics)
```
- `array_copy` – a **new copy** of the current array so that previously stored
  frames never get overwritten.
- `highlighted_indices` – list of indices that will be colored differently in
  the next frame.
- `statistics` – a dictionary with `comparisons`, `swaps`, `aux_elements`
  (extra memory used), and `elapsed_time`.

The very first yield always returns the initial array with zero statistics.
This guarantees the animation starts from the original unsorted state.

### 2. Rendering and HUD
The `renderer.py` module draws vertical bars using `matplotlib`:
- Non‑highlighted bars are painted in a neutral gray, while highlighted ones
  receive bright colors from the `tab10` palette – a scheme friendly to
  colour‑blind viewers.
- Four persistent `Text` objects in the top‑left corner act as the HUD,
  updated on every frame without redrawing the entire axis.

### 3. Animator – the brain
`SortAnimator` (in `animator.py`) ties the generator to `FuncAnimation`:
- It maintains a **frame cache** (`_frames` list) so that stepping forward
  (right‑arrow key) always adds a frame, while stepping backward is instantly
  served from the cache.
- On generator exhaustion (`StopIteration`), the animation stops
  automatically, and the final array is validated to be sorted.
- Pause/resume is achieved by stopping/starting the event source; this does
  **not** advance the generator, so `elapsed_time` correctly excludes pauses.

### 4. Exporter
`exporter.py` can save the whole animation as GIF/MP4 or export frame data
as CSV/JSON:
- For video, the axes are set up once and bars are updated in‑place,
  avoiding costly `ax.clear()` calls that previously caused freezes.
- A **key‑frame filter** can be applied: it keeps only those frames where
  the array actually changed, which is especially useful for algorithms that
  yield many comparison‑only steps (though in our implementation every yield
  currently changes the array).

### 5. Console interface
`console_ui.py` handles both **interactive** and **batch** modes:
- Interactive mode asks step‑by‑step for algorithm, array (random or manual),
  and animation speed, then launches the visualisation.
- Batch mode accepts command‑line arguments (e.g. `--algorithm merge
  --size 100 --export-gif merge.gif`) and performs the action immediately.
- User preferences (last algorithm, size, speed) are stored in
  `~/.sorting_visualizer.ini` and reloaded in the next interactive session.

## Project structure

```
sorting-visualizer/
├── src/
│   ├── algorithms/        # Each algorithm in its own file (generator classes)
│   ├── data/              # Random array generator
│   ├── visualization/     # Animator, renderer, exporter, colour themes
│   ├── metrics/           # Placeholder for algorithm comparison feature
│   ├── ui/                # Console (CLI) and optional GUI
│   ├── config.py          # Global constants (max array size, colours, logging)
│   └── config_io.py       # Read/write user settings
├── tests/                 # Unit tests (pytest)
├── scripts/               # Setup & run scripts for Windows / Unix
├── docs/                  # Additional documentation
├── .github/workflows/     # CI pipeline (lint, type‑check, tests)
├── logs/                  # Application logs (gitignored)
├── pyproject.toml         # Build config, linter & formatter settings
├── requirements.txt       # Exact dependencies
└── README.md
```

## Testing and code quality

- **Pytest** unit tests cover every algorithm (initial frame, sorting
  correctness, frame independence, empty/single‑element arrays, and
  Counting‑Sort‑specific compatibility checks).
- **CI/CD** via GitHub Actions runs `ruff`, `black --check`, `mypy`, and
  `pytest` on Python 3.10–3.13 for every push and pull request.
- **Pre‑commit hooks** ensure consistent formatting and type safety before
  any commit leaves your machine.
- **Strict typing** with `mypy` in strict mode; all public functions and
  methods are fully annotated.

## License

This project is licensed under the MIT License. See [LICENSE](https://github.com/AshtonPL1/sorting-visualizer/blob/main/LICENSE) for details.

## Contact

Author: **Borovoy Nikita**  
Email: nurmag00@bk.ru  
GitHub: [AshtonPL1](https://github.com/AshtonPL1)
```

Скопируй весь этот блок (от `# Sorting Visualizer` до последней строки с GitHub-ссылкой) и вставь в свой `README.md`. После этого сделай `git commit` и `git push` — твой репозиторий засияет ещё ярче. Если нужно добавить скриншоты или ещё какие-то детали, я помогу.
