# 10 Geburtstagsfeier: Flow als Rahmen um Crews

## Lernziel

Dieses Beispiel bleibt lebensnah, wird aber anspruchsvoller: Eine kleine
Kindergeburtstagsfeier hat mehrere Teilaufgaben. Hier sieht man, warum ein Flow
spaeter mehrere Crews oder Agentenablaeufe koordinieren kann.

## Use-Case

Samstag von 15:00 bis 18:00 kommen Kinder zu Besuch. Es braucht Kuchen, Spiele,
Einkauf, Helfer und eine kurze Nachricht an die Eltern.

```text
Wunsch aufnehmen
-> Planungs-Crew macht Vorschlag
-> Validator prueft Budget, Zeit und Helfer
-> bei Problemen zur Planung zurueck
-> bei PASS Nachricht an Eltern schreiben
```

## Was passiert?

- Der Flow haelt den Gesamtzustand.
- Eine Planungs-Crew waere fuer Kuchen, Spiele und Aufgaben zustaendig.
- Ein Validator prueft, ob der Plan alltagstauglich ist.
- Eine zweite Crew koennte daraus eine kurze Elternnachricht schreiben.

## Was man lernt

- Crews erledigen Rollenarbeit.
- Der Flow haelt den Prozess zusammen.
- Der Flow entscheidet, ob ueberarbeitet oder abgeschlossen wird.
- Das Muster ist realistisch fuer Planung, Support, Coding und andere
  mehrstufige Prozesse.

## Unterschied: Crew, Process, Flow

```text
Crew:
    Wer arbeitet mit welchen Rollen?

Process:
    Wie laufen Tasks innerhalb einer Crew?

Flow:
    Wann startet was, welcher Pfad kommt danach,
    wann wird wiederholt und wann ist Schluss?
```

## Start

```powershell
crewai-examples 10
crewai-examples geburtstag
```

Linux/macOS:

```bash
crewai-examples 10
crewai-examples geburtstag
```
