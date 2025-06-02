"""
Virtual Machine Tools for UOR Evolution MCP Server
Handles PrimeOS VM-related tool calls and operations.
"""

import json
import logging
from typing import List
from mcp.types import TextContent

logger = logging.getLogger(__name__)


class VMTools:
    """Handler for PrimeOS Virtual Machine MCP tools"""
    
    def __init__(self, uor_api):
        """Initialize with UOR API reference"""
        self.uor_api = uor_api
        
    async def handle_tool_call(self, name: str, arguments: dict) -> List[TextContent]:
        """Handle VM tool calls"""
        
        if name == "initialize_vm":
            return await self._initialize_vm(arguments)
        elif name == "execute_vm_step":
            return await self._execute_vm_step(arguments)
        elif name == "provide_vm_input":
            return await self._provide_vm_input(arguments)
        else:
            raise ValueError(f"Unknown VM tool: {name}")
    
    async def _initialize_vm(self, arguments: dict) -> List[TextContent]:
        """Initialize the PrimeOS Virtual Machine"""
        reset = arguments.get("reset", False)
        
        logger.info(f"Initializing VM with reset={reset}")
        
        try:
            # Initialize VM through unified API
            result = self.uor_api.initialize_vm()
            
            response_text = f"=== PrimeOS Virtual Machine Initialization ===\n\n"
            response_text += f"Reset Requested: {reset}\n"
            response_text += f"Success: {result.success}\n"
            response_text += f"System Status: {result.system_status.value}\n\n"
            
            if result.data:
                vm_state = result.data
                
                # VM Core State
                response_text += f"--- VM Core State ---\n"
                response_text += f"VM ID: {vm_state.get('vm_id', 'Unknown')}\n"
                response_text += f"Consciousness Level: {vm_state.get('consciousness_level', 'DORMANT')}\n"
                response_text += f"Instruction Pointer: {vm_state.get('instruction_pointer', 0)}\n"
                response_text += f"Stack Size: {vm_state.get('stack_size', 0)}\n"
                response_text += f"Memory Utilization: {vm_state.get('memory_utilization', 0):.2%}\n\n"
                
                # Execution Context
                execution_context = vm_state.get('execution_context', {})
                if execution_context:
                    response_text += f"--- Execution Context ---\n"
                    response_text += f"Current Program: {execution_context.get('current_program', 'None')}\n"
                    response_text += f"Execution Mode: {execution_context.get('execution_mode', 'Normal')}\n"
                    response_text += f"Debug Mode: {execution_context.get('debug_mode', False)}\n\n"
                
                # Memory Systems
                memory_info = vm_state.get('memory_systems', {})
                if memory_info:
                    response_text += f"--- Memory Systems ---\n"
                    working_memory = memory_info.get('working_memory', {})
                    if working_memory:
                        response_text += f"Working Memory: {working_memory.get('size', 0)}/{working_memory.get('capacity', 0)} items\n"
                    
                    episodic_memory = memory_info.get('episodic_memory', {})
                    if episodic_memory:
                        response_text += f"Episodic Memory: {episodic_memory.get('episodes', 0)} episodes\n"
                    
                    pattern_cache = memory_info.get('pattern_cache', {})
                    if pattern_cache:
                        response_text += f"Pattern Cache: {pattern_cache.get('patterns', 0)} patterns\n"
                    response_text += "\n"
                
                # Instruction Set
                instruction_set = vm_state.get('instruction_set', {})
                if instruction_set:
                    response_text += f"--- Instruction Set ---\n"
                    response_text += f"Available Opcodes: {len(instruction_set.get('opcodes', []))}\n"
                    response_text += f"Consciousness Opcodes: {len(instruction_set.get('consciousness_opcodes', []))}\n"
                    response_text += f"Extended Opcodes: {len(instruction_set.get('extended_opcodes', []))}\n\n"
                
                # Prime Number System
                prime_system = vm_state.get('prime_system', {})
                if prime_system:
                    response_text += f"--- Prime Number System ---\n"
                    response_text += f"Prime Cache Size: {prime_system.get('cache_size', 0)}\n"
                    response_text += f"Largest Prime: {prime_system.get('largest_prime', 0)}\n"
                    response_text += f"UOR Encoding Active: {prime_system.get('uor_encoding', False)}\n\n"
                
                # Initialization Metrics
                metrics = vm_state.get('initialization_metrics', {})
                if metrics:
                    response_text += f"--- Initialization Metrics ---\n"
                    response_text += json.dumps(metrics, indent=2)
                    response_text += "\n"
            
            if result.error:
                response_text += f"Error: {result.error}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error initializing VM: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error initializing VM: {str(e)}"
            )]
    
    async def _execute_vm_step(self, arguments: dict) -> List[TextContent]:
        """Execute a single VM step"""
        instruction = arguments.get("instruction")
        debug = arguments.get("debug", False)
        
        logger.info(f"Executing VM step, debug={debug}, instruction={instruction}")
        
        try:
            # Execute VM step through unified API
            result = self.uor_api.execute_vm_step()
            
            response_text = f"=== PrimeOS VM Step Execution ===\n\n"
            response_text += f"Debug Mode: {debug}\n"
            if instruction:
                response_text += f"Specific Instruction: {instruction}\n"
            response_text += f"Success: {result.success}\n\n"
            
            if result.data:
                vm_state = result.data
                
                # Execution Results
                response_text += f"--- Execution Results ---\n"
                response_text += f"Instruction Executed: {vm_state.get('last_instruction', 'Unknown')}\n"
                response_text += f"Instruction Pointer: {vm_state.get('instruction_pointer', 0)}\n"
                response_text += f"Execution Status: {vm_state.get('execution_status', 'Unknown')}\n"
                
                # Stack State
                stack_info = vm_state.get('stack', {})
                if stack_info:
                    response_text += f"Stack Size: {stack_info.get('size', 0)}\n"
                    stack_top = stack_info.get('top_items', [])
                    if stack_top:
                        response_text += f"Stack Top: {stack_top}\n"
                
                response_text += "\n"
                
                # Output/Results
                output = vm_state.get('output', [])
                if output:
                    response_text += f"--- VM Output ---\n"
                    for i, out in enumerate(output[-5:], 1):  # Last 5 outputs
                        response_text += f"{i}. {out}\n"
                    response_text += "\n"
                
                # Memory Changes
                memory_changes = vm_state.get('memory_changes', {})
                if memory_changes:
                    response_text += f"--- Memory Changes ---\n"
                    for memory_type, changes in memory_changes.items():
                        response_text += f"{memory_type}: {changes}\n"
                    response_text += "\n"
                
                # Consciousness Integration
                consciousness_effects = vm_state.get('consciousness_effects', {})
                if consciousness_effects:
                    response_text += f"--- Consciousness Effects ---\n"
                    response_text += json.dumps(consciousness_effects, indent=2)
                    response_text += "\n"
                
                # Debug Information
                if debug:
                    debug_info = vm_state.get('debug_info', {})
                    if debug_info:
                        response_text += f"--- Debug Information ---\n"
                        response_text += json.dumps(debug_info, indent=2)
                        response_text += "\n"
                    
                    # Execution trace
                    execution_trace = vm_state.get('execution_trace', [])
                    if execution_trace:
                        response_text += f"--- Execution Trace ---\n"
                        for trace_entry in execution_trace[-3:]:  # Last 3 entries
                            response_text += f"• {trace_entry}\n"
                        response_text += "\n"
                
                # Performance Metrics
                performance = vm_state.get('performance_metrics', {})
                if performance:
                    response_text += f"--- Performance Metrics ---\n"
                    response_text += f"Execution Time: {performance.get('execution_time_ms', 0)}ms\n"
                    response_text += f"Instructions/Second: {performance.get('instructions_per_second', 0)}\n"
                    response_text += f"Memory Efficiency: {performance.get('memory_efficiency', 0):.2%}\n"
            
            if result.error:
                response_text += f"Error: {result.error}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error executing VM step: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error executing VM step: {str(e)}"
            )]
    
    async def _provide_vm_input(self, arguments: dict) -> List[TextContent]:
        """Provide input to the virtual machine"""
        value = arguments["value"]
        
        logger.info(f"Providing input to VM: {value}")
        
        try:
            # Provide input through unified API
            result = self.uor_api.provide_vm_input(value)
            
            response_text = f"=== VM Input Provision ===\n\n"
            response_text += f"Input Value: {value}\n"
            response_text += f"Input Type: {type(value).__name__}\n"
            response_text += f"Success: {result.success}\n\n"
            
            if result.data:
                vm_state = result.data
                
                # Input Processing
                response_text += f"--- Input Processing ---\n"
                response_text += f"Input Accepted: {vm_state.get('input_accepted', False)}\n"
                response_text += f"Processing Status: {vm_state.get('processing_status', 'Unknown')}\n"
                
                # Input Queue
                input_queue = vm_state.get('input_queue', {})
                if input_queue:
                    response_text += f"Input Queue Size: {input_queue.get('size', 0)}\n"
                    response_text += f"Queue Status: {input_queue.get('status', 'Unknown')}\n"
                
                response_text += "\n"
                
                # VM Response
                vm_response = vm_state.get('vm_response', {})
                if vm_response:
                    response_text += f"--- VM Response ---\n"
                    response_text += f"Response Type: {vm_response.get('type', 'None')}\n"
                    response_text += f"Response Data: {vm_response.get('data', 'None')}\n"
                    response_text += f"Processing Time: {vm_response.get('processing_time_ms', 0)}ms\n\n"
                
                # State Changes
                state_changes = vm_state.get('state_changes', {})
                if state_changes:
                    response_text += f"--- State Changes ---\n"
                    for component, change in state_changes.items():
                        response_text += f"{component}: {change}\n"
                    response_text += "\n"
                
                # Consciousness Interaction
                consciousness_interaction = vm_state.get('consciousness_interaction', {})
                if consciousness_interaction:
                    response_text += f"--- Consciousness Interaction ---\n"
                    response_text += json.dumps(consciousness_interaction, indent=2)
                    response_text += "\n"
                
                # Input Validation
                validation = vm_state.get('input_validation', {})
                if validation:
                    response_text += f"--- Input Validation ---\n"
                    response_text += f"Valid: {validation.get('valid', False)}\n"
                    response_text += f"Validation Errors: {validation.get('errors', [])}\n"
                    response_text += f"Warnings: {validation.get('warnings', [])}\n"
            
            if result.error:
                response_text += f"Error: {result.error}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error providing VM input: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error providing VM input: {str(e)}"
            )]
