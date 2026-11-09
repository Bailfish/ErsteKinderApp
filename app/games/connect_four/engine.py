"""Clean domain engine for Connect Four (4 Gewinnt)."""

from enum import Enum
from typing import Any
from app.games.base import BaseGameEngine


class Disc( int, Enum):
    """Board cell values."""

    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2


class GameMode(str, Enum):
    """Game mode: against AI or second human player."""

    AI = "ai"
    PVP = "pvp"


class Difficulty(str, Enum):
    """AI difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ConnectFourEngine(BaseGameEngine):
    """Domain logic for 6x7 Connect Four game."""

    ROWS = 6
    COLS = 7

    def __init__(
        self,
        mode: GameMode = GameMode.AI,
        difficulty: Difficulty = Difficulty.EASY,
        game_id: str | None = None,
    ) -> None:
        super().__init__(game_id=game_id)
        self.mode: GameMode = GameMode(mode)
        self.difficulty: Difficulty = Difficulty(difficulty)
        self.board: list[list[int]] = []
        self.current_player: int = Disc.PLAYER_ONE
        self.winner: int | None = None
        self.is_draw: bool = False
        self.winning_cells: list[tuple[int, int]] = []
        self.move_history: list[dict[str, int]] = []
        self.reset()

    def reset(self) -> None:
        self.board = [[int(Disc.EMPTY) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = int(Disc.PLAYER_ONE)
        self.winner = None
        self.is_draw = False
        self.winning_cells = []
        self.move_history = []

    @property
    def is_game_over(self) -> bool:
        return self.winner is not None or self.is_draw

    def get_valid_columns(self) -> list[int]:
        if self.is_game_over:
            return []
        return [col for col in range(self.COLS) if self.board[0][col] == Disc.EMPTY]

    def drop_disc(self, column: int) -> dict[str, int]:
        """Drop a disc for the current player into the given column (0-6)."""
        if self.is_game_over:
            raise ValueError("Game is already over.")
        if column < 0 or column >= self.COLS:
            raise ValueError(f"Column {column} is out of bounds (0-{self.COLS - 1}).")
        if self.board[0][column] != Disc.EMPTY:
            raise ValueError(f"Column {column} is already full.")

        target_row = -1
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][column] == Disc.EMPTY:
                target_row = row
                break

        player = self.current_player
        self.board[target_row][column] = player
        move_info = {"row": target_row, "col": column, "player": player}
        self.move_history.append(move_info)

        win_coords = self.find_winning_line(self.board, player)
        if win_coords:
            self.winner = player
            self.winning_cells = win_coords
        elif all(self.board[0][c] != Disc.EMPTY for c in range(self.COLS)):
            self.is_draw = True
        else:
            self.current_player = (
                int(Disc.PLAYER_TWO)
                if player == Disc.PLAYER_ONE
                else int(Disc.PLAYER_ONE)
            )
        return move_info

    @classmethod
    def find_winning_line(
        cls, board: list[list[int]], player: int
    ) -> list[tuple[int, int]]:
        """Check horizontal, vertical, and both diagonal directions for 4 in a row."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(cls.ROWS):
            for c in range(cls.COLS):
                if board[r][c] != player:
                    continue
                for dr, dc in directions:
                    coords = [(r + i * dr, c + i * dc) for i in range(4)]
                    if all(
                        0 <= nr < cls.ROWS
                        and 0 <= nc < cls.COLS
                        and board[nr][nc] == player
                        for nr, nc in coords
                    ):
                        return coords
        return []

    def clone_board(self) -> list[list[int]]:
        return [row[:] for row in self.board]

    def get_state(self) -> dict[str, Any]:
        return {
            "game_id": self.game_id,
            "mode": self.mode.value,
            "difficulty": self.difficulty.value,
            "board": self.board,
            "rows": self.ROWS,
            "cols": self.COLS,
            "current_player": self.current_player,
            "winner": self.winner,
            "is_draw": self.is_draw,
            "is_game_over": self.is_game_over,
            "winning_cells": [list(cell) for cell in self.winning_cells],
            "valid_columns": self.get_valid_columns(),
            "move_count": len(self.move_history),
        }
