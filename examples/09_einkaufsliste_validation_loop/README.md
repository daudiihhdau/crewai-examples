# 09 Einkaufsliste: Flow mit Budgetpruefung

## Lernziel

Dieses Beispiel zeigt einen Loop mit klarer Pruefung. Der Flow versucht eine
Einkaufsliste zu bauen, bis sie ins Budget passt.

## Use-Case

Du willst fuer maximal 18 Euro einkaufen. Der Flow stellt einen Warenkorb
zusammen und prueft danach maschinell:

```text
summe <= 18
```

Wenn die Liste zu teuer ist, startet eine neue Runde.

## Was passiert?

- Der Flow merkt sich das Budget.
- Jede Runde erzeugt einen Warenkorb.
- Ein Validator prueft die Summe.
- Bei `PASS` stoppt der Flow.
- Bei `FAIL` wird Feedback gespeichert und neu versucht.

## Was man lernt

- Loops brauchen ein hartes Abbruchkriterium.
- Loops brauchen eine maximale Rundenzahl.
- Der Validator sollte kein Agentengefuehl sein, sondern Code.
- Das ist dieselbe Grundidee wie Coder -> Tester -> Coder, nur viel einfacher.

## Start

```powershell
crewai-examples 09
crewai-examples einkaufsliste
```

Linux/macOS:

```bash
crewai-examples 09
crewai-examples einkaufsliste
```
