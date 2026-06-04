from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable


@dataclass
class FlowState:
    title: str
    values: dict[str, Any] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)

    def remember(self, key: str, value: Any) -> Any:
        self.values[key] = value
        self.log.append(f"{key}: {value}")
        return value


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}"


def run_steps(state: FlowState, steps: list[Callable[[FlowState], None]]) -> str:
    for step in steps:
        state.log.append(f"STEP: {step.__name__}")
        step(state)
    return "\n".join(f"- {entry}" for entry in state.log)


def run_07_flow_intro() -> str:
    state = FlowState(title="07 Flow Intro")

    def start(state: FlowState) -> None:
        state.remember("ziel", "Eine einfache Tagesplanung erstellen.")
        state.remember("zeit", datetime.now().strftime("%H:%M:%S"))

    def prepare_data(state: FlowState) -> None:
        state.remember("termine", ["Einkauf", "Waesche", "15 Minuten Spaziergang"])

    def finish(state: FlowState) -> None:
        termine = ", ".join(state.values["termine"])
        state.remember("ergebnis", f"Heute erledigen: {termine}.")

    return "\n\n".join(
        [
            "# 07 Flow Intro",
            section(
                "Idee",
                "Ein Flow ist Ablaufsteuerung mit Zustand. In diesem Beispiel gibt es "
                "noch keine Agenten, sondern nur klar benannte Schritte.",
            ),
            section("Ablauf", run_steps(state, [start, prepare_data, finish])),
            section(
                "Unterschied zur Crew",
                "Eine Crew wuerde mehrere Tasks an Agents geben. Der Flow entscheidet "
                "hier selbst, welche Schritte in welcher Reihenfolge laufen und welche "
                "Daten im State gespeichert werden.",
            ),
        ]
    )


def run_08_flow_branching() -> str:
    state = FlowState(title="08 Flow Branching")

    def start(state: FlowState) -> None:
        state.remember("regen_chance", random.randint(10, 90))
        state.remember("budget", random.choice([10, 18, 25, 35]))

    def choose_branch(state: FlowState) -> None:
        if state.values["regen_chance"] > 55:
            state.remember("route", "drinnen")
        elif state.values["budget"] < 20:
            state.remember("route", "sparsam")
        else:
            state.remember("route", "draussen")

    def execute_branch(state: FlowState) -> None:
        route = state.values["route"]
        plans = {
            "drinnen": "Kaffee zu Hause, Waesche, kurzer Anruf.",
            "sparsam": "Spaziergang, Brote vorbereiten, Bibliothek.",
            "draussen": "Markt, kleiner Imbiss, Parkrunde.",
        }
        state.remember("plan", plans[route])

    return "\n\n".join(
        [
            "# 08 Flow mit Branching",
            section(
                "Idee",
                "Ein Flow kann anhand von Daten einen Pfad waehlen. Hier entscheiden "
                "Regenwahrscheinlichkeit und Budget ueber den Tagesplan.",
            ),
            section("Ablauf", run_steps(state, [start, choose_branch, execute_branch])),
            section(
                "Warum man das braucht",
                "Bei Crews laeuft eine Task-Liste meist linear. Bei Flows kann der "
                "Ablauf zur Laufzeit anders abbiegen.",
            ),
        ]
    )


def run_09_flow_loop_validation() -> str:
    state = FlowState(title="09 Flow Loop Validation")
    max_rounds = 5

    def estimate_cart() -> dict[str, Any]:
        items = random.sample(["Brot", "Milch", "Aepfel", "Kaffee", "Nudeln", "Kaese"], k=4)
        total = sum(random.randint(2, 8) for _ in items)
        return {"items": items, "total": total}

    state.remember("budget", 18)
    for round_number in range(1, max_rounds + 1):
        cart = estimate_cart()
        state.remember(f"runde_{round_number}_warenkorb", cart)
        if cart["total"] <= state.values["budget"]:
            state.remember("status", "PASS")
            state.remember("finaler_warenkorb", cart)
            break
        state.remember(
            f"runde_{round_number}_feedback",
            f"{cart['total']} Euro ist zu teuer. Neuer Versuch mit kleinerer Liste.",
        )
    else:
        state.remember("status", "FAIL")

    return "\n\n".join(
        [
            "# 09 Flow mit Validierungsloop",
            section(
                "Idee",
                "Ein Flow kann einen Schritt wiederholen, bis ein Validator gruen ist. "
                "Das ist die einfache Form des Ping-Pong-Musters aus Beispiel 06.",
            ),
            section("Ablauf", "\n".join(f"- {entry}" for entry in state.log)),
            section(
                "Warum man das braucht",
                "Loops lohnen sich, wenn es eine harte Bedingung gibt: Budget passt, "
                "Tests bestehen, JSON ist gueltig oder Pflichtfelder sind vollstaendig.",
            ),
        ]
    )


def run_10_flow_orchestrates_crews() -> str:
    state = FlowState(title="10 Flow orchestriert Crews")
    state.remember("eingang", "Kleine Geburtstagsfeier am Samstag planen.")
    state.remember("crew_1", "Planungs-Crew erstellt Einkauf, Ablauf und Aufgaben.")
    state.remember("validator", "Budget, Zeit und Anzahl Helfer werden geprueft.")
    state.remember("route", "Bei Fehlern zur Planungs-Crew zurueck, sonst zur Zusammenfassung.")
    state.remember("crew_2", "Zusammenfassungs-Crew schreibt die finale Nachricht.")

    return "\n\n".join(
        [
            "# 10 Flow orchestriert Crews",
            section(
                "Idee",
                "In produktiven Setups ist ein Flow oft der Rahmen um mehrere Crews. "
                "Die Crews erledigen Denk- oder Schreibarbeit, der Flow entscheidet "
                "ueber Reihenfolge, Wiederholung, Abbruch und Uebergabe.",
            ),
            section("Pseudo-Ablauf", "\n".join(f"- {entry}" for entry in state.log)),
            section(
                "CrewAI-Form",
                "In echtem CrewAI wuerde man dafuer Flow-State, Start-Schritte, "
                "Listener und Router verwenden. Dieses Beispiel haelt es bewusst "
                "didaktisch, damit zuerst das Muster klar wird.",
            ),
        ]
    )


FLOW_EXAMPLE_RUNNERS = {
    "07": run_07_flow_intro,
    "08": run_08_flow_branching,
    "09": run_09_flow_loop_validation,
    "10": run_10_flow_orchestrates_crews,
}
