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
    state = FlowState(title="07 Morgenroutine")

    def start(state: FlowState) -> None:
        state.remember("ziel", "Morgens puenktlich aus dem Haus kommen.")
        state.remember("zeit", datetime.now().strftime("%H:%M:%S"))

    def prepare_data(state: FlowState) -> None:
        state.remember("fixpunkte", ["Bus um 08:12", "Brotbox packen", "Muellsack mitnehmen"])
        state.remember("puffer_minuten", 12)

    def finish(state: FlowState) -> None:
        fixpunkte = ", ".join(state.values["fixpunkte"])
        state.remember("ergebnis", f"07:35 starten: {fixpunkte}. Puffer bleibt erhalten.")

    return "\n\n".join(
        [
            "# 07 Morgenroutine als Flow",
            section(
                "Alltagssituation",
                "Eine Morgenroutine hat feste Schritte: erst Ziel klaeren, dann "
                "Fixpunkte sammeln, dann eine einfache Reihenfolge bauen.",
            ),
            section("Ablauf", run_steps(state, [start, prepare_data, finish])),
            section(
                "Was man daran lernt",
                "Der Flow merkt sich kleine Fakten im State. Das ist praktisch, wenn "
                "ein Ablauf nicht kreativ, sondern verlaesslich und geordnet sein soll.",
            ),
        ]
    )


def run_08_flow_branching() -> str:
    state = FlowState(title="08 Wochenendplan")

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
            "drinnen": "Pfannkuchen machen, Waesche starten, Filmabend vorbereiten.",
            "sparsam": "Thermoskanne fuellen, Brote schmieren, Bibliothek und Parkbank.",
            "draussen": "Wochenmarkt, Spielplatzrunde, kleiner Imbiss.",
        }
        state.remember("plan", plans[route])

    return "\n\n".join(
        [
            "# 08 Wochenendplan mit Abzweigung",
            section(
                "Alltagssituation",
                "Samstagvormittag soll geplant werden. Je nach Regen und Budget nimmt "
                "der Flow einen anderen Weg.",
            ),
            section("Ablauf", run_steps(state, [start, choose_branch, execute_branch])),
            section(
                "Was man daran lernt",
                "Branching ist nuetzlich, wenn ein Plan nicht immer gleich sein soll. "
                "Der State enthaelt die Fakten, die Route waehlt den passenden Alltagspfad.",
            ),
        ]
    )


def run_09_flow_loop_validation() -> str:
    state = FlowState(title="09 Einkaufsliste pruefen")
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
            "# 09 Einkaufsliste mit Budgetpruefung",
            section(
                "Alltagssituation",
                "Beim Einkaufen soll die Liste unter 18 Euro bleiben. Wenn der "
                "Warenkorb zu teuer ist, versucht der Flow es erneut.",
            ),
            section("Ablauf", "\n".join(f"- {entry}" for entry in state.log)),
            section(
                "Was man daran lernt",
                "Ein Loop braucht ein klares Ende. Hier entscheidet nicht ein Agent "
                "nach Gefuehl, sondern die Bedingung: Summe kleiner oder gleich Budget.",
            ),
        ]
    )


def run_10_flow_orchestrates_crews() -> str:
    state = FlowState(title="10 Geburtstagsfeier")
    state.remember("eingang", "Kindergeburtstag am Samstag von 15:00 bis 18:00 planen.")
    state.remember("crew_1", "Planungs-Crew klaert Kuchen, Spiele, Einkauf und Aufgaben.")
    state.remember("validator", "Budget 60 Euro, 3 Stunden Zeit und 2 Helfer werden geprueft.")
    state.remember("route", "Bei Problemen zur Planung zurueck, sonst Einladungstext schreiben.")
    state.remember("crew_2", "Nachrichten-Crew formuliert eine kurze Info an die Eltern.")

    return "\n\n".join(
        [
            "# 10 Geburtstagsfeier mit Flow und Crews",
            section(
                "Alltagssituation",
                "Eine kleine Feier hat mehrere Baustellen: Essen, Spiele, Helfer, "
                "Budget und Nachricht an die Eltern. Der Flow haelt das zusammen.",
            ),
            section("Pseudo-Ablauf", "\n".join(f"- {entry}" for entry in state.log)),
            section(
                "Was man daran lernt",
                "Crews koennen Teilaufgaben erledigen. Der Flow entscheidet, ob der "
                "Plan schon alltagstauglich ist oder noch einmal ueberarbeitet wird.",
            ),
        ]
    )


FLOW_EXAMPLE_RUNNERS = {
    "07": run_07_flow_intro,
    "08": run_08_flow_branching,
    "09": run_09_flow_loop_validation,
    "10": run_10_flow_orchestrates_crews,
}
