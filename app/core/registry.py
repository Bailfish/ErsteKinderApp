"""Central registry of all available minigames displayed on the start page."""

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class GameMetadata:
    """Metadata describing a minigame for the start page and navigation."""

    id: str
    title: str
    subtitle: str
    description: str
    icon: str
    url: str
    accent_color: str
    badges: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["badges"] = list(self.badges)
        return data


class GameRegistry:
    """Registry holding all registered minigames."""

    def __init__(self) -> None:
        self._games: dict[str, GameMetadata] = {}

    def register(self, metadata: GameMetadata) -> None:
        self._games[metadata.id] = metadata

    def get(self, game_id: str) -> GameMetadata | None:
        return self._games.get(game_id)

    def list_all(self) -> list[GameMetadata]:
        return list(self._games.values())


def _create_default_registry() -> GameRegistry:
    registry = GameRegistry()
    registry.register(
        GameMetadata(
            id="connect_four",
            title="4 Gewinnt",
            subtitle="Strategie & Köpfchen",
            description="Wirf abwechselnd bunte Spielsteine ein und bringe als Erster vier in eine Reihe! Gegen Computer (Leicht, Mittel, Schwer) oder zu zweit.",
            icon="🔴🟡",
            url="/games/connect-four",
            accent_color="#FF6B6B",
            badges=("1–2 Spieler", "3 KI-Stufen", "Strategie"),
        )
    )
    registry.register(
        GameMetadata(
            id="color_sort",
            title="Farbsortierspiel",
            subtitle="Bunte Reagenzgläser",
            description="Schütte die bunten Flüssigkeiten geschickt in den Reagenzgläsern um, bis in jedem Glas nur noch eine einzige Farbe ist!",
            icon="🧪🌈",
            url="/games/color-sort",
            accent_color="#4ECDC4",
            badges=("Knobelspaß", "Immer lösbar", "Undo-Hilfe"),
        )
    )
    registry.register(
        GameMetadata(
            id="paint_by_numbers",
            title="Malen nach Zahlen",
            subtitle="Kreatives Ausmalstudio",
            description="Tippe die Zahlen an, um tolle Beispielbilder bunt auszumalen – oder lade dein eigenes Foto mit einstellbarer Farbanzahl hoch!",
            icon="🎨🖌️",
            url="/games/paint-by-numbers",
            accent_color="#FFD166",
            badges=("Beispielbilder", "Eigene Fotos", "Farb-Granularität"),
        )
    )
    registry.register(
        GameMetadata(
            id="jump_and_run",
            title="Hüpf & Flitz",
            subtitle="Action Jump & Run",
            description="Springe über Hindernisse und ducke dich unter fliegenden Wolken hindurch! Wie viele Punkte schaffst du?",
            icon="🏃‍♂️⭐",
            url="/games/jump-and-run",
            accent_color="#6A4C93",
            badges=("Reaktion", "Springen & Ducken", "Highscore"),
        )
    )
    return registry


_DEFAULT_REGISTRY = _create_default_registry()


def get_game_registry() -> GameRegistry:
    """Return the singleton game registry."""
    return _DEFAULT_REGISTRY
