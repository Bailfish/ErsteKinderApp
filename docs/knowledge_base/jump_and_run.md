# Jump and Run (`jump_and_run`)

## 1. Übersicht & Spielziel
Im **Jump and Run** steuert das Kind eine laufende Spielfigur durch eine bunte Landschaft. Von rechts kommen verschiedenartige Hindernisse auf den Spieler zu, denen man durch rechtzeitiges **Springen** oder **Ducken** ausweichen muss. Für jedes überstandene Hindernis und jede gelaufene Sekunde steigt der Punktestand.

## 2. Spielregeln im Detail
1. **Spieler-Zustand (`PlayerState`):**
   - Position `y` über dem Boden (`y = 0` entspricht dem Boden).
   - Vertikale Geschwindigkeit `vy` und Schwerkraft `gravity`.
   - Aktionen:
     - **Springen (`jump()`):** Wenn die Figur auf dem Boden steht (`is_grounded == True`), erhält sie einen positiven Sprungimpuls nach oben, um Boden-Hindernisse (Steine, Kisten, Kakteen) zu überspringen.
     - **Ducken (`duck(active)`):** Verringert die Körperhöhe der Spielfigur, um tief fliegenden Luft-Hindernissen (Vögel, Wolken-Blitze) auszuweichen.
2. **Hindernisse (`Obstacle`):**
   - `ground` (Boden-Hindernis): Muss übersprungen werden.
   - `air` (Flug-Hindernis): Schwebt auf Kopfhöhe; man kann darunter hindurchducken oder hoch darüber springen.
3. **Kollision & Punktestand:**
   - Überschneiden sich die Hitbox des Spielers und die Hitbox eines Hindernisses (AABB-Kollision), endet der Lauf (`game_over = True`).
   - Jedes erfolgreich passierte Hindernis bringt Bonuspunkte (+10 Punkte) zusätzlich zur Laufdistanz.

## 3. Schwierigkeitsgrade
- **Leicht (`easy`):** Langsames Lauftempo, große Abstände zwischen Hindernissen, hauptsächlich Boden-Hindernisse.
- **Mittel (`medium`):** Mittleres Tempo, Mischung aus Boden- und Flug-Hindernissen, leicht ansteigende Geschwindigkeit.
- **Schwer (`hard`):** Schnelles Tempo, kürzere Reaktionsabstände, schnellere Beschleunigung.

## 4. Einstellungen im Zahnrad-Menü (⚙️)
- **Steuerung (`control_scheme`):**
  - *Tastatur:* `Leertaste` oder `Pfeil hoch` / `W` zum Springen; `Pfeil runter` / `S` zum Ducken.
  - *Maus / Touch:* Klick/Tippen auf die Spielfläche oder große On-Screen-Buttons („Springen ⬆️“ / „Ducken ⬇️“).
- **Sprungtaste anpassbar (`primary_key`):** Wahl zwischen `Space` (Leertaste), `ArrowUp` (Pfeil oben) oder `KeyW`.
- **Schwierigkeitsgrad:** Leicht / Mittel / Schwer.

## 5. Architektur & Code-Verweise
- **Engine:** `app/games/jump_and_run/engine.py` (`JumpAndRunEngine`, `PlayerState`, `Obstacle`)
- **Router:** `app/games/jump_and_run/router.py`
- **Tests:** `tests/test_jump_and_run.py`

## 6. API-Endpunkte
- `POST /api/jump-and-run/new` – Initialisiert eine neue Spiel-Session mit Physik- und Schwierigkeits-Parametern.
- `POST /api/jump-and-run/step` – Berechnet Spiel-Ticks (`dt`, `action`: `jump`, `duck`, `none`) inkl. Kollisionsprüfung.
- `POST /api/jump-and-run/score` – Speichert und validiert erreichte Highscores.
