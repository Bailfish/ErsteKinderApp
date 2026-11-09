---
name: knowledge-base-manager
description: Erstellt und aktualisiert die Knowledge Base (docs/knowledge_base/) für alle Minispiele, ihre Spielregeln, Steuerungsoptionen, Schwierigkeitsgrade und API-Endpunkte.
---

# Skill: Knowledge Base Manager (`knowledge-base-manager`)

Verwende diesen Skill immer dann, wenn ein neues Minispiel erstellt wird oder sich Spielregeln, Schwierigkeitsstufen, Steuerungsoptionen (Zahnrad-Menü) oder API-Routen eines Spiels ändern.

## Ablageort der Knowledge Base
- Index-Datei: `docs/knowledge_base/INDEX.md`
- Einzeldokumente pro Spiel:
  - `docs/knowledge_base/connect_four.md` (4 Gewinnt)
  - `docs/knowledge_base/color_sort.md` (Farbsortierspiel)
  - `docs/knowledge_base/paint_by_numbers.md` (Ausmalspiel / Malen nach Zahlen)
  - `docs/knowledge_base/jump_and_run.md` (Jump and Run)

## Pflicht-Abschnitte jeder Spiel-Dokumentation
Jede Datei in `docs/knowledge_base/<game_id>.md` **muss** folgende Struktur enthalten:

1. **Übersicht & Spielziel** (Kurze, kindgerechte und technische Beschreibung)
2. **Spielregeln im Detail** (Gültige Züge, Gewinn-/Verlustbedingungen, Sonderfälle)
3. **Schwierigkeitsgrade & Spielmodi** (z. B. KI-Stufen Leicht/Mittel/Schwer, Farbgranularität, Geschwindigkeit)
4. **Einstellungen im Zahnrad-Menü (⚙️)** (Steuerungsoptionen, Tastenbelegung, Audio, Reset)
5. **Architektur & relevante Code-Dateien** (Verweis auf Engine, Router, Frontend-JS und Testdatei)
6. **API-Endpunkte** (Kurze Übersicht über Request/Response-Formate)

## Checkliste beim Ausführen des Skills
1. Prüfe die tatsächliche Implementierung in `app/games/<game_id>/engine.py` und `router.py`.
2. Erstelle oder aktualisiere `docs/knowledge_base/<game_id>.md`.
3. Aktualisiere `docs/knowledge_base/INDEX.md`, falls ein neues Spiel hinzugekommen ist oder sich Eckdaten geändert haben.
4. Prüfe, ob `SURGERY_MAP.md` ebenfalls ein Update benötigt.
