# Farbsortierspiel (`color_sort`)

## 1. Übersicht & Spielziel
Im **Farbsortierspiel** befinden sich verschiedenfarbige Flüssigkeitsschichten gemischt in mehreren Reagenzgläsern. Ziel ist es, die Farben durch Umschütten so zu sortieren, dass am Ende **jedes befüllte Reagenzglas nur noch eine einzige Farbe** (4 Schichten derselben Farbe) enthält.

## 2. Spielregeln im Detail
1. **Reagenzgläser & Kapazität:** Jedes Reagenzglas fasst maximal **4 Farbschichten** (`capacity = 4`).
2. **Startzustand:** Je nach Schwierigkeitsgrad gibt es $N$ Farben (verteilt auf $N$ Gläser) sowie **2 komplett leere Hilfsgläser**.
3. **Umschütt-Regeln (`pour(from_idx, to_idx)`):**
   - Es kann nur die **oberste Farbschicht** (bzw. mehrere direkt zusammenhängende Schichten derselben Farbe oben) aus dem Quellglas gegossen werden.
   - Das Quellglas darf nicht leer sein.
   - Das Zielglas muss noch mindestens **1 freien Platz** haben.
   - Das Zielglas muss entweder **komplett leer** sein **oder** seine oberste Farbschicht muss **exakt dieselbe Farbe** haben wie die oberste Schicht des Quellglases.
   - Liegen im Quellglas oben z. B. 2 gleiche Farbschichten und das Zielglas hat 2 freie Plätze, fließen beide Einheiten in einem Zug hinüber.
4. **Undo-Funktion:** Jeder gültige Zug wird in der Historie gespeichert und kann jederzeit rückgängig gemacht werden.
5. **Siegbedingung:** Jedes Glas im Spiel ist entweder komplett leer oder vollständig (4/4) mit einer einzigen Farbe gefüllt.

## 3. Schwierigkeitsgrade & Lösbarkeits-Garantie
Der Level-Generator (`app/games/color_sort/generator.py`) startet mit sortierten Gläsern und führt gültige Rückwärts-Mischzüge durch, sodass jedes Level garantiert lösbar ist:
- **Leicht (`easy`):** 3 Farben + 2 leere Gläser (5 Gläser gesamt).
- **Mittel (`medium`):** 5 Farben + 2 leere Gläser (7 Gläser gesamt).
- **Schwer (`hard`):** 7 Farben + 2 leere Gläser (9 Gläser gesamt).

## 4. Einstellungen im Zahnrad-Menü (⚙️)
- **Steuerung:**
  - *Maus / Touch:* Erstes Glas antippen (wird angehoben), danach Zielglas antippen.
  - *Tastatur:* Zifferntasten `1`–`9` zur Auswahl von Quell- und Zielglas, `Z` oder `Backspace` für Rückgängig (Undo).
- **Schwierigkeitsgrad:** Leicht (3 Farben), Mittel (5 Farben), Schwer (7 Farben).

## 5. Architektur & Code-Verweise
- **Engine:** `app/games/color_sort/engine.py` (`ColorSortEngine`)
- **Level-Generator:** `app/games/color_sort/generator.py` (`generate_solvable_tubes`)
- **Router:** `app/games/color_sort/router.py`
- **Tests:** `tests/test_color_sort.py`

## 6. API-Endpunkte
- `POST /api/color-sort/new` – Erstellt ein neues lösbares Level (`difficulty`, optional `seed`).
- `POST /api/color-sort/pour` – Schüttet Farbe von `from_tube` nach `to_tube`.
- `POST /api/color-sort/undo` – Macht den letzten Zug rückgängig.
