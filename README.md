# CrewAI Vortragskonzept fuer Claude Code

Dieses Projekt ist ein kleines Vortrags- und Workshop-Setup fuer CrewAI mit
Claude/Anthropic. Die Beispiele starten bewusst lebensnah: Einkaufszettel,
Wochenendplan, Abendessen, Tagesplanung und kleiner Umzug. Das letzte Beispiel
ist eine kleine Dark-Factory fuer Software: mehrere Agents bauen gemeinsam einen
Python-Taschenrechner.

Die Beispiele werden Schritt fuer Schritt anspruchsvoller und sind jeweils
getrennt: eigene README, eigene Agent-Config, eigene Task-Config.

Wichtig: Claude Code selbst ist kein CrewAI-Modell-Endpunkt. Claude Code kann
dir beim Bearbeiten und Starten dieses Projekts helfen, aber CrewAI braucht zum
Ausfuehren einen Anthropic API Key.

## Voraussetzungen

- Python `>=3.10` und `<3.14`
- Windows mit PowerShell oder Linux/macOS mit einer Shell wie Bash/Zsh
- Anthropic API Key in `ANTHROPIC_API_KEY`

Die Python-Abhaengigkeiten stehen in `pyproject.toml`:

- `crewai[anthropic]`
- `pydantic`
- `PyYAML`

## Installation unter Windows

Im Projektordner in PowerShell ausfuehren:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Danach den API Key fuer die aktuelle PowerShell setzen:

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Optional kannst du das Modell ueberschreiben:

```powershell
$env:CREWAI_MODEL="anthropic/claude-sonnet-4-20250514"
```

Wenn `CREWAI_MODEL` nicht gesetzt ist, nutzt das Projekt
`anthropic/claude-sonnet-4-20250514`.

## Installation unter Linux/macOS

Im Projektordner in Bash oder Zsh ausfuehren:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Danach den API Key fuer die aktuelle Shell setzen:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Optional kannst du das Modell ueberschreiben:

```bash
export CREWAI_MODEL="anthropic/claude-sonnet-4-20250514"
```

Wenn `CREWAI_MODEL` nicht gesetzt ist, nutzt das Projekt
`anthropic/claude-sonnet-4-20250514`.

## Beispiele starten unter Windows

```powershell
crewai-examples 01
crewai-examples 02
crewai-examples 03
crewai-examples 04
crewai-examples 05
crewai-examples 06
```

Aliases funktionieren ebenfalls:

```powershell
crewai-examples basic
crewai-examples review
crewai-examples cooking
crewai-examples weekend
crewai-examples moving
crewai-examples coder
crewai-examples calculator
```

Alternativ geht der Start direkt als Python-Modul:

```powershell
python -m examples.main 01
```

## Beispiele starten unter Linux/macOS

```bash
crewai-examples 01
crewai-examples 02
crewai-examples 03
crewai-examples 04
crewai-examples 05
crewai-examples 06
```

Aliases funktionieren ebenfalls:

```bash
crewai-examples basic
crewai-examples review
crewai-examples cooking
crewai-examples weekend
crewai-examples moving
crewai-examples coder
crewai-examples calculator
```

Alternativ geht der Start direkt als Python-Modul:

```bash
python3 -m examples.main 01
```

## Vortragsdramaturgie

0. `00_config_erklaerung`: erklaert alle Config-Felder, die spaeter vorkommen.
1. `01_single_agent_no_tool`: ein Agent, eine Task, keine Tools.
2. `02_two_agents_no_tools`: zwei Agents, zwei Tasks, keine Tools.
3. `03_one_agent_one_tool`: ein Agent, eine Task, ein Tool.
4. `04_one_agent_multiple_tools`: ein Agent, mehrere Tools.
5. `05_multi_agent_with_tools`: mehrere Agents, Tools und Task-Kontext.
6. `06_dark_factory_calculator`: Dark-Factory mit Produktdesigner, Coder, Tester,
   QA-Checker sowie unterschiedlichen Modellen und Temperaturen pro Agent.

Die Idee: Erst Rollen und Tasks verstehen, dann Zusammenarbeit, danach Tools,
danach mehrere Tools, danach mehrere Agents mit Kontext, zuletzt eine kleine
Software-Dark-Factory mit agentenspezifischem Modell-Setup.

## Projektstruktur

```text
README.md
pyproject.toml
examples/
  main.py
  tools.py
  00_config_erklaerung/
    README.md
    config/
      agents.yaml
      tasks.yaml
  01_single_agent_no_tool/
    README.md
    config/
      agents.yaml
      tasks.yaml
  02_two_agents_no_tools/
    README.md
    config/
      agents.yaml
      tasks.yaml
  03_one_agent_one_tool/
    README.md
    config/
      agents.yaml
      tasks.yaml
  04_one_agent_multiple_tools/
    README.md
    config/
      agents.yaml
      tasks.yaml
  05_multi_agent_with_tools/
    README.md
    config/
      agents.yaml
      tasks.yaml
  06_dark_factory_calculator/
    README.md
    config/
      agents.yaml
      tasks.yaml
```

## Was wo passiert

- `examples/main.py` ist der Runner. Er nimmt das CLI-Argument entgegen, laedt
  die passende YAML-Config und startet die Crew.
- `examples/tools.py` enthaelt alle eigenen Tools. Tools sind Python-Code, weil
  sie echte Logik ausfuehren. Viele Tools erzeugen Lauf-IDs, Uhrzeiten,
  Zufallswerte oder kleine Berechnungen, damit im Vortrag sichtbar wird, dass
  wirklich Python-Code ausgefuehrt wurde.
- `agents.yaml` beschreibt Rollen, Ziele, Backstories und erlaubte Tools.
- Im letzten Beispiel beschreibt `agents.yaml` zusaetzlich pro Agent ein eigenes
  `llm`-Profil mit Modell, Temperatur und Tokenlimit.
- `tasks.yaml` beschreibt Aufgaben, erwartete Ergebnisse und optionalen
  Task-Kontext.
- Jede Beispiel-README erklaert Lernziel, Besonderheiten und Takeaways.

## Eigene Beispiele anlegen

1. Einen neuen Ordner unter `examples/` anlegen, z. B. `07_mein_beispiel`.
2. Darin `README.md`, `config/agents.yaml` und `config/tasks.yaml` erstellen.
3. Falls neue Tools noetig sind, diese in `examples/tools.py` implementieren.
4. Die Tools in `TOOL_REGISTRY` in `examples/main.py` registrieren.
5. Das neue Beispiel in `EXAMPLES` in `examples/main.py` eintragen.

## Typische Fehler

- `ANTHROPIC_API_KEY` fehlt: Der Crew-Run kann kein Claude-Modell aufrufen.
- Virtuelle Umgebung ist nicht aktiv: `crewai-examples` wird nicht gefunden.
- Neues Tool steht in YAML, aber nicht in `TOOL_REGISTRY`: Der Runner kennt den
  Tool-Namen nicht.
- Task-Kontext verweist auf eine Task, die in `tasks.yaml` erst spaeter
  definiert ist: Kontext-Tasks muessen vor der nutzenden Task stehen.

## Was der Vortrag vermitteln soll

- CrewAI trennt Rollen, Aufgaben, Tools und Ablauf.
- YAML ist gut fuer Prompts, Rollen und Aufgaben geeignet.
- Python bleibt der richtige Ort fuer Tool-Logik und Orchestrierung.
- Tools sind nicht nur Datenquellen, sondern koennen auch Guardrails sein.
- Mehrere Agents lohnen sich erst, wenn sie unterschiedliche Rollen oder
  Denkmodi abbilden.
