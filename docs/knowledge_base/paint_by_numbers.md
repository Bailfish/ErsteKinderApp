# Ausmalspiel – Malen nach Zahlen (`paint_by_numbers`)

## 1. Übersicht & Spielziel
Das **Ausmalspiel (Malen nach Zahlen)** zeigt Bilder, die in klar abgegrenzte Bereiche (Regionen) unterteilt sind. Jeder Bereich trägt eine **Zahl (1, 2, 3, …)**, die für eine bestimmte Farbe in der Farbpalette steht. Tippt das Kind die passende Farbe und danach den Bereich mit dieser Zahl an, füllt sich das Feld bunt. Zusätzlich können **eigene Bilder hochgeladen** und mit **einstellbarer Farb-Granularität** in ein Ausmalbild umgewandelt werden.

## 2. Spielregeln im Detail
1. **Farbpalette:** Jede Farbe besitzt eine eindeutige **Nummer (`color_number`: 1 bis $K$)** und einen Hex-Farbcode (`#RRGGBB`).
2. **Regionen (Felder):** Jedes Bild besteht aus nummerierten Regionen (`region_id`, `target_color_number`, `painted_color_number`).
3. **Ausmalen (`paint_region`):**
   - Der Spieler wählt eine Farbnummer in der Palette aus und tippt auf einen Bereich im Bild.
   - **Standard-Modus (Kinderfreundlich / Hilfemodus):** Stimmt die gewählte Farbnummer mit der Zahl im Feld überein, wird das Feld dauerhaft in dieser Farbe ausgemalt. Stimmt sie nicht überein, gibt das Spiel einen freundlichen Hinweis („Fast! Dieses Feld hat die Nummer X“).
   - **Freier Modus (optional in den Einstellungen):** Auch andere Farben sind erlaubt; für den 100%-Abschluss zählen korrekt ausgemalte Felder.
4. **Eigene Bilder hochladen & Farb-Granularität:**
   - Über den Upload-Dialog kann jedes Bild (`PNG`, `JPG`, `WEBP`) hochgeladen werden.
   - Der Parameter **Granularität (`num_colors`, einstellbar von 3 bis 16 Farben)** bestimmt, in wie viele unterschiedliche Farben das hochgeladene Bild quantisiert und in ein Ausmal-Raster/Regionen-Modell zerlegt wird.
5. **Siegbedingung:** Sobald alle Regionen des Bildes mit ihrer zugehörigen Farbe gefüllt sind, ist das Kunstwerk zu 100 % fertiggestellt.

## 3. Vorlagen & Granularitäts-Stufen
- **Mitgelieferte Beispielbilder:**
  1. `sunny_house` – Sonniges Haus mit Garten
  2. `space_rocket` – Weltraum-Rakete mit Sternen
  3. `happy_butterfly` – Bunter Schmetterling
  4. `sailboat_sea` – Segelboot auf dem Meer
- **Eigener Bildupload (`granularity` / `num_colors`):**
  - *Grob / Leicht:* 4–6 Farben (große, einfache Farbflächen)
  - *Mittel:* 7–10 Farben (ausgewogene Details)
  - *Fein / Detailliert:* 11–16 Farben (feine Farbabstufungen)

## 4. Einstellungen im Zahnrad-Menü (⚙️)
- **Steuerung:**
  - *Maus / Touch:* Farbe antippen -> Zahlenfeld im Bild antippen.
  - *Tastatur:* Zifferntasten `1`–`9` wählen direkt die Farbnummer aus.
- **Zahlen-Prüfung (`strict_mode`):** Ein (nur richtige Farbnummer füllt das Feld) / Aus (freies Ausmalen).
- **Standard-Farbanzahl (Granularität) beim Upload:** 4 bis 16 Farben.

## 5. Architektur & Code-Verweise
- **Engine:** `app/games/paint_by_numbers/engine.py` (`PaintByNumbersEngine`)
- **Bildverarbeitung & Quantisierung:** `app/games/paint_by_numbers/image_processor.py` (`ImageProcessor`)
- **Beispielbilder:** `app/games/paint_by_numbers/templates_data.py`
- **Router:** `app/games/paint_by_numbers/router.py`
- **Tests:** `tests/test_paint_by_numbers.py`

## 6. API-Endpunkte
- `GET /api/paint-by-numbers/templates` – Liste aller Beispielbilder.
- `POST /api/paint-by-numbers/new` – Startet ein Ausmalspiel mit einem Beispielbild.
- `POST /api/paint-by-numbers/upload` – Lädt ein eigenes Bild hoch und erzeugt ein Ausmalspiel mit `num_colors` (Granularität) und `grid_size`.
- `POST /api/paint-by-numbers/paint` – Malt eine Region (`region_id`) mit `color_number` aus.
