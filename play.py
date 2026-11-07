"""Interactive driver for the sliding number puzzle."""

from __future__ import annotations

from puzzle import NumberPuzzle


def main() -> None:
    print("Number Puzzle Game")
    size_input = input("Board size (default 4): ").strip()
    size = int(size_input) if size_input else 4
    puzzle = NumberPuzzle(size=size)
    puzzle.shuffle()

    print("Shuffled board. Moves: W/A/S/D or up/down/left/right. 'q' to quit, 'r' to reset.")
    while True:
        print()
        print(puzzle.render())
        print(f"Moves: {puzzle.moves}  |  Manhattan distance: {puzzle.manhattan_distance()}")
        if puzzle.is_solved():
            print(f"Solved in {puzzle.moves} moves!")
            break
        cmd = input("Move: ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            print("Goodbye.")
            break
        if cmd in ("r", "reset"):
            puzzle.reset()
            puzzle.shuffle()
            continue
        # allow moving a tile by number
        if cmd.isdigit():
            if puzzle.move_tile(int(cmd)):
                continue
            print("That tile cannot move right now.")
            continue
        if puzzle.move(cmd):
            continue
        print("Invalid move. Use w/a/s/d, up/down/left/right, a tile number, r, or q.")


if __name__ == "__main__":
    main()
