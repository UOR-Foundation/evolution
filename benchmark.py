"""Benchmark PrimeVM execution speed.

The script measures how long it takes to run a small UOR program
both directly via ``vm_execute`` and through ``EnhancedVMInterface``.
For each iteration we capture the final VM state and count how many
executions end with the expected stack contents.  Reported metrics
include the total time taken and the number of correct runs.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import List

from config_loader import get_config_value
from phase1_vm_enhancements import (
    chunk_add,
    chunk_halt,
    chunk_mul,
    chunk_push,
    chunk_sub,
    vm_execute,
)
from enhanced_vm_interface import EnhancedVMInterface


def _load_program(spec: str) -> List[int]:
    """Return a UOR program from a name or file."""
    builtins = {
        "add": [chunk_push(10), chunk_push(20), chunk_add(), chunk_halt()],
        "sub": [chunk_push(20), chunk_push(10), chunk_sub(), chunk_halt()],
        "mul": [chunk_push(4), chunk_push(3), chunk_mul(), chunk_halt()],
    }
    if spec in builtins:
        return builtins[spec]

    path = Path(spec)
    data = json.loads(path.read_text())
    if not isinstance(data, list) or not all(isinstance(i, int) for i in data):
        raise ValueError("Program file must contain a JSON array of integers")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--program",
        default="add",
        help="Program name ('add', 'sub', 'mul') or path to JSON file",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=get_config_value("benchmark.iterations", 100),
        help="Number of iterations to execute",
    )

    args = parser.parse_args()

    program = _load_program(args.program)
    iterations = args.iterations

    # Execute once to determine the expected final VM stack for correctness
    expected_stack = []
    for state in vm_execute(program):
        expected_stack = state.get("stack", [])
        if state.get("halt_flag") or state.get("error_msg"):
            break

    # Baseline direct execution. We also track how many iterations
    # finish with the expected stack to provide a basic correctness
    # measurement alongside the timing metric.
    start = time.time()
    baseline_correct = 0
    for _ in range(iterations):
        final_state = {}
        for step in vm_execute(program):
            final_state = step
            if step.get("halt_flag") or step.get("error_msg"):
                break
        if (
            final_state.get("stack") == expected_stack
            and final_state.get("halt_flag")
            and not final_state.get("error_msg")
        ):
            baseline_correct += 1
    baseline = time.time() - start

    # Via interface
    iface = EnhancedVMInterface(program)
    start = time.time()
    interface_correct = 0
    for _ in range(iterations):
        iface.start()
        events = iface.run_until_halt()
        final_state = events[-1] if events else {}
        if (
            final_state.get("stack") == expected_stack
            and final_state.get("halt_flag")
            and not final_state.get("error_msg")
        ):
            interface_correct += 1
    interface_time = time.time() - start

    print(f"Baseline time: {baseline:.4f}s ({baseline_correct}/{iterations} correct)")
    print(
        f"Interface time: {interface_time:.4f}s ({interface_correct}/{iterations} correct)"
    )


if __name__ == "__main__":
    main()
