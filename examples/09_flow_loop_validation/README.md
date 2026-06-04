# 09 Flow mit Validierungsloop

## Lernziel

Dieses Beispiel macht den Schritt von Branching zu Wiederholung. Ein Flow kann
einen Schritt erneut ausfuehren, bis ein Validator zufrieden ist.

## Use-Case

Ein kleiner Warenkorb soll unter 18 Euro bleiben. Der Flow erzeugt Vorschlaege
und prueft danach maschinell:

```text
total <= budget
```

Wenn der Warenkorb zu teuer ist, startet eine neue Runde.

## Was ist neu?

- Der Flow hat ein klares Abbruchkriterium.
- Jede Runde schreibt Feedback in den State.
- Das System weiss selbst, wann es fertig ist.
- Das Muster ist die einfache Variante von Coder -> Tester -> Coder.

## Warum braucht man das?

Loops sind sinnvoll, wenn ein Ergebnis nicht nur schoen klingen, sondern eine
harte Bedingung erfuellen muss:

- Budget passt
- Unit-Tests bestehen
- JSON ist gueltig
- Pflichtfelder sind vollstaendig
- Linting ist gruen

## Mitnehmen

- Loops brauchen ein Limit, damit sie nicht endlos laufen.
- Loops brauchen ein klares PASS/FAIL-Signal.
- Der Validator sollte moeglichst deterministisch sein.
- Agenten duerfen verbessern, aber Tools oder Code sollten entscheiden.

## Start

```powershell
crewai-examples 09
```

Linux/macOS:

```bash
crewai-examples 09
```
