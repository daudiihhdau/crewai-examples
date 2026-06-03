# 00 Aufbau der Config

Dieses Kapitel ist kein ausfuehrbares Crew-Beispiel, sondern die Erklaerstation
fuer den Vortrag. Es zeigt alle Config-Felder, die in den spaeteren Beispielen
verwendet werden.

## Dateien

- `agents.yaml`: beschreibt die Agents.
- `tasks.yaml`: beschreibt die Tasks.

Die echten Beispiele verwenden dieselbe Struktur, aber meist nur einen Teil der
Felder. Im letzten Beispiel kommen dann alle fortgeschritteneren Felder zusammen:
Tools, Task-Kontext und eigene LLM-Einstellungen pro Agent.

## agents.yaml

```yaml
beispiel_agent:
  role: Beispielrolle
  goal: Kurzes Ziel des Agents.
  backstory: >
    Hintergrund und Arbeitsstil des Agents.
  tools:
    - beispiel_tool
  llm:
    model: anthropic/claude-sonnet-4-20250514
    model_env: CREWAI_STARKES_MODELL
    temperature: 0.2
    max_tokens: 2200
  verbose: true
```

### Felder

- `beispiel_agent`: frei waehlbare technische ID des Agents. Tasks verweisen mit
  `agent` auf diese ID.
- `role`: Rolle des Agents, z. B. `Tester` oder `Kochhelfer`.
- `goal`: Ziel, auf das der Agent hinarbeitet.
- `backstory`: Kontext, Arbeitsstil und Perspektive des Agents.
- `tools`: Liste der Tool-Namen, die dieser Agent benutzen darf. Die Namen
  muessen in `TOOL_REGISTRY` in `examples/main.py` registriert sein.
- `llm`: optionales Modellprofil fuer diesen Agent. Wenn es fehlt, nutzt der
  Agent das globale Modell.
- `model`: Standardmodell fuer diesen Agent.
- `model_env`: optionale Umgebungsvariable, die `model` ueberschreibt.
- `temperature`: Kreativitaet/Streuung der Antworten. Niedriger ist
  deterministischer, hoeher ist freier.
- `max_tokens`: grobes Limit fuer die Antwortlaenge des Modells.
- `verbose`: zeigt beim Lauf mehr CrewAI-Ausgabe, inklusive Tool-Nutzung.

## tasks.yaml

```yaml
erste_task:
  agent: beispiel_agent
  description: >
    Aufgabe, die der Agent bearbeiten soll.
  expected_output: >
    Gewuenschtes Format und Inhalt der Antwort.

zweite_task:
  agent: anderer_agent
  context:
    - erste_task
  description: >
    Aufgabe, die das Ergebnis aus erste_task als Kontext nutzt.
  expected_output: >
    Gewuenschtes Ergebnis der zweiten Task.
```

### Felder

- `erste_task`: frei waehlbare technische ID der Task.
- `agent`: technische ID des Agents aus `agents.yaml`, der diese Task bearbeitet.
- `context`: optionale Liste frueherer Task-IDs. Diese Tasks muessen in der YAML
  vor der nutzenden Task stehen.
- `description`: eigentliche Aufgabenstellung. Hier steht auch, welche Tools
  aufgerufen werden sollen.
- `expected_output`: beschreibt das erwartete Ergebnis, z. B. Format, Sprache,
  Pflichtabschnitte oder Codeblock.

## Zusammenhang mit Python

`examples/main.py` laedt zuerst `agents.yaml` und `tasks.yaml`. Danach:

1. Agents werden aus den Agent-Configs gebaut.
2. Tool-Namen werden ueber `TOOL_REGISTRY` in echte Python-Tools uebersetzt.
3. LLM-Einstellungen aus `llm` werden pro Agent angewendet.
4. Tasks werden in YAML-Reihenfolge erstellt.
5. `context` verbindet spaetere Tasks mit frueheren Task-Ergebnissen.
6. Die Crew laeuft sequenziell mit `Process.sequential`.

## Wichtig fuer neue Beispiele

- Agent-IDs und Task-IDs sollten kurz und eindeutig sein.
- Tool-Namen in YAML muessen exakt zur Registry passen.
- Kontext-Tasks muessen vor der Task stehen, die sie nutzt.
- Ein eigenes `llm`-Profil ist optional und lohnt sich vor allem, wenn Rollen
  unterschiedliche Anforderungen haben.
