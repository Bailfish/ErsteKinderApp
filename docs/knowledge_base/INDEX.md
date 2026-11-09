# Knowledge Base – ErsteKinderApp Minispiele

Willkommen in der zentralen **Knowledge Base** der `ErsteKinderApp`. Hier sind alle verfügbaren Minispiele, deren Spielregeln, Schwierigkeitsgrade, Steuerungsoptionen im Zahnrad-Menü (⚙️) sowie technische Schnittstellen dokumentiert.

## Übersicht der Minispiele

| ID | Spielname | Kurzbeschreibung | Modi / Besonderheiten | Doku-Link |
| :--- | :--- | :--- | :--- | :--- |
| `connect_four` | **4 Gewinnt** | Klassisches Strategiespiel auf einem 6×7-Raster | Gegen Computer (*Leicht*, *Mittel*, *Schwer*) oder 2. Spieler | [`connect_four.md`](connect_four.md) |
| `color_sort` | **Farbsortierspiel** | Sortiere bunte Flüssigkeiten in Reagenzgläsern | Garantierte Lösbarkeit, Undo-Funktion, 3 Schwierigkeitsstufen | [`color_sort.md`](color_sort.md) |
| `paint_by_numbers` | **Ausmalspiel (Malen nach Zahlen)** | Tippe nummerierte Felder an, um Bilder bunt auszumalen | Beispielbilder + **Eigener Bildupload** mit einstellbarer Farb-Granularität | [`paint_by_numbers.md`](paint_by_numbers.md) |
| `jump_and_run` | **Jump & Run** | Weiche herannahenden Hindernissen durch Springen & Ducken aus | Einstellbare Steuerung (Tastatur/Maus/Touch), dynamische Hindernisse | [`jump_and_run.md`](jump_and_run.md) |

## Globales Zahnrad-Einstellungsmenü (⚙️)
Jedes Minispiel besitzt oben rechts ein **Zahnrad-Symbol**. Darüber können jederzeit folgende Parameter angepasst werden:
- **Steuerungsart (`control_scheme`):** `mouse_touch` (Maus / Antippen), `keyboard` (Tastatur) oder `hybrid` (Beides aktiv).
- **Primäre Aktionstaste (`primary_key`):** z. B. `Space` (Leertaste), `ArrowUp` (Pfeil hoch) oder `KeyW`.
- **Schwierigkeitsgrad (`difficulty`):** `easy` (Leicht), `medium` (Mittel), `hard` (Schwer).
- **Soundeffekte (`sound_enabled`):** Ein / Aus.
