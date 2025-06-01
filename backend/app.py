from flask import Flask, jsonify, send_from_directory, request # <<< ADD 'request' to imports
import os
import sys
import random
import datetime
import logging
from typing import List, Optional, Tuple

from config_loader import load_config, get_config_value

logger = logging.getLogger(__name__)

PRIME_IDX_SUCCESS = int(get_config_value("prime_idx_success", 1))
PRIME_IDX_FAILURE = int(get_config_value("prime_idx_failure", 0))
# String, as OP_PRINT output is stringified
STUCK_SIGNAL_PRINT_VALUE = str(get_config_value("stuck_signal_print_value", "99"))

# --- Path Setup --- (keep your existing correct path setup)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(current_script_dir)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

CONFIG = load_config(os.path.join(PROJECT_ROOT, "config.yaml"))


def _parse_bool(value: object) -> bool:
    """Return ``True`` if ``value`` is truthy."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "on", "t"}


def get_debug_flag() -> bool:
    """Return the debug flag from ``APP_DEBUG`` or config."""
    env_val = os.environ.get("APP_DEBUG")
    if env_val is not None:
        return _parse_bool(env_val)
    cfg_val = get_config_value("debug", False)
    return _parse_bool(cfg_val)


DEBUG_MODE = get_debug_flag()

if not logger.handlers:
    logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

from phase1_vm_enhancements import (
    vm_execute, # For the main VM
    _PRIMES as VM_PRIMES, _PRIME_IDX as VM_PRIME_IDX, get_prime as vm_get_prime, 
    _factor as vm_factor, _is_prime as vm_is_prime, _extend_primes_to as vm_extend_primes_to,
    OP_PUSH, OP_ADD, OP_PRINT, OP_HALT, OP_JUMP, OP_POKE_CHUNK, OP_BUILD_CHUNK,
    OP_DUP, OP_SWAP, OP_DROP, OP_CALL, OP_RETURN, OP_PEEK_CHUNK, OP_FACTORIZE,
    OP_GET_PRIME, OP_GET_PRIME_IDX, OP_COMPARE_EQ, OP_JUMP_IF_ZERO, OP_NOP,
    OP_MOD, OP_INPUT, chunk_push
    # BLOCK_TAG, NTT_TAG
)

# --- Log File Setup ---
# Log file path can be configured via the ``LOG_FILE_PATH`` environment
# variable or ``vm.log_file`` in ``config.yaml``. A relative path will be
# resolved against ``PROJECT_ROOT``.
_cfg_log_file = os.environ.get("LOG_FILE_PATH") or get_config_value("vm.log_file", "log.txt")
LOG_FILE_PATH = _cfg_log_file
if not os.path.isabs(LOG_FILE_PATH):
    LOG_FILE_PATH = os.path.join(PROJECT_ROOT, LOG_FILE_PATH)

def append_to_log(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        logger.debug(f"Error writing to log file: {e}")

# --- Flask App Setup ---
app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'frontend'), static_url_path='')

class AdaptiveTeacher:
    """Analyzes VM performance and adjusts teaching strategy.
    Tracks metrics, identifies weaknesses, manages curriculum."""

    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.curriculum = AdaptiveCurriculum()
        self.sequence_gen = SequenceGenerator()
        self.difficulty = get_config_value("teacher.difficulty", "MEDIUM")
        self.current_goal = None
        self.goal_type = None

    def record_attempt(self, target: int, success: bool) -> None:
        """Update statistics after the VM attempts to hit ``target``."""
        self.monitor.record_attempt(success)
        self.curriculum.record_attempt(target, success)
        self._adjust_difficulty()

    def _adjust_difficulty(self) -> None:
        """Automatically modify difficulty based on recent performance."""
        rate = self.monitor.success_rate()
        if rate > 0.8:
            self.difficulty = "HARD"
        elif rate < 0.5:
            self.difficulty = "EASY"
        else:
            self.difficulty = "MEDIUM"

    def next_goal(self) -> Tuple[int, str]:
        """Determine the next goal and return a hint for the VM."""
        self.goal_type = self.curriculum.choose_goal_type()
        if self.goal_type == "sequence":
            seq = self.sequence_gen.fibonacci(5)
            self.current_goal = seq[-1]
            hint = "follow fibonacci pattern"
        elif self.goal_type == "reinforcement":
            rng = self.curriculum.weakest_range() or 0
            self.current_goal = random.randint(rng, rng + 4)
            hint = "practice weak range"
        elif self.goal_type == "challenge":
            self.current_goal = random.randint(0, 20)
            hint = "challenge mode"
        else:
            self.current_goal = random.randint(0, DIFFICULTY_LEVELS[self.difficulty]["range_max"])
            hint = "standard goal"
        self.curriculum.register_goal(self.current_goal, self.goal_type)
        return self.current_goal, hint


class SequenceGenerator:
    """Creates mathematical sequences for pattern learning."""

    @staticmethod
    def arithmetic(start: int = 0, step: int = 1, length: int = 5) -> List[int]:
        return [start + step * i for i in range(length)]

    @staticmethod
    def geometric(start: int = 1, ratio: int = 2, length: int = 5) -> List[int]:
        seq = [start]
        for _ in range(1, length):
            seq.append(seq[-1] * ratio)
        return seq

    @staticmethod
    def fibonacci(length: int = 5) -> List[int]:
        seq = [0, 1]
        while len(seq) < length:
            seq.append(seq[-1] + seq[-2])
        return seq[:length]

    @staticmethod
    def primes(length: int = 5) -> List[int]:
        seq = []
        n = 2
        while len(seq) < length:
            for p in range(2, int(n ** 0.5) + 1):
                if n % p == 0:
                    break
            else:
                seq.append(n)
            n += 1
        return seq


class AdaptiveCurriculum:
    """Tracks skill development and generates targeted practice."""

    def __init__(self):
        self.range_stats: dict[int, dict[str, int]] = {}
        self.goal_history: List[Tuple[int, str]] = []

    def _range_key(self, value: int) -> int:
        return (value // 5) * 5

    def register_goal(self, target: int, goal_type: str) -> None:
        self.goal_history.append((target, goal_type))

    def record_attempt(self, target: int, success: bool) -> None:
        key = self._range_key(target)
        stats = self.range_stats.setdefault(key, {"attempts": 0, "successes": 0})
        stats["attempts"] += 1
        if success:
            stats["successes"] += 1

    def weakest_range(self) -> Optional[int]:
        weakest = None
        lowest = 1.1
        for key, data in self.range_stats.items():
            if data["attempts"] == 0:
                continue
            rate = data["successes"] / data["attempts"]
            if rate < lowest:
                lowest = rate
                weakest = key
        return weakest

    def choose_goal_type(self) -> str:
        if self.weakest_range() is not None and random.random() < 0.4:
            return "reinforcement"
        if random.random() < 0.2:
            return "sequence"
        if random.random() > 0.9:
            return "challenge"
        return "standard"


class PerformanceMonitor:
    """Real-time tracking and visualization of VM performance."""

    def __init__(self) -> None:
        self.total_attempts = 0
        self.successes = 0
        self.attempts_per_success: List[int] = []
        self.current_attempts = 0

    def record_attempt(self, success: bool) -> None:
        self.total_attempts += 1
        self.current_attempts += 1
        if success:
            self.successes += 1
            self.attempts_per_success.append(self.current_attempts)
            self.current_attempts = 0

    def success_rate(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.successes / max(1, len(self.attempts_per_success) + (1 if self.current_attempts else 0))

    def average_attempts(self) -> float:
        if not self.attempts_per_success:
            return 0.0
        return sum(self.attempts_per_success) / len(self.attempts_per_success)

    def trend(self) -> float:
        if len(self.attempts_per_success) < 3:
            return 0.0
        recent_avg = sum(self.attempts_per_success[-3:]) / 3
        overall = self.average_attempts()
        return overall - recent_avg

# --- Global VM State ---
current_vm_program = []
current_vm_stack = []
current_vm_ip = 0
current_vm_output_log = []
vm_halted = False
vm_error = None
vm_generator = None
MAX_INSTRUCTIONS_PER_STEP_CYCLE = int(get_config_value("vm.max_instructions_per_cycle", 1))
vm_is_waiting_for_input = False

# --- NEW GLOBALS FOR GOAL-SEEKING DEMO ---
current_target_value_idx = None  # Stores the prime index the VM is trying to output
vm_interaction_phase = "IDLE"    # Phases: "IDLE", "SEND_TARGET", "AWAITING_ATTEMPT_RESULT"
                                 # "SEND_TARGET": VM expects us to send it a new target value.
                                 # "AWAITING_ATTEMPT_RESULT": VM has made an attempt, expects 0/1 feedback.

# --- NEW GLOBALS FOR ADAPTIVE TEACHING ---
vm_attempts_on_current_target = 0
DIFFICULTY_LEVELS = get_config_value(
    "difficulty_levels",
    {
        "EASY": {"range_max": 4, "max_attempts_before_struggle": 5, "quick_success_threshold": 1},
        "MEDIUM": {"range_max": 9, "max_attempts_before_struggle": 4, "quick_success_threshold": 1},
        "HARD": {"range_max": 14, "max_attempts_before_struggle": 3, "quick_success_threshold": 2},
    },
)
current_difficulty_level_name = get_config_value("teacher.difficulty", "MEDIUM")
QUICK_SUCCESS_STREAK_TO_UPGRADE = int(
    get_config_value("streak_thresholds.quick_success_to_upgrade", 3)
)
STRUGGLE_STREAK_TO_DOWNGRADE = int(
    get_config_value("streak_thresholds.struggle_to_downgrade", 2)
)
consecutive_quick_successes = 0
consecutive_struggles = 0

# --- Helper to load UOR program ---
def load_uor_program(filename: str | None = None) -> bool:
    """Load a UOR program into ``current_vm_program``.

    If ``filename`` is ``None`` the value from
    ``paths.default_uor_program`` in the configuration will be used.
    """
    global current_vm_program
    if filename is None:
        filename = get_config_value(
            "paths.default_uor_program", "goal_seeker_demo.uor.txt"
        )
    program_path = os.path.join(PROJECT_ROOT, "backend", "uor_programs", filename)
    current_vm_program = []
    try:
        with open(program_path, "r") as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith("#"): # Ignore empty lines and comments
                    current_vm_program.append(int(stripped_line))
        print(f"Loaded UOR program with {len(current_vm_program)} instructions.")
        return True
    except FileNotFoundError:
        print(f"Error: UOR program file not found at {program_path}")
        return False
    except ValueError:
        print(f"Error: Invalid integer in UOR program file {program_path}")
        return False

# --- Helper to get current VM state for API response ---
def get_vm_state_dict():
    decoded_program = []
    for i, chunk in enumerate(current_vm_program):
        decoded_instruction = f"Chunk: {chunk}"
        decoded_program.append({
            "address": i,
            "raw_chunk": chunk,
            "decoded": decode_chunk_to_string(chunk)
        })

    return {
        "program_memory": decoded_program,
        "stack": list(current_vm_stack),
        "instruction_pointer": current_vm_ip,
        "output_log": list(current_vm_output_log),
        "halted": vm_halted,
        "error": vm_error,
        "needs_input": vm_is_waiting_for_input, 
        "current_target": current_target_value_idx,
        "interaction_phase": vm_interaction_phase,
        # Adaptive teaching info
        "difficulty_level": current_difficulty_level_name,
        "attempts_on_target": vm_attempts_on_current_target,
        "quick_success_streak": consecutive_quick_successes,
        "struggle_streak": consecutive_struggles
    }

# --- Simple Chunk Decoder (Can be significantly improved) ---
def decode_chunk_to_string(chunk_value: int) -> str:
    if chunk_value == 0: return "RAW_ZERO (Error/Corrupt)"
    if chunk_value == 1: return "RAW_ONE (Likely NOP/Data)"

    try:
        raw_factors = vm_factor(chunk_value)
        logical_factors = [] # Will be populated after checksum peel

        # --- Start of revised decoder section ---
        potential_checksum_prime = None
        potential_checksum_exponent = 0
        temp_factors_for_xor_calc = []
        for p, e_val_raw in raw_factors:
            if e_val_raw >= 6 and potential_checksum_prime is None:
                potential_checksum_prime = p; potential_checksum_exponent = e_val_raw
            else: temp_factors_for_xor_calc.append((p, e_val_raw))
        if potential_checksum_prime is not None:
            xor_sum_verify = 0
            for p_vf, e_vf in temp_factors_for_xor_calc:
                if p_vf in VM_PRIME_IDX: xor_sum_verify ^= VM_PRIME_IDX[p_vf] * e_vf
            vm_extend_primes_to(xor_sum_verify)
            expected_checksum_prime = vm_get_prime(xor_sum_verify)
            if potential_checksum_prime == expected_checksum_prime:
                if potential_checksum_exponent > 6: logical_factors.append((potential_checksum_prime, potential_checksum_exponent - 6))
                logical_factors.extend(temp_factors_for_xor_calc)
            else: logical_factors = raw_factors
        else: logical_factors = raw_factors
        if not logical_factors and chunk_value > 1: return f"DECODE_ERR_NO_LOGIC ({chunk_value})"

        # --- Attempt to identify standard opcode (exp 4) ---
        operation_prime_val = None
        op_prime_candidates = []
        if logical_factors:
            for p_op_scan, e_op_scan in logical_factors:
                if e_op_scan == 4: op_prime_candidates.append(p_op_scan)
        if len(op_prime_candidates) == 1: operation_prime_val = op_prime_candidates[0]
        elif len(op_prime_candidates) > 1: return f"AMBIGUOUS_OP ({chunk_value})"

        if operation_prime_val:
            op_name = "UNKNOWN_OP"
            operand_str = ""
            if operation_prime_val == OP_PUSH:
                op_name = "PUSH"
                operand_p_val = None
                for p_lf, e_lf in logical_factors:
                    if p_lf != OP_PUSH and e_lf == 5: operand_p_val = p_lf; break
                if operand_p_val:
                    if operand_p_val in VM_PRIME_IDX: operand_str = f" (idx: {VM_PRIME_IDX[operand_p_val]})"
                    else: operand_str = f" (PVAL: {operand_p_val})" 
            # ... (elif for OP_ADD, OP_PRINT, OP_JUMP, OP_HALT etc. - these should work if logical_factors is just [(OP,4)])
            elif operation_prime_val == OP_ADD: op_name = "ADD"
            elif operation_prime_val == OP_PRINT: op_name = "PRINT"
            elif operation_prime_val == OP_HALT: op_name = "HALT"
            elif operation_prime_val == OP_JUMP: op_name = "JUMP"
            elif operation_prime_val == OP_POKE_CHUNK: op_name = "POKE_CHUNK"
            elif operation_prime_val == OP_BUILD_CHUNK: op_name = "BUILD_CHUNK"
            elif operation_prime_val == OP_DUP: op_name = "DUP"
            elif operation_prime_val == OP_SWAP: op_name = "SWAP"
            elif operation_prime_val == OP_DROP: op_name = "DROP"
            elif operation_prime_val == OP_MOD: op_name = "MOD"
            elif operation_prime_val == OP_INPUT: op_name = "INPUT"
            elif operation_prime_val == OP_NOP: op_name = "NOP"
            else: op_name = f"OP({VM_PRIME_IDX.get(operation_prime_val, operation_prime_val)})"
            
            return f"{op_name}{operand_str}"

        # --- If not a standard opcode, check for special PUSH (idx: 0) structure ---
        # For chunk_push(0), logical_factors is [(OP_PUSH, 9)]
        if len(logical_factors) == 1 and logical_factors[0][0] == OP_PUSH and logical_factors[0][1] > 5 : # e.g. (OP_PUSH, 9)
            return f"PUSH (idx: {VM_PRIME_IDX[OP_PUSH]})" # This is PUSH (idx: 0)

        # --- Fallback for data chunks (if not identified as an operation) ---
        if logical_factors: # Check if logical_factors is not empty
            if len(logical_factors) == 1 and logical_factors[0][1] == 3:
                p1, _ = logical_factors[0]
                if p1 in VM_PRIME_IDX:
                    val_idx = VM_PRIME_IDX[p1]
                    return f"DATA_P3 (val_idx:{val_idx})"
                else:
                    return f"DATA_P3_UNKNOWN_P (val:{p1})"

            if len(logical_factors) == 2: 
                p_a, e_a = logical_factors[0]
                p_b, e_b = logical_factors[1]
                char_p, pos_p = None, None
                if e_a == 1 and e_b == 2: char_p, pos_p = p_b, p_a
                elif e_a == 2 and e_b == 1: char_p, pos_p = p_a, p_b
                
                if char_p and pos_p and char_p in VM_PRIME_IDX and pos_p in VM_PRIME_IDX:
                    char_idx, pos_idx = VM_PRIME_IDX[char_p], VM_PRIME_IDX[pos_p]
                    return f"DATA_PAIR (pos:{pos_idx}, val_idx:{char_idx})"
                else:
                    return f"DATA_PAIR_UNKNOWN_P (p1:{p_a}, p2:{p_b})"
                
    except ValueError as e_val: 
        return f"INVALID_CHUNK ({chunk_value} - {e_val})"
    except Exception as e_exc: 
        return f"DECODE_ERR ({chunk_value} - {type(e_exc).__name__})"

    return f"CHUNK_UNRECOGNIZED ({chunk_value})"

# --- VM Instance & Execution Logic ---
# This needs to be carefully managed to run step-by-step.
# vm_execute is a generator. We need to pull from it.
vm_generator = None

def initialize_vm():
    global current_vm_stack, current_vm_ip, current_vm_output_log, vm_halted, vm_error, \
           vm_generator, current_vm_program, vm_is_waiting_for_input, \
           current_target_value_idx, vm_interaction_phase

    append_to_log("--- VM INITIALIZATION START (Goal-Seeker) ---")
    # Load the goal_seeker UOR program from configuration
    program_filename = get_config_value(
        "paths.default_uor_program", "goal_seeker_demo.uor.txt"
    )
    if not load_uor_program(program_filename):
        vm_error = "Failed to load UOR program."
        append_to_log(f"ERROR: {vm_error}")
        append_to_log("--- VM INITIALIZATION FAILED (Goal-Seeker) ---")
        return

    current_vm_stack = []
    current_vm_ip = 0
    current_vm_output_log = []
    vm_halted = False
    vm_error = None
    vm_is_waiting_for_input = False

    # --- Initialize for Goal-Seeking Demo & Adaptive Teaching ---
    global vm_attempts_on_current_target, consecutive_quick_successes, consecutive_struggles, current_difficulty_level_name # Ensure globals are accessible

    vm_attempts_on_current_target = 0
    consecutive_quick_successes = 0
    consecutive_struggles = 0

    difficulty_params = DIFFICULTY_LEVELS[current_difficulty_level_name]
    current_target_value_idx = random.randint(0, difficulty_params["range_max"])
    append_to_log(f"INIT: Difficulty: {current_difficulty_level_name}. Initial TARGET set by app.py: {current_target_value_idx}")

    # app.py creates the PUSH instruction for this initial target/attempt
    # and POKEs it into program memory at address 0.
    # The UOR program expects its first instruction (Addr 0) to be this PUSH.
    if len(current_vm_program) > 0:
        try:
            initial_attempt_push_chunk = chunk_push(current_target_value_idx) # UOR for PUSH(target)
            current_vm_program[0] = initial_attempt_push_chunk
            append_to_log(f"INIT: Overwrote program[0] with PUSH({current_target_value_idx}), UOR: {initial_attempt_push_chunk}")
        except Exception as e:
            vm_error = f"Error setting up initial PUSH for goal-seeker: {e}"
            append_to_log(f"ERROR: {vm_error}")
            append_to_log("--- VM INITIALIZATION FAILED (Goal-Seeker Setup) ---")
            current_vm_program = [] 
            return
    else:
        vm_error = "Cannot set initial PUSH for goal-seeker: Program is empty after load."
        append_to_log(f"ERROR: {vm_error}")
        append_to_log("--- VM INITIALIZATION FAILED (Goal-Seeker Setup) ---")
        return
        
    # Set the interaction phase. After the VM executes program[0] (PUSH current_target)
    # and PRINTs it, it will call OP_INPUT to get feedback.
    vm_interaction_phase = "AWAITING_ATTEMPT_RESULT"
    append_to_log(f"INIT: Interaction phase set to: {vm_interaction_phase}")
    # --- End Goal-Seeking Init ---

    initial_last_poked_val_for_addr0 = current_target_value_idx
    initial_sfc = 0
    
    initial_last_chosen_slot_addr_value = 1 # This is the literal address 1.
    initial_last_chosen_instr_type_value = 2 # This is the literal decision value 2.

    stack_for_this_vm_run = [
        initial_last_poked_val_for_addr0,
        initial_sfc,
        initial_last_chosen_slot_addr_value,
        initial_last_chosen_instr_type_value
    ]
    
    # Update the global current_vm_stack so get_vm_state_dict() is accurate even before the first step
    current_vm_stack = list(stack_for_this_vm_run) 
    
    vm_generator = vm_execute(list(current_vm_program), list(stack_for_this_vm_run))  # Use the locally defined stack

    # Log messages updated for new stack convention
    loaded_program_filename = program_filename  # record which file was loaded
    append_to_log(
        f"VM Initialized (Ambitious). Program: {loaded_program_filename}. Initial Target (for Addr0 PUSH): {current_target_value_idx}. Phase: {vm_interaction_phase}"
    )
    append_to_log(f"Initial Stack (contents: [last_pokéd_addr0_val, sfc, last_slot_addr_val, last_instr_type_val]): {current_vm_stack}. Initial IP: {current_vm_ip}.")
    append_to_log(f"VM waiting for input (at init end): {vm_is_waiting_for_input}")
    append_to_log("--- VM INITIALIZATION COMPLETE (Ambitious Goal-Seeker) ---")

# --- API Endpoints ---
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route('/api/init', methods=['POST'])
def api_init_vm():
    initialize_vm()
    if vm_error:
        return jsonify({"success": False, "error": vm_error, "state": get_vm_state_dict()}), 500
    return jsonify({"success": True, "state": get_vm_state_dict()})

@app.route('/api/step', methods=['POST'])
def api_step_vm():
    global vm_generator, current_vm_ip, current_vm_stack, current_vm_program, \
           current_vm_output_log, vm_halted, vm_error, vm_is_waiting_for_input # Added vm_is_waiting_for_input

    if vm_is_waiting_for_input:
        append_to_log(f"--- VM STEP Attempted while WAITING FOR INPUT (IP: {current_vm_ip}) ---")
        # Return current state, indicating it still needs input
        response_state = get_vm_state_dict()
        response_state['needs_input'] = True
        return jsonify({
            "success": False, # Or True, but with a message. Let's use False for "action not performed"
            "error": "VM is waiting for input. Use /api/provide_input.",
            "state": response_state
        }), 400 # Bad request, wrong endpoint or state

    if vm_halted or vm_error:
        append_to_log(f"--- VM STEP Attempted while HALTED/ERROR (IP: {current_vm_ip}, Halted: {vm_halted}, Error: {vm_error}) ---")
        response_state = get_vm_state_dict() # vm_is_waiting_for_input should be False here
        response_state['needs_input'] = False # Not waiting if halted/error
        return jsonify({"success": False, "error": vm_error or "VM is halted.", "state": response_state})

    if vm_generator is None:
        append_to_log(f"--- VM STEP Attempted with NO GENERATOR ---")
        initialize_vm() # This sets vm_is_waiting_for_input to False
        if vm_error:
            append_to_log(f"  Initialization failed: {vm_error}")
            response_state = get_vm_state_dict()
            response_state['needs_input'] = vm_is_waiting_for_input # Should be False
            return jsonify({"success": False, "error": vm_error, "state": response_state}), 500
        if vm_generator is None: # Should not happen if initialize_vm is correct
            append_to_log(f"  Generator still None after re-init.")
            response_state = get_vm_state_dict()
            response_state['needs_input'] = vm_is_waiting_for_input # Should be False
            return jsonify({"success": False, "error": "VM generator not initialized. Call /api/init first.", "state": response_state}), 400
        append_to_log(f"  VM re-initialized. Current IP: {current_vm_ip}")
        # vm_is_waiting_for_input is False after initialize_vm()

    try:
        # Log IP *before* this step is processed by VM
        append_to_log(f"--- VM STEP START (Processing UOR_addr {current_vm_ip}) ---")
        step_result = next(vm_generator, None)
        
        # --- LOGGING FOR THE RAW STEP RESULT ---
        raw_log_message = ""
        if isinstance(step_result, dict):
            raw_log_message = (
                f"  Yielded IP: {step_result.get('ip')}\n"
                f"  Yielded Stack: {step_result.get('stack')}\n"
                f"  Yielded Output: {step_result.get('output_this_step')}\n"
                f"  Yielded Halt: {step_result.get('halt_flag')}\n"
                f"  Yielded Error: {step_result.get('error_msg')}\n"
                f"  Yielded Needs Input: {step_result.get('needs_input')}\n"
            )
            if 'program' in step_result and current_vm_program != step_result.get('program', current_vm_program):
                 raw_log_message += f"  Program memory CHANGED by this step.\n"
            else:
                 raw_log_message += f"  Program memory NOT reported as changed or same as current.\n"
        elif step_result is None:
            raw_log_message = "  VM generator exhausted (step_result is None)."
        else:
            raw_log_message = f"  Unexpected step_result type: {type(step_result)}, value: {step_result}"
        append_to_log(raw_log_message)
        # --- END LOGGING FOR RAW STEP RESULT ---

        if step_result is None: # Generator exhausted
            vm_halted = True
            vm_is_waiting_for_input = False # Not waiting if fully stopped
            append_to_log("  Outcome: VM generator exhausted, setting vm_halted = True.")
        elif isinstance(step_result, dict):
            # Store the IP that was *just processed* by the VM
            processed_ip_for_log = current_vm_ip 

            # --- Check if VM is now waiting for input ---
            if step_result.get('needs_input'):
                vm_is_waiting_for_input = True
                # The VM has yielded its state *before* receiving input.
                # Update our globals to reflect this yielded state.
                current_vm_ip = step_result.get('ip', current_vm_ip)
                current_vm_stack = list(step_result.get('stack', current_vm_stack)) # Use list() for new copy
                
                # Program memory might have changed if POKE happened right before OP_INPUT
                if 'program' in step_result and current_vm_program != step_result.get('program'):
                    current_vm_program = list(step_result.get('program')) # Use list() for new copy
                    append_to_log("  Program memory changed by VM just before it requested input.")
                
                # Other state vars based on what OP_INPUT yields (should be non-halting, no error)
                vm_halted = step_result.get('halt_flag', False) 
                vm_error = step_result.get('error_msg', None)
                # Output log does not change for the step that requests input
                
                append_to_log(f"  VM NOW WAITING FOR INPUT. State reported by OP_INPUT: IP={current_vm_ip}, Stack={current_vm_stack}")
                append_to_log(f"  Instruction at UOR_addr {processed_ip_for_log} (OP_INPUT) was processed.")

            else:
                # --- Normal step processing (not waiting for input from this step) ---
                vm_is_waiting_for_input = False # Explicitly set if not waiting

                current_vm_ip = step_result.get('ip', current_vm_ip)
                current_vm_stack = list(step_result.get('stack', current_vm_stack))
                
                if 'program' in step_result:
                    if current_vm_program != step_result.get('program'):
                        append_to_log(f"  POKE DETECTED: Program memory is being updated from yielded state.")
                        for idx, (old_chunk, new_chunk) in enumerate(zip(current_vm_program, step_result.get('program'))):
                            if old_chunk != new_chunk:
                                append_to_log(f"    Change at addr {idx}: {old_chunk} -> {new_chunk}")
                        current_vm_program = list(step_result.get('program'))
                        append_to_log(f"  Master current_vm_program was updated from yielded program.")

                output_this_step = step_result.get('output_this_step')
                if output_this_step is not None: # Check for not None
                    current_vm_output_log.append(output_this_step)
                    append_to_log(f"  PRINT Output: {output_this_step}")
                
                if step_result.get('halt_flag', False):
                    vm_halted = True
                    append_to_log("  HALT instruction processed.")
                
                error_msg = step_result.get('error_msg')
                if error_msg:
                    vm_error = error_msg
                    append_to_log(f"  ERROR reported by VM: {error_msg}")

                append_to_log(
                    f"  State Updated (Normal Step): New IP={current_vm_ip}, Stack={current_vm_stack}, "
                    f"OutputLog={current_vm_output_log}, Halted={vm_halted}, Error={vm_error}"
                )
                append_to_log(f"  Instruction at UOR_addr {processed_ip_for_log} (before IP update to {current_vm_ip}) was processed.")
        else: 
            vm_error = f"UNEXPECTED step_result type after processing: {type(step_result)}"
            append_to_log(vm_error)
            vm_halted = True # Halt on unexpected type
            vm_is_waiting_for_input = False

        append_to_log("--- VM STEP END ---")
        response_state = get_vm_state_dict()
        response_state['needs_input'] = vm_is_waiting_for_input # Inform frontend of current status
        return jsonify({"success": True, "state": response_state})

    except StopIteration:
        vm_halted = True
        vm_is_waiting_for_input = False
        append_to_log("--- VM STEP (StopIteration) ---")
        append_to_log("  Outcome: StopIteration from next(vm_generator), setting vm_halted = True.")
        append_to_log("--- VM STEP END ---")
        response_state = get_vm_state_dict()
        response_state['needs_input'] = vm_is_waiting_for_input
        return jsonify({"success": True, "state": response_state}) # Success, VM ended normally

    except ValueError as e: 
        vm_error = f"ValueError in app.py /api/step: {str(e)}"
        append_to_log(f"--- VM STEP (ValueError in app.py) ---")
        append_to_log(f"  ERROR in app.py: {vm_error}")
        append_to_log("--- VM STEP END ---")
        vm_halted = True
        vm_is_waiting_for_input = False
        response_state = get_vm_state_dict()
        response_state['error'] = vm_error # Ensure error is in the state
        response_state['needs_input'] = vm_is_waiting_for_input
        return jsonify({"success": False, "error": vm_error, "state": response_state}), 400

    except Exception as e:
        import traceback
        vm_error = f"General Exception in app.py /api/step: {str(e)}"
        append_to_log(f"--- VM STEP (General Exception in app.py) ---")
        append_to_log(f"  ERROR in app.py: {vm_error}\n{traceback.format_exc()}")
        append_to_log("--- VM STEP END ---")
        vm_halted = True
        vm_is_waiting_for_input = False
        response_state = get_vm_state_dict()
        response_state['error'] = vm_error # Ensure error is in the state
        response_state['needs_input'] = vm_is_waiting_for_input
        return jsonify({"success": False, "error": vm_error, "state": response_state}), 500

@app.route('/api/provide_input', methods=['POST'])
def api_provide_input():
    global vm_generator, current_vm_ip, current_vm_stack, current_vm_program, \
           current_vm_output_log, vm_halted, vm_error, vm_is_waiting_for_input, \
           current_target_value_idx, vm_interaction_phase, \
           vm_attempts_on_current_target, consecutive_quick_successes, consecutive_struggles, \
           current_difficulty_level_name # Add all new globals used in this function

    append_to_log(f"--- API CALL: /api/provide_input (Phase: {vm_interaction_phase}, Currently waiting: {vm_is_waiting_for_input}) ---")

    if not vm_is_waiting_for_input:
        append_to_log("  Error: VM is not currently waiting for input.")
        response_state = get_vm_state_dict() # get_vm_state_dict now includes phase and target
        return jsonify({
            "success": False, 
            "error": "VM is not currently waiting for input.",
            "state": response_state
        }), 400

    if vm_generator is None or vm_halted or vm_error:
        append_to_log(f"  Error: VM not runnable (Halted: {vm_halted}, Error: {vm_error}, Gen None: {vm_generator is None}). Resetting 'waiting' flag.")
        vm_is_waiting_for_input = False 
        response_state = get_vm_state_dict()
        # response_state['needs_input'] = False
        return jsonify({
            "success": False,
            "error": "VM is not in a state to receive input (halted, error, or not initialized).",
            "state": response_state
        }), 400

    # Determine what value to send to the VM based on the interaction phase
    value_to_send_to_vm = None

    if vm_interaction_phase == "SEND_TARGET":
        if current_target_value_idx is None: 
            append_to_log(f"  Error: Phase is SEND_TARGET, but current_target_value_idx is None. Re-initializing target.")
            difficulty_params = DIFFICULTY_LEVELS[current_difficulty_level_name] 
            current_target_value_idx = random.randint(0, difficulty_params["range_max"]) 
        
        value_to_send_to_vm = current_target_value_idx
        append_to_log(f"  Phase: SEND_TARGET. Sending target prime_idx '{value_to_send_to_vm}' to VM (Difficulty: {current_difficulty_level_name}).")
        vm_interaction_phase = "AWAITING_ATTEMPT_RESULT"

    elif vm_interaction_phase == "AWAITING_ATTEMPT_RESULT":

        vm_attempts_on_current_target += 1
        append_to_log(f"  Attempt #{vm_attempts_on_current_target} for target {current_target_value_idx} (Difficulty: {current_difficulty_level_name})")

        difficulty_params = DIFFICULTY_LEVELS[current_difficulty_level_name]

        if current_vm_output_log and current_vm_output_log[-1] == STUCK_SIGNAL_PRINT_VALUE:
            append_to_log(f"    FYI: Detected STUCK SIGNAL print ('{STUCK_SIGNAL_PRINT_VALUE}') from UOR on a previous step.")

        actual_attempt_output_to_check = None
        if current_vm_output_log:

            actual_attempt_output_to_check = current_vm_output_log[-1]

        if actual_attempt_output_to_check is None: # Catches empty current_vm_output_log
            append_to_log("  Warning: AWAITING_ATTEMPT_RESULT but no output from VM to check. Sending FAILURE.")
            value_to_send_to_vm = PRIME_IDX_FAILURE 
        elif actual_attempt_output_to_check == STUCK_SIGNAL_PRINT_VALUE:
            append_to_log(f"  Warning: Last VM output was STUCK SIGNAL ('{STUCK_SIGNAL_PRINT_VALUE}'). UOR should print its attempt value before OP_INPUT. Sending FAILURE for this cycle.")
            value_to_send_to_vm = PRIME_IDX_FAILURE

        else:
            try:
                last_vm_output_idx = int(actual_attempt_output_to_check)
                if last_vm_output_idx == current_target_value_idx: # VM SUCCEEDED
                    value_to_send_to_vm = PRIME_IDX_SUCCESS
                    append_to_log(f"  SUCCESS: VM Output '{last_vm_output_idx}' matched Target '{current_target_value_idx}' in {vm_attempts_on_current_target} attempts.")
                    
                    consecutive_struggles = 0 
                    if vm_attempts_on_current_target <= difficulty_params["quick_success_threshold"]:
                        consecutive_quick_successes += 1
                        append_to_log(f"    Quick success! Streak: {consecutive_quick_successes}/{QUICK_SUCCESS_STREAK_TO_UPGRADE}.")
                        if consecutive_quick_successes >= QUICK_SUCCESS_STREAK_TO_UPGRADE:
                            if current_difficulty_level_name == "EASY":
                                current_difficulty_level_name = "MEDIUM"
                                append_to_log(f"    Difficulty INCREASED to MEDIUM.")
                            elif current_difficulty_level_name == "MEDIUM":
                                current_difficulty_level_name = "HARD"
                                append_to_log(f"    Difficulty INCREASED to HARD.")
                            consecutive_quick_successes = 0 
                    else: 
                        consecutive_quick_successes = 0 
                        append_to_log(f"    Success was not 'quick' ({vm_attempts_on_current_target} attempts > threshold {difficulty_params['quick_success_threshold']}) for this difficulty. Quick success streak reset.")

                    difficulty_params = DIFFICULTY_LEVELS[current_difficulty_level_name] 
                    current_target_value_idx = random.randint(0, difficulty_params["range_max"])
                    vm_interaction_phase = "SEND_TARGET" 
                    vm_attempts_on_current_target = 0 
                    append_to_log(f"  New TARGET: {current_target_value_idx} (Difficulty: {current_difficulty_level_name}). Phase: {vm_interaction_phase}.")

                else: # VM FAILED (MISMATCH)
                    value_to_send_to_vm = PRIME_IDX_FAILURE
                    append_to_log(f"  FAILURE: VM Output '{last_vm_output_idx}' mismatched Target '{current_target_value_idx}'. Attempt {vm_attempts_on_current_target}.")

                    if vm_attempts_on_current_target >= difficulty_params["max_attempts_before_struggle"]:
                        append_to_log(f"    VM is struggling with target {current_target_value_idx} (attempts: {vm_attempts_on_current_target} >= max: {difficulty_params['max_attempts_before_struggle']}).")
                        consecutive_quick_successes = 0 
                        consecutive_struggles += 1
                        append_to_log(f"    Struggle detected! Streak: {consecutive_struggles}/{STRUGGLE_STREAK_TO_DOWNGRADE}.")
                        if consecutive_struggles >= STRUGGLE_STREAK_TO_DOWNGRADE:
                            if current_difficulty_level_name == "HARD":
                                current_difficulty_level_name = "MEDIUM"
                                append_to_log(f"    Difficulty DECREASED to MEDIUM.")
                            elif current_difficulty_level_name == "MEDIUM":
                                current_difficulty_level_name = "EASY"
                                append_to_log(f"    Difficulty DECREASED to EASY.")
                            consecutive_struggles = 0 

                            difficulty_params = DIFFICULTY_LEVELS[current_difficulty_level_name] 
                            current_target_value_idx = random.randint(0, difficulty_params["range_max"])
                            vm_interaction_phase = "SEND_TARGET" 
                            vm_attempts_on_current_target = 0 
                            append_to_log(f"    Due to downgrade, new TARGET: {current_target_value_idx} (Difficulty: {current_difficulty_level_name}). VM will be sent this next.")
            except ValueError:
                append_to_log(f"  Error: Could not parse VM output '{actual_attempt_output_to_check}' as int for feedback. Sending FAILURE.")
                value_to_send_to_vm = PRIME_IDX_FAILURE
                # Also consider this a failed attempt for struggle counting if desired, though it's an unexpected output.
                # For now, just sends failure.
    
    try:
        posted_data = request.get_json(silent=True)
        if posted_data and 'value' in posted_data and vm_interaction_phase not in ["SEND_TARGET", "AWAITING_ATTEMPT_RESULT"]:
            user_input_val = int(posted_data['value'])

            append_to_log(f"  Note: Frontend POSTed value '{posted_data['value']}'. Current goal-seeker ignores this if phase is target/feedback.")
        elif posted_data and 'value' in posted_data:
             append_to_log(f"  Note: Frontend POSTed value '{posted_data['value']}' during target/feedback phase. It will be ignored by app.py logic for sending to VM this time.")


    except Exception as e:
        append_to_log(f"  Warning: Error processing 'value' from POST data during input: {str(e)}")


    if value_to_send_to_vm is None:
        append_to_log(f"  Error: No value determined to send to VM in phase '{vm_interaction_phase}'. Sending default FAILURE.")
        value_to_send_to_vm = PRIME_IDX_FAILURE 

        vm_error = f"Internal app.py error: Unhandled input phase '{vm_interaction_phase}'."

    append_to_log(f"--- VM SENDING VALUE TO GENERATOR (Value: {value_to_send_to_vm}) ---")

    try:
        step_result = vm_generator.send(value_to_send_to_vm)
        vm_is_waiting_for_input = False # Input was consumed by send()

        # --- Process step_result (this is the state *after* VM processes the sent input and yields again) ---
        raw_log_message_after_send = "" # Build log message for step_result
        if isinstance(step_result, dict):
            raw_log_message_after_send = (
                f"  Yielded (after send) IP: {step_result.get('ip')}\n"
                f"  Yielded (after send) Stack: {step_result.get('stack')}\n"
                f"  Yielded (after send) Output: {step_result.get('output_this_step')}\n"
                f"  Yielded (after send) Halt: {step_result.get('halt_flag')}\n"
                f"  Yielded (after send) Error: {step_result.get('error_msg')}\n"
                f"  Yielded (after send) Needs Input: {step_result.get('needs_input')}\n"
            )
            if 'program' in step_result and current_vm_program != step_result.get('program', current_vm_program):
                 raw_log_message_after_send += f"  Program memory CHANGED by this step (after send).\n"
            else:
                 raw_log_message_after_send += f"  Program memory NOT reported as changed or same as current (after send).\n"
        elif step_result is None:
            raw_log_message_after_send = "  VM generator exhausted (step_result is None after send)."
        else:
            raw_log_message_after_send = f"  Unexpected step_result type (after send): {type(step_result)}, value: {step_result}"
        append_to_log(raw_log_message_after_send)
        # --- END LOGGING FOR RAW STEP RESULT (after send) ---

        if step_result is None:
            vm_halted = True
            append_to_log("  Outcome: VM generator exhausted after input processing, setting vm_halted = True.")
        elif isinstance(step_result, dict):
            # Update global state based on what the VM yielded *after* processing the input
            processed_ip_for_log_after_send = current_vm_ip # IP state before applying this new step_result

            current_vm_ip = step_result.get('ip', current_vm_ip)
            current_vm_stack = list(step_result.get('stack', current_vm_stack))

            if 'program' in step_result and current_vm_program != step_result.get('program'):
                append_to_log(f"  POKE DETECTED after input processing & subsequent VM step.")
                current_vm_program = list(step_result.get('program'))
                append_to_log(f"  Master current_vm_program was updated.")
            
            output_this_step = step_result.get('output_this_step')
            if output_this_step is not None:
                current_vm_output_log.append(output_this_step)
                append_to_log(f"  PRINT Output (after input processing): {output_this_step}")

            if step_result.get('halt_flag', False):
                vm_halted = True
                append_to_log("  HALT instruction processed (after input).")
            
            error_msg = step_result.get('error_msg')
            if error_msg:
                vm_error = error_msg
                append_to_log(f"  ERROR reported by VM (after input): {error_msg}")

            # CRITICAL: Check if the VM is *again* asking for input
            if step_result.get('needs_input'):
                vm_is_waiting_for_input = True
                append_to_log(f"  VM NOW WAITING FOR INPUT AGAIN (Phase: {vm_interaction_phase}). State: IP={current_vm_ip}, Stack={current_vm_stack}")
            
            append_to_log(
                f"  State Updated (After Input Processed by VM): New IP={current_vm_ip}, Stack={current_vm_stack}, "
                f"OutputLog={current_vm_output_log}, Halted={vm_halted}, Error={vm_error}, Phase: {vm_interaction_phase}, Waiting: {vm_is_waiting_for_input}"
            )
            # append_to_log(f"  Instruction at UOR_addr {processed_ip_for_log_after_send} (before this state update) was processed.")
        else: # Unexpected type from step_result
            vm_error = f"UNEXPECTED step_result type after send(): {type(step_result)}"
            append_to_log(vm_error)
            vm_halted = True

        append_to_log("--- VM PROVIDE_INPUT END (SUCCESSFUL SEND & VM STEP) ---")
        response_state = get_vm_state_dict() # This will include the latest phase, target, and needs_input
        return jsonify({"success": True, "state": response_state})

    except StopIteration:
        vm_halted = True
        vm_is_waiting_for_input = False
        append_to_log("--- VM PROVIDE_INPUT (StopIteration after send) ---")
        append_to_log("  Outcome: StopIteration from vm_generator.send(), VM ended. Setting vm_halted = True.")
        append_to_log("--- VM PROVIDE_INPUT END ---")
        response_state = get_vm_state_dict()
        return jsonify({"success": True, "state": response_state})
    except Exception as e:
        import traceback
        vm_error = f"General Exception in app.py during /api/provide_input: {str(e)}"
        append_to_log(f"--- VM PROVIDE_INPUT (General Exception in app.py) ---")
        append_to_log(f"  ERROR in app.py: {vm_error}\n{traceback.format_exc()}")
        append_to_log("--- VM PROVIDE_INPUT END ---")
        vm_halted = True 
        vm_is_waiting_for_input = False
        response_state = get_vm_state_dict()
        return jsonify({"success": False, "error": vm_error, "state": response_state}), 500

if __name__ == '__main__':
    initialize_vm()  # Load program on startup
    app.run(debug=DEBUG_MODE, port=5000, use_reloader=False)
