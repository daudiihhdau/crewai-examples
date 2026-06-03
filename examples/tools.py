from __future__ import annotations

import ast
from datetime import datetime
import random
import subprocess
import sys
import tempfile
import textwrap
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


def tool_lauf_info(tool_name: str) -> str:
    lauf_id = random.randint(1000, 9999)
    zeit = datetime.now().strftime("%H:%M:%S")
    return f"[Python-Tool ausgefuehrt: {tool_name}, Lauf-ID {lauf_id}, Zeit {zeit}]"


class VorratsCheckInput(BaseModel):
    gericht: str = Field(..., description="Gericht, das gekocht werden soll.")


class VorratsCheckTool(BaseTool):
    name: str = "vorrats_check"
    description: str = "Liefert einfache Vorratsinfos fuer ein Alltagsgericht."
    args_schema: Type[BaseModel] = VorratsCheckInput

    def _run(self, gericht: str) -> str:
        fehlende_zutaten = ["Paprika", "Zucchini", "Kaese", "Brot", "Zitrone", "Petersilie"]
        auswahl = random.sample(fehlende_zutaten, k=3)
        geschaetzte_kosten = sum(random.randint(2, 5) for _ in auswahl)
        portionen = random.choice([2, 3, 4])
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Vorratscheck fuer {gericht}:\n"
            "- Vorhanden: Nudeln, Reis, Tomaten, Zwiebeln, Eier, Joghurt.\n"
            f"- Heute zufaellig als knapp markiert: {', '.join(auswahl)}.\n"
            "- Nicht vorhanden: frische Kraeuter, Zitronen.\n"
            f"- Geschaetzte Zusatzkosten: {geschaetzte_kosten} Euro.\n"
            f"- Aus den Vorraeten werden ungefaehr {portionen} Portionen.\n"
            "- Hinweis: Es soll schnell gehen und wenig Abwasch machen."
        )


class WetterNotizInput(BaseModel):
    tag: str = Field(..., description="Tag oder Zeitraum fuer die Planung.")


class WetterNotizTool(BaseTool):
    name: str = "wetter_notiz"
    description: str = "Liefert eine einfache Wetterannahme fuer Alltagsplanung."
    args_schema: Type[BaseModel] = WetterNotizInput

    def _run(self, tag: str) -> str:
        regen_chance = random.randint(30, 85)
        temperatur = random.randint(14, 22)
        beste_stunde = random.choice(["09:30", "10:00", "10:30", "11:00"])
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Wetterannahme fuer {tag}:\n"
            f"- Vormittag: trocken, etwa {temperatur} Grad.\n"
            f"- Nachmittag: Regenwahrscheinlichkeit {regen_chance} Prozent.\n"
            "- Abend: kuehl, aber trocken.\n"
            f"- Beste Zeit fuer Erledigungen draussen: gegen {beste_stunde}.\n"
            "- Empfehlung: Erledigungen draussen eher vormittags planen."
        )


class BudgetNotizInput(BaseModel):
    zweck: str = Field(..., description="Zweck der Ausgabe.")


class BudgetNotizTool(BaseTool):
    name: str = "budget_notiz"
    description: str = "Liefert ein kleines Alltagsbudget mit Prioritaeten."
    args_schema: Type[BaseModel] = BudgetNotizInput

    def _run(self, zweck: str) -> str:
        budget = random.choice([25, 30, 35, 40])
        grundzutaten = random.randint(14, 22)
        rest = budget - grundzutaten
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Budgetnotiz fuer {zweck}:\n"
            f"- Maximalbudget heute: {budget} Euro.\n"
            f"- Geschaetzte Grundzutaten: {grundzutaten} Euro.\n"
            f"- Frei fuer Extras: {rest} Euro.\n"
            "- Wichtig: Grundzutaten zuerst, Extras nur wenn Geld uebrig ist.\n"
            "- Sparidee: ein Gericht fuer zwei Tage planen.\n"
            "- Nicht kaufen: Dinge, die nur fuer ein einzelnes Rezept gebraucht werden."
        )


class KalenderNotizInput(BaseModel):
    tag: str = Field(..., description="Tag, fuer den Termine geprueft werden.")


class KalenderNotizTool(BaseTool):
    name: str = "kalender_notiz"
    description: str = "Liefert einfache Terminannahmen fuer einen Tag."
    args_schema: Type[BaseModel] = KalenderNotizInput

    def _run(self, tag: str) -> str:
        einkauf_minuten = random.choice([30, 40, 45, 50])
        puffer = random.choice([10, 15, 20])
        ende = 17 + ((einkauf_minuten + puffer) // 60)
        end_minute = (einkauf_minuten + puffer) % 60
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Terminuebersicht fuer {tag}:\n"
            "- 09:00 bis 10:00: Telefonat.\n"
            "- 12:30 bis 13:30: Mittagspause.\n"
            "- 17:00 bis 18:00: Einkauf moeglich.\n"
            f"- Python-Schaetzung: Einkauf plus Puffer dauert {einkauf_minuten + puffer} Minuten.\n"
            f"- Realistisches Ende bei Start 17:00: {ende:02d}:{end_minute:02d}.\n"
            "- Freier Block: 19:00 bis 20:00 fuer Kochen oder Vorbereitung."
        )


class UmzugsKistenNotizInput(BaseModel):
    raum: str = Field(..., description="Raum, fuer den Packhinweise gebraucht werden.")


class UmzugsKistenNotizTool(BaseTool):
    name: str = "umzugs_kisten_notiz"
    description: str = "Liefert einfache Packhinweise fuer einen kleinen Umzug."
    args_schema: Type[BaseModel] = UmzugsKistenNotizInput

    def _run(self, raum: str) -> str:
        kisten = random.randint(4, 8)
        helfer = random.choice([1, 2, 3])
        minuten = kisten * 12 // helfer
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Packhinweise fuer {raum}:\n"
            f"- Python-Schaetzung: {kisten} Kisten, {helfer} Helfer, etwa {minuten} Minuten Tragezeit.\n"
            "- Zerbrechliches getrennt packen und deutlich markieren.\n"
            "- Schwere Dinge in kleine Kisten.\n"
            "- Dinge fuer den ersten Abend separat legen.\n"
            "- Beschriftung: Raum plus kurzer Inhalt."
        )


class MailSendenInput(BaseModel):
    empfaenger: list[str] = Field(..., description="Empfaenger der simulierten Mail.")
    betreff: str = Field(..., description="Betreff der Mail.")
    nachricht: str = Field(..., description="Nachrichtentext.")


class MailSendenTool(BaseTool):
    name: str = "mail_senden"
    description: str = "Simuliert das Senden einer Mail und liefert eine Versandbestaetigung."
    args_schema: Type[BaseModel] = MailSendenInput

    def _run(self, empfaenger: list[str], betreff: str, nachricht: str) -> str:
        zustellnummer = random.randint(100000, 999999)
        zeichen = len(nachricht)
        return (
            f"{tool_lauf_info(self.name)}\n"
            "Mail-Versand simuliert.\n"
            f"- Empfaenger: {', '.join(empfaenger)}.\n"
            f"- Betreff: {betreff}.\n"
            f"- Nachrichtenlaenge: {zeichen} Zeichen.\n"
            f"- Simulierte Versandnummer: MAIL-{zustellnummer}.\n"
            "- Hinweis: Es wurde keine echte Mail verschickt."
        )


class TaschenrechnerAnforderungenInput(BaseModel):
    produkt: str = Field(..., description="Name des kleinen Produkts.")


class TaschenrechnerAnforderungenTool(BaseTool):
    name: str = "taschenrechner_anforderungen"
    description: str = "Liefert einfache Anforderungen fuer einen Python-Taschenrechner."
    args_schema: Type[BaseModel] = TaschenrechnerAnforderungenInput

    def _run(self, produkt: str) -> str:
        prioritaet = random.choice(["Division durch 0", "unbekannter Operator", "lesbare Beispiele"])
        operatoren = ["+", "-", "*", "/"]
        random.shuffle(operatoren)
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Anforderungen fuer {produkt}:\n"
            "- Muss addieren, subtrahieren, multiplizieren und dividieren koennen.\n"
            f"- Operator-Reihenfolge fuer die Demo: {', '.join(operatoren)}.\n"
            f"- Heute besonders pruefen: {prioritaet}.\n"
            "- Division durch 0 muss eine klare Fehlermeldung liefern.\n"
            "- Eingabe: zwei Zahlen und ein Operator als String.\n"
            "- Ausgabe: Zahl oder lesbare Fehlermeldung.\n"
            "- Code soll fuer Einsteiger gut lesbar sein und keine externen Pakete nutzen."
        )


class CodeVorgabenInput(BaseModel):
    sprache: str = Field(..., description="Programmiersprache fuer das Beispiel.")


class CodeVorgabenTool(BaseTool):
    name: str = "code_vorgaben"
    description: str = "Liefert einfache Code-Vorgaben fuer das Taschenrechner-Beispiel."
    args_schema: Type[BaseModel] = CodeVorgabenInput

    def _run(self, sprache: str) -> str:
        beispiel_a = random.randint(2, 9)
        beispiel_b = random.randint(2, 9)
        beispiel_ergebnis = beispiel_a + beispiel_b
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Code-Vorgaben fuer {sprache}:\n"
            "- Nutze eine Funktion calculate(a: float, operator: str, b: float).\n"
            "- Erlaubte Operatoren: +, -, *, /.\n"
            f"- Dynamischer Beispielaufruf: calculate({beispiel_a}, '+', {beispiel_b}) ergibt {beispiel_ergebnis}.\n"
            "- Gib bei Division durch 0 eine lesbare Fehlermeldung zurueck.\n"
            "- Gib bei unbekanntem Operator ebenfalls eine lesbare Fehlermeldung zurueck.\n"
            "- Fuege eine kleine Funktion run_examples() mit Beispielaufrufen hinzu."
        )


class TestfallVorschlaegeInput(BaseModel):
    produkt: str = Field(..., description="Produkt, fuer das Testfaelle gebraucht werden.")


class TestfallVorschlaegeTool(BaseTool):
    name: str = "testfall_vorschlaege"
    description: str = "Liefert einfache Testfaelle fuer den Taschenrechner."
    args_schema: Type[BaseModel] = TestfallVorschlaegeInput

    def _run(self, produkt: str) -> str:
        a = random.randint(4, 12)
        b = random.randint(2, 6)
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"Testfall-Vorschlaege fuer {produkt}:\n"
            "- Addition: 2 + 3 ergibt 5.\n"
            "- Subtraktion: 7 - 4 ergibt 3.\n"
            "- Multiplikation: 3 * 4 ergibt 12.\n"
            "- Division: 8 / 2 ergibt 4.\n"
            f"- Dynamischer Zusatztest: {a} * {b} ergibt {a * b}.\n"
            "- Fehlerfall: 8 / 0 liefert eine klare Fehlermeldung.\n"
            "- Fehlerfall: unbekannter Operator liefert eine klare Fehlermeldung."
        )


class TaschenrechnerQaCheckInput(BaseModel):
    funktionen: list[str] = Field(..., description="Funktionsnamen, die geprueft werden.")


class TaschenrechnerQaCheckTool(BaseTool):
    name: str = "taschenrechner_qa_check"
    description: str = "Prueft, ob ein Taschenrechner-Beispiel die wichtigsten Bausteine nennt."
    args_schema: Type[BaseModel] = TaschenrechnerQaCheckInput

    def _run(self, funktionen: list[str]) -> str:
        required = {"calculate", "run_examples"}
        missing = sorted(required - set(funktionen))
        score = 100 - len(missing) * 35 - random.randint(0, 5)
        if missing:
            return (
                f"{tool_lauf_info(self.name)}\n"
                "QA-Check nicht bestanden.\n"
                f"- Fehlende Funktionen: {', '.join(missing)}\n"
                f"- Dynamischer QA-Score: {score}/100.\n"
                "- Erwartet werden calculate und run_examples."
            )
        return (
            f"{tool_lauf_info(self.name)}\n"
            "QA-Check bestanden.\n"
            "- calculate ist vorhanden.\n"
            "- run_examples ist vorhanden.\n"
            f"- Dynamischer QA-Score: {score}/100.\n"
            "- Bitte pruefen: Division durch 0 und unbekannter Operator."
        )


class UnitTestsAusfuehrenInput(BaseModel):
    code: str = Field(..., description="Python-Code des Taschenrechners.")


class UnitTestsAusfuehrenTool(BaseTool):
    name: str = "unit_tests_ausfuehren"
    description: str = "Fuehrt echte unittest-Tests fuer den Taschenrechner-Code aus."
    args_schema: Type[BaseModel] = UnitTestsAusfuehrenInput

    def _run(self, code: str) -> str:
        with tempfile.TemporaryDirectory() as temp_dir:
            calculator_path = f"{temp_dir}/calculator.py"
            tests_path = f"{temp_dir}/test_calculator.py"
            with open(calculator_path, "w", encoding="utf-8") as code_file:
                code_file.write(textwrap.dedent(code).strip() + "\n")
            with open(tests_path, "w", encoding="utf-8") as tests_file:
                tests_file.write(
                    textwrap.dedent(
                        """
                        import unittest
                        from calculator import calculate


                        class CalculatorTest(unittest.TestCase):
                            def test_addition(self):
                                self.assertEqual(calculate(2, "+", 3), 5)

                            def test_subtraction(self):
                                self.assertEqual(calculate(7, "-", 4), 3)

                            def test_multiplication(self):
                                self.assertEqual(calculate(3, "*", 4), 12)

                            def test_division(self):
                                self.assertEqual(calculate(8, "/", 2), 4)

                            def test_division_by_zero(self):
                                result = calculate(8, "/", 0)
                                self.assertIsInstance(result, str)
                                self.assertIn("0", result)

                            def test_unknown_operator(self):
                                result = calculate(8, "%", 2)
                                self.assertIsInstance(result, str)
                                self.assertTrue("operator" in result.lower() or "unbekannt" in result.lower())


                        if __name__ == "__main__":
                            unittest.main()
                        """
                    ).strip()
                    + "\n"
                )
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "-v"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        status = "PASS" if result.returncode == 0 else "FAIL"
        output = (result.stdout + "\n" + result.stderr).strip()
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"UNIT_TEST_STATUS: {status}\n"
            "Befehl: python -m unittest -v\n"
            f"Ausgabe:\n{output}"
        )


class LintingAusfuehrenInput(BaseModel):
    code: str = Field(..., description="Python-Code des Taschenrechners.")


class LintingAusfuehrenTool(BaseTool):
    name: str = "linting_ausfuehren"
    description: str = "Fuehrt ein einfaches echtes Python-Linting mit ast-Analyse aus."
    args_schema: Type[BaseModel] = LintingAusfuehrenInput

    def _run(self, code: str) -> str:
        issues: list[str] = []
        normalized_code = textwrap.dedent(code).strip() + "\n"
        try:
            tree = ast.parse(normalized_code)
        except SyntaxError as error:
            issues.append(f"Syntaxfehler in Zeile {error.lineno}: {error.msg}")
            tree = None

        for line_number, line in enumerate(normalized_code.splitlines(), start=1):
            if len(line) > 100:
                issues.append(f"Zeile {line_number} ist laenger als 100 Zeichen.")
            if "\t" in line:
                issues.append(f"Zeile {line_number} enthaelt Tabs statt Leerzeichen.")

        if tree is not None:
            functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
            for function_name in ["calculate", "run_examples"]:
                if function_name not in functions:
                    issues.append(f"Funktion {function_name} fehlt.")
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in {"eval", "exec"}:
                        issues.append(f"Unsichere Funktion {node.func.id} wird verwendet.")

        status = "PASS" if not issues else "FAIL"
        issue_text = "\n".join(f"- {issue}" for issue in issues) if issues else "- Keine Lint-Probleme gefunden."
        return (
            f"{tool_lauf_info(self.name)}\n"
            f"LINT_STATUS: {status}\n"
            "Pruefungen: Syntax per ast.parse, Pflichtfunktionen, Zeilenlaenge, Tabs, eval/exec.\n"
            f"Ergebnis:\n{issue_text}"
        )
