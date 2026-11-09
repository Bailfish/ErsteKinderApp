"""Clean domain engine for the Paint by Numbers (Ausmalspiel) minigame."""

from typing import Any
from app.games.base import BaseGameEngine
from app.games.paint_by_numbers.templates_data import get_preset_template


class PaintByNumbersEngine(BaseGameEngine):
    """Domain logic for managing regions, palette numbers, and painting progress."""

    def __init__(
        self,
        template_data: dict[str, Any] | None = None,
        template_id: str = "sunny_house",
        strict_mode: bool = True,
        game_id: str | None = None,
    ) -> None:
        super().__init__(game_id=game_id)
        self.template_id = template_id
        self.strict_mode = strict_mode
        self._raw_template = (
            template_data
            if template_data is not None
            else get_preset_template(template_id)
        )
        self.palette: list[dict[str, Any]] = []
        self.regions: list[dict[str, Any]] = []
        self.reset()

    def reset(self) -> None:
        self.palette = [dict(p) for p in self._raw_template["palette"]]
        self.regions = []
        for reg in self._raw_template["regions"]:
            self.regions.append(
                {
                    "id": reg["id"],
                    "number": int(reg["number"]),
                    "label_x": reg["label_x"],
                    "label_y": reg["label_y"],
                    "path_d": reg["path_d"],
                    "painted_number": None,
                    "painted_hex": None,
                    "is_completed": False,
                }
            )

    def _get_color_by_number(self, color_number: int) -> dict[str, Any]:
        for item in self.palette:
            if int(item["number"]) == int(color_number):
                return item
        raise ValueError(f"Color number {color_number} is not in the palette.")

    def _get_region(self, region_id: str) -> dict[str, Any]:
        for reg in self.regions:
            if reg["id"] == region_id:
                return reg
        raise ValueError(f"Region '{region_id}' does not exist.")

    def paint_region(self, region_id: str, color_number: int) -> dict[str, Any]:
        """Attempt to paint `region_id` with `color_number`.

        In `strict_mode`, only the matching target number fills the region.
        """
        region = self._get_region(region_id)
        color_info = self._get_color_by_number(color_number)
        matches_target = int(region["number"]) == int(color_number)

        if self.strict_mode and not matches_target:
            return {
                "accepted": False,
                "matches_target": False,
                "region_id": region_id,
                "expected_number": region["number"],
                "chosen_number": color_number,
                "message": f"Fast! Dieses Feld hat die Zahl {region['number']}.",
            }

        region["painted_number"] = int(color_number)
        region["painted_hex"] = color_info["hex"]
        region["is_completed"] = matches_target
        return {
            "accepted": True,
            "matches_target": matches_target,
            "region_id": region_id,
            "expected_number": region["number"],
            "chosen_number": color_number,
            "painted_hex": color_info["hex"],
            "message": "Super ausgemalt!" if matches_target else "Farbe aufgetragen!",
        }

    @property
    def completed_count(self) -> int:
        return sum(1 for r in self.regions if r["is_completed"])

    @property
    def total_count(self) -> int:
        return len(self.regions)

    @property
    def is_finished(self) -> bool:
        return self.total_count > 0 and self.completed_count == self.total_count

    @property
    def progress_percent(self) -> int:
        if self.total_count == 0:
            return 100
        return round((self.completed_count / self.total_count) * 100)

    def get_hint(self, color_number: int | None = None) -> dict[str, Any] | None:
        """Return an unpainted region (optionally filtered by `color_number`)."""
        for reg in self.regions:
            if not reg["is_completed"]:
                if color_number is None or reg["number"] == int(color_number):
                    return {
                        "region_id": reg["id"],
                        "number": reg["number"],
                        "label_x": reg["label_x"],
                        "label_y": reg["label_y"],
                    }
        return None

    def get_state(self) -> dict[str, Any]:
        return {
            "game_id": self.game_id,
            "template_id": self._raw_template.get("id", self.template_id),
            "title": self._raw_template.get("title", "Ausmalbild"),
            "view_box": self._raw_template.get("view_box", "0 0 600 450"),
            "strict_mode": self.strict_mode,
            "palette": self.palette,
            "regions": self.regions,
            "completed_count": self.completed_count,
            "total_count": self.total_count,
            "progress_percent": self.progress_percent,
            "is_finished": self.is_finished,
        }
