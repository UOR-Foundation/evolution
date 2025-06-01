"""Simple benchmarking utility for PrimeVM."""

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

    # Baseline direct execution
    start = time.time()
    for _ in range(iterations):
        for _ in vm_execute(program):
            pass
    baseline = time.time() - start

    # Via interface
    iface = EnhancedVMInterface(program)
    start = time.time()
    for _ in range(iterations):
        iface.start()
        iface.run_until_halt()
    interface_time = time.time() - start

    print(f"Baseline time: {baseline:.4f}s")
    print(f"Interface time: {interface_time:.4f}s")


if __name__ == "__main__":
    main()
