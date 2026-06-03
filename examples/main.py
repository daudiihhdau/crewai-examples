from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml
from crewai import Agent, Crew, LLM, Process, Task

from examples.tools import (
    BudgetNotizTool,
    CodeVorgabenTool,
    KalenderNotizTool,
    MailSendenTool,
    TaschenrechnerAnforderungenTool,
    TaschenrechnerQaCheckTool,
    TestfallVorschlaegeTool,
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


def resolve_example(example: str) -> dict[str, Any]:
    if example in EXAMPLES:
        return EXAMPLES[example]
    for example_config in EXAMPLES.values():
        if example in example_config["aliases"]:
            return example_config
    raise ValueError(f"Unknown example: {example}")


def run_example(example: str) -> str:
    example_config = resolve_example(example)
    config_dir = example_config["config_dir"]
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
