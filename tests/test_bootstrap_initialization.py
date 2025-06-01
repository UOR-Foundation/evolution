import unittest
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager

from core.prime_vm import ConsciousPrimeVM
from consciousness.consciousness_integration import ConsciousnessIntegrator
from modules.strange_loops.loop_detector import StrangeLoopDetector
from consciousness.perspective_engine import PerspectiveEngine


class TestBootstrapInitialization(unittest.TestCase):
    """Verify bootstrap initialization stage."""

    def test_initialize_components(self):
        vm = ConsciousPrimeVM()
        integrator = ConsciousnessIntegrator(vm)

        # Remove components to force bootstrap logic
        integrator.loop_detector = None
        integrator.loop_factory = None
        integrator.emergence_monitor = None
        integrator.multi_level_awareness = None
        integrator.recursive_self_model = None
        integrator.perspective_engine = None
        integrator.consciousness_core.loop_detector = None
        integrator.consciousness_core.emergence_monitor = None
        integrator.consciousness_core.multi_level_awareness = None
        integrator.consciousness_core.perspective_engine = None

        # Execute initialization stage
        integrator._execute_bootstrap_stage()

        self.assertIsInstance(integrator.loop_detector, StrangeLoopDetector)
        self.assertIsInstance(integrator.perspective_engine, PerspectiveEngine)
        self.assertIs(integrator.consciousness_core.loop_detector, integrator.loop_detector)
        self.assertIs(integrator.consciousness_core.perspective_engine, integrator.perspective_engine)


if __name__ == "__main__":
    unittest.main()
