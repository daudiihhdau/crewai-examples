# 10 Flow orchestriert Crews

## Lernziel

Dieses Beispiel zeigt den anspruchsvolleren Zielzustand: Ein Flow kann mehrere
Crews oder Agentenablaeufe koordinieren. Die Crew macht Denk- und Schreibarbeit,
der Flow kontrolliert den Prozess.

## Use-Case

Eine kleine Geburtstagsfeier wird geplant:

```text
Flow startet mit Wunsch
-> Planungs-Crew erstellt Plan
-> Validator prueft Budget, Zeit und Helfer
-> bei Fehlern zur Planungs-Crew zurueck
-> bei PASS zur Zusammenfassungs-Crew
-> finale Nachricht
```

## Was ist neu?

- Der Flow ist der Rahmen um mehrere moegliche Crews.
- Crews bleiben fuer Rollen und Aufgaben zustaendig.
- Der Flow entscheidet ueber Wiederholung, Abbruch und Uebergabe.
- Das Muster laesst sich auf echte Coding-, Support- oder Planungsprozesse
  uebertragen.

## Unterschied: Crew, Process, Flow

```text
Crew:
    Gruppe von Agents und Tasks.

Process:
    Wie Tasks innerhalb einer Crew abgearbeitet werden,
    z. B. sequential oder hierarchical.

Flow:
    Uebergeordnete Ablaufsteuerung mit State, Branching, Loops
    und Integration von Crews, Tools oder normalem Python-Code.
```

## Warum braucht man Flows?

Flows werden wichtig, wenn ein Workflow produktionsnaeher wird:

- Entscheidungen zur Laufzeit
- mehrere moegliche Pfade
- Wiederholung mit Abbruchkriterium
- Zustand ueber mehrere Schritte hinweg
- Kombination aus normalem Python-Code, Tools und Crews

## Mitnehmen

- Ein Flow ist nicht einfach ein weiterer Agent.
- Ein Flow ist die Prozesslogik um Agenten herum.
- Crews sind gut fuer Arbeitsrollen.
- Flows sind gut fuer Steuerung, Zustand und Verlaesslichkeit.
- Je kritischer das Ergebnis, desto wichtiger werden echte Validatoren.

## Start

```powershell
crewai-examples 10
```

Linux/macOS:

```bash
crewai-examples 10
```
