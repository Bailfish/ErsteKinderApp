"""Abstract base class for all minigame engines (Clean Architecture)."""

from abc import ABC, abstractmethod
from typing import Any
import uuid


class BaseGameEngine(ABC):
    """Common interface for all minigame domain engines."""

    def __init__(self, game_id: str | None = None) -> None:
        self.game_id: str = game_id or str(uuid.uuid4())

    @abstractmethod
    def reset(self) -> None:
        """Reset the game to its initial state."""

    @abstractmethod
    def get_state(self) -> dict[str, Any]:
        """Return a serializable dictionary representing the current game state."""
