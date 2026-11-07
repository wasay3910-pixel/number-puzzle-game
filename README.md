# Number Puzzle Game (Python)

An interactive sliding **N-puzzle** (15-puzzle) with input validation and
win-state detection.

## Features

* Configurable board size (default 4x4).
* Guaranteed-solvable shuffles (shuffled from the solved state).
* Move by direction (`w/a/s/d`, `up/down/left/right`) or by tile number.
* Move counter and Manhattan-distance heuristic display.
* Reset and quit commands.

## Run

```bash
python play.py
```

## Tests

```bash
python -m pytest -q
```

## Requirements

Python 3.10+. No external dependencies.

## License

MIT
