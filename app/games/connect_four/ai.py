"""Connect Four AI opponents: Easy, Medium, and Hard (Minimax with Alpha-Beta Pruning)."""

import math
import random
from app.games.connect_four.engine import ConnectFourEngine, Difficulty, Disc


class ConnectFourAI:
    """AI opponent supporting easy, medium, and hard difficulty levels."""

    ROWS = ConnectFourEngine.ROWS
    COLS = ConnectFourEngine.COLS

    @classmethod
    def choose_move(
        cls,
        engine: ConnectFourEngine,
        difficulty: Difficulty | None = None,
        rng: random.Random | None = None,
    ) -> int:
        valid_cols = engine.get_valid_columns()
        if not valid_cols:
            raise ValueError("No valid columns available for AI move.")

        active_diff = Difficulty(difficulty or engine.difficulty)
        rand = rng or random.Random()
        ai_player = engine.current_player
        opp_player = (
            int(Disc.PLAYER_ONE)
            if ai_player == Disc.PLAYER_TWO
            else int(Disc.PLAYER_TWO)
        )
        board = engine.clone_board()

        if active_diff == Difficulty.EASY:
            for col in valid_cols:
                sim = cls._simulate_drop(board, col, ai_player)
                if ConnectFourEngine.find_winning_line(sim, ai_player):
                    return col
            return rand.choice(valid_cols)

        depth = 3 if active_diff == Difficulty.MEDIUM else 5
        col, _ = cls._minimax(
            board, depth, -math.inf, math.inf, True, ai_player, opp_player
        )
        return col if col is not None else valid_cols[0]

    @classmethod
    def _get_valid_cols(cls, board: list[list[int]]) -> list[int]:
        return [c for c in (3, 2, 4, 1, 5, 0, 6) if board[0][c] == Disc.EMPTY]

    @classmethod
    def _simulate_drop(
        cls, board: list[list[int]], col: int, player: int
    ) -> list[list[int]]:
        new_board = [row[:] for row in board]
        for r in range(cls.ROWS - 1, -1, -1):
            if new_board[r][col] == Disc.EMPTY:
                new_board[r][col] = player
                break
        return new_board

    @classmethod
    def _minimax(
        cls,
        board: list[list[int]],
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        ai_player: int,
        opp_player: int,
    ) -> tuple[int | None, float]:
        valid_cols = cls._get_valid_cols(board)
        if ConnectFourEngine.find_winning_line(board, ai_player):
            return None, 100000.0 + depth
        if ConnectFourEngine.find_winning_line(board, opp_player):
            return None, -100000.0 - depth
        if not valid_cols:
            return None, 0.0
        if depth == 0:
            return None, cls._evaluate_board(board, ai_player, opp_player)

        best_col = valid_cols[0]
        if maximizing:
            max_eval = -math.inf
            for col in valid_cols:
                child = cls._simulate_drop(board, col, ai_player)
                _, score = cls._minimax(
                    child, depth - 1, alpha, beta, False, ai_player, opp_player
                )
                if score > max_eval:
                    max_eval, best_col = score, col
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return best_col, max_eval

        min_eval = math.inf
        for col in valid_cols:
            child = cls._simulate_drop(board, col, opp_player)
            _, score = cls._minimax(
                child, depth - 1, alpha, beta, True, ai_player, opp_player
            )
            if score < min_eval:
                min_eval, best_col = score, col
            beta = min(beta, min_eval)
            if alpha >= beta:
                break
        return best_col, min_eval

    @classmethod
    def _evaluate_board(
        cls, board: list[list[int]], ai_player: int, opp_player: int
    ) -> float:
        score = 0.0
        center_col = [board[r][cls.COLS // 2] for r in range(cls.ROWS)]
        score += center_col.count(ai_player) * 4.0 - center_col.count(opp_player) * 3.0

        for r in range(cls.ROWS):
            for c in range(cls.COLS - 3):
                score += cls._score_window(
                    [board[r][c + i] for i in range(4)], ai_player, opp_player
                )
        for c in range(cls.COLS):
            for r in range(cls.ROWS - 3):
                score += cls._score_window(
                    [board[r + i][c] for i in range(4)], ai_player, opp_player
                )
        for r in range(cls.ROWS - 3):
            for c in range(cls.COLS - 3):
                score += cls._score_window(
                    [board[r + i][c + i] for i in range(4)], ai_player, opp_player
                )
                score += cls._score_window(
                    [board[r + 3 - i][c + i] for i in range(4)], ai_player, opp_player
                )
        return score

    @staticmethod
    def _score_window(window: list[int], ai_player: int, opp_player: int) -> float:
        ai_c = window.count(ai_player)
        opp_c = window.count(opp_player)
        emp = window.count(Disc.EMPTY)
        score = 0.0
        if ai_c == 3 and emp == 1:
            score += 12.0
        elif ai_c == 2 and emp == 2:
            score += 3.0
        if opp_c == 3 and emp == 1:
            score -= 15.0
        elif opp_c == 2 and emp == 2:
            score -= 4.0
        return score
