# 06 Dark-Factory: Taschenrechner-Crew

## Lernziel

Das letzte Beispiel zeigt eine kleine "Dark Factory" fuer Software: mehrere
Agents arbeiten nacheinander an einem winzigen Produkt. Gebaut wird kein grosses
System, sondern ein einfacher Taschenrechner in Python.

## Rollen

- Produktdesigner: legt fest, was der Taschenrechner koennen soll.
- Coder: schreibt den Python-Code.
- Tester: entwirft einfache Testfaelle.
- QA-Checker: prueft, ob Code und Tests zur Anforderung passen.

## Besonderheiten

- Vier Agents mit klar getrennten Aufgaben.
- Task-Kontext wandert von Produktidee zu Code, Tests und QA.
- Jede Station nutzt ein eigenes Tool:
  `taschenrechner_anforderungen`, `code_vorgaben`,
  `testfall_vorschlaege`, `unit_tests_ausfuehren`,
  `linting_ausfuehren`, `bash_befehl_ausfuehren` und
  `taschenrechner_qa_check`.
- `bash_befehl_ausfuehren` darf beliebige Bash-Kommandos ausfuehren, z. B.
  `python --version`, `pip install ...`, `pytest` oder eigene Skripte. Das ist
  fuer eine Dark-Factory realistisch, sollte aber nur in einer passenden
  Entwicklungsumgebung laufen.
- Coder und Tester arbeiten in einer echten Pruefschleife:
  Der Coder schreibt Code, der Runner fuehrt Linting und Unit-Tests aus, der
  Tester bewertet die echten Ergebnisse und gibt Feedback zurueck. Bei Fehlern
  startet die Coder-Runde erneut.
- Die Unit-Tests werden wirklich mit `python -m unittest -v` ausgefuehrt.
- Das Linting wird wirklich mit Python-Code ausgefuehrt: Syntaxpruefung per
  `ast.parse`, Pflichtfunktionen, Zeilenlaenge, Tabs und `eval`/`exec`.
- Auf Windows braucht das Bash-Tool Git Bash oder WSL. Unter Linux/macOS ist
  Bash meist direkt verfuegbar.
- Die Agents nutzen unterschiedliche Modelle und Temperaturen:
  Produktdesigner und Tester laufen mit einem leichten Modell, Coder und
  QA-Checker mit einem staerkeren Modell.
- Das Produkt bleibt klein genug, um es im Vortrag komplett zu verstehen.

## Mitnehmen

- Eine Agenten-Crew kann wie eine kleine Produktionslinie funktionieren.
- Rollen helfen, Denken zu trennen: Produkt, Umsetzung, Test, Qualitaet.
- Eine Agentenschleife ist dann sinnvoll, wenn ein Pruefergebnis maschinell
  entschieden werden kann: hier `UNIT_TEST_STATUS: PASS` und `LINT_STATUS: PASS`.
- Pro Agent kann ein eigenes `llm`-Profil in `agents.yaml` stehen.
- Auch ein Coder-Beispiel sollte klein genug bleiben, damit man die CrewAI-Idee
  erkennt und nicht im Produkt selbst versinkt.

## Ist das der normale CrewAI-Weg?

Nicht immer. Der typische CrewAI-Ablauf ist erstmal linear:

```text
Agent A -> Task A
Agent B -> Task B bekommt Kontext von Task A
Agent C -> Task C bekommt Kontext von Task A und B
```

Das reicht fuer viele Beispiele. Man beschreibt Agents in `agents.yaml`, Tasks
in `tasks.yaml` und verbindet Tasks ueber `context`.

Die Coder-Tester-Schleife in diesem Beispiel ist bewusst fortgeschrittener. Sie
steht nicht nur in YAML, sondern in `examples/main.py`, weil Python entscheiden
muss:

- Wie viele Runden sind erlaubt?
- Welches Tester-Feedback bekommt der Coder in der naechsten Runde?
- Wann ist das Ziel erreicht?
- Was passiert bei Fehlern?

Best Practice:

```text
Einfacher Ablauf:
    YAML-Tasks mit context reichen.

Mehrstufige Pipeline:
    mehrere Tasks nacheinander in YAML.

Feedback-Schleife:
    Python-Orchestrierung um CrewAI herum.

Harte Qualitaetspruefung:
    echte Tools, Tests oder Validatoren ausfuehren.
```

Diese Schleife lohnt sich hier, weil es ein klares Abbruchkriterium gibt:

```text
UNIT_TEST_STATUS: PASS
und
LINT_STATUS: PASS
```

Ohne klares Kriterium koennen Agentenschleifen schnell unklar werden. Dann
diskutieren Agents nur weiter, ohne dass das System sicher weiss, wann es fertig
ist.

## Modelle anpassen

In `config/agents.yaml` stehen pro Agent eigene `llm`-Einstellungen. Du kannst
die Modelle direkt in YAML aendern oder per Umgebungsvariable ueberschreiben:

```powershell
$env:CREWAI_LEICHTES_MODELL="anthropic/dein-leichtes-modell"
$env:CREWAI_STARKES_MODELL="anthropic/dein-starkes-modell"
```

## Start

```powershell
crewai-examples 06
```

Die Pruefschleife laeuft standardmaessig maximal vier Runden. Du kannst das
ueber eine Umgebungsvariable aendern.

Windows:

```powershell
$env:CREWAI_DARK_FACTORY_MAX_RUNS="6"
crewai-examples 06
```

Linux/macOS:

```bash
export CREWAI_DARK_FACTORY_MAX_RUNS="6"
crewai-examples 06
```
