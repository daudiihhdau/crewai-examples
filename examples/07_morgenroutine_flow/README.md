# 07 Morgenroutine: erster Flow mit State

## Lernziel

Dieses Beispiel fuehrt Flows mit einer einfachen Alltagssituation ein: Morgens
puenktlich aus dem Haus kommen. Es gibt noch keine Agenten und keine Tools. Der
Flow sammelt nur Fakten, merkt sie sich im State und baut daraus einen kleinen
Plan.

## Use-Case

Du musst den Bus um 08:12 bekommen. Vorher sollen Brotbox, Schluessel und
Muellsack nicht vergessen werden.

```text
start -> fixpunkte_sammeln -> plan_bauen
```

## Was passiert?

- `start` merkt sich das Ziel.
- `fixpunkte_sammeln` legt Buszeit, Brotbox und Muellsack in den State.
- `plan_bauen` erstellt daraus einen einfachen Morgenplan.

## Was man lernt

- Ein Flow ist gut fuer Ablaufsteuerung.
- Der State ist wie ein kleiner Notizzettel fuer den ganzen Ablauf.
- Nicht jede Aufgabe braucht sofort Agents.
- Man startet mit Flows am besten bei kleinen, klaren Alltagsablaeufen.

## CrewAI-Begriffe

```text
Flow      = Klasse fuer den gesamten Ablauf
@start    = Einstiegspunkt
@listen   = Schritt reagiert auf vorherigen Schritt
@router   = Schritt entscheidet spaeter den naechsten Pfad
state     = gemeinsamer Zustand des Flows
```

Dieses Beispiel bildet die Idee didaktisch mit einfachem Python nach. So sieht
man zuerst das Muster, bevor die volle CrewAI-Flow-API dazukommt.

## Start

```powershell
crewai-examples 07
crewai-examples morgenroutine
```

Linux/macOS:

```bash
crewai-examples 07
crewai-examples morgenroutine
```
