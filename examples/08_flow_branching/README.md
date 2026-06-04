# 08 Flow mit Branching

## Lernziel

Dieses Beispiel zeigt, warum Flows mehr koennen als eine lineare Task-Liste:
Sie koennen zur Laufzeit einen Pfad auswaehlen.

## Use-Case

Ein Tagesplan soll sich nach einfachen Daten richten:

- hohe Regenwahrscheinlichkeit: Plan fuer drinnen
- wenig Budget: sparsamer Plan
- sonst: Plan fuer draussen

## Was ist neu?

Der Flow hat eine Entscheidungsstelle:

```text
start -> choose_branch -> execute_branch
```

`choose_branch` entscheidet anhand des State, welcher Plan entsteht.

## Warum braucht man das?

Bei einer normalen Crew mit `Process.sequential` laufen Tasks nacheinander. Das
ist gut fuer einfache Pipelines. Branching wird wichtig, wenn ein Ablauf nicht
immer gleich sein soll.

## Mitnehmen

- Branching gehoert in die Orchestrierung.
- Agents koennen Inhalte liefern, aber der Flow entscheidet den Pfad.
- Bedingungen sollten moeglichst klar und maschinell pruefbar sein.
- Branching ist der erste Schritt zu robusteren Workflows.

## Start

```powershell
crewai-examples 08
```

Linux/macOS:

```bash
crewai-examples 08
```
