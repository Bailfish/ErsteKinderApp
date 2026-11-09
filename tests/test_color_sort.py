"""Unit tests for the Color Sort (Farbsortierspiel) engine and generator."""

import pytest
from app.games.color_sort.engine import ColorSortEngine
from app.games.color_sort.generator import generate_solvable_tubes


def test_generator_creates_valid_solvable_tubes() -> None:
    for diff, expected_tubes in (("easy", 5), ("medium", 7), ("hard", 9)):
        tubes = generate_solvable_tubes(difficulty=diff, seed=123)
        assert len(tubes) == expected_tubes
        assert tubes[-1] == []
        assert tubes[-2] == []
        non_empty = tubes[:-2]
        assert all(len(t) == 4 for t in non_empty)


def test_color_sort_pour_undo_and_win() -> None:
    initial = [
        ["red", "red", "red", "blue"],
        ["blue", "blue", "blue", "red"],
        [],
    ]
    engine = ColorSortEngine(tubes=initial)
    assert not engine.is_solved()
    assert len(engine.get_valid_moves()) > 0

    # Pour top 'blue' from tube 0 into empty tube 2
    moved = engine.pour(0, 2)
    assert moved == 1
    assert engine.tubes[2] == ["blue"]

    # Pour top 'red' from tube 1 onto 'red' in tube 0
    moved_red = engine.pour(1, 0)
    assert moved_red == 1
    assert engine.is_tube_complete(0) is True

    # Undo and re-do
    assert engine.undo() is True
    assert engine.is_tube_complete(0) is False
    engine.pour(1, 0)

    # Pour remaining 3 'blue' from tube 1 into tube 2
    moved_blues = engine.pour(1, 2)
    assert moved_blues == 3
    assert engine.is_solved() is True
    assert engine.get_state()["is_solved"] is True


def test_color_sort_invalid_pours() -> None:
    initial = [
        ["red", "red", "red", "blue"],
        ["green", "green", "green", "yellow"],
        [],
    ]
    engine = ColorSortEngine(tubes=initial)
    assert engine.undo() is False
    assert engine.can_pour(0, 0) is False
    assert engine.can_pour(-1, 2) is False
    assert engine.can_pour(2, 0) is False  # source empty
    assert engine.can_pour(0, 1) is False  # target full & wrong color

    with pytest.raises(ValueError):
        engine.pour(0, 1)
