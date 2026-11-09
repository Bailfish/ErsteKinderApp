# SURGERY MAP – ErsteKinderApp

Diese **Surgery Map** dient KI-Agenten und Entwicklern als schnelle Orientierungskarte, um ohne langes Suchen direkt die richtigen Dateien, Klassen, Funktionen und Tests im Projekt zu finden.

---

## 1. Projekt-Übersicht & Architektur-Prinzipien

- **Framework:** FastAPI + Jinja2 Templates + HTML5/CSS/JS Frontend
- **Architektur:** Clean Architecture mit strikter Trennung zwischen:
  1. **Domain / Game Engine (`app/games/<game>/engine.py`)** – Reine Python-Spiellogik ohne Web-/HTTP-Abhängigkeiten.
  2. **API / Controller (`app/games/<game>/router.py`)** – FastAPI-Router, validiert Eingaben (Pydantic) und ruft die Engine auf.
  3. **Core & Settings (`app/core/`)** – Spiel-Registrierung (`registry.py`) und Zahnrad-Einstellungsmenü (`settings.py`).
  4. **Presentation (`app/templates/` & `app/static/`)** – Kindgerechte UI inkl. gemeinsamem Zahnrad-Einstellungs-Modal.

---

## 2. Schnellzugriff: Wo liegt welche Funktion?

| Bereich / Funktion | Datei (Relativer Pfad) | Zentrale Klassen / Funktionen |
| :--- | :--- | :--- |
| **App-Einstiegspunkt & Startseite** | `app/main.py` | `create_app()`, `app`, `GET /`, `GET /health` |
| **Globale Spiel-Registrierung** | `app/core/registry.py` | `GameMetadata`, `GameRegistry`, `get_game_registry()` |
| **Zahnrad-Menü / Einstellungen (⚙️)** | `app/core/settings.py` | `ControlScheme`, `GameSettings`, `SettingsManager`, `/api/settings/{game_id}` |
| **Abstrakte Spiel-Basisklasse** | `app/games/base.py` | `BaseGameEngine` |
| **4 Gewinnt – Spiellogik** | `app/games/connect_four/engine.py` | `ConnectFourEngine`, `Disc`, `GameMode`, `Difficulty` |
| **4 Gewinnt – Computergegner (KI)** | `app/games/connect_four/ai.py` | `ConnectFourAI` (`choose_move`: `easy`, `medium`, `hard` via Minimax + Alpha-Beta) |
| **4 Gewinnt – API & View** | `app/games/connect_four/router.py` | `router` (`/games/connect-four`, `/api/connect-four/...`) |
| **Farbsortierspiel – Spiellogik** | `app/games/color_sort/engine.py` | `ColorSortEngine`, `Tube`, `pour()`, `undo()`, `is_solved()` |
| **Farbsortierspiel – Level-Generator** | `app/games/color_sort/generator.py` | `generate_solvable_tubes()`, `PALETTE` |
| **Farbsortierspiel – API & View** | `app/games/color_sort/router.py` | `router` (`/games/color-sort`, `/api/color-sort/...`) |
| **Ausmalspiel – Spiellogik** | `app/games/paint_by_numbers/engine.py` | `PaintByNumbersEngine`, `Region`, `ColorSlot`, `paint_region()` |
| **Ausmalspiel – Eigene Bilder & Quantisierung** | `app/games/paint_by_numbers/image_processor.py` | `ImageProcessor`, `process_uploaded_image()`, `quantize_and_segment()` |
| **Ausmalspiel – Beispielbilder** | `app/games/paint_by_numbers/templates_data.py` | `PRESET_TEMPLATES`, `get_preset_template()` |
| **Ausmalspiel – API & View** | `app/games/paint_by_numbers/router.py` | `router` (`/games/paint-by-numbers`, `/api/paint-by-numbers/upload`, `...`) |
| **Jump & Run – Physik & Hindernisse** | `app/games/jump_and_run/engine.py` | `JumpAndRunEngine`, `PlayerState`, `Obstacle`, `step()`, `jump()`, `duck()` |
| **Jump & Run – API & View** | `app/games/jump_and_run/router.py` | `router` (`/games/jump-and-run`, `/api/jump-and-run/...`) |
| **Gemeinsames Layout & Zahnrad-UI** | `app/templates/base.html` | Header, Navigation, Zahnrad-Button (`#settings-gear-btn`), Settings-Modal |
| **Startseiten-Template** | `app/templates/index.html` | Kachel-Auswahl aller registrierten Minispiele |
| **Zahnrad-Frontend-Logik** | `app/static/js/settings_modal.js` | `GameSettingsController` (lädt/speichert Steuerung, Ton, Schwierigkeit) |

---

## 3. Test-Suite & Zuordnung (`tests/`)

Alle Tests liegen in `tests/` und werden mit `pytest` ausgeführt (Mindest-Coverage: **80 %**).

| Testdatei | Getestete Module |
| :--- | :--- |
| `tests/test_core_and_settings.py` | `app/core/registry.py`, `app/core/settings.py`, `app/games/base.py`, Startseite |
| `tests/test_connect_four.py` | `app/games/connect_four/engine.py`, `ai.py` (Leicht, Mittel, Schwer, PvP) |
| `tests/test_color_sort.py` | `app/games/color_sort/engine.py`, `generator.py` (Umschütten, Undo, Sieg) |
| `tests/test_paint_by_numbers.py` | `app/games/paint_by_numbers/engine.py`, `image_processor.py`, `templates_data.py` |
| `tests/test_jump_and_run.py` | `app/games/jump_and_run/engine.py` (Sprung-Physik, Ducken, Kollision, Spawning) |
| `tests/test_api_routes.py` | Alle FastAPI-Endpunkte (`connect_four`, `color_sort`, `paint_by_numbers`, `jump_and_run`, `settings`) |

---

## 4. Agent Skills & Knowledge Base

- **Skills (`.agents/skills/`):**
  - `git-commit`: `.agents/skills/git-commit/SKILL.md`
  - `git-feature-branch`: `.agents/skills/git-feature-branch/SKILL.md`
  - `knowledge-base-manager`: `.agents/skills/knowledge-base-manager/SKILL.md`
- **Knowledge Base (`docs/knowledge_base/`):**
  - `docs/knowledge_base/INDEX.md`
  - `docs/knowledge_base/connect_four.md`
  - `docs/knowledge_base/color_sort.md`
  - `docs/knowledge_base/paint_by_numbers.md`
  - `docs/knowledge_base/jump_and_run.md`

---

## 5. Rezept: Wie fügt man ein neues Minispiel hinzu?

1. **Feature-Branch anlegen** (Skill `git-feature-branch`): `git checkout -b feature/<game_id>`
2. **Engine erstellen:** `app/games/<game_id>/engine.py` (erbt von `BaseGameEngine`).
3. **Router erstellen:** `app/games/<game_id>/router.py` und in `app/main.py` einbinden.
4. **Spiel registrieren:** In `app/core/registry.py` Metadaten und Standard-Einstellungen eintragen.
5. **Frontend erstellen:** `app/templates/games/<game_id>.html` + `app/static/js/<game_id>.js`.
6. **Tests schreiben:** `tests/test_<game_id>.py` (Coverage >= 80 % sicherstellen).
7. **Knowledge Base & Surgery Map aktualisieren** (Skill `knowledge-base-manager`).

---

## 6. Wichtige Befehle

```bash
# Entwicklungsserver starten
.venv/bin/uvicorn app.main:app --reload --port 8000

# Tests inkl. Coverage-Gate (>= 80%) ausführen
.venv/bin/pytest
```
