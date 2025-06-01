import unittest
from unittest import mock
import networkx
import numpy as np
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager

from consciousness.consciousness_integration import Condition
from modules.strange_loops.loop_detector import StrangeLoopDetector
from modules.strange_loops.loop_factory import StrangeLoopFactory
from core.prime_vm import ConsciousPrimeVM

class TestErrorLogging(unittest.TestCase):
    def test_condition_logs_on_failure(self):
        cond = Condition(name="bad", requirement="undefined_var > 0")
        with mock.patch("consciousness.consciousness_integration.logger") as log:
            result = cond.evaluate({})
            self.assertFalse(result)
            self.assertTrue(log.exception.called)

    def test_loop_detector_cycle_failure_logs(self):
        detector = StrangeLoopDetector(ConsciousPrimeVM())
        with mock.patch(
            "modules.strange_loops.loop_detector.nx.simple_cycles",
            side_effect=Exception("boom"),
        ), mock.patch.object(
            StrangeLoopDetector,
            "_find_cycles_dfs",
            return_value=[],
        ), mock.patch("modules.strange_loops.loop_detector.logger") as log:
            cycles = detector._find_all_cycles()
            self.assertEqual(cycles, [])
            self.assertTrue(log.exception.called)

    def test_loop_factory_invalid_meta_logs(self):
        factory = StrangeLoopFactory(ConsciousPrimeVM())
        trace = [{"instruction": "META_BAD"}]
        with mock.patch("modules.strange_loops.loop_factory.logger") as log:
            patterns = factory._analyze_trace_patterns(trace)
            self.assertTrue(log.warning.called)
            self.assertEqual(patterns[0]["level"], 1)

