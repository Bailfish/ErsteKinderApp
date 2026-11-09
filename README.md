# ErsteKinderApp – Kinder-Minispiele Webapp

Eine kindgerechte, farbenfrohe Webanwendung in Python (**FastAPI**, **Clean Architecture**) mit vier direkt spielbaren Minispielen:

1. **4 Gewinnt (`connect_four`)**: Spiele gegen einen 2. menschlichen Spieler oder gegen Computergegner in 3 Schwierigkeitsstufen (*Leicht*, *Mittel*, *Schwer*).
2. **Farbsortierspiel (`color_sort`)**: Sortiere bunte Flüssigkeiten in Reagenzgläsern so um, dass jedes Glas nur noch eine einzige Farbe enthält.
3. **Ausmalspiel – Malen nach Zahlen (`paint_by_numbers`)**: Male liebevolle Beispielbilder durch Antippen der nummerierten Felder aus oder lade **eigene Bilder** hoch (mit frei einstellbarer Farb-Granularität von 3 bis 16 Farben).
4. **Jump & Run (`jump_and_run`)**: Weiche herannahenden Boden- und Luft-Hindernissen durch geschicktes Springen und Ducken aus.

Jedes Spiel verfügt oben rechts über ein **Zahnrad-Menü (⚙️)** zum Anpassen der Steuerung (Tastatur, Maus/Touch, Sprungtaste), des Schwierigkeitsgrads und des Tons.

---

## Schnellstart

```bash
# 1. Virtuelle Umgebung aktivieren
source .venv/bin/activate

# 2. Webapp starten
uvicorn app.main:app --reload --port 8000
```
Öffne anschließend **http://127.0.0.1:8000** im Browser.

## Tests & Coverage (Mindestens 80 %)

```bash
.venv/bin/pytest
```

## Dokumentation für Entwickler & KI-Agenten

- **Architektur-Landkarte:** [`SURGERY_MAP.md`](SURGERY_MAP.md)
- **Spielregeln & Knowledge Base:** [`docs/knowledge_base/INDEX.md`](docs/knowledge_base/INDEX.md)
- **Agent Skills:** `.agents/skills/` (`git-commit`, `git-feature-branch`, `knowledge-base-manager`)
