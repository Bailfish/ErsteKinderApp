---
name: git-feature-branch
description: Erstellt, wechselt und integriert Feature-Branches nach einheitlicher Namenskonvention für neue Minispiele und Features.
---

# Skill: Git Feature Branch (`git-feature-branch`)

Verwende diesen Skill, um isolierte Feature-Branches für neue Minispiele, Erweiterungen oder Refactorings zu erstellen und sauber in `main` zurückzuführen.

## Namenskonvention
Branches folgen immer dem Muster:
- `feature/<spiel-oder-thema>` (z. B. `feature/connect-four`, `feature/color-sort`, `feature/paint-by-numbers`, `feature/jump-and-run`)
- `fix/<problem>` (z. B. `fix/color-sort-undo`)
- `docs/<thema>` (z. B. `docs/knowledge-base-update`)

## Ablauf (Schritt-für-Schritt)

### 1. Aktuellen Status und Branch prüfen
```bash
git status
git branch --show-current
```
Stelle sicher, dass der Arbeitsbaum sauber ist, bevor du den Branch wechselst.

### 2. Feature-Branch von `main` erstellen
```bash
git checkout main
git checkout -b feature/<name>
```

### 3. Auf dem Feature-Branch entwickeln & committen
Entwickle das Feature nach dem Clean-Code-Prinzip (Engine -> Router -> Template/JS -> Tests -> Knowledge Base) und nutze den Skill `git-commit` für saubere Zwischen- oder Abschluss-Commits.

### 4. Feature-Branch nach `main` mergen (optional nach Abschluss)
Sobald alle Tests (`pytest --cov=app --cov-fail-under=80`) grün sind:
```bash
git checkout main
git merge --no-ff feature/<name> -m "Merge branch 'feature/<name>' into main"
```
