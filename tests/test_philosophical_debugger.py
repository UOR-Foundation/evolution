import os
import importlib.util
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


def test_transcendental_analysis_not_implemented():
    debugger = PhilosophicalDebugger()
    argument = PhilosophicalArgument(
        argument_id="T1",
        argument_type=ArgumentType.TRANSCENDENTAL,
        premises=["Experience is only possible with categories"],
        conclusion="Therefore categories exist a priori",
    )
    with pytest.raises(NotImplementedError):
        debugger._analyze_validity(argument)
