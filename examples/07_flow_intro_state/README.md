# 07 Flow Intro: State und Schritte

## Lernziel

Dieses Beispiel fuehrt CrewAI Flows als neues Konzept ein. Bis Beispiel 06
standen Agents, Tasks, Tools und Crews im Mittelpunkt. Ab hier geht es um
Ablaufsteuerung: Ein Flow haelt Zustand, fuehrt Schritte aus und entscheidet,
was als Naechstes passiert.

## Use-Case

Eine einfache Tagesplanung wird in drei klaren Schritten aufgebaut:

```text
start -> prepare_data -> finish
```

Es gibt noch keine Agenten. Das ist Absicht, damit zuerst der Unterschied
zwischen Crew und Flow sichtbar wird.

## Was ist neu?

- Ein Flow hat einen `state`, also Zwischendaten, die Schritte gemeinsam nutzen.
- Schritte sind normale Python-Funktionen mit klaren Namen.
- Der Ablauf ist explizit im Code sichtbar.
- Keine LLM-Antwort entscheidet ueber die Reihenfolge.

In echten CrewAI Flows sieht man dafuer typischerweise Begriffe wie:

```text
Flow      = Klasse fuer den gesamten Ablauf
@start    = Einstiegspunkt
@listen   = Schritt reagiert auf vorherigen Schritt
@router   = Schritt entscheidet den naechsten Pfad
state     = gemeinsamer Zustand des Flows
```

Die Beispiele 07 bis 10 bilden diese Ideen didaktisch mit einfachem Python nach,
damit man das Muster versteht, bevor man die volle API nutzt.

## Unterschied zur Crew

Eine Crew ist gut, wenn Agents Aufgaben bearbeiten sollen:

```text
Agent -> Task -> Antwort
```

Ein Flow ist gut, wenn der Ablauf selbst wichtig wird:

```text
Schritt -> State aktualisieren -> naechster Schritt
```

## Mitnehmen

- Flows sind Orchestrierung.
- Crews sind Agentenarbeit.
- Der einfachste Flow braucht noch kein Branching und keine Schleife.
- State ist der Ort, an dem Zwischenergebnisse sauber abgelegt werden.

## Start

```powershell
crewai-examples 07
```

Linux/macOS:

```bash
crewai-examples 07
```
