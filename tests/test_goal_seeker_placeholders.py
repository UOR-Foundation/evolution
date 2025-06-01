import pytest
from generate_goal_seeker_uor import (
    generate_goal_seeker_program,
    FEEDBACK_SUCCESS_IDX,
)
from phase1_vm_enhancements import chunk_push, parse_opcode_and_operand, OP_PUSH


def test_placeholder_resolution():
    program, meta = generate_goal_seeker_program(initial_prime_idx=FEEDBACK_SUCCESS_IDX, return_debug=True)

    labels = meta['labels']
    jump_placeholders = meta['jump_placeholders']
    slot_placeholders = meta['slot_placeholders']
    selected_addresses = meta['selected_addresses']

    mapping = {
        'dynamic_slot_choice': selected_addresses[0],
        'default_lsc_success': selected_addresses[1],
        'lsc_carry': selected_addresses[2],
        'lsc_failure': selected_addresses[3],
    }

    for idx, label in jump_placeholders:
        opcode, operand = parse_opcode_and_operand(program[idx])
        assert opcode == OP_PUSH
        assert operand == labels[label]

    for key, idx in slot_placeholders.items():
        opcode, operand = parse_opcode_and_operand(program[idx])
        assert opcode == OP_PUSH
        assert operand == mapping[key]

