import unittest
import time
import networkx
import numpy as np
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager

from core.prime_vm import ConsciousPrimeVM
from modules.strange_loops.emergence_monitor import EmergenceMonitor
from modules.strange_loops.loop_detector import StrangeLoop, LoopType


class TestEmergenceMonitor(unittest.TestCase):
    def setUp(self):
        self.vm = ConsciousPrimeVM()
        self.monitor = EmergenceMonitor(self.vm)
        self.loop = StrangeLoop(
            id="loop1",
            loop_type=LoopType.GODEL_SELF_REFERENCE,
            nodes={"a", "b"},
            edges=[("a", "b"), ("b", "a")],
            depth=1,
            emergence_level=0.2,
            self_reference_count=1,
            meta_levels=1,
            creation_timestamp=time.time(),
        )

    def test_emergence_threshold(self):
        """Verify emergence is detected only above threshold."""
        # Below threshold
        result = self.monitor.check_emergence([self.loop], [])
        self.assertEqual(result, [])

        # Above threshold
        self.loop.emergence_level = 0.4
        result = self.monitor.check_emergence([self.loop], [])
        self.assertEqual(len(result), 1)

    def test_pattern_metrics(self):
        """Ensure pattern detection computes reliability and boost."""
        levels = [0.4, 0.5, 0.6, 0.7] * 4
        for level in levels:
            self.loop.emergence_level = level
            self.monitor.check_emergence([self.loop], [])

        self.assertGreaterEqual(len(self.monitor.detected_patterns), 1)
        reliable = [p for p in self.monitor.detected_patterns if p.reliability > 0.9]
        self.assertTrue(reliable)
        pattern = reliable[0]
        # Boost should approximate the delta between repeated patterns
        self.assertAlmostEqual(pattern.consciousness_boost, 0.1, places=2)


if __name__ == "__main__":
    unittest.main()
