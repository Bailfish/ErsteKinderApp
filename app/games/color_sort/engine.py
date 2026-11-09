"""Clean domain engine for the Color Sort (Reagenzgläser) game."""

from typing import Any
from app.games.base import BaseGameEngine
from app.games.color_sort.generator import PALETTE, generate_solvable_tubes


class ColorSortEngine(BaseGameEngine):
    """Domain logic for pouring colored liquid layers between test tubes."""

    CAPACITY = 4
    EMPTY_TUBES = 2

    def __init__(
        self,
        difficulty: str = "easy",
        tubes: list[list[str]] | None = None,
        seed: int | None = None,
        game_id: str | None = None,
    ) -> None:
        super().__init__(game_id=game_id)
        self.difficulty = difficulty if difficulty in ("easy", "medium", "hard") else "easy"
        self.seed = seed
        self._initial_tubes = [t[:] for t in tubes] if tubes is not None else None
        self.tubes: list[list[str]] = []
        self.history: list[list[list[str]]] = []
        self.move_count: int = 0
        self.reset()

    def reset(self) -> None:
        if self._initial_tubes is not None:
            self.tubes = [t[:] for t in self._initial_tubes]
        else:
            self.tubes = generate_solvable_tubes(
                difficulty=self.difficulty,
                capacity=self.CAPACITY,
                empty_tubes=self.EMPTY_TUBES,
                seed=self.seed,
            )
        self.history = []
        self.move_count = 0

    def can_pour(self, from_idx: int, to_idx: int) -> bool:
        """Check whether pouring from tube `from_idx` to `to_idx` is valid."""
        if from_idx == to_idx:
            return False
        if not (0 <= from_idx < len(self.tubes)) or not (0 <= to_idx < len(self.tubes)):
            return False

        source = self.tubes[from_idx]
        target = self.tubes[to_idx]
        if not source or len(target) >= self.CAPACITY:
            return False

        if not target:
            return True
        return source[-1] == target[-1]

    def pour(self, from_idx: int, to_idx: int) -> int:
        """Pour matching top liquid layers from `from_idx` into `to_idx`.

        Returns the number of liquid units transferred.
        """
        if not self.can_pour(from_idx, to_idx):
            raise ValueError(f"Invalid pour from tube {from_idx} to tube {to_idx}.")

        # Save snapshot for undo
        self.history.append([t[:] for t in self.tubes])

        source = self.tubes[from_idx]
        target = self.tubes[to_idx]
        color = source[-1]
        moved = 0

        while source and source[-1] == color and len(target) < self.CAPACITY:
            target.append(source.pop())
            moved += 1

        self.move_count += 1
        return moved

    def undo(self) -> bool:
        """Undo the last pour move if available."""
        if not self.history:
            return False
        self.tubes = self.history.pop()
        self.move_count = max(0, self.move_count - 1)
        return True

    def is_tube_complete(self, idx: int) -> bool:
        """Return True if a tube is full with a single uniform color."""
        tube = self.tubes[idx]
        return len(tube) == self.CAPACITY and len(set(tube)) == 1

    def is_solved(self) -> bool:
        """Return True if every tube is either completely empty or uniformly full."""
        for tube in self.tubes:
            if not tube:
                continue
            if len(tube) != self.CAPACITY or len(set(tube)) != 1:
                return False
        return True

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return all currently valid (from_idx, to_idx) pairs."""
        moves: list[tuple[int, int]] = []
        for i in range(len(self.tubes)):
            for j in range(len(self.tubes)):
                if self.can_pour(i, j):
                    moves.append((i, j))
        return moves

    def get_state(self) -> dict[str, Any]:
        return {
            "game_id": self.game_id,
            "difficulty": self.difficulty,
            "capacity": self.CAPACITY,
            "tubes": self.tubes,
            "tube_count": len(self.tubes),
            "move_count": self.move_count,
            "can_undo": len(self.history) > 0,
            "is_solved": self.is_solved(),
            "completed_tubes": [
                self.is_tube_complete(i) for i in range(len(self.tubes))
            ],
            "palette": {c["id"]: c for c in PALETTE},
        }
