"""Gear settings menu (⚙️) domain model, manager, and API router."""

from enum import Enum
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


class ControlScheme(str, Enum):
    """Available control modes in the gear settings menu."""

    HYBRID = "hybrid"
    MOUSE_TOUCH = "mouse_touch"
    KEYBOARD = "keyboard"


class DifficultyLevel(str, Enum):
    """Standard difficulty levels across games."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameSettings(BaseModel):
    """Configurable settings per minigame (accessible via the gear icon ⚙️)."""

    game_id: str
    control_scheme: ControlScheme = Field(default=ControlScheme.HYBRID)
    primary_key: str = Field(default="Space")
    secondary_key: str = Field(default="ArrowDown")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    sound_enabled: bool = Field(default=True)
    show_hints: bool = Field(default=True)
    custom_options: dict[str, Any] = Field(default_factory=dict)


class GameSettingsUpdate(BaseModel):
    """Partial update payload for game settings."""

    control_scheme: ControlScheme | None = None
    primary_key: str | None = None
    secondary_key: str | None = None
    difficulty: DifficultyLevel | None = None
    sound_enabled: bool | None = None
    show_hints: bool | None = None
    custom_options: dict[str, Any] | None = None


class SettingsManager:
    """Manages default and updated settings for each minigame."""

    VALID_GAMES = {"connect_four", "color_sort", "paint_by_numbers", "jump_and_run"}

    def __init__(self) -> None:
        self._settings: dict[str, GameSettings] = self._build_defaults()

    @staticmethod
    def _build_defaults() -> dict[str, GameSettings]:
        return {
            "connect_four": GameSettings(
                game_id="connect_four",
                primary_key="Space",
                secondary_key="ArrowLeft",
                custom_options={"mode": "ai"},
            ),
            "color_sort": GameSettings(
                game_id="color_sort",
                primary_key="Enter",
                secondary_key="KeyZ",
                custom_options={"auto_pour_top_stack": True},
            ),
            "paint_by_numbers": GameSettings(
                game_id="paint_by_numbers",
                primary_key="Space",
                secondary_key="KeyH",
                custom_options={"default_granularity": 6, "strict_number_match": True},
            ),
            "jump_and_run": GameSettings(
                game_id="jump_and_run",
                primary_key="Space",
                secondary_key="ArrowDown",
                custom_options={"show_touch_buttons": True},
            ),
        }

    def get_settings(self, game_id: str) -> GameSettings:
        if game_id not in self.VALID_GAMES:
            raise KeyError(f"Unknown game_id: {game_id}")
        return self._settings[game_id]

    def update_settings(self, game_id: str, update: GameSettingsUpdate) -> GameSettings:
        current = self.get_settings(game_id)
        data = current.model_dump()
        update_data = update.model_dump(exclude_none=True)
        if "custom_options" in update_data:
            merged = dict(data.get("custom_options", {}))
            merged.update(update_data["custom_options"])
            update_data["custom_options"] = merged
        data.update(update_data)
        updated = GameSettings(**data)
        self._settings[game_id] = updated
        return updated

    def reset_settings(self, game_id: str) -> GameSettings:
        if game_id not in self.VALID_GAMES:
            raise KeyError(f"Unknown game_id: {game_id}")
        self._settings[game_id] = self._build_defaults()[game_id]
        return self._settings[game_id]


settings_manager = SettingsManager()
settings_router = APIRouter(prefix="/api/settings", tags=["settings"])


@settings_router.get("/{game_id}", response_model=GameSettings)
def get_game_settings(game_id: str) -> GameSettings:
    try:
        return settings_manager.get_settings(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@settings_router.put("/{game_id}", response_model=GameSettings)
def update_game_settings(game_id: str, payload: GameSettingsUpdate) -> GameSettings:
    try:
        return settings_manager.update_settings(game_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@settings_router.post("/{game_id}/reset", response_model=GameSettings)
def reset_game_settings(game_id: str) -> GameSettings:
    try:
        return settings_manager.reset_settings(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
