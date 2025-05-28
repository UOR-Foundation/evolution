import unittest
from phase1_vm_enhancements import (
    chunk_push, chunk_print, chunk_halt,
    chunk_add, chunk_sub, chunk_mul,
    chunk_input, chunk_insert, chunk_delete,
    vm_execute
)
from enhanced_vm_interface import EnhancedVMInterface

class DummyTeacher:
    def __init__(self):
        self.last_guess = None

    def provide_feedback(self, state, last_output=None):
        if last_output is not None:
            self.last_guess = str(last_output)
        else:
            self.last_guess = state.get('output_this_step')
        if self.last_guess is not None and int(self.last_guess) == 42:
            return 1
        return 0

class TestVMInstructions(unittest.TestCase):
    def run_program(self, program):
        output = []
        final_state = {}
        for step in vm_execute(program):
            final_state = step
            if step.get('output_this_step') is not None:
                output.append(step['output_this_step'])
            if step.get('halt_flag') or step.get('error_msg'):
                break
        return ''.join(str(o) for o in output), final_state

    def test_sub(self):
        prog = [chunk_push(5), chunk_push(3), chunk_sub(), chunk_print(), chunk_halt()]
        out, state = self.run_program(prog)
        self.assertEqual(out, str(5 - 3))
        self.assertTrue(state.get('halt_flag'))

    def test_mul(self):
        prog = [chunk_push(4), chunk_push(3), chunk_mul(), chunk_print(), chunk_halt()]
        out, state = self.run_program(prog)
        self.assertEqual(out, str(4 * 3))
        self.assertTrue(state.get('halt_flag'))

    def test_insert_delete(self):
        # Insert a PUSH(0) at index 1 then delete the first instruction
        prog = [
            chunk_push(chunk_push(0)),  # chunk to insert
            chunk_push(1),
            chunk_insert(),
            chunk_push(0),
            chunk_delete(),
            chunk_halt(),
        ]
        out, state = self.run_program(prog)
        self.assertTrue(state.get('halt_flag'))
        program = state.get('program')
        self.assertEqual(len(program), 6)
        self.assertEqual(program[0], chunk_push(0))

class TestEnhancedInterface(unittest.TestCase):
    def test_bidirectional(self):
        prog = [chunk_push(42), chunk_print(), chunk_input(), chunk_halt()]
        teacher = DummyTeacher()
        iface = EnhancedVMInterface(prog, teacher=teacher)
        iface.run_until_halt()
        self.assertEqual(teacher.last_guess, '42')
        self.assertTrue(any(e.get('needs_input') for e in iface.events))

if __name__ == '__main__':
    unittest.main()
