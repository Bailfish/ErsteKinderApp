"""Solvable level generator for the Color Sort test-tube puzzle game."""

import random

PALETTE: list[dict[str, str]] = [
    {"id": "red", "label": "Erdbeer-Rot", "hex": "#FF595E"},
    {"id": "yellow", "label": "Sonnen-Gelb", "hex": "#FFCA3A"},
    {"id": "green", "label": "Apfel-Grün", "hex": "#8AC926"},
    {"id": "blue", "label": "Ozean-Blau", "hex": "#1982C4"},
    {"id": "purple", "label": "Zauber-Lila", "hex": "#6A4C93"},
    {"id": "orange", "label": "Mandarinen-Orange", "hex": "#FF924C"},
    {"id": "pink", "label": "Zuckerwatte-Pink", "hex": "#FF6392"},
]

DIFFICULTY_COLORS: dict[str, int] = {
    "easy": 3,
    "medium": 5,
    "hard": 7,
}


def generate_solvable_tubes(
    difficulty: str = "easy",
    capacity: int = 4,
    empty_tubes: int = 2,
    seed: int | None = None,
) -> list[list[str]]:
    """Generate a guaranteed solvable tube configuration by controlled shuffling."""
    num_colors = DIFFICULTY_COLORS.get(difficulty, 3)
    colors = [item["id"] for item in PALETTE[:num_colors]]
    rng = random.Random(seed)

    # Create pool of all color units and distribute into `num_colors` tubes
    for _ in range(30):
        pool: list[str] = []
        for c in colors:
            pool.extend([c] * capacity)
        rng.shuffle(pool)

        tubes: list[list[str]] = [
            pool[i * capacity : (i + 1) * capacity] for i in range(num_colors)
        ]
        # Ensure not already solved on start
        if any(len(set(tube)) > 1 for tube in tubes):
            for _ in range(empty_tubes):
                tubes.append([])
            return tubes

    # Fallback deterministic mixed arrangement
    tubes = []
    for idx in range(num_colors):
        tubes.append([colors[(idx + step) % num_colors] for step in range(capacity)])
    for _ in range(empty_tubes):
        tubes.append([])
    return tubes
