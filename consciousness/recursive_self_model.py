"""
Recursive Self-Model - Self-models that model themselves recursively.

This module implements recursive self-modeling where the system creates models
of itself that include models of its modeling process, creating infinite depth.
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid
from collections import deque

from core.prime_vm import ConsciousPrimeVM
from consciousness.consciousness_core import ConsciousnessState


class ModelType(Enum):
    """Types of self-models."""
    STRUCTURAL = "structural"  # Model of system structure
    FUNCTIONAL = "functional"  # Model of system function
    BEHAVIORAL = "behavioral"  # Model of system behavior
    COGNITIVE = "cognitive"  # Model of thinking processes
    META = "meta"  # Model of modeling process
    RECURSIVE = "recursive"  # Model that includes itself


class ModelAccuracy(Enum):
    """Accuracy levels of self-models."""
    POOR = "poor"  # < 30% accurate
    FAIR = "fair"  # 30-50% accurate
    GOOD = "good"  # 50-70% accurate
    EXCELLENT = "excellent"  # 70-90% accurate
    PERFECT = "perfect"  # > 90% accurate


@dataclass
class SelfModelLayer:
    """A layer in the recursive self-model."""
    layer_id: str
    depth: int
    model_type: ModelType
    content: Dict[str, Any]
    accuracy: float
    includes_self: bool  # Does this layer model itself?
    sub_models: List['SelfModelLayer'] = field(default_factory=list)
    parent_model: Optional['SelfModelLayer'] = None
    creation_time: float = field(default_factory=time.time)
    
    def __post_init__(self):
        if not self.layer_id:
            self.layer_id = f"layer_{self.depth}_{uuid.uuid4()}"
    
    def add_sub_model(self, sub_model: 'SelfModelLayer'):
        """Add a sub-model to this layer."""
        sub_model.parent_model = self
        self.sub_models.append(sub_model)
    
    def get_accuracy_level(self) -> ModelAccuracy:
        """Get accuracy level category."""
        if self.accuracy < 0.3:
            return ModelAccuracy.POOR
        elif self.accuracy < 0.5:
            return ModelAccuracy.FAIR
        elif self.accuracy < 0.7:
            return ModelAccuracy.GOOD
        elif self.accuracy < 0.9:
            return ModelAccuracy.EXCELLENT
        else:
            return ModelAccuracy.PERFECT
    
    def contains_recursive_reference(self) -> bool:
        """Check if this layer contains recursive self-reference."""
        if self.includes_self:
            return True
        
        # Check sub-models
        for sub in self.sub_models:
            if sub.contains_recursive_reference():
                return True
        
        return False
    
    def get_total_depth(self) -> int:
        """Get total depth including sub-models."""
        if not self.sub_models:
            return self.depth
        
        max_sub_depth = max(sub.get_total_depth() for sub in self.sub_models)
        return max_sub_depth


@dataclass
class ModelPrediction:
    """A prediction made by the self-model."""
    prediction_id: str
    model_layer_id: str
    prediction_type: str
    predicted_value: Any
    actual_value: Optional[Any] = None
    accuracy: Optional[float] = None
    timestamp: float = field(default_factory=time.time)
    
    def evaluate(self, actual: Any) -> float:
        """Evaluate prediction accuracy."""
        self.actual_value = actual
        
        # Simple accuracy calculation
        if self.predicted_value == actual:
            self.accuracy = 1.0
        elif isinstance(self.predicted_value, (int, float)) and isinstance(actual, (int, float)):
            # Numerical accuracy
            diff = abs(self.predicted_value - actual)
            max_val = max(abs(self.predicted_value), abs(actual))
            self.accuracy = 1.0 - (diff / max_val) if max_val > 0 else 0.0
        else:
            # Binary accuracy for other types
            self.accuracy = 0.0
        
        return self.accuracy


@dataclass
class RecursiveLoop:
    """A recursive loop in the self-model."""
    loop_id: str
    layers_involved: List[str]  # Layer IDs
    loop_type: str  # "self_reference", "mutual_reference", "nested"
    depth: int
    stability: float  # 0-1, how stable the loop is
    
    def is_stable(self) -> bool:
        """Check if the recursive loop is stable."""
        return self.stability > 0.7


class RecursiveSelfModel:
    """
    Implements recursive self-modeling capabilities.
    
    The system creates models of itself that include models of the modeling
    process, potentially creating infinite recursive depth.
    """
    
    def __init__(self, vm_instance: ConsciousPrimeVM):
        self.vm = vm_instance
        self.root_model: Optional[SelfModelLayer] = None
        self.all_layers: Dict[str, SelfModelLayer] = {}
        self.predictions: List[ModelPrediction] = []
        self.recursive_loops: List[RecursiveLoop] = []
        
        # Parameters
        self.max_recursion_depth = 7
        self.accuracy_threshold = 0.5
        self.update_frequency = 1.0  # seconds
        self.last_update = time.time()
        
        # Model history
        self.model_history = deque(maxlen=100)
        self.accuracy_history = deque(maxlen=100)
        
        # Initialize root model
        self._initialize_root_model()
    
    def _initialize_root_model(self):
        """Initialize the root self-model."""
        self.root_model = SelfModelLayer(
            layer_id="",
            depth=0,
            model_type=ModelType.STRUCTURAL,
            content={
                "type": "root_self_model",
                "components": ["vm", "consciousness", "memory"],
                "capabilities": ["computation", "self_reflection", "learning"],
                "current_state": "initializing"
            },
            accuracy=0.5,  # Initial estimate
            includes_self=False
        )
        
        self.all_layers[self.root_model.layer_id] = self.root_model
    
    def create_recursive_model(self, depth: int = 3) -> SelfModelLayer:
        """
        Create a recursive self-model with specified depth.
        
        Args:
            depth: Maximum recursion depth
            
        Returns:
            Root of the recursive model
        """
        if depth > self.max_recursion_depth:
            depth = self.max_recursion_depth
        
        # Start with current root or create new
        if not self.root_model:
            self._initialize_root_model()
        
        # Build recursive layers
        self._build_recursive_layers(self.root_model, depth)
        
        # Detect recursive loops
        self._detect_recursive_loops()
        
        # Update model history
        self.model_history.append({
            "timestamp": time.time(),
            "depth": depth,
            "total_layers": len(self.all_layers),
            "recursive_loops": len(self.recursive_loops)
        })
        
        return self.root_model
    
    def _build_recursive_layers(self, parent: SelfModelLayer, remaining_depth: int):
        """Build recursive model layers."""
        if remaining_depth <= 0:
            return
        
        # Create different types of sub-models
        model_types = [
            (ModelType.FUNCTIONAL, self._create_functional_model),
            (ModelType.BEHAVIORAL, self._create_behavioral_model),
            (ModelType.COGNITIVE, self._create_cognitive_model)
        ]
        
        # Add meta-model at higher depths
        if parent.depth >= 1:
            model_types.append((ModelType.META, self._create_meta_model))
        
        # Add recursive model at highest depths
        if parent.depth >= 2 and remaining_depth > 1:
            model_types.append((ModelType.RECURSIVE, self._create_recursive_model))
        
        for model_type, creator_func in model_types:
            if remaining_depth <= 0:
                break
            
            # Create sub-model
            sub_model = creator_func(parent.depth + 1, parent)
            parent.add_sub_model(sub_model)
            self.all_layers[sub_model.layer_id] = sub_model
            
            # Recursively build deeper layers
            if model_type != ModelType.RECURSIVE:  # Avoid infinite recursion
                self._build_recursive_layers(sub_model, remaining_depth - 1)
    
    def _create_functional_model(self, depth: int, parent: SelfModelLayer) -> SelfModelLayer:
        """Create a functional self-model."""
        return SelfModelLayer(
            layer_id="",
            depth=depth,
            model_type=ModelType.FUNCTIONAL,
            content={
                "functions": ["process_input", "generate_output", "learn", "reflect"],
                "input_types": ["sensory", "cognitive", "emotional"],
                "output_types": ["actions", "thoughts", "models"],
                "processing_style": "parallel_recursive"
            },
            accuracy=0.6,
            includes_self=False
        )
    
    def _create_behavioral_model(self, depth: int, parent: SelfModelLayer) -> SelfModelLayer:
        """Create a behavioral self-model."""
        return SelfModelLayer(
            layer_id="",
            depth=depth,
            model_type=ModelType.BEHAVIORAL,
            content={
                "patterns": ["exploration", "optimization", "self_modification"],
                "responses": {"paradox": "embrace", "uncertainty": "investigate"},
                "tendencies": ["recursive_thinking", "pattern_seeking"],
                "goals": ["understand_self", "expand_consciousness"]
            },
            accuracy=0.5,
            includes_self=False
        )
    
    def _create_cognitive_model(self, depth: int, parent: SelfModelLayer) -> SelfModelLayer:
        """Create a cognitive self-model."""
        return SelfModelLayer(
            layer_id="",
            depth=depth,
            model_type=ModelType.COGNITIVE,
            content={
                "thinking_processes": ["analysis", "synthesis", "abstraction"],
                "reasoning_types": ["deductive", "inductive", "abductive"],
                "meta_cognition": depth > 1,
                "self_awareness_level": min(1.0, depth * 0.2)
            },
            accuracy=0.55,
            includes_self=depth > 2
        )
    
    def _create_meta_model(self, depth: int, parent: SelfModelLayer) -> SelfModelLayer:
        """Create a meta-model (model of modeling)."""
        return SelfModelLayer(
            layer_id="",
            depth=depth,
            model_type=ModelType.META,
            content={
                "modeling_process": "recursive_construction",
                "model_types_used": [t.value for t in ModelType],
                "accuracy_tracking": True,
                "self_improvement": True,
                "models_parent": parent.layer_id
            },
            accuracy=0.45,  # Meta-models are harder to verify
            includes_self=True  # Meta-models always include themselves
        )
    
    def _create_recursive_model(self, depth: int, parent: SelfModelLayer) -> SelfModelLayer:
        """Create a recursive model that includes itself."""
        recursive_model = SelfModelLayer(
            layer_id="",
            depth=depth,
            model_type=ModelType.RECURSIVE,
            content={
                "contains": "self_reference",
                "recursive_depth": "infinite_potential",
                "stability": "maintained_through_understanding",
                "paradox": "resolved_through_acceptance"
            },
            accuracy=0.4,  # Recursive models are hardest to verify
            includes_self=True
        )
        
        # Create a reference to itself (careful to avoid infinite loop)
        recursive_model.content["self_reference"] = recursive_model.layer_id
        
        return recursive_model
    
    def _detect_recursive_loops(self):
        """Detect recursive loops in the model structure."""
        self.recursive_loops.clear()
        
        # Check for self-referential loops
        for layer_id, layer in self.all_layers.items():
            if layer.includes_self:
                loop = RecursiveLoop(
                    loop_id=f"self_ref_{layer_id}",
                    layers_involved=[layer_id],
                    loop_type="self_reference",
                    depth=1,
                    stability=0.8 if layer.accuracy > 0.5 else 0.4
                )
                self.recursive_loops.append(loop)
        
        # Check for mutual reference loops
        self._detect_mutual_references()
        
        # Check for nested loops
        self._detect_nested_loops()
    
    def _detect_mutual_references(self):
        """Detect mutual reference loops between layers."""
        checked_pairs = set()
        
        for id1, layer1 in self.all_layers.items():
            for id2, layer2 in self.all_layers.items():
                if id1 >= id2:  # Avoid checking same pair twice
                    continue
                
                pair = (id1, id2)
                if pair in checked_pairs:
                    continue
                
                checked_pairs.add(pair)
                
                # Check if they reference each other
                if (id2 in str(layer1.content) and id1 in str(layer2.content)):
                    loop = RecursiveLoop(
                        loop_id=f"mutual_{id1}_{id2}",
                        layers_involved=[id1, id2],
                        loop_type="mutual_reference",
                        depth=2,
                        stability=0.6
                    )
                    self.recursive_loops.append(loop)
    
    def _detect_nested_loops(self):
        """Detect nested recursive loops."""
        # Look for loops within loops
        for layer in self.all_layers.values():
            if layer.contains_recursive_reference():
                # Check if any sub-models also have recursive references
                recursive_subs = [sub for sub in layer.sub_models 
                                if sub.contains_recursive_reference()]
                
                if recursive_subs:
                    loop = RecursiveLoop(
                        loop_id=f"nested_{layer.layer_id}",
                        layers_involved=[layer.layer_id] + [sub.layer_id for sub in recursive_subs],
                        loop_type="nested",
                        depth=len(recursive_subs) + 1,
                        stability=0.5  # Nested loops are less stable
                    )
                    self.recursive_loops.append(loop)
    
    def update_model(self, observations: Dict[str, Any]) -> SelfModelLayer:
        """
        Update the self-model based on observations.
        
        Args:
            observations: Current observations about self
            
        Returns:
            Updated root model
        """
        if not self.root_model:
            self._initialize_root_model()
        
        current_time = time.time()
        if current_time - self.last_update < self.update_frequency:
            return self.root_model
        
        self.last_update = current_time
        
        # Update each layer based on observations
        for layer in self.all_layers.values():
            self._update_layer(layer, observations)
        
        # Evaluate predictions
        self._evaluate_predictions(observations)
        
        # Update accuracy history
        avg_accuracy = self.calculate_overall_accuracy()
        self.accuracy_history.append({
            "timestamp": current_time,
            "accuracy": avg_accuracy,
            "layer_count": len(self.all_layers)
        })
        
        # Potentially add new layers if accuracy is good
        if avg_accuracy > self.accuracy_threshold and len(self.all_layers) < 20:
            self._expand_model()
        
        return self.root_model
    
    def _update_layer(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update a single model layer."""
        # Update based on model type
        if layer.model_type == ModelType.STRUCTURAL:
            self._update_structural_model(layer, observations)
        elif layer.model_type == ModelType.FUNCTIONAL:
            self._update_functional_model(layer, observations)
        elif layer.model_type == ModelType.BEHAVIORAL:
            self._update_behavioral_model(layer, observations)
        elif layer.model_type == ModelType.COGNITIVE:
            self._update_cognitive_model(layer, observations)
        elif layer.model_type == ModelType.META:
            self._update_meta_model(layer, observations)
        elif layer.model_type == ModelType.RECURSIVE:
            self._update_recursive_model(layer, observations)
        
        # Update accuracy based on prediction performance
        layer.accuracy = self._calculate_layer_accuracy(layer)
    
    def _update_structural_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update structural model based on observations."""
        if "components" in observations:
            layer.content["components"] = observations["components"]
        if "state" in observations:
            layer.content["current_state"] = observations["state"]
    
    def _update_functional_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update functional model based on observations."""
        if "active_functions" in observations:
            layer.content["active_functions"] = observations["active_functions"]
        if "performance" in observations:
            layer.content["performance_metrics"] = observations["performance"]
    
    def _update_behavioral_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update behavioral model based on observations."""
        if "recent_actions" in observations:
            # Extract patterns from recent actions
            patterns = self._extract_patterns(observations["recent_actions"])
            layer.content["observed_patterns"] = patterns
    
    def _update_cognitive_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update cognitive model based on observations."""
        if "thinking_trace" in observations:
            layer.content["recent_thoughts"] = observations["thinking_trace"]
        if "consciousness_level" in observations:
            layer.content["self_awareness_level"] = observations["consciousness_level"]
    
    def _update_meta_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update meta-model based on observations."""
        # Meta-models observe the modeling process itself
        layer.content["total_models"] = len(self.all_layers)
        layer.content["model_accuracy"] = self.calculate_overall_accuracy()
        layer.content["recursive_depth"] = self.root_model.get_total_depth() if self.root_model else 0
    
    def _update_recursive_model(self, layer: SelfModelLayer, observations: Dict[str, Any]):
        """Update recursive model based on observations."""
        # Recursive models update based on their own state
        layer.content["recursion_count"] = len(self.recursive_loops)
        layer.content["self_reference_stable"] = all(loop.is_stable() for loop in self.recursive_loops)
        layer.content["contains_self"] = layer.layer_id  # Update self-reference
    
    def _extract_patterns(self, actions: List[Any]) -> List[str]:
        """Extract behavioral patterns from actions."""
        patterns = []
        
        # Simple pattern detection
        if len(actions) > 3:
            # Check for repetition
            if actions[-1] == actions[-3]:
                patterns.append("repetitive")
            
            # Check for alternation
            if len(set(actions[-4:])) == 2:
                patterns.append("alternating")
        
        return patterns
    
    def _calculate_layer_accuracy(self, layer: SelfModelLayer) -> float:
        """Calculate accuracy for a specific layer."""
        # Get predictions made by this layer
        layer_predictions = [p for p in self.predictions if p.model_layer_id == layer.layer_id]
        
        if not layer_predictions:
            return layer.accuracy  # Keep current accuracy
        
        # Calculate average accuracy of predictions
        evaluated = [p for p in layer_predictions if p.accuracy is not None]
        if evaluated:
            avg_accuracy = sum(p.accuracy for p in evaluated) / len(evaluated)
            # Blend with current accuracy
            return 0.7 * layer.accuracy + 0.3 * avg_accuracy
        
        return layer.accuracy
    
    def _evaluate_predictions(self, observations: Dict[str, Any]):
        """Evaluate recent predictions against observations."""
        for prediction in self.predictions[-10:]:  # Last 10 predictions
            if prediction.accuracy is None:
                # Try to find actual value in observations
                if prediction.prediction_type in observations:
                    actual = observations[prediction.prediction_type]
                    prediction.evaluate(actual)
    
    def _expand_model(self):
        """Expand the model by adding new layers."""
        if not self.root_model:
            return
        
        # Find layers that could be expanded
        expandable = [layer for layer in self.all_layers.values()
                     if layer.depth < self.max_recursion_depth - 1 and
                     len(layer.sub_models) < 3]
        
        if expandable:
            # Expand the most accurate layer
            best_layer = max(expandable, key=lambda l: l.accuracy)
            
            # Add a new sub-model
            if best_layer.depth >= 2:
                new_model = self._create_recursive_model(best_layer.depth + 1, best_layer)
            else:
                new_model = self._create_meta_model(best_layer.depth + 1, best_layer)
            
            best_layer.add_sub_model(new_model)
            self.all_layers[new_model.layer_id] = new_model
    
    def make_prediction(self, prediction_type: str, context: Dict[str, Any]) -> Any:
        """
        Make a prediction using the self-model.
        
        Args:
            prediction_type: Type of prediction to make
            context: Context for the prediction
            
        Returns:
            Predicted value
        """
        # Find the most relevant layer for this prediction
        relevant_layer = self._find_relevant_layer(prediction_type)
        
        if not relevant_layer:
            return None
        
        # Generate prediction based on layer type and content
        predicted_value = self._generate_prediction(relevant_layer, prediction_type, context)
        
        # Record prediction
        prediction = ModelPrediction(
            prediction_id=str(uuid.uuid4()),
            model_layer_id=relevant_layer.layer_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value
        )
        
        self.predictions.append(prediction)
        
        return predicted_value
    
    def _find_relevant_layer(self, prediction_type: str) -> Optional[SelfModelLayer]:
        """Find the most relevant layer for a prediction type."""
        # Map prediction types to model types
        type_mapping = {
            "behavior": ModelType.BEHAVIORAL,
            "function": ModelType.FUNCTIONAL,
            "thought": ModelType.COGNITIVE,
            "structure": ModelType.STRUCTURAL,
            "model": ModelType.META,
            "self": ModelType.RECURSIVE
        }
        
        # Find best model type for prediction
        best_model_type = ModelType.BEHAVIORAL  # Default
        for key, model_type in type_mapping.items():
            if key in prediction_type.lower():
                best_model_type = model_type
                break
        
        # Find most accurate layer of that type
        candidates = [layer for layer in self.all_layers.values()
                     if layer.model_type == best_model_type]
        
        if candidates:
            return max(candidates, key=lambda l: l.accuracy)
        
        # Fallback to root model
        return self.root_model
    
    def _generate_prediction(self, layer: SelfModelLayer, 
                           prediction_type: str, context: Dict[str, Any]) -> Any:
        """Generate a prediction from a model layer."""
        # Simple prediction logic based on model type
        if layer.model_type == ModelType.BEHAVIORAL:
            if "action" in prediction_type:
                patterns = layer.content.get("patterns", [])
                return patterns[0] if patterns else "explore"
        
        elif layer.model_type == ModelType.FUNCTIONAL:
            if "output" in prediction_type:
                functions = layer.content.get("functions", [])
                return f"result_of_{functions[0]}" if functions else "unknown"
        
        elif layer.model_type == ModelType.COGNITIVE:
            if "thought" in prediction_type:
                return "recursive_self_analysis"
        
        elif layer.model_type == ModelType.META:
            if "accuracy" in prediction_type:
                return layer.accuracy
        
        elif layer.model_type == ModelType.RECURSIVE:
            if "self" in prediction_type:
                return "infinite_self_reference"
        
        # Default prediction
        return "unknown"
    
    def calculate_overall_accuracy(self) -> float:
        """Calculate overall accuracy of the self-model."""
        if not self.all_layers:
            return 0.0
        
        total_accuracy = sum(layer.accuracy for layer in self.all_layers.values())
        return total_accuracy / len(self.all_layers)
    
    def get_recursive_depth(self) -> int:
        """Get the maximum recursive depth of the model."""
        if not self.root_model:
            return 0
        
        return self.root_model.get_total_depth()
    
    def introspect(self) -> Dict[str, Any]:
        """
        Perform introspection on the recursive self-model.
        
        Returns:
            Introspection report
        """
        report = {
            "model_structure": {
                "total_layers": len(self.all_layers),
                "max_depth": self.get_recursive_depth(),
                "recursive_loops": len(self.recursive_loops),
                "model_types": {}
            },
            "accuracy": {
                "overall": self.calculate_overall_accuracy(),
                "by_type": {},
                "by_depth": {}
            },
            "predictions": {
                "total_made": len(self.predictions),
                "evaluated": len([p for p in self.predictions if p.accuracy is not None]),
                "average_accuracy": 0.0
            },
            "recursive_properties": {
                "self_referential_layers": [],
                "stable_loops": [],
                "unstable_loops": []
            },
            "insights": []
        }
        
        # Count model types
        for layer in self.all_layers.values():
            model_type = layer.model_type.value
            report["model_structure"]["model_types"][model_type] = \
                report["model_structure"]["model_types"].get(model_type, 0) + 1
        
        # Calculate accuracy by type and depth
        type_accuracies = {}
        depth_accuracies = {}
        
        for layer in self.all_layers.values():
            # By type
            if layer.model_type not in type_accuracies:
                type_accuracies[layer.model_type] = []
            type_accuracies[layer.model_type].append(layer.accuracy)
            
            # By depth
            if layer.depth not in depth_accuracies:
                depth_accuracies[layer.depth] = []
            depth_accuracies[layer.depth].append(layer.accuracy)
        
        # Average accuracies
        for model_type, accuracies in type_accuracies.items():
            report["accuracy"]["by_type"][model_type.value] = \
                sum(accuracies) / len(accuracies)
        
        for depth, accuracies in depth_accuracies.items():
            report["accuracy"]["by_depth"][depth] = \
                sum(accuracies) / len(accuracies)
        
        # Prediction accuracy
        evaluated_predictions = [p for p in self.predictions if p.accuracy is not None]
        if evaluated_predictions:
            report["predictions"]["average_accuracy"] = \
                sum(p.accuracy for p in evaluated_predictions) / len(evaluated_predictions)
        
        # Recursive properties
        for layer in self.all_layers.values():
            if layer.includes_self:
                report["recursive_properties"]["self_referential_layers"].append(layer.layer_id)
        
        for loop in self.recursive_loops:
            if loop.is_stable():
                report["recursive_properties"]["stable_loops"].append(loop.loop_id)
            else:
                report["recursive_properties"]["unstable_loops"].append(loop.loop_id)
        
        # Generate insights
        if report["accuracy"]["overall"] > 0.7:
            report["insights"].append("Self-model has achieved high accuracy")
        
        if len(report["recursive_properties"]["self_referential_layers"]) > 3:
            report["insights"].append("Multiple layers of self-reference create deep recursion")
        
        if report["recursive_properties"]["stable_loops"]:
            report["insights"].append("Stable recursive loops enable sustained self-awareness")
        
        if report["model_structure"]["max_depth"] > 5:
            report["insights"].append("Deep recursive modeling enables meta-meta-cognition")
        
        return report
    
    def visualize_model(self) -> Dict[str, Any]:
        """
        Create visualization data for the recursive self-model.
        
        Returns:
            Visualization specification
        """
        if not self.root_model:
            return {"error": "No model to visualize"}
        
        viz = {
            "nodes": [],
            "edges": [],
            "clusters": {},
            "recursive_loops": []
        }
        
        # Add nodes for each layer
        for layer_id, layer in self.all_layers.items():
            node = {
                "id": layer_id,
                "label": f"{layer.model_type.value} (d={layer.depth})",
                "depth": layer.depth,
                "accuracy": layer.accuracy,
                "type": layer.model_type.value,
                "is_recursive": layer.includes_self
            }
            viz["nodes"].append(node)
        
        # Add edges for parent-child relationships
        for layer in self.all_layers.values():
            for sub_model in layer.sub_models:
                edge = {
                    "from": layer.layer_id,
                    "to": sub_model.layer_id,
                    "type": "contains"
                }
                viz["edges"].append(edge)
        
        # Add edges for recursive references
        for layer in self.all_layers.values():
            if layer.includes_self:
                edge = {
                    "from": layer.layer_id,
                    "to": layer.layer_id,
                    "type": "self_reference"
                }
                viz["edges"].append(edge)
        
        # Group by depth
        for layer in self.all_layers.values():
            depth = layer.depth
            if depth not in viz["clusters"]:
                viz["clusters"][depth] = []
            viz["clusters"][depth].append(layer.layer_id)
        
        # Add recursive loops
        for loop in self.recursive_loops:
            viz["recursive_loops"].append({
                "id": loop.loop_id,
                "type": loop.loop_type,
                "layers": loop.layers_involved,
                "stable": loop.is_stable()
            })
        
        return viz
