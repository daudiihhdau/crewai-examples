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

## Python installieren

### Windows

Empfohlen ist eine normale Python-Installation von `python.org` oder ueber den
Windows-Paketmanager `winget`.

Mit `winget`:

```powershell
winget install Python.Python.3.12
```

Danach PowerShell neu oeffnen und pruefen:

```powershell
python --version
pip --version
```

Falls `python` nicht gefunden wird, pruefe bei der Installation, ob Python zum
`PATH` hinzugefuegt wurde. Alternativ funktioniert auf vielen Windows-Systemen
auch der Python-Launcher:

```powershell
py --version
py -m pip --version
```

### Linux

Unter Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Pruefen:

```bash
python3 --version
python3 -m pip --version
```

Unter anderen Distributionen installierst du entsprechend `python3`, `venv` und
`pip` ueber den jeweiligen Paketmanager.

### macOS

Mit Homebrew:

```bash
brew install python
```

Pruefen:

```bash
python3 --version
python3 -m pip --version
```

## Was ist eine virtuelle Umgebung?

Eine virtuelle Umgebung ist ein lokaler Python-Arbeitsbereich fuer dieses
Projekt. Die Abhaengigkeiten werden dann in `.venv` installiert und nicht global
auf deinem System verteilt.

Dieses Projekt nutzt:

```text
.venv/
```

Der Ordner muss nicht nach GitHub gepusht werden. Er kann jederzeit neu erstellt
werden.

## Installation ohne virtuelle Umgebung

Du kannst das Projekt auch ohne `.venv` installieren. Das ist fuer schnelle
Server-Tests okay, aber weniger sauber, weil die Pakete dann in die aktuelle
Python-Umgebung installiert werden.

Nutze diese Variante nur, wenn du weisst, welche Python-Umgebung aktiv ist, z. B.
auf einem frischen Server oder in einem Wegwerf-Container.

### Windows ohne venv

```powershell
python -m pip install -e .
```

Mit Python-Launcher:

```powershell
py -m pip install -e .
```

Start:

```powershell
crewai-examples 01
```

Falls `crewai-examples` nicht gefunden wird, nutze direkt:

```powershell
python -m examples.main 01
```

### Linux/macOS ohne venv

```bash
python3 -m pip install -e .
```

Start:

```bash
crewai-examples 01
```

Falls `crewai-examples` nicht gefunden wird, nutze direkt:

```bash
python3 -m examples.main 01
```

Auf manchen Linux-Systemen verhindert Python globale Installationen und zeigt
einen Hinweis wie `externally-managed-environment`. Dann nimm besser die
`.venv`-Variante oder, nur wenn du es wirklich willst:

```bash
python3 -m pip install -e . --break-system-packages
```

## Installation unter Windows

Im Projektordner in PowerShell ausfuehren:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Falls du den Windows-Python-Launcher nutzt:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e .
```

Was hier passiert:

- `python -m venv .venv` erstellt die virtuelle Umgebung.
- `.\.venv\Scripts\Activate.ps1` aktiviert sie in der aktuellen PowerShell.
- `pip install -e .` liest `pyproject.toml`, installiert die Abhaengigkeiten und
  registriert den Befehl `crewai-examples`.

Danach den API Key fuer die aktuelle PowerShell setzen:

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Optional kannst du das Modell ueberschreiben:

```powershell
$env:CREWAI_MODEL="anthropic/claude-sonnet-4-6"
```

Wenn `CREWAI_MODEL` nicht gesetzt ist, nutzt das Projekt
`anthropic/claude-sonnet-4-6`.

## Installation unter Linux/macOS

Im Projektordner in Bash oder Zsh ausfuehren:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Was hier passiert:

- `python3 -m venv .venv` erstellt die virtuelle Umgebung.
- `source .venv/bin/activate` aktiviert sie in der aktuellen Shell.
- `pip install -e .` liest `pyproject.toml`, installiert die Abhaengigkeiten und
  registriert den Befehl `crewai-examples`.

Danach den API Key fuer die aktuelle Shell setzen:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Optional kannst du das Modell ueberschreiben:

```bash
export CREWAI_MODEL="anthropic/claude-sonnet-4-6"
```

Wenn `CREWAI_MODEL` nicht gesetzt ist, nutzt das Projekt
`anthropic/claude-sonnet-4-6`.

## pyproject.toml starten und verstehen

`pyproject.toml` ist die Projektbeschreibung fuer Python. Darin stehen Name,
Python-Version, Abhaengigkeiten und der Startbefehl:

```toml
[project.scripts]
crewai-examples = "examples.main:main"
```

Das bedeutet: Nach `pip install -e .` kannst du das Projekt mit
`crewai-examples` starten. Intern ruft Python dann die Funktion `main()` aus
`examples/main.py` auf.

Typischer Ablauf:

```text
pyproject.toml -> pip install -e . -> crewai-examples -> examples.main:main
```

Wenn du das Projekt ohne installierten Script-Befehl starten willst, geht auch:

```powershell
python -m examples.main 01
```

oder unter Linux/macOS:

```bash
python3 -m examples.main 01
```

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
