# 4 Gewinnt (`connect_four`)

## 1. Übersicht & Spielziel
**4 Gewinnt** ist ein rundenbasiertes Strategiespiel für zwei Parteien auf einem senkrechten Spielbrett mit **7 Spalten** und **6 Reihen**. Ziel ist es, als Erster **vier eigene Spielsteine** in eine horizontale, vertikale oder diagonale Reihe zu bringen.

## 2. Spielregeln im Detail
1. **Spielfeld:** 6 Zeilen (`rows = 6`) × 7 Spalten (`cols = 7`).
2. **Spielsteine:** Spieler 1 spielt mit **Rot (`1`)**, Spieler 2 bzw. der Computer spielt mit **Gelb (`2`)**. Leere Felder haben den Wert `0`.
3. **Zugmechanik (Schwerkraft):** Ein Spielstein wird in eine der 7 Spalten (`0` bis `6`) eingeworfen und fällt automatisch auf das unterste freie Feld dieser Spalte.
4. **Ungültige Züge:** Ist eine Spalte bereits voll (oberste Zeile belegt) oder das Spiel bereits beendet, ist der Einwurf in diese Spalte nicht erlaubt.
5. **Spielende:**
   - **Sieg:** Vier Steine derselben Farbe liegen unmittelbar nebeneinander (waagerecht, senkrecht oder diagonal). Die 4 Gewinnkoordinaten werden hervorgehoben.
   - **Unentschieden (Remis):** Alle 42 Felder sind belegt, ohne dass jemand eine Viererreihe gebildet hat.

## 3. Schwierigkeitsgrade & Spielmodi
- **2 Spieler (`pvp`):** Zwei menschliche Spieler wechseln sich am selben Gerät ab.
- **Gegen Computer (`ai`):**
  - **Leicht (`easy`):** Nutzt sofortige Gewinnzüge und blockiert offensichtliche direkte 4er-Drohungen mit gewisser Wahrscheinlichkeit, wählt ansonsten zufällige gültige Spalten.
  - **Mittel (`medium`):** Nutzt den **Minimax-Algorithmus** mit Suchtiefe 3 und einer Heuristik für Zweier-/Dreier-Ketten.
  - **Schwer (`hard`):** Nutzt **Minimax mit Alpha-Beta-Pruning** (Suchtiefe 5), bevorzugt die mittlere Spalte und erkennt Doppel-Drohungen frühzeitig.

## 4. Einstellungen im Zahnrad-Menü (⚙️)
- **Steuerung:**
  - *Maus / Touch:* Antippen der gewünschten Spalte.
  - *Tastatur:* Pfeiltasten Links/Rechts oder Tasten `1`–`7` zur Spaltenwahl, `Leertaste`/`Enter` zum Einwerfen.
- **Standard-Schwierigkeit:** Leicht / Mittel / Schwer.
- **Spielmodus:** Gegen Computer oder 2. Spieler.

## 5. Architektur & Code-Verweise
- **Engine:** `app/games/connect_four/engine.py` (`ConnectFourEngine`)
- **KI:** `app/games/connect_four/ai.py` (`ConnectFourAI`)
- **Router:** `app/games/connect_four/router.py`
- **Tests:** `tests/test_connect_four.py`

## 6. API-Endpunkte
- `POST /api/connect-four/new` – Startet ein neues Spiel (`mode`, `difficulty`).
- `POST /api/connect-four/move` – Führt einen Spielerzug in Spalte `column` aus (und berechnet im KI-Modus direkt den Gegenzug).
- `GET /api/connect-four/state/{game_id}` – Liefert den aktuellen Spielzustand.
