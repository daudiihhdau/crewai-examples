from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
from typing import Any

import yaml
from crewai import Agent, Crew, LLM, Process, Task

from examples.tools import (
    BudgetNotizTool,
    CodeVorgabenTool,
    KalenderNotizTool,
    LintingAusfuehrenTool,
    MailSendenTool,
    TaschenrechnerAnforderungenTool,
    TaschenrechnerQaCheckTool,
    TestfallVorschlaegeTool,
    UnitTestsAusfuehrenTool,
    UmzugsKistenNotizTool,
    VorratsCheckTool,
    WetterNotizTool,
)


DEFAULT_MODEL = "anthropic/claude-sonnet-4-6"
TOOL_REGISTRY = {
    "vorrats_check": VorratsCheckTool,
    "wetter_notiz": WetterNotizTool,
    "budget_notiz": BudgetNotizTool,
    "kalender_notiz": KalenderNotizTool,
    "umzugs_kisten_notiz": UmzugsKistenNotizTool,
    "mail_senden": MailSendenTool,
    "taschenrechner_anforderungen": TaschenrechnerAnforderungenTool,
    "code_vorgaben": CodeVorgabenTool,
    "testfall_vorschlaege": TestfallVorschlaegeTool,
    "taschenrechner_qa_check": TaschenrechnerQaCheckTool,
    "unit_tests_ausfuehren": UnitTestsAusfuehrenTool,
    "linting_ausfuehren": LintingAusfuehrenTool,
}
EXAMPLES = {
    "01": {
        "config_dir": Path(__file__).parent / "01_single_agent_no_tool" / "config",
        "aliases": ["single", "no-tool", "basic"],
    },
    "02": {
        "config_dir": Path(__file__).parent / "02_two_agents_no_tools" / "config",
        "aliases": ["two-agents", "review"],
    },
    "03": {
        "config_dir": Path(__file__).parent / "03_one_agent_one_tool" / "config",
        "aliases": ["cooking", "one-tool"],
    },
    "04": {
        "config_dir": Path(__file__).parent / "04_one_agent_multiple_tools" / "config",
        "aliases": ["weekend", "multi-tool"],
    },
    "05": {
        "config_dir": Path(__file__).parent / "05_multi_agent_with_tools" / "config",
        "aliases": ["moving", "multi-agent"],
    },
    "06": {
        "config_dir": Path(__file__).parent / "06_dark_factory_calculator" / "config",
        "aliases": ["coder", "calculator", "dark-factory"],
    },
}
EXAMPLE_CHOICES = sorted(
    [example_name for example_name in EXAMPLES]
    + [alias for example_config in EXAMPLES.values() for alias in example_config["aliases"]]
)


def build_llm(llm_config: dict[str, Any] | None = None) -> LLM:
    llm_config = llm_config or {}
    model = os.getenv("CREWAI_MODEL", DEFAULT_MODEL)
    if "model" in llm_config:
        model = llm_config["model"]
    if "model_env" in llm_config:
        model = os.getenv(llm_config["model_env"], model)

    return LLM(
        model=model,
        temperature=float(llm_config.get("temperature", os.getenv("CREWAI_TEMPERATURE", "0.4"))),
        max_tokens=int(llm_config.get("max_tokens", os.getenv("CREWAI_MAX_TOKENS", "2500"))),
    )


def load_config(config_dir: Path, filename: str) -> dict[str, Any]:
    with (config_dir / filename).open(encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)


def build_agent(agent_config: dict[str, Any]) -> Agent:
    tool_names = agent_config.get("tools", [])
    tools = [TOOL_REGISTRY[tool_name]() for tool_name in tool_names]
    return Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        tools=tools,
        llm=build_llm(agent_config.get("llm")),
        verbose=agent_config.get("verbose", True),
    )


def run_single_task(agent: Agent, description: str, expected_output: str) -> str:
    task = Task(description=description, expected_output=expected_output, agent=agent)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
    return str(crew.kickoff())


def extract_python_code(text: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def checks_are_green(unit_test_result: str, lint_result: str) -> bool:
    return "UNIT_TEST_STATUS: PASS" in unit_test_result and "LINT_STATUS: PASS" in lint_result


def resolve_example(example: str) -> dict[str, Any]:
    if example in EXAMPLES:
        return EXAMPLES[example]
    for example_config in EXAMPLES.values():
        if example in example_config["aliases"]:
            return example_config
    raise ValueError(f"Unknown example: {example}")


def run_dark_factory_calculator(config_dir: Path) -> str:
    agents_config = load_config(config_dir, "agents.yaml")
    tasks_config = load_config(config_dir, "tasks.yaml")
    agents = {
        agent_name: build_agent(agent_config)
        for agent_name, agent_config in agents_config.items()
    }

    design_config = tasks_config["design_calculator"]
    design_result = run_single_task(
        agents[design_config["agent"]],
        design_config["description"],
        design_config["expected_output"],
    )

    max_iterations = int(os.getenv("CREWAI_DARK_FACTORY_MAX_RUNS", "4"))
    tester_feedback = "Noch kein Tester-Feedback. Starte mit einer sauberen ersten Version."
    final_code = ""
    final_lint_result = ""
    final_unit_test_result = ""
    transcript = [
        "# Dark-Factory Ergebnis",
        "## Produktdesign",
        design_result,
    ]

    for iteration in range(1, max_iterations + 1):
        coder_config = tasks_config["write_calculator_code"]
        coder_description = (
            f"{coder_config['description']}\n\n"
            f"Iteration {iteration} von maximal {max_iterations}.\n"
            "Produktanforderungen:\n"
            f"{design_result}\n\n"
            "Rueckmeldung vom Tester aus der letzten Runde:\n"
            f"{tester_feedback}\n\n"
            "Wenn die Rueckmeldung Fehler nennt, liefere eine korrigierte komplette Version. "
            "Gib genau einen Python-Codeblock aus."
        )
        coder_result = run_single_task(
            agents[coder_config["agent"]],
            coder_description,
            coder_config["expected_output"],
        )
        final_code = extract_python_code(coder_result)

        lint_result = LintingAusfuehrenTool()._run(final_code)
        unit_test_result = UnitTestsAusfuehrenTool()._run(final_code)
        final_lint_result = lint_result
        final_unit_test_result = unit_test_result

        tester_config = tasks_config["design_tests"]
        tester_description = (
            f"{tester_config['description']}\n\n"
            f"Iteration {iteration}: Du bist jetzt in der Pruefschleife mit dem Coder.\n"
            "Der folgende Code wurde vom Runner wirklich gelintet und getestet:\n"
            f"```python\n{final_code}\n```\n\n"
            "Echtes Linting-Ergebnis:\n"
            f"{lint_result}\n\n"
            "Echtes Unit-Test-Ergebnis:\n"
            f"{unit_test_result}\n\n"
            "Gib dem Coder eine konkrete deutsche Rueckmeldung. Wenn alles gruen ist, "
            "schreibe deutlich: TESTER_STATUS: PASS. Wenn etwas fehlschlaegt, schreibe "
            "TESTER_STATUS: FAIL und liste die noetigen Korrekturen."
        )
        tester_feedback = run_single_task(
            agents[tester_config["agent"]],
            tester_description,
            tester_config["expected_output"],
        )

        transcript.extend(
            [
                f"## Iteration {iteration}",
                "### Coder",
                coder_result,
                "### Echtes Linting",
                lint_result,
                "### Echte Unit-Tests",
                unit_test_result,
                "### Tester",
                tester_feedback,
            ]
        )

        if checks_are_green(unit_test_result, lint_result):
            break

    qa_config = tasks_config["run_qa_check"]
    qa_description = (
        f"{qa_config['description']}\n\n"
        "Finaler Code:\n"
        f"```python\n{final_code}\n```\n\n"
        "Finales echtes Linting:\n"
        f"{final_lint_result}\n\n"
        "Finale echte Unit-Tests:\n"
        f"{final_unit_test_result}\n\n"
        "Finales Tester-Feedback:\n"
        f"{tester_feedback}\n\n"
        "Bewerte, ob das Ziel erreicht wurde. Wenn Linting und Unit-Tests PASS sind, "
        "formuliere eine klare Freigabe."
    )
    qa_result = run_single_task(
        agents[qa_config["agent"]],
        qa_description,
        qa_config["expected_output"],
    )
    transcript.extend(["## QA-Checker", qa_result])
    return "\n\n".join(transcript)


def run_example(example: str) -> str:
    example_config = resolve_example(example)
    config_dir = example_config["config_dir"]
    if config_dir.name == "config" and config_dir.parent.name == "06_dark_factory_calculator":
        return run_dark_factory_calculator(config_dir)

    agents_config = load_config(config_dir, "agents.yaml")
    tasks_config = load_config(config_dir, "tasks.yaml")
    agents = {
        agent_name: build_agent(agent_config)
        for agent_name, agent_config in agents_config.items()
    }
    tasks: dict[str, Task] = {}
    for task_name, task_config in tasks_config.items():
        context_names = task_config.get("context", [])
        task_args = {
            "description": task_config["description"],
            "expected_output": task_config["expected_output"],
            "agent": agents[task_config["agent"]],
        }
        if context_names:
            task_args["context"] = [tasks[context_name] for context_name in context_names]
        tasks[task_name] = Task(**task_args)
    crew = Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        process=Process.sequential,
        verbose=True,
    )
    return str(crew.kickoff())


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CrewAI Anthropic examples.")
    parser.add_argument(
        "example",
        choices=EXAMPLE_CHOICES,
        help="Example to run.",
    )
    args = parser.parse_args()

    result = run_example(args.example)

    print("\n=== RESULT ===\n")
    print(result)


if __name__ == "__main__":
    main()
