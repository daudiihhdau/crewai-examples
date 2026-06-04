# 08 Wochenendplan: Flow mit Abzweigung

## Lernziel

Dieses Beispiel zeigt Branching an einem normalen Samstag. Der Plan haengt von
zwei einfachen Dingen ab: Regen und Budget.

## Use-Case

Du willst Samstagvormittag etwas Schoenes machen. Der Flow entscheidet:

- viel Regen: drinnen bleiben
- wenig Budget: sparsame Variante
- sonst: raus auf Markt, Spielplatz oder Parkrunde

```text
daten_sammeln -> route_waehlen -> plan_ausgeben
```

## Was passiert?

- Der Flow erzeugt eine Regenwahrscheinlichkeit.
- Der Flow erzeugt ein kleines Tagesbudget.
- Eine Bedingung entscheidet den Pfad.
- Je nach Pfad entsteht ein anderer Plan.

## Was man lernt

- Branching ist praktisch, wenn ein Ablauf nicht immer gleich sein soll.
- Der Flow entscheidet anhand von Daten, nicht anhand eines Bauchgefuehls.
- Eine Crew waere hier uebertrieben, weil keine Rolle kreativ zusammenarbeiten
  muss.
- Flows machen solche Alltagsentscheidungen gut sichtbar.

## Start

```powershell
crewai-examples 08
crewai-examples wochenendplan
```

Linux/macOS:

```bash
crewai-examples 08
crewai-examples wochenendplan
```
