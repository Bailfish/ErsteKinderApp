"""Unit tests for Connect Four (4 Gewinnt) engine and AI difficulties."""

import random
import pytest
from app.games.connect_four.ai import ConnectFourAI
from app.games.connect_four.engine import ConnectFourEngine, Difficulty, Disc, GameMode


def test_connect_four_horizontal_win() -> None:
    engine = ConnectFourEngine(mode=GameMode.PVP)
    for col in range(3):
        engine.drop_disc(col)  # P1
        engine.drop_disc(col)  # P2
    engine.drop_disc(3)  # P1 completes 4 in bottom row (0, 1, 2, 3)

    assert engine.winner == Disc.PLAYER_ONE
    assert engine.is_game_over is True
    assert len(engine.winning_cells) == 4
    assert engine.get_valid_columns() == []

    with pytest.raises(ValueError):
        engine.drop_disc(4)


def test_connect_four_vertical_and_diagonal_wins() -> None:
    # Vertical win
    eng_v = ConnectFourEngine(mode=GameMode.PVP)
    for _ in range(3):
        eng_v.drop_disc(0)  # P1
        eng_v.drop_disc(1)  # P2
    eng_v.drop_disc(0)  # P1 wins vertically in col 0
    assert eng_v.winner == Disc.PLAYER_ONE

    # Diagonal win (\ or /)
    eng_d = ConnectFourEngine(mode=GameMode.PVP)
    # Build stairs for P1 at (5,0), (4,1), (3,2), (2,3)
    moves = [
        0, 1,  # (5,0)=P1, (5,1)=P2
        1, 2,  # (4,1)=P1, (5,2)=P2
        2, 3,  # (4,2)=P1, (5,3)=P2
        2, 3,  # (3,2)=P1, (4,3)=P2
        4, 3,  # (5,4)=P1, (3,3)=P2
        3,     # (2,3)=P1 -> Diagonal!
    ]
    for m in moves:
        eng_d.drop_disc(m)
    assert eng_d.winner == Disc.PLAYER_ONE


def test_connect_four_invalid_columns_and_full_column() -> None:
    engine = ConnectFourEngine(mode=GameMode.PVP)
    with pytest.raises(ValueError):
        engine.drop_disc(-1)
    with pytest.raises(ValueError):
        engine.drop_disc(7)

    for _ in range(6):
        engine.drop_disc(0)
    with pytest.raises(ValueError):
        engine.drop_disc(0)


def test_connect_four_ai_easy_medium_hard() -> None:
    rng = random.Random(42)
    for diff in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
        engine = ConnectFourEngine(mode=GameMode.AI, difficulty=diff)
        engine.drop_disc(3)  # P1 plays center
        ai_col = ConnectFourAI.choose_move(engine, difficulty=diff, rng=rng)
        assert 0 <= ai_col < 7
        engine.drop_disc(ai_col)
        assert engine.get_state()["move_count"] == 2


def test_connect_four_ai_takes_winning_move_and_blocks() -> None:
    engine = ConnectFourEngine(mode=GameMode.AI, difficulty=Difficulty.HARD)
    # P1 has 3 in a row at bottom (cols 0, 1, 2), P2 has 3 in col 6
    for col in range(3):
        engine.drop_disc(col)  # P1
        engine.drop_disc(6)    # P2
    # Now P1 plays col 5 (non-winning), so P2 can win immediately at col 6!
    engine.drop_disc(5)
    assert ConnectFourAI.choose_move(engine, difficulty=Difficulty.EASY) == 6
    assert ConnectFourAI.choose_move(engine, difficulty=Difficulty.MEDIUM) == 6
    assert ConnectFourAI.choose_move(engine, difficulty=Difficulty.HARD) == 6
