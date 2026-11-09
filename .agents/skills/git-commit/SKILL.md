---
name: git-commit
description: Erstellt strukturierte, konventionelle Git-Commits nach erfolgreicher Prüfung der Test-Suite und Test-Coverage (>= 80%).
---

# Skill: Git Commit (`git-commit`)

Verwende diesen Skill immer dann, wenn Änderungen im Repository committet werden sollen.

## Voraussetzungen & Qualitäts-Gate
Bevor ein Commit durchgeführt wird, **muss** sichergestellt sein:
1. Alle Unit- und Integrationstests laufen fehlerfrei durch.
2. Die Test-Coverage liegt bei **mindestens 80 %**.
3. Keine temporären Dateien (`.venv`, `__pycache__`, `.coverage`) werden versehentlich gestaged.

## Ablauf (Schritt-für-Schritt)

### 1. Tests und Coverage prüfen
Führe die Test-Suite aus:
```bash
.venv/bin/pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```
*Schlägt der Befehl fehl oder liegt die Coverage unter 80 %, darf noch nicht committet werden. Behebe zuerst den Fehler oder ergänze Tests.*

### 2. Git-Status und Diff inspizieren
```bash
git status --short
git diff --stat
```
Prüfe, ob bei Änderungen an Spielregeln auch `docs/knowledge_base/` und bei strukturellen Änderungen `SURGERY_MAP.md` aktualisiert wurden.

### 3. Dateien stagen und Conventional Commit erstellen
Nutze das Conventional-Commit-Format:
- `feat(<scope>): <kurze Beschreibung>` – Neues Feature oder Minispiel
- `fix(<scope>): <kurze Beschreibung>` – Fehlerbehebung
- `test(<scope>): <kurze Beschreibung>` – Neue oder erweiterte Tests
- `docs(<scope>): <kurze Beschreibung>` – Änderungen an Knowledge Base oder Surgery Map
- `refactor(<scope>): <kurze Beschreibung>` – Clean-Code-Verbesserungen

Beispiel:
```bash
git add -A
git commit -m "feat(connect-four): implement engine and minimax AI with >80% test coverage"
```
