"""Clean domain engine for the Jump and Run obstacle-dodging minigame."""

from dataclasses import asdict, dataclass
import random
from typing import Any
from app.games.base import BaseGameEngine


@dataclass
class PlayerState:
    x: float = 80.0
    y: float = 0.0
    vy: float = 0.0
    width: float = 44.0
    standing_height: float = 60.0
    ducking_height: float = 32.0
    is_ducking: bool = False

    @property
    def height(self) -> float:
        if self.is_ducking and self.is_grounded:
            return self.ducking_height
        return self.standing_height

    @property
    def is_grounded(self) -> bool:
        return self.y <= 0.001


@dataclass
class Obstacle:
    id: int
    kind: str
    x: float
    y: float
    width: float
    height: float
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DIFFICULTY_CONFIG: dict[str, dict[str, float]] = {
    "easy": {
        "base_speed": 240.0,
        "max_speed": 380.0,
        "acceleration": 4.0,
        "spawn_min_gap": 320.0,
        "spawn_max_gap": 480.0,
        "air_chance": 0.2,
    },
    "medium": {
        "base_speed": 310.0,
        "max_speed": 480.0,
        "acceleration": 7.0,
        "spawn_min_gap": 260.0,
        "spawn_max_gap": 410.0,
        "air_chance": 0.35,
    },
    "hard": {
        "base_speed": 380.0,
        "max_speed": 580.0,
        "acceleration": 10.0,
        "spawn_min_gap": 220.0,
        "spawn_max_gap": 350.0,
        "air_chance": 0.45,
    },
}


class JumpAndRunEngine(BaseGameEngine):
    WORLD_WIDTH = 800.0
    JUMP_VELOCITY = 540.0
    GRAVITY = 1350.0

    def __init__(
        self,
        difficulty: str = "easy",
        seed: int | None = None,
        game_id: str | None = None,
    ) -> None:
        super().__init__(game_id=game_id)
        self.difficulty = difficulty if difficulty in DIFFICULTY_CONFIG else "easy"
        self.seed = seed
        self._rng = random.Random(seed)
        self.player = PlayerState()
        self.obstacles: list[Obstacle] = []
        self.speed = 0.0
        self.distance = 0.0
        self.score = 0
        self.obstacles_dodged = 0
        self.game_over = False
        self._next_id = 1
        self._until_spawn = 0.0
        self.reset()

    def reset(self) -> None:
        self._rng = random.Random(self.seed)
        cfg = DIFFICULTY_CONFIG[self.difficulty]
        self.player = PlayerState()
        self.obstacles = []
        self.speed = cfg["base_speed"]
        self.distance = 0.0
        self.score = 0
        self.obstacles_dodged = 0
        self.game_over = False
        self._next_id = 1
        self._until_spawn = 280.0
        self.spawn_obstacle(start_x=520.0)

    def jump(self) -> bool:
        if self.game_over or not self.player.is_grounded:
            return False
        self.player.is_ducking = False
        self.player.vy = self.JUMP_VELOCITY
        return True

    def duck(self, active: bool = True) -> None:
        if self.game_over:
            return
        self.player.is_ducking = active
        if active and not self.player.is_grounded and self.player.vy > -250.0:
            self.player.vy = -350.0

    def spawn_obstacle(
        self, start_x: float | None = None, kind: str | None = None
    ) -> Obstacle:
        cfg = DIFFICULTY_CONFIG[self.difficulty]
        chosen = kind or (
            "air" if self._rng.random() < cfg["air_chance"] else "ground"
        )
        x_pos = start_x if start_x is not None else self.WORLD_WIDTH + 40.0
        if chosen == "air":
            obs = Obstacle(self._next_id, "air", x_pos, 42.0, 46.0, 30.0)
        else:
            obs = Obstacle(self._next_id, "ground", x_pos, 0.0, 36.0, 44.0)
        self._next_id += 1
        self.obstacles.append(obs)
        self._until_spawn = self._rng.uniform(
            cfg["spawn_min_gap"], cfg["spawn_max_gap"]
        )
        return obs

    def step(self, dt: float, action: str | None = None) -> dict[str, Any]:
        if self.game_over:
            return self.get_state()
        dt_c = max(0.0, min(0.25, float(dt)))
        if action == "jump":
            self.jump()
        elif action == "duck":
            self.duck(True)
        elif action == "stand":
            self.duck(False)

        if not self.player.is_grounded or self.player.vy > 0:
            self.player.y += self.player.vy * dt_c
            self.player.vy -= self.GRAVITY * dt_c
            if self.player.y <= 0.0:
                self.player.y, self.player.vy = 0.0, 0.0

        cfg = DIFFICULTY_CONFIG[self.difficulty]
        self.speed = min(
            cfg["max_speed"], self.speed + cfg["acceleration"] * dt_c
        )
        dx = self.speed * dt_c
        self.distance += dx
        self._until_spawn -= dx
        if self._until_spawn <= 0:
            self.spawn_obstacle()

        rem: list[Obstacle] = []
        for obs in self.obstacles:
            obs.x -= dx
            if self.check_collision(self.player, obs):
                self.game_over = True
            if not obs.passed and (obs.x + obs.width) < self.player.x:
                obs.passed = True
                self.obstacles_dodged += 1
            if obs.x + obs.width > -60.0:
                rem.append(obs)
        self.obstacles = rem
        self.score = int(self.distance / 15.0) + self.obstacles_dodged * 10
        return self.get_state()

    @staticmethod
    def check_collision(p: PlayerState, o: Obstacle) -> bool:
        pad = 4.0
        return (
            p.x + pad < o.x + o.width - pad and p.x + p.width - pad > o.x + pad
        ) and (p.y + pad < o.y + o.height and p.y + p.height - pad > o.y)

    def get_state(self) -> dict[str, Any]:
        p = self.player
        return {
            "game_id": self.game_id,
            "difficulty": self.difficulty,
            "config": DIFFICULTY_CONFIG[self.difficulty],
            "player": {
                "x": p.x,
                "y": round(p.y, 2),
                "vy": round(p.vy, 2),
                "width": p.width,
                "height": p.height,
                "is_ducking": p.is_ducking,
                "is_grounded": p.is_grounded,
            },
            "obstacles": [o.to_dict() for o in self.obstacles],
            "speed": round(self.speed, 2),
            "distance": round(self.distance, 1),
            "score": self.score,
            "obstacles_dodged": self.obstacles_dodged,
            "game_over": self.game_over,
        }

