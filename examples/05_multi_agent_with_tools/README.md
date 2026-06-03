# 05 Kleiner Umzug mit mehreren Agents und Tool

## Lernziel

Mehrere Agents arbeiten mit Kontext und Tool-Nutzung. Der Use-Case ist ein
kleiner Wohnungsumzug, kein technisches Projekt.

## Besonderheiten

- Ein Agent sammelt Packhinweise mit einem Tool.
- Ein zweiter Agent macht daraus eine Nachricht an Helfer und nutzt
  `mail_senden`, um den Versand zu simulieren.
- Die zweite Task nutzt die erste Task als Kontext.

## Mitnehmen

- Unterschiedliche Rollen koennen denselben Alltagsfall sinnvoll aufteilen.
- Tool-Kontext kann zuerst gesammelt und danach weiterverwendet werden.
- Tools koennen auch Aktionen simulieren, z. B. einen Mail-Versand.
- Task-Kontext ist eine einfache Form von Zusammenarbeit.

## Start

```powershell
crewai-examples 05
```
