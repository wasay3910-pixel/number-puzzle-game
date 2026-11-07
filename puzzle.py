"""Sliding number puzzle (N-puzzle) on an N x N grid.

The board holds tiles numbered 1..N*N-1 and one blank (0). A move
slides a tile into the blank. The puzzle is always generated from the
solved state by random legal moves, so it is guaranteed solvable.
"""

from __future__ import annotations

import random
from typing import List, Tuple

Coord = Tuple[int, int]


class NumberPuzzle:
    """An N x N sliding number puzzle."""

    def __init__(self, size: int = 4, seed: int | None = None) -> None:
        if size < 2:
            raise ValueError("size must be at least 2")
        self.size = size
        self._rng = random.Random(seed)
        self.board: List[List[int]] = self._solved_board()
        self.moves = 0
        self._blank = (size - 1, size - 1)

    # ------------------------------------------------------------------ #
    # Construction helpers
    # ------------------------------------------------------------------ #
    def _solved_board(self) -> List[List[int]]:
        n = self.size
        board = [[r * n + c + 1 for c in range(n)] for r in range(n)]
        board[n - 1][n - 1] = 0
        return board

    def reset(self) -> None:
        """Reset to the solved state."""
        self.board = self._solved_board()
        self.moves = 0
        self._blank = (self.size - 1, self.size - 1)

    def shuffle(self, steps: int = 1000) -> None:
        """Shuffle by performing ``steps`` random legal moves.

        Shuffling from the solved state (instead of random permutation)
        guarantees the resulting configuration is solvable.
        """
        if steps < 1:
            raise ValueError("steps must be positive")
        self.reset()
        directions = ("up", "down", "left", "right")
        for _ in range(steps):
            # Keep trying until a legal move is made.
            while True:
                d = self._rng.choice(directions)
                if self.move(d, count_move=False):
                    break
        self.moves = 0

    # ------------------------------------------------------------------ #
    # State queries
    # ------------------------------------------------------------------ #
    @property
    def blank(self) -> Coord:
        return self._blank

    def is_solved(self) -> bool:
        return self.board == self._solved_board()

    def can_move(self, direction: str) -> bool:
        br, bc = self._blank
        n = self.size
        if direction == "up":
            return br > 0
        if direction == "down":
            return br < n - 1
        if direction == "left":
            return bc > 0
        if direction == "right":
            return bc < n - 1
        return False

    # ------------------------------------------------------------------ #
    # Moves
    # ------------------------------------------------------------------ #
    def move(self, direction: str, count_move: bool = True) -> bool:
        """Slide a tile into the blank in ``direction``.

        ``direction`` describes where the *tile* comes from relative to the
        blank: moving the blank "up" means the tile above slides down.
        Returns True on success.
        """
        direction = direction.strip().lower()
        alias = {
            "w": "up", "s": "down", "a": "left", "d": "right",
            "u": "up", "l": "left", "r": "right",
        }
        direction = alias.get(direction, direction)

        if not self.can_move(direction):
            return False

        br, bc = self._blank
        if direction == "up":
            sr, sc = br - 1, bc
        elif direction == "down":
            sr, sc = br + 1, bc
        elif direction == "left":
            sr, sc = br, bc - 1
        elif direction == "right":
            sr, sc = br, bc + 1
        else:
            return False

        self.board[br][bc], self.board[sr][sc] = self.board[sr][sc], self.board[br][bc]
        self._blank = (sr, sc)
        if count_move:
            self.moves += 1
        return True

    def move_tile(self, value: int) -> bool:
        """Move the tile with the given value into the blank if adjacent."""
        if value < 1 or value > self.size * self.size - 1:
            return False
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == value:
                    br, bc = self._blank
                    if abs(r - br) + abs(c - bc) == 1:
                        # slide tile into blank
                        self.board[br][bc], self.board[r][c] = self.board[r][c], self.board[br][bc]
                        self._blank = (r, c)
                        self.moves += 1
                        return True
                    return False
        return False

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def render(self) -> str:
        lines = []
        width = len(str(self.size * self.size - 1))
        for row in self.board:
            cells = []
            for v in row:
                cells.append(" " * width if v == 0 else str(v).rjust(width))
            lines.append(" | ".join(cells))
        return "\n".join(lines)

    def manhattan_distance(self) -> int:
        """Sum of Manhattan distances of tiles from their goal positions."""
        total = 0
        n = self.size
        for r in range(n):
            for c in range(n):
                v = self.board[r][c]
                if v == 0:
                    continue
                gr, gc = divmod(v - 1, n)
                total += abs(r - gr) + abs(c - gc)
        return total
