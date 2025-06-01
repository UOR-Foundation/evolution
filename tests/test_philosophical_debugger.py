import os
import importlib.util
from enum import Enum
import pytest

MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "utils", "philosophical_debugger.py")
spec = importlib.util.spec_from_file_location("phd", MODULE_PATH)
phd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phd)

PhilosophicalDebugger = phd.PhilosophicalDebugger
PhilosophicalArgument = phd.PhilosophicalArgument
ArgumentType = phd.ArgumentType


def test_abductive_analysis_returns_result():
    debugger = PhilosophicalDebugger()
    argument = PhilosophicalArgument(
        argument_id="A1",
        argument_type=ArgumentType.ABDUCTIVE,
        premises=["We observe smoke in the air"],
        conclusion="The best explanation is that something causes a fire",
    )
    result = debugger._analyze_validity(argument)
    assert result["is_valid"] in {True, False}
    assert "explanation_score" in result


def test_transcendental_analysis_returns_result():
    debugger = PhilosophicalDebugger()
    argument = PhilosophicalArgument(
        argument_id="T1",
        argument_type=ArgumentType.TRANSCENDENTAL,
        premises=["Experience is only possible with categories"],
        conclusion="Therefore categories exist a priori",
    )
    result = debugger._analyze_validity(argument)
    assert result["is_valid"] in {True, False}
    assert "explanation" in result


def test_unknown_argument_type_fallback():
    class UnknownType(Enum):
        MYSTERY = "mystery"

    debugger = PhilosophicalDebugger()
    argument = PhilosophicalArgument(
        argument_id="U1",
        argument_type=UnknownType.MYSTERY,  # type: ignore[arg-type]
        premises=["Some premise"],
        conclusion="Some conclusion",
    )
    result = debugger._analyze_validity(argument)
    assert result == {
        "is_valid": False,
        "explanation": "Unsupported argument type: mystery",
    }
