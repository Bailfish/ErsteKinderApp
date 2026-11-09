"""Unit tests for core registry, gear settings manager, and base classes."""

import pytest
from app.core.registry import GameRegistry, get_game_registry
from app.core.settings import (
    ControlScheme,
    DifficultyLevel,
    GameSettingsUpdate,
    SettingsManager,
)


def test_default_game_registry_contains_all_four_games() -> None:
    registry = get_game_registry()
    games = registry.list_all()
    ids = [g.id for g in games]
    assert ids == ["connect_four", "color_sort", "paint_by_numbers", "jump_and_run"]
    for g in games:
        d = g.to_dict()
        assert d["url"].startswith("/games/")
        assert isinstance(d["badges"], list)


def test_custom_registry_register_and_get() -> None:
    reg = GameRegistry()
    assert reg.get("missing") is None
    default_game = get_game_registry().get("connect_four")
    assert default_game is not None
    reg.register(default_game)
    assert reg.get("connect_four") == default_game


def test_settings_manager_get_update_and_reset() -> None:
    mgr = SettingsManager()
    s = mgr.get_settings("jump_and_run")
    assert s.control_scheme == ControlScheme.HYBRID
    assert s.primary_key == "Space"

    updated = mgr.update_settings(
        "jump_and_run",
        GameSettingsUpdate(
            control_scheme=ControlScheme.KEYBOARD,
            primary_key="ArrowUp",
            difficulty=DifficultyLevel.HARD,
            sound_enabled=False,
            custom_options={"extra": 42},
        ),
    )
    assert updated.control_scheme == ControlScheme.KEYBOARD
    assert updated.primary_key == "ArrowUp"
    assert updated.difficulty == DifficultyLevel.HARD
    assert updated.sound_enabled is False
    assert updated.custom_options["extra"] == 42
    assert updated.custom_options["show_touch_buttons"] is True

    reset = mgr.reset_settings("jump_and_run")
    assert reset.control_scheme == ControlScheme.HYBRID
    assert reset.primary_key == "Space"

    with pytest.raises(KeyError):
        mgr.get_settings("unknown_game")
    with pytest.raises(KeyError):
        mgr.reset_settings("unknown_game")
