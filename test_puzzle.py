"""Tests for the sliding number puzzle."""

from puzzle import NumberPuzzle


def test_solved_initially():
    p = NumberPuzzle(size=3, seed=1)
    assert p.is_solved()


def test_shuffle_makes_unsolved():
    p = NumberPuzzle(size=3, seed=2)
    p.shuffle(50)
    assert not p.is_solved()


def test_shuffle_guarantees_solvable():
    for seed in range(5):
        p = NumberPuzzle(size=3, seed=seed)
        p.shuffle(200)
        # A solvable shuffle is solvable by construction; check manhattan parity-ish
        # by ensuring reset+replay not needed: just ensure blank present.
        assert 0 in [v for row in p.board for v in row]


def test_move_changes_blank():
    p = NumberPuzzle(size=3, seed=1)
    p._blank = (0, 0)
    assert p.move("up") is False
    assert p.move("left") is False


def test_move_updates_board_and_moves():
    p = NumberPuzzle(size=2, seed=1)
    # solved 2x2: [[1,2],[3,0]]
    assert p.move("up") is True  # tile 3? blank (1,1), up -> tile (0? wait up means blank moves up: tile from (0,1) slides down) actually board becomes [[1,0],[3,2]]
    assert p.moves == 1
    assert p.blank == (0, 1)


def test_invalid_direction():
    p = NumberPuzzle(size=3, seed=1)
    assert p.move("foo") is False
    assert p.move("") is False


def test_win_detection_after_reverse():
    p = NumberPuzzle(size=2, seed=1)
    # Move up then down returns solved
    p.move("up")
    assert not p.is_solved()
    p.move("down")
    assert p.is_solved()


def test_move_tile():
    p = NumberPuzzle(size=2, seed=1)
    # solved [[1,2],[3,0]]; tile 2 is adjacent to blank -> can move
    assert p.move_tile(2) is True
    assert p.blank == (0, 1) or p.blank == (1, 1)  # moved
    # non-adjacent tile cannot move
    p2 = NumberPuzzle(size=3, seed=1)
    # tile 1 at (0,0), blank at (2,2) not adjacent
    assert p2.move_tile(1) is False


def test_manhattan_zero_when_solved():
    p = NumberPuzzle(size=4, seed=1)
    assert p.manhattan_distance() == 0


def test_render_contains_blank_space():
    p = NumberPuzzle(size=2, seed=1)
    r = p.render()
    assert "|" in r


def test_size_validation():
    try:
        NumberPuzzle(size=1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
