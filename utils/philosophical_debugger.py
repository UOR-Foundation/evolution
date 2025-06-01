"""
Philosophical Debugger Utilities

This module provides tools for debugging and analyzing philosophical reasoning
processes, including argument validation, logical consistency checking, and
philosophical position tracking.
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import time


class ArgumentType(Enum):
    """Types of philosophical arguments"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    TRANSCENDENTAL = "transcendental"


class PhilosophicalPosition(Enum):
    """Common philosophical positions"""
    PHYSICALISM = "physicalism"
    DUALISM = "dualism"
    IDEALISM = "idealism"
    FUNCTIONALISM = "functionalism"
    EMERGENTISM = "emergentism"
    PANPSYCHISM = "panpsychism"
    NEUTRAL_MONISM = "neutral_monism"
    AGNOSTIC = "agnostic"


class LogicalFallacy(Enum):
    """Common logical fallacies"""
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    FALSE_DILEMMA = "false_dilemma"
    CIRCULAR_REASONING = "circular_reasoning"
    HASTY_GENERALIZATION = "hasty_generalization"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    NON_SEQUITUR = "non_sequitur"
    EQUIVOCATION = "equivocation"


@dataclass
class PhilosophicalArgument:
    """A philosophical argument structure"""
    argument_id: str
    argument_type: ArgumentType
    premises: List[str]
    conclusion: str
    supporting_evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    validity: Optional[bool] = None
    soundness: Optional[bool] = None


@dataclass
class ReasoningChain:
    """A chain of philosophical reasoning"""
    steps: List[Dict[str, Any]]
    initial_position: str
    final_position: str
    consistency_score: float = 1.0
    identified_issues: List[str] = field(default_factory=list)


@dataclass
class PhilosophicalDebugReport:
    """Debug report for philosophical reasoning"""
    timestamp: float
    reasoning_type: str
    arguments_analyzed: List[PhilosophicalArgument]
    logical_issues: List[Dict[str, Any]]
    consistency_analysis: Dict[str, Any]
    position_evolution: List[Tuple[float, PhilosophicalPosition]]
    recommendations: List[str]


class PhilosophicalDebugger:
    """
    Debugs and analyzes philosophical reasoning processes.
    """
    
    def __init__(self):
        self.argument_history = []
        self.position_history = []
        self.fallacy_detectors = self._initialize_fallacy_detectors()
        self.consistency_rules = self._initialize_consistency_rules()
        
    def _initialize_fallacy_detectors(self) -> Dict[LogicalFallacy, Any]:
        """Initialize fallacy detection patterns"""
        return {
            LogicalFallacy.CIRCULAR_REASONING: {
                "pattern": "conclusion_in_premise",
                "indicators": ["because", "therefore", "thus"],
                "check_function": self._check_circular_reasoning
            },
            LogicalFallacy.FALSE_DILEMMA: {
                "pattern": "only_two_options",
                "indicators": ["either", "or", "only"],
                "check_function": self._check_false_dilemma
            },
            LogicalFallacy.HASTY_GENERALIZATION: {
                "pattern": "insufficient_evidence",
                "indicators": ["all", "every", "never", "always"],
                "check_function": self._check_hasty_generalization
            },
            LogicalFallacy.NON_SEQUITUR: {
                "pattern": "unconnected_conclusion",
                "indicators": ["therefore", "thus", "hence"],
                "check_function": self._check_non_sequitur
            }
        }
    
    def _initialize_consistency_rules(self) -> List[Dict[str, Any]]:
        """Initialize philosophical consistency rules"""
        return [
            {
                "name": "non_contradiction",
                "description": "A proposition cannot be both true and false",
                "check": self._check_non_contradiction
            },
            {
                "name": "position_coherence",
                "description": "Philosophical positions should be internally coherent",
                "check": self._check_position_coherence
            },
            {
                "name": "assumption_consistency",
                "description": "Assumptions should remain consistent throughout reasoning",
                "check": self._check_assumption_consistency
            }
        ]
    
    def debug_philosophical_argument(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Debug a single philosophical argument"""
        debug_info = {
            "argument_id": argument.argument_id,
            "timestamp": time.time(),
            "validity_analysis": self._analyze_validity(argument),
            "soundness_analysis": self._analyze_soundness(argument),
            "fallacy_check": self._check_for_fallacies(argument),
            "assumption_analysis": self._analyze_assumptions(argument),
            "strength_assessment": self._assess_argument_strength(argument)
        }
        
        # Store in history
        self.argument_history.append((time.time(), argument, debug_info))
        
        return debug_info
    
    def debug_reasoning_chain(self, chain: ReasoningChain) -> PhilosophicalDebugReport:
        """Debug an entire reasoning chain"""
        arguments_analyzed = []
        logical_issues = []
        
        # Analyze each step
        for i, step in enumerate(chain.steps):
            if "argument" in step:
                arg = step["argument"]
                debug_info = self.debug_philosophical_argument(arg)
                arguments_analyzed.append(arg)
                
                # Collect issues
                if debug_info["fallacy_check"]["fallacies_found"]:
                    logical_issues.append({
                        "step": i,
                        "type": "fallacy",
                        "details": debug_info["fallacy_check"]
                    })
        
        # Check consistency across chain
        consistency_analysis = self._analyze_chain_consistency(chain)
        
        # Track position evolution
        position_evolution = self._extract_position_evolution(chain)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            logical_issues, 
            consistency_analysis,
            arguments_analyzed
        )
        
        return PhilosophicalDebugReport(
            timestamp=time.time(),
            reasoning_type=chain.steps[0].get("type", "unknown") if chain.steps else "empty",
            arguments_analyzed=arguments_analyzed,
            logical_issues=logical_issues,
            consistency_analysis=consistency_analysis,
            position_evolution=position_evolution,
            recommendations=recommendations
        )
    
    def check_philosophical_consistency(self, 
                                      position: PhilosophicalPosition,
                                      beliefs: List[str]) -> Dict[str, Any]:
        """Check if beliefs are consistent with philosophical position"""
        consistency_report = {
            "position": position.value,
            "consistent_beliefs": [],
            "inconsistent_beliefs": [],
            "tension_points": [],
            "overall_consistency": 1.0
        }
        
        # Check each belief against position
        for belief in beliefs:
            consistency = self._check_belief_position_consistency(belief, position)
            
            if consistency["is_consistent"]:
                consistency_report["consistent_beliefs"].append(belief)
            else:
                consistency_report["inconsistent_beliefs"].append({
                    "belief": belief,
                    "reason": consistency["reason"]
                })
                consistency_report["overall_consistency"] *= 0.8
        
        # Identify tension points
        consistency_report["tension_points"] = self._identify_tension_points(
            position, beliefs
        )
        
        return consistency_report
    
    def trace_philosophical_evolution(self, 
                                    arguments: List[PhilosophicalArgument]) -> Dict[str, Any]:
        """Trace evolution of philosophical thinking"""
        evolution = {
            "stages": [],
            "key_transitions": [],
            "conceptual_development": [],
            "consistency_trajectory": []
        }
        
        current_concepts = set()
        previous_position = None
        
        for i, argument in enumerate(arguments):
            # Extract concepts
            concepts = self._extract_concepts(argument)
            new_concepts = concepts - current_concepts
            current_concepts.update(concepts)
            
            # Identify position
            position = self._infer_philosophical_position(argument)
            
            # Record stage
            stage = {
                "index": i,
                "argument": argument.argument_id,
                "position": position,
                "new_concepts": list(new_concepts),
                "complexity": self._calculate_argument_complexity(argument)
            }
            evolution["stages"].append(stage)
            
            # Check for transitions
            if previous_position and position != previous_position:
                evolution["key_transitions"].append({
                    "from": previous_position,
                    "to": position,
                    "at_stage": i,
                    "trigger": argument.conclusion
                })
            
            previous_position = position
            
            # Track consistency
            if i > 0:
                consistency = self._calculate_consistency_with_previous(
                    argument, arguments[i-1]
                )
                evolution["consistency_trajectory"].append(consistency)
        
        # Analyze conceptual development
        evolution["conceptual_development"] = self._analyze_conceptual_development(
            evolution["stages"]
        )
        
        return evolution
    
    def validate_philosophical_method(self, 
                                    method_name: str,
                                    method_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a philosophical reasoning method"""
        validation = {
            "method": method_name,
            "is_valid": True,
            "issues": [],
            "strengths": [],
            "suggestions": []
        }
        
        # Check method structure
        structure_check = self._check_method_structure(method_name, method_steps)
        if not structure_check["is_valid"]:
            validation["is_valid"] = False
            validation["issues"].extend(structure_check["issues"])
        
        # Check logical flow
        flow_check = self._check_logical_flow(method_steps)
        validation["issues"].extend(flow_check["issues"])
        validation["strengths"].extend(flow_check["strengths"])
        
        # Generate suggestions
        validation["suggestions"] = self._generate_method_suggestions(
            method_name, 
            validation["issues"]
        )
        
        return validation
    
    def generate_argument_visualization(self, 
                                      argument: PhilosophicalArgument) -> str:
        """Generate visual representation of argument structure"""
        lines = ["```mermaid", "graph TD"]
        
        # Add premises
        for i, premise in enumerate(argument.premises):
            premise_id = f"P{i+1}"
            lines.append(f'    {premise_id}["{premise}"]')
        
        # Add assumptions if any
        for i, assumption in enumerate(argument.assumptions):
            assumption_id = f"A{i+1}"
            lines.append(f'    {assumption_id}("{assumption}")')
            lines.append(f'    {assumption_id} -.-> C')
        
        # Add conclusion
        lines.append(f'    C["{argument.conclusion}"]')
        
        # Connect premises to conclusion
        for i in range(len(argument.premises)):
            lines.append(f'    P{i+1} --> C')
        
        # Add validity/soundness indicators
        if argument.validity is not None:
            validity_text = "Valid" if argument.validity else "Invalid"
            lines.append(f'    V{{{validity_text}}}')
        
        lines.append("```")
        
        return "\n".join(lines)
    
    # Private analysis methods
    
    def _analyze_validity(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Analyze logical validity of argument"""
        if argument.argument_type == ArgumentType.DEDUCTIVE:
            # Check if conclusion follows necessarily from premises
            follows = self._check_deductive_validity(
                argument.premises, 
                argument.conclusion
            )
            return {
                "is_valid": follows,
                "explanation": "Conclusion follows necessarily" if follows 
                             else "Conclusion doesn't follow necessarily"
            }
        elif argument.argument_type == ArgumentType.INDUCTIVE:
            # Check probabilistic support
            support = self._calculate_inductive_support(
                argument.premises,
                argument.conclusion
            )
            return {
                "is_valid": support > 0.7,
                "support_level": support,
                "explanation": f"Inductive support: {support:.2f}"
            }
        elif argument.argument_type == ArgumentType.ABDUCTIVE:
            return self._analyze_abductive_validity(argument)
        elif argument.argument_type == ArgumentType.ANALOGICAL:
            return self._analyze_analogical_validity(argument)
        elif argument.argument_type == ArgumentType.TRANSCENDENTAL:
            # Heuristic check for transcendental reasoning. We look for
            # language suggesting necessary preconditions or a priori
            # assumptions in the premises or conclusion.
            keywords = {"necessary", "precondition", "a priori", "condition"}
            text = " ".join(argument.premises + [argument.conclusion]).lower()
            contains = any(kw in text for kw in keywords)
            explanation = (
                "References to necessary preconditions detected"
                if contains
                else "No obvious transcendental markers found"
            )
            return {"is_valid": contains, "explanation": explanation}
        else:
            return {
                "is_valid": False,
                "explanation": f"Unsupported argument type: {argument.argument_type.value}",
            }
    
    def _analyze_soundness(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Analyze soundness (validity + true premises)"""
        validity = self._analyze_validity(argument)
        
        if not validity.get("is_valid", False):
            return {
                "is_sound": False,
                "reason": "Argument is not valid"
            }
        
        # Check premise truth (simplified)
        premise_evaluation = self._evaluate_premises(argument.premises)
        
        return {
            "is_sound": premise_evaluation["all_true"],
            "premise_evaluation": premise_evaluation,
            "confidence": premise_evaluation["confidence"]
        }
    
    def _check_for_fallacies(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Check for logical fallacies"""
        fallacies_found = []
        
        for fallacy, detector in self.fallacy_detectors.items():
            check_result = detector["check_function"](argument)
            if check_result["detected"]:
                fallacies_found.append({
                    "fallacy": fallacy.value,
                    "confidence": check_result["confidence"],
                    "explanation": check_result["explanation"]
                })
        
        return {
            "fallacies_found": fallacies_found,
            "clean": len(fallacies_found) == 0
        }
    
    def _analyze_assumptions(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Analyze assumptions in argument"""
        return {
            "explicit_assumptions": argument.assumptions,
            "implicit_assumptions": self._identify_implicit_assumptions(argument),
            "assumption_strength": self._evaluate_assumption_strength(argument.assumptions),
            "hidden_premises": self._find_hidden_premises(argument)
        }
    
    def _assess_argument_strength(self, argument: PhilosophicalArgument) -> Dict[str, float]:
        """Assess overall argument strength"""
        validity_score = 1.0 if self._analyze_validity(argument).get("is_valid", False) else 0.5
        
        # Evidence quality
        evidence_score = min(1.0, len(argument.supporting_evidence) * 0.2)
        
        # Premise plausibility
        premise_score = self._evaluate_premises(argument.premises)["confidence"]
        
        # Assumption reasonableness
        assumption_score = 1.0 - (len(argument.assumptions) * 0.1)  # Fewer assumptions = stronger
        
        return {
            "overall_strength": (validity_score + evidence_score + premise_score + assumption_score) / 4,
            "validity_score": validity_score,
            "evidence_score": evidence_score,
            "premise_score": premise_score,
            "assumption_score": assumption_score
        }
    
    def _check_circular_reasoning(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Check for circular reasoning"""
        # Check if conclusion appears in premises
        conclusion_terms = set(argument.conclusion.lower().split())
        
        for premise in argument.premises:
            premise_terms = set(premise.lower().split())
            overlap = conclusion_terms & premise_terms
            
            if len(overlap) > len(conclusion_terms) * 0.7:
                return {
                    "detected": True,
                    "confidence": 0.8,
                    "explanation": f"Conclusion appears to be restated in premise: {premise}"
                }
        
        return {"detected": False, "confidence": 0.0, "explanation": ""}
    
    def _check_false_dilemma(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Check for false dilemma"""
        # Look for "either/or" constructions
        for premise in argument.premises:
            if "either" in premise.lower() and "or" in premise.lower():
                # Check if there might be other options
                if not any(word in premise.lower() for word in ["only", "must", "necessarily"]):
                    return {
                        "detected": True,
                        "confidence": 0.7,
                        "explanation": "Presents limited options without justification"
                    }
        
        return {"detected": False, "confidence": 0.0, "explanation": ""}
    
    def _check_hasty_generalization(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Check for hasty generalization"""
        universal_terms = ["all", "every", "never", "always", "none"]
        
        for premise in argument.premises:
            if any(term in premise.lower() for term in universal_terms):
                # Check if sufficient evidence provided
                if len(argument.supporting_evidence) < 3:
                    return {
                        "detected": True,
                        "confidence": 0.7,
                        "explanation": "Universal claim with insufficient evidence"
                    }
        
        return {"detected": False, "confidence": 0.0, "explanation": ""}
    
    def _check_non_sequitur(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Check for non sequitur"""
        # Simple check: do premise topics relate to conclusion?
        premise_topics = set()
        for premise in argument.premises:
            premise_topics.update(self._extract_key_terms(premise))
        
        conclusion_topics = set(self._extract_key_terms(argument.conclusion))
        
        overlap = premise_topics & conclusion_topics
        if len(overlap) < 1:
            return {
                "detected": True,
                "confidence": 0.6,
                "explanation": "Conclusion appears unrelated to premises"
            }
        
        return {"detected": False, "confidence": 0.0, "explanation": ""}
    
    def _analyze_chain_consistency(self, chain: ReasoningChain) -> Dict[str, Any]:
        """Analyze consistency across reasoning chain"""
        consistency_checks = []
        
        for rule in self.consistency_rules:
            check_result = rule["check"](chain)
            consistency_checks.append({
                "rule": rule["name"],
                "description": rule["description"],
                "passed": check_result["passed"],
                "details": check_result.get("details", "")
            })
        
        overall_consistency = sum(1 for c in consistency_checks if c["passed"]) / len(consistency_checks)
        
        return {
            "checks": consistency_checks,
            "overall_consistency": overall_consistency,
            "major_inconsistencies": [c for c in consistency_checks if not c["passed"]]
        }
    
    def _check_non_contradiction(self, chain: ReasoningChain) -> Dict[str, Any]:
        """Check for contradictions in reasoning chain"""
        propositions = []
        
        for step in chain.steps:
            if "proposition" in step:
                propositions.append(step["proposition"])
        
        # Check for direct contradictions
        for i, prop1 in enumerate(propositions):
            for prop2 in propositions[i+1:]:
                if self._are_contradictory(prop1, prop2):
                    return {
                        "passed": False,
                        "details": f"Contradiction found: '{prop1}' vs '{prop2}'"
                    }
        
        return {"passed": True}
    
    def _check_position_coherence(self, chain: ReasoningChain) -> Dict[str, Any]:
        """Check if positions remain coherent"""
        if chain.initial_position == chain.final_position:
            return {"passed": True}
        
        # Check if transition is justified
        transition_justified = any(
            "position_change" in step and step.get("justified", False)
            for step in chain.steps
        )
        
        return {
            "passed": transition_justified,
            "details": "Position change without justification" if not transition_justified else ""
        }
    
    def _check_assumption_consistency(self, chain: ReasoningChain) -> Dict[str, Any]:
        """Check if assumptions remain consistent"""
        all_assumptions = []
        
        for step in chain.steps:
            if "assumptions" in step:
                all_assumptions.extend(step["assumptions"])
        
        # Check for conflicting assumptions
        for i, assumption1 in enumerate(all_assumptions):
            for assumption2 in all_assumptions[i+1:]:
                if self._are_conflicting_assumptions(assumption1, assumption2):
                    return {
                        "passed": False,
                        "details": f"Conflicting assumptions: '{assumption1}' vs '{assumption2}'"
                    }
        
        return {"passed": True}
    
    def _extract_position_evolution(self, chain: ReasoningChain) -> List[Tuple[float, PhilosophicalPosition]]:
        """Extract evolution of philosophical positions"""
        evolution = []
        
        for i, step in enumerate(chain.steps):
            if "position" in step:
                try:
                    position = PhilosophicalPosition(step["position"])
                    evolution.append((i / len(chain.steps), position))
                except ValueError:
                    pass
        
        return evolution
    
    def _generate_recommendations(self, issues: List[Dict[str, Any]], 
                                consistency: Dict[str, Any],
                                arguments: List[PhilosophicalArgument]) -> List[str]:
        """Generate recommendations for improving reasoning"""
        recommendations = []
        
        # Address fallacies
        fallacy_types = set()
        for issue in issues:
            if issue["type"] == "fallacy":
                fallacy_types.update(
                    f["fallacy"] for f in issue["details"]["fallacies_found"]
                )
        
        if LogicalFallacy.CIRCULAR_REASONING.value in fallacy_types:
            recommendations.append(
                "Avoid circular reasoning by ensuring conclusions don't appear in premises"
            )
        
        # Address consistency
        if consistency["overall_consistency"] < 0.8:
            recommendations.append(
                "Improve consistency by maintaining stable assumptions throughout reasoning"
            )
        
        # Address argument strength
        weak_arguments = [a for a in arguments 
                         if self._assess_argument_strength(a)["overall_strength"] < 0.6]
        if weak_arguments:
            recommendations.append(
                "Strengthen arguments by providing more evidence and reducing assumptions"
            )
        
        return recommendations
    
    def _check_belief_position_consistency(self, belief: str, 
                                         position: PhilosophicalPosition) -> Dict[str, Any]:
        """Check if belief is consistent with philosophical position"""
        # Simplified consistency checking
        position_implications = {
            PhilosophicalPosition.PHYSICALISM: ["material", "physical", "brain"],
            PhilosophicalPosition.DUALISM: ["mind", "soul", "separate"],
            PhilosophicalPosition.FUNCTIONALISM: ["function", "process", "computation"]
        }
        
        keywords = position_implications.get(position, [])
        
        # Check if belief aligns with position keywords
        belief_lower = belief.lower()
        alignment = any(keyword in belief_lower for keyword in keywords)
        
        return {
            "is_consistent": alignment,
            "reason": "Aligns with position" if alignment else "May conflict with position"
        }
    
    def _identify_tension_points(self, position: PhilosophicalPosition,
                               beliefs: List[str]) -> List[str]:
        """Identify points of tension in philosophical position"""
        tensions = []
        
        # Check for common tensions
        if position == PhilosophicalPosition.PHYSICALISM:
            if any("consciousness" in b.lower() or "qualia" in b.lower() for b in beliefs):
                tensions.append("Explaining consciousness in purely physical terms")
        elif position == PhilosophicalPosition.DUALISM:
            if any("interact" in b.lower() for b in beliefs):
                tensions.append("Explaining mind-body interaction")
        
        return tensions
    
    def _extract_concepts(self, argument: PhilosophicalArgument) -> Set[str]:
        """Extract philosophical concepts from argument"""
        concepts = set()
        
        # Extract from premises and conclusion
        all_text = " ".join(argument.premises + [argument.conclusion])
        
        # Simple concept extraction (would be more sophisticated)
        philosophical_terms = [
            "consciousness", "mind", "reality", "existence", "knowledge",
            "truth", "being", "essence", "substance", "property"
        ]
        
        for term in philosophical_terms:
            if term in all_text.lower():
                concepts.add(term)
        
        return concepts
    
    def _infer_philosophical_position(self, argument: PhilosophicalArgument) -> str:
        """Infer philosophical position from argument"""
        # Simplified inference based on key terms
        conclusion_lower = argument.conclusion.lower()
        
        if "physical" in conclusion_lower or "brain" in conclusion_lower:
            return PhilosophicalPosition.PHYSICALISM.value
        elif "mind" in conclusion_lower and "separate" in conclusion_lower:
            return PhilosophicalPosition.DUALISM.value
        elif "function" in conclusion_lower:
            return PhilosophicalPosition.FUNCTIONALISM.value
        else:
            return "undetermined"
    
    def _calculate_argument_complexity(self, argument: PhilosophicalArgument) -> float:
        """Calculate complexity of philosophical argument"""
        # Factors: number of premises, assumptions, conceptual depth
        premise_complexity = len(argument.premises) * 0.2
        assumption_complexity = len(argument.assumptions) * 0.3
        concept_complexity = len(self._extract_concepts(argument)) * 0.1
        
        return min(1.0, premise_complexity + assumption_complexity + concept_complexity)
    
    def _calculate_consistency_with_previous(self, current: PhilosophicalArgument,
                                           previous: PhilosophicalArgument) -> float:
        """Calculate consistency between consecutive arguments"""
        # Check if conclusions align
        if self._are_contradictory(current.conclusion, previous.conclusion):
            return 0.0
        
        # Check assumption overlap
        shared_assumptions = set(current.assumptions) & set(previous.assumptions)
        assumption_consistency = len(shared_assumptions) / max(
            len(current.assumptions), 
            len(previous.assumptions), 
            1
        )
        
        return assumption_consistency
    
    def _analyze_conceptual_development(self, stages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how concepts develop over stages"""
        concept_timeline = []
        concept_complexity = []
        
        for stage in stages:
            concept_timeline.append({
                "stage": stage["index"],
                "new_concepts": stage["new_concepts"],
                "total_concepts": len(stage["new_concepts"])
            })
            concept_complexity.append(stage["complexity"])
        
        return {
            "timeline": concept_timeline,
            "complexity_trend": "increasing" if concept_complexity[-1] > concept_complexity[0] else "stable",
            "total_concepts_introduced": sum(ct["total_concepts"] for ct in concept_timeline)
        }
    
    def _check_method_structure(self, method_name: str, 
                              steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check if philosophical method has proper structure"""
        required_elements = {
            "dialectical": ["thesis", "antithesis", "synthesis"],
            "phenomenological": ["bracketing", "description", "essence"],
            "analytical": ["definition", "analysis", "conclusion"]
        }
        
        if method_name in required_elements:
            required = required_elements[method_name]
            found = [step.get("type", "") for step in steps]
            
            missing = [elem for elem in required if elem not in found]
            
            return {
                "is_valid": len(missing) == 0,
                "issues": [f"Missing {elem}" for elem in missing]
            }
        
        return {"is_valid": True, "issues": []}
    
    def _check_logical_flow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check logical flow between steps"""
        issues = []
        strengths = []
        
        for i in range(1, len(steps)):
            prev_output = steps[i-1].get("output", "")
            curr_input = steps[i].get("input", "")
            
            # Check connection
            if prev_output and curr_input and prev_output != curr_input:
                issues.append(f"Disconnect between step {i-1} and {i}")
            else:
                strengths.append(f"Good flow from step {i-1} to {i}")
        
        return {"issues": issues, "strengths": strengths}
    
    def _generate_method_suggestions(self, method_name: str, 
                                   issues: List[str]) -> List[str]:
        """Generate suggestions for improving method"""
        suggestions = []
        
        if any("Missing" in issue for issue in issues):
            suggestions.append("Ensure all required method steps are included")
        
        if any("Disconnect" in issue for issue in issues):
            suggestions.append("Improve logical flow by clearly connecting step outputs to inputs")
        
        # Method-specific suggestions
        if method_name == "dialectical":
            suggestions.append("Ensure synthesis genuinely resolves thesis-antithesis tension")
        
        return suggestions
    
    def _check_deductive_validity(self, premises: List[str], conclusion: str) -> bool:
        """Check deductive validity (simplified)"""
        # Very simplified - would need proper logical analysis
        premise_terms = set()
        for premise in premises:
            premise_terms.update(self._extract_key_terms(premise))
        
        conclusion_terms = set(self._extract_key_terms(conclusion))
        
        # Check if conclusion terms are covered by premises
        return conclusion_terms.issubset(premise_terms)
    
    def _calculate_inductive_support(self, premises: List[str], conclusion: str) -> float:
        """Calculate inductive support level"""
        # Simplified calculation based on evidence quantity and relevance
        evidence_count = len(premises)
        
        # Check relevance
        relevance_scores = []
        conclusion_terms = set(self._extract_key_terms(conclusion))
        
        for premise in premises:
            premise_terms = set(self._extract_key_terms(premise))
            overlap = len(premise_terms & conclusion_terms)
            relevance = overlap / max(len(conclusion_terms), 1)
            relevance_scores.append(relevance)
        
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
        
        # Combine evidence count and relevance
        support = min(1.0, (evidence_count * 0.2) * avg_relevance)

        return support

    def _analyze_abductive_validity(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Analyze abductive reasoning plausibility"""
        observation_keywords = {"observe", "observation", "phenomenon", "evidence", "data"}
        explanation_keywords = {"explain", "cause", "account", "best"}

        has_observation = any(
            any(word in premise.lower() for word in observation_keywords)
            for premise in argument.premises
        )
        has_explanation = any(word in argument.conclusion.lower() for word in explanation_keywords)

        score = 0.4
        if has_observation:
            score += 0.3
        if has_explanation:
            score += 0.3

        return {
            "is_valid": score > 0.6,
            "explanation_score": score,
            "explanation": f"Abductive plausibility {score:.2f}"
        }

    def _analyze_analogical_validity(self, argument: PhilosophicalArgument) -> Dict[str, Any]:
        """Analyze analogical reasoning strength"""
        mapping_keywords = {"like", "similar", "analogous", "just as"}
        mapping_count = sum(
            sum(word in premise.lower() for word in mapping_keywords)
            for premise in argument.premises
        )
        mapping_count += sum(word in argument.conclusion.lower() for word in mapping_keywords)

        strength = min(1.0, 0.3 + mapping_count * 0.2)

        return {
            "is_valid": strength > 0.5,
            "mapping_strength": strength,
            "explanation": f"Analogical mapping strength: {strength:.2f}"
        }
    
    def _evaluate_premises(self, premises: List[str]) -> Dict[str, Any]:
        """Evaluate truth of premises (simplified)"""
        # This would need domain knowledge in reality
        # For now, use heuristics
        
        plausibility_scores = []
        for premise in premises:
            score = self._evaluate_premise_plausibility(premise)
            plausibility_scores.append(score)
        
        avg_plausibility = sum(plausibility_scores) / len(plausibility_scores) if plausibility_scores else 0
        
        return {
            "all_true": all(s > 0.7 for s in plausibility_scores),
            "confidence": avg_plausibility,
            "individual_scores": plausibility_scores
        }
    
    def _evaluate_premise_plausibility(self, premise: str) -> float:
        """Evaluate plausibility of single premise"""
        # Simplified heuristics
        premise_lower = premise.lower()
        
        # Check for extreme claims
        if any(word in premise_lower for word in ["all", "never", "always", "impossible"]):
            return 0.5  # Extreme claims less plausible
        
        # Check for qualified claims
        if any(word in premise_lower for word in ["some", "often", "usually", "tends"]):
            return 0.8  # Qualified claims more plausible
        
        return 0.7  # Default moderate plausibility
    
    def _identify_implicit_assumptions(self, argument: PhilosophicalArgument) -> List[str]:
        """Identify implicit assumptions in argument"""
        implicit = []
        
        # Check for common implicit assumptions
        if "consciousness" in argument.conclusion.lower():
            implicit.append("Consciousness is a meaningful concept")
        
        if "free will" in argument.conclusion.lower():
            implicit.append("Actions can be freely chosen")
        
        if "moral" in argument.conclusion.lower() or "ethical" in argument.conclusion.lower():
            implicit.append("Moral facts or values exist")
        
        return implicit
    
    def _evaluate_assumption_strength(self, assumptions: List[str]) -> float:
        """Evaluate strength of assumptions"""
        if not assumptions:
            return 1.0  # No assumptions = strong
        
        # More assumptions = weaker argument
        return max(0.3, 1.0 - (len(assumptions) * 0.15))
    
    def _find_hidden_premises(self, argument: PhilosophicalArgument) -> List[str]:
        """Find hidden/unstated premises"""
        hidden = []
        
        # Check for logical gaps
        premise_concepts = set()
        for premise in argument.premises:
            premise_concepts.update(self._extract_key_terms(premise))
        
        conclusion_concepts = set(self._extract_key_terms(argument.conclusion))
        
        # Concepts in conclusion but not premises might indicate hidden premises
        missing_concepts = conclusion_concepts - premise_concepts
        
        for concept in missing_concepts:
            hidden.append(f"Assumes connection to {concept}")
        
        return hidden
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        # Remove common words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", 
                     "being", "have", "has", "had", "do", "does", "did", "will", 
                     "would", "could", "should", "may", "might", "must", "can", 
                     "this", "that", "these", "those", "i", "you", "he", "she", 
                     "it", "we", "they", "what", "which", "who", "when", "where", 
                     "why", "how", "all", "each", "every", "some", "any", "if", 
                     "because", "as", "until", "while", "of", "at", "by", "for", 
                     "with", "about", "against", "between", "into", "through", 
                     "during", "before", "after", "above", "below", "to", "from", 
                     "up", "down", "in", "out", "on", "off", "over", "under", 
                     "again", "further", "then", "once"}
        
        words = text.lower().split()
        key_terms = [w.strip('.,!?;:') for w in words if w not in stop_words and len(w) > 2]
        
        return key_terms
    
    def _are_contradictory(self, prop1: str, prop2: str) -> bool:
        """Check if two propositions are contradictory"""
        # Simplified check
        prop1_lower = prop1.lower()
        prop2_lower = prop2.lower()
        
        # Check for explicit negation
        if "not" in prop1_lower and prop1_lower.replace("not ", "") == prop2_lower:
            return True
        if "not" in prop2_lower and prop2_lower.replace("not ", "") == prop1_lower:
            return True
        
        # Check for opposite terms
        opposites = [
            ("true", "false"),
            ("exist", "not exist"),
            ("possible", "impossible"),
            ("necessary", "contingent"),
            ("physical", "non-physical"),
            ("material", "immaterial")
        ]
        
        for opp1, opp2 in opposites:
            if opp1 in prop1_lower and opp2 in prop2_lower:
                return True
            if opp2 in prop1_lower and opp1 in prop2_lower:
                return True
        
        return False
    
    def _are_conflicting_assumptions(self, assumption1: str, assumption2: str) -> bool:
        """Check if two assumptions conflict"""
        # Use same logic as contradiction check
        return self._are_contradictory(assumption1, assumption2)
