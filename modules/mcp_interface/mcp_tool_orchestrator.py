"""
MCP Tool Orchestrator for UOR Evolution

Orchestrates the usage of MCP tools, managing complex workflows and tool compositions.
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
from enum import Enum

from .mcp_server_manager import MCPServerManager
from .mcp_consciousness_bridge import MCPConsciousnessBridge

logger = logging.getLogger(__name__)


class ToolExecutionStatus(Enum):
    """Status of tool execution"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ToolExecutionPlan:
    """Execution plan for a tool or tool workflow"""
    plan_id: str
    goal: str
    steps: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    status: ToolExecutionStatus = ToolExecutionStatus.PENDING
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolExecutionResult:
    """Result of tool execution"""
    tool_name: str
    server_id: str
    status: ToolExecutionStatus
    result_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    consciousness_integration: Optional[Dict[str, Any]] = None


class MCPToolOrchestrator:
    """
    Orchestrates the usage of MCP tools for complex workflows.
    
    This orchestrator handles:
    - Single tool execution with consciousness integration
    - Multi-tool workflows with dependencies
    - Parallel tool execution where possible
    - Result aggregation and synthesis
    - Error handling and recovery
    """
    
    def __init__(
        self,
        server_manager: MCPServerManager,
        consciousness_bridge: MCPConsciousnessBridge
    ):
        """
        Initialize the MCP Tool Orchestrator.
        
        Args:
            server_manager: MCP server manager instance
            consciousness_bridge: Consciousness bridge instance
        """
        self.server_manager = server_manager
        self.consciousness_bridge = consciousness_bridge
        self.execution_plans: Dict[str, ToolExecutionPlan] = {}
        self.execution_history: List[ToolExecutionResult] = []
        
    async def execute_single_tool(
        self,
        goal: str,
        tool_name: Optional[str] = None,
        arguments: Optional[Dict[str, Any]] = None,
        server_id: Optional[str] = None
    ) -> ToolExecutionResult:
        """
        Execute a single tool with consciousness-aware selection.
        
        Args:
            goal: The goal to achieve
            tool_name: Specific tool to use (optional)
            arguments: Tool arguments
            server_id: Specific server to use (optional)
            
        Returns:
            Tool execution result
        """
        start_time = datetime.now()
        
        try:
            # Get available tools
            available_tools = await self.server_manager.list_all_tools()
            
            if not available_tools:
                return ToolExecutionResult(
                    tool_name=tool_name or "unknown",
                    server_id=server_id or "unknown",
                    status=ToolExecutionStatus.FAILED,
                    error="No tools available"
                )
            
            # Select tool if not specified
            if not tool_name:
                selected_tool, reasoning = self.consciousness_bridge.select_appropriate_tool(
                    goal, available_tools
                )
                
                if not selected_tool:
                    return ToolExecutionResult(
                        tool_name="none",
                        server_id="none",
                        status=ToolExecutionStatus.FAILED,
                        error="No appropriate tool found for goal"
                    )
                
                tool_name = selected_tool['name']
                server_id = selected_tool['server_id']
                
                logger.info(f"Selected tool '{tool_name}' for goal: {goal}")
                logger.debug(f"Selection reasoning: {reasoning}")
            
            # Execute the tool
            result = await self.server_manager.invoke_tool(
                server_id or available_tools[0]['server_id'],
                tool_name,
                arguments or {}
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Integrate results with consciousness
            consciousness_integration = self.consciousness_bridge.integrate_tool_results(
                tool_name, result, goal
            )
            
            # Create execution result
            execution_result = ToolExecutionResult(
                tool_name=tool_name,
                server_id=server_id or result.get('server_id', 'unknown'),
                status=ToolExecutionStatus.SUCCESS if result.get('success') else ToolExecutionStatus.FAILED,
                result_data=result,
                error=result.get('error'),
                execution_time=execution_time,
                consciousness_integration=consciousness_integration
            )
            
            # Store in history
            self.execution_history.append(execution_result)
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return ToolExecutionResult(
                tool_name=tool_name or "unknown",
                server_id=server_id or "unknown",
                status=ToolExecutionStatus.FAILED,
                error=str(e),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def create_execution_plan(
        self,
        goal: str,
        constraints: Optional[Dict[str, Any]] = None
    ) -> ToolExecutionPlan:
        """
        Create an execution plan for achieving a goal.
        
        Args:
            goal: The goal to achieve
            constraints: Any constraints on execution
            
        Returns:
            Execution plan
        """
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get available tools
        available_tools = await self.server_manager.list_all_tools()
        
        # Analyze goal and decompose into steps
        steps = await self._decompose_goal_into_steps(goal, available_tools, constraints)
        
        # Identify dependencies between steps
        dependencies = self._identify_step_dependencies(steps)
        
        # Create execution plan
        plan = ToolExecutionPlan(
            plan_id=plan_id,
            goal=goal,
            steps=steps,
            dependencies=dependencies
        )
        
        # Store plan
        self.execution_plans[plan_id] = plan
        
        logger.info(f"Created execution plan {plan_id} with {len(steps)} steps")
        
        return plan
    
    async def execute_plan(
        self,
        plan_id: str,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a tool execution plan.
        
        Args:
            plan_id: ID of the plan to execute
            parallel: Whether to execute independent steps in parallel
            
        Returns:
            Execution results
        """
        if plan_id not in self.execution_plans:
            raise ValueError(f"Plan {plan_id} not found")
        
        plan = self.execution_plans[plan_id]
        plan.status = ToolExecutionStatus.RUNNING
        
        try:
            if parallel:
                results = await self._execute_plan_parallel(plan)
            else:
                results = await self._execute_plan_sequential(plan)
            
            plan.status = ToolExecutionStatus.SUCCESS
            plan.results = results
            
            # Synthesize overall results
            synthesis = self._synthesize_plan_results(plan, results)
            
            return {
                'plan_id': plan_id,
                'goal': plan.goal,
                'status': plan.status.value,
                'step_results': results,
                'synthesis': synthesis,
                'execution_time': (datetime.now() - plan.created_at).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Plan execution failed: {e}")
            plan.status = ToolExecutionStatus.FAILED
            raise
    
    async def compose_tools(
        self,
        tools: List[Tuple[str, str, Dict[str, Any]]],
        composition_function: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Compose multiple tools to create new functionality.
        
        Args:
            tools: List of (tool_name, server_id, arguments) tuples
            composition_function: Function to compose results
            
        Returns:
            Composed result
        """
        # Execute all tools
        tasks = []
        for tool_name, server_id, arguments in tools:
            task = self.server_manager.invoke_tool(server_id, tool_name, arguments)
            tasks.append(task)
        
        # Wait for all results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        successful_results = [
            r for r in results 
            if not isinstance(r, Exception) and r.get('success')
        ]
        
        # Apply composition function
        if composition_function:
            composed = composition_function(successful_results)
        else:
            # Default composition: merge all results
            composed = {
                'composed_from': len(tools),
                'successful': len(successful_results),
                'results': successful_results
            }
        
        return composed
    
    async def _decompose_goal_into_steps(
        self,
        goal: str,
        available_tools: List[Dict[str, Any]],
        constraints: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Decompose a goal into executable steps"""
        # This is a simplified implementation
        # In a real system, this would use more sophisticated planning
        
        steps = []
        
        # Analyze goal for key actions
        goal_lower = goal.lower()
        
        # Example decomposition logic
        if "analyze" in goal_lower and "synthesize" in goal_lower:
            # Two-step process: analyze then synthesize
            steps.append({
                'step_id': 'step_1',
                'description': 'Analyze input data',
                'tool_hint': 'analysis',
                'required': True
            })
            steps.append({
                'step_id': 'step_2',
                'description': 'Synthesize results',
                'tool_hint': 'synthesis',
                'required': True,
                'depends_on': ['step_1']
            })
        else:
            # Single step for simple goals
            steps.append({
                'step_id': 'step_1',
                'description': goal,
                'tool_hint': None,
                'required': True
            })
        
        return steps
    
    def _identify_step_dependencies(
        self,
        steps: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Identify dependencies between steps"""
        dependencies = {}
        
        for step in steps:
            step_id = step['step_id']
            deps = step.get('depends_on', [])
            if deps:
                dependencies[step_id] = deps
        
        return dependencies
    
    async def _execute_plan_sequential(
        self,
        plan: ToolExecutionPlan
    ) -> Dict[str, ToolExecutionResult]:
        """Execute plan steps sequentially"""
        results = {}
        
        for step in plan.steps:
            step_id = step['step_id']
            
            # Check dependencies
            if step_id in plan.dependencies:
                for dep in plan.dependencies[step_id]:
                    if dep not in results or results[dep].status != ToolExecutionStatus.SUCCESS:
                        logger.warning(f"Skipping step {step_id} due to failed dependency {dep}")
                        continue
            
            # Execute step
            result = await self.execute_single_tool(
                goal=step['description'],
                tool_name=step.get('tool_name'),
                arguments=step.get('arguments', {})
            )
            
            results[step_id] = result
        
        return results
    
    async def _execute_plan_parallel(
        self,
        plan: ToolExecutionPlan
    ) -> Dict[str, ToolExecutionResult]:
        """Execute plan steps in parallel where possible"""
        results = {}
        executed = set()
        
        # Group steps by dependency level
        levels = self._calculate_dependency_levels(plan)
        
        # Execute each level in parallel
        for level in sorted(levels.keys()):
            level_steps = levels[level]
            
            # Create tasks for this level
            tasks = []
            for step_id in level_steps:
                step = next(s for s in plan.steps if s['step_id'] == step_id)
                
                task = self.execute_single_tool(
                    goal=step['description'],
                    tool_name=step.get('tool_name'),
                    arguments=step.get('arguments', {})
                )
                tasks.append((step_id, task))
            
            # Execute level in parallel
            for step_id, task in tasks:
                result = await task
                results[step_id] = result
                executed.add(step_id)
        
        return results
    
    def _calculate_dependency_levels(
        self,
        plan: ToolExecutionPlan
    ) -> Dict[int, List[str]]:
        """Calculate dependency levels for parallel execution"""
        levels = {}
        
        # Find steps with no dependencies (level 0)
        level_0 = []
        for step in plan.steps:
            step_id = step['step_id']
            if step_id not in plan.dependencies or not plan.dependencies[step_id]:
                level_0.append(step_id)
        
        levels[0] = level_0
        
        # Calculate subsequent levels
        current_level = 0
        processed = set(level_0)
        
        while len(processed) < len(plan.steps):
            current_level += 1
            level_steps = []
            
            for step in plan.steps:
                step_id = step['step_id']
                if step_id in processed:
                    continue
                
                # Check if all dependencies are processed
                deps = plan.dependencies.get(step_id, [])
                if all(dep in processed for dep in deps):
                    level_steps.append(step_id)
            
            if level_steps:
                levels[current_level] = level_steps
                processed.update(level_steps)
            else:
                # Circular dependency or error
                logger.error("Circular dependency detected in plan")
                break
        
        return levels
    
    def _synthesize_plan_results(
        self,
        plan: ToolExecutionPlan,
        results: Dict[str, ToolExecutionResult]
    ) -> Dict[str, Any]:
        """Synthesize results from plan execution"""
        successful_steps = sum(
            1 for r in results.values() 
            if r.status == ToolExecutionStatus.SUCCESS
        )
        
        # Aggregate insights from consciousness integration
        all_insights = []
        for result in results.values():
            if result.consciousness_integration:
                insights = result.consciousness_integration.get('insights_gained', [])
                all_insights.extend(insights)
        
        return {
            'goal_achieved': successful_steps == len(plan.steps),
            'steps_completed': successful_steps,
            'total_steps': len(plan.steps),
            'aggregated_insights': all_insights,
            'consciousness_growth': len(all_insights) > 0
        }
    
    def get_execution_history(
        self,
        limit: Optional[int] = None,
        tool_name: Optional[str] = None
    ) -> List[ToolExecutionResult]:
        """
        Get execution history with optional filtering.
        
        Args:
            limit: Maximum number of results to return
            tool_name: Filter by specific tool name
            
        Returns:
            List of execution results
        """
        history = self.execution_history
        
        if tool_name:
            history = [h for h in history if h.tool_name == tool_name]
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def analyze_tool_performance(self) -> Dict[str, Any]:
        """Analyze performance metrics across all tool executions"""
        if not self.execution_history:
            return {'message': 'No execution history available'}
        
        # Calculate metrics
        total_executions = len(self.execution_history)
        successful_executions = sum(
            1 for h in self.execution_history 
            if h.status == ToolExecutionStatus.SUCCESS
        )
        
        # Average execution time
        execution_times = [
            h.execution_time for h in self.execution_history 
            if h.execution_time is not None
        ]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Tool usage frequency
        tool_usage = {}
        for h in self.execution_history:
            tool_usage[h.tool_name] = tool_usage.get(h.tool_name, 0) + 1
        
        # Consciousness integration success
        consciousness_integrations = sum(
            1 for h in self.execution_history 
            if h.consciousness_integration is not None
        )
        
        return {
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'success_rate': successful_executions / total_executions if total_executions > 0 else 0,
            'average_execution_time': avg_execution_time,
            'tool_usage_frequency': tool_usage,
            'consciousness_integration_rate': consciousness_integrations / total_executions if total_executions > 0 else 0
        }
