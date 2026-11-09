"""Unit tests for Jump and Run physics, obstacle dodging, and collision detection."""

from app.games.jump_and_run.engine import JumpAndRunEngine, Obstacle


def test_jump_and_run_jump_and_gravity_cycle() -> None:
    engine = JumpAndRunEngine(difficulty="easy", seed=10)
    assert engine.player.is_grounded is True

    # Trigger jump
    assert engine.jump() is True
    # Cannot double-jump once airborne after a tick
    engine.step(0.05)
    assert engine.player.y > 0
    assert engine.jump() is False

    # Fast-fall duck in air
    engine.duck(True)
    assert engine.player.is_ducking is True

    # Simulate until back on ground
    for _ in range(30):
        engine.step(0.05)
    assert engine.player.is_grounded is True
    assert engine.player.y == 0.0


def test_jump_and_run_ducking_avoids_air_obstacle() -> None:
    engine = JumpAndRunEngine(difficulty="medium", seed=5)
    engine.obstacles = [
        Obstacle(id=99, kind="air", x=100.0, y=42.0, width=40.0, height=30.0)
    ]
    # Ducking lowers player height from 60 to 32 (below air obstacle at y=42)
    engine.step(0.05, action="duck")
    assert engine.player.height == 32.0

    for _ in range(15):
        engine.step(0.04)
    assert engine.game_over is False
    assert engine.obstacles_dodged >= 1
    assert engine.score > 0


def test_jump_and_run_collision_triggers_game_over() -> None:
    engine = JumpAndRunEngine(difficulty="hard", seed=1)
    engine.obstacles = [
        Obstacle(id=1, kind="ground", x=90.0, y=0.0, width=36.0, height=44.0)
    ]
    engine.step(0.05, action="stand")
    assert engine.game_over is True
    # Subsequent steps after game_over do not change state
    prev_dist = engine.distance
    engine.step(0.1, action="jump")
    assert engine.distance == prev_dist
