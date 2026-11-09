"""Preset child-friendly vector templates for the Paint by Numbers minigame."""

from typing import Any

PRESET_TEMPLATES: dict[str, dict[str, Any]] = {
    "sunny_house": {
        "id": "sunny_house",
        "title": "Sonniges Haus",
        "icon": "🏡☀️",
        "view_box": "0 0 600 450",
        "palette": [
            {"number": 1, "name": "Himmelblau", "hex": "#70D6FF"},
            {"number": 2, "name": "Sonnengelb", "hex": "#FFD166"},
            {"number": 3, "name": "Wiesengrün", "hex": "#8AC926"},
            {"number": 4, "name": "Ziegelrot", "hex": "#FF595E"},
            {"number": 5, "name": "Hauswand-Creme", "hex": "#FFF3B0"},
            {"number": 6, "name": "Holzbraun", "hex": "#9E6240"},
        ],
        "regions": [
            {"id": "sky", "number": 1, "label_x": 120, "label_y": 80, "path_d": "M0 0H600V310H0Z"},
            {"id": "meadow", "number": 3, "label_x": 100, "label_y": 380, "path_d": "M0 310H600V450H0Z"},
            {"id": "sun", "number": 2, "label_x": 500, "label_y": 85, "path_d": "M450 85A50 50 0 1 0 550 85A50 50 0 1 0 450 85Z"},
            {"id": "house_wall", "number": 5, "label_x": 240, "label_y": 240, "path_d": "M180 180H420V340H180Z"},
            {"id": "roof", "number": 4, "label_x": 300, "label_y": 135, "path_d": "M150 180L300 75L450 180Z"},
            {"id": "door", "number": 6, "label_x": 300, "label_y": 290, "path_d": "M275 245H325V340H275Z"},
            {"id": "window_left", "number": 2, "label_x": 225, "label_y": 230, "path_d": "M200 205H250V255H200Z"},
            {"id": "window_right", "number": 2, "label_x": 375, "label_y": 230, "path_d": "M350 205H400V255H350Z"},
            {"id": "tree_trunk", "number": 6, "label_x": 95, "label_y": 285, "path_d": "M80 230H110V335H80Z"},
            {"id": "tree_crown", "number": 3, "label_x": 95, "label_y": 185, "path_d": "M40 185A55 55 0 1 0 150 185A55 55 0 1 0 40 185Z"},
        ],
    },
    "space_rocket": {
        "id": "space_rocket",
        "title": "Weltraum-Rakete",
        "icon": "🚀🪐",
        "view_box": "0 0 600 450",
        "palette": [
            {"number": 1, "name": "Weltraum-Blau", "hex": "#1B263B"},
            {"number": 2, "name": "Raketen-Silber", "hex": "#E0E1DD"},
            {"number": 3, "name": "Feuer-Rot", "hex": "#EF476F"},
            {"number": 4, "name": "Sternen-Gelb", "hex": "#FFD166"},
            {"number": 5, "name": "Fenster-Türkis", "hex": "#06D6A0"},
        ],
        "regions": [
            {"id": "space_bg", "number": 1, "label_x": 90, "label_y": 70, "path_d": "M0 0H600V450H0Z"},
            {"id": "planet", "number": 4, "label_x": 490, "label_y": 110, "path_d": "M440 110A50 50 0 1 0 540 110A50 50 0 1 0 440 110Z"},
            {"id": "star_left", "number": 4, "label_x": 120, "label_y": 220, "path_d": "M120 180L135 210L165 215L140 235L148 265L120 248L92 265L100 235L75 215L105 210Z"},
            {"id": "rocket_body", "number": 2, "label_x": 300, "label_y": 250, "path_d": "M250 140H350V320H250Z"},
            {"id": "rocket_nose", "number": 3, "label_x": 300, "label_y": 105, "path_d": "M250 140L300 55L350 140Z"},
            {"id": "fin_left", "number": 3, "label_x": 225, "label_y": 300, "path_d": "M250 250L195 330L250 320Z"},
            {"id": "fin_right", "number": 3, "label_x": 375, "label_y": 300, "path_d": "M350 250L405 330L350 320Z"},
            {"id": "rocket_window", "number": 5, "label_x": 300, "label_y": 195, "path_d": "M270 195A30 30 0 1 0 330 195A30 30 0 1 0 270 195Z"},
            {"id": "flame", "number": 4, "label_x": 300, "label_y": 365, "path_d": "M265 320L300 415L335 320Z"},
        ],
    },
    "happy_butterfly": {
        "id": "happy_butterfly",
        "title": "Bunter Schmetterling",
        "icon": "🦋🌸",
        "view_box": "0 0 600 450",
        "palette": [
            {"number": 1, "name": "Himmel-Hellblau", "hex": "#CAF0F8"},
            {"number": 2, "name": "Flügel-Pink", "hex": "#FF6392"},
            {"number": 3, "name": "Flügel-Orange", "hex": "#FF9F1C"},
            {"number": 4, "name": "Punkt-Gelb", "hex": "#FFE66D"},
            {"number": 5, "name": "Körper-Lila", "hex": "#6A4C93"},
        ],
        "regions": [
            {"id": "bg", "number": 1, "label_x": 70, "label_y": 60, "path_d": "M0 0H600V450H0Z"},
            {"id": "wing_tl", "number": 2, "label_x": 190, "label_y": 150, "path_d": "M285 210C120 60,80 220,285 240Z"},
            {"id": "wing_tr", "number": 2, "label_x": 410, "label_y": 150, "path_d": "M315 210C480 60,520 220,315 240Z"},
            {"id": "wing_bl", "number": 3, "label_x": 210, "label_y": 300, "path_d": "M285 240C130 250,150 390,285 320Z"},
            {"id": "wing_br", "number": 3, "label_x": 390, "label_y": 300, "path_d": "M315 240C470 250,450 390,315 320Z"},
            {"id": "dot_l", "number": 4, "label_x": 200, "label_y": 175, "path_d": "M175 175A25 25 0 1 0 225 175A25 25 0 1 0 175 175Z"},
            {"id": "dot_r", "number": 4, "label_x": 400, "label_y": 175, "path_d": "M375 175A25 25 0 1 0 425 175A25 25 0 1 0 375 175Z"},
            {"id": "body", "number": 5, "label_x": 300, "label_y": 240, "path_d": "M285 130H315V350H285Z"},
        ],
    },
}


def list_preset_templates() -> list[dict[str, str]]:
    return [
        {"id": t["id"], "title": t["title"], "icon": t["icon"]}
        for t in PRESET_TEMPLATES.values()
    ]


def get_preset_template(template_id: str) -> dict[str, Any]:
    if template_id not in PRESET_TEMPLATES:
        raise KeyError(f"Unknown template_id: {template_id}")
    tpl = PRESET_TEMPLATES[template_id]
    return {
        "id": tpl["id"],
        "title": tpl["title"],
        "icon": tpl["icon"],
        "view_box": tpl["view_box"],
        "palette": [dict(p) for p in tpl["palette"]],
        "regions": [dict(r) for r in tpl["regions"]],
    }
