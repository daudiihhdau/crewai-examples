# 03 Abendessen mit einem Tool

## Lernziel

Ein Agent nutzt zum ersten Mal ein Tool. Der Use-Case bleibt alltaeglich: ein
Kochhelfer plant ein Abendessen anhand eines Vorratschecks.

## Besonderheiten

- Ein Agent.
- Ein Tool: `vorrats_check`.
- Die Task verlangt, dass das Tool zuerst genutzt wird.

## Mitnehmen

- Tools geben kontrollierten Kontext.
- Tool-Namen in YAML muessen in `TOOL_REGISTRY` registriert sein.
- Python enthaelt die Tool-Logik, YAML enthaelt den Prompt.

## Start

```powershell
crewai-examples 03
```
