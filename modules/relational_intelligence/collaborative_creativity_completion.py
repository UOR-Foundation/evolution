"""
This file contains the missing helper methods for collaborative_creativity.py
These should be added to the CollaborativeCreativityEngine class
"""

import numpy as np
from datetime import datetime
from typing import List, Dict, Any


class CollaborativeCreativityCompletionMethods:
    """Helper methods for CollaborativeCreativityEngine"""
    
    def _calculate_collective_focus(self, session) -> float:
        """Calculate collective focus level"""
        if not session.ideas_generated:
            return 0.5
        
        # Check if ideas are focused on session topic
        focus_scores = []
        for idea in session.ideas_generated[-5:]:  # Last 5 ideas
            if session.focus_area.lower() in idea.content.lower():
                focus_scores.append(1.0)
            else:
                focus_scores.append(0.5)
        
        return np.mean(focus_scores) if focus_scores else 0.5
    
    def _calculate_idea_velocity(self, session) -> float:
        """Calculate ideas per minute"""
        if not session.ideas_generated:
            return 0.0
        
        duration = (datetime.now() - session.start_time).total_seconds() / 60
        if duration == 0:
            return 0.0
        
        return len(session.ideas_generated) / duration
    
    def _assess_quality_consistency(self, session) -> float:
        """Assess consistency of idea quality"""
        if len(session.ideas_generated) < 3:
            return 0.5
        
        quality_scores = [idea.get_overall_score() for idea in session.ideas_generated[-10:]]
        if not quality_scores:
            return 0.5
        
        # Low variance indicates consistency
        variance = np.var(quality_scores)
        consistency = 1.0 / (1.0 + variance * 10)  # Scale variance impact
        
        return consistency
    
    def _enhance_session_for_flow(self, session) -> None:
        """Enhance session parameters for flow state"""
        session.session_dynamics['energy_level'] = min(
            session.session_dynamics['energy_level'] * 1.2, 1.0
        )
        session.session_dynamics['harmony'] = min(
            session.session_dynamics['harmony'] * 1.1, 1.0
        )
    
    def _generate_improvisation(self, participant: str, prompt: str, session) -> str:
        """Generate improvisation based on prompt"""
        # Simple implementation - could use more sophisticated generation
        return f"{participant} improvises on '{prompt}' with creative twist"
    
    def _generate_project_milestones(self, project_type: str, 
                                   objectives: List[str]) -> List[Dict[str, Any]]:
        """Generate project milestones based on type and objectives"""
        milestones = []
        
        # Standard creative project phases
        phases = ['ideation', 'development', 'refinement', 'implementation', 'review']
        
        for i, phase in enumerate(phases):
            milestone = {
                'milestone_id': f"milestone_{i+1}",
                'phase': phase,
                'description': f"{phase.capitalize()} phase for {project_type}",
                'success_criteria': [f"Complete {phase} objectives"],
                'estimated_duration': '1-2 weeks',
                'completed': False
            }
            milestones.append(milestone)
        
        return milestones
    
    def _create_development_stages(self, idea, development_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create development stages for an idea"""
        stages = []
        
        # Standard development stages
        stage_templates = [
            {'name': 'research', 'duration': '3 days', 'focus': 'feasibility study'},
            {'name': 'prototype', 'duration': '1 week', 'focus': 'proof of concept'},
            {'name': 'iteration', 'duration': '2 weeks', 'focus': 'refinement'},
            {'name': 'finalization', 'duration': '1 week', 'focus': 'polish and complete'}
        ]
        
        for template in stage_templates:
            stage = {
                'stage_name': template['name'],
                'duration': template['duration'],
                'focus': template['focus'],
                'deliverables': [f"{template['name']} output"],
                'success_metrics': {'completion': 0.0, 'quality': 0.0}
            }
            stages.append(stage)
        
        return stages
    
    def _assess_complementarity(self, participant1: str, 
                              participant2: str) -> Dict[str, float]:
        """Assess how well participants complement each other"""
        complementarity = {
            'skill_complement': 0.7,
            'style_complement': 0.6,
            'perspective_complement': 0.8,
            'overall': 0.7
        }
        
        # Could be enhanced with actual participant data
        return complementarity
    
    def _assess_creative_tension(self, participant1: str, participant2: str) -> float:
        """Assess productive creative tension"""
        # Moderate tension is often productive
        return 0.6
    
    def _assess_mutual_inspiration(self, participant1: str, participant2: str) -> float:
        """Assess mutual inspiration level"""
        # Base on historical interactions if available
        return 0.7
    
    def _calculate_idea_building_rate(self, participant1: str, participant2: str) -> float:
        """Calculate rate of building on each other's ideas"""
        # Could analyze actual building patterns
        return 0.65
    
    def _assess_conflict_productivity(self, participant1: str, participant2: str) -> float:
        """Assess how productive their conflicts are"""
        # Some conflict can be creatively productive
        return 0.5
    
    def _evaluate_team_composition(self, team: List[str], 
                                 requirements: Dict[str, Any]) -> float:
        """Evaluate team composition score"""
        score = 0.5  # Base score
        
        # Check for diversity
        if len(set(team)) == len(team):  # All unique
            score += 0.1
        
        # Check synergies
        synergy_sum = 0.0
        pair_count = 0
        for i in range(len(team)):
            for j in range(i+1, len(team)):
                pair = tuple(sorted([team[i], team[j]]))
                if hasattr(self, 'synergy_matrix') and pair in self.synergy_matrix:
                    synergy_sum += self.synergy_matrix[pair].synergy_score
                    pair_count += 1
        
        if pair_count > 0:
            avg_synergy = synergy_sum / pair_count
            score += avg_synergy * 0.3
        
        return min(score, 1.0)
    
    def _analyze_idea_quality(self, session) -> Dict[str, Any]:
        """Analyze distribution of idea quality"""
        if not session.ideas_generated:
            return {'mean': 0, 'std': 0, 'high_quality_ratio': 0}
        
        quality_scores = [idea.get_overall_score() for idea in session.ideas_generated]
        
        return {
            'mean': np.mean(quality_scores),
            'std': np.std(quality_scores),
            'high_quality_ratio': sum(1 for s in quality_scores if s > 0.7) / len(quality_scores),
            'distribution': {
                'low': sum(1 for s in quality_scores if s < 0.4),
                'medium': sum(1 for s in quality_scores if 0.4 <= s < 0.7),
                'high': sum(1 for s in quality_scores if s >= 0.7)
            }
        }
    
    def _identify_collaboration_patterns(self, session) -> List[Dict[str, Any]]:
        """Identify patterns in collaboration"""
        patterns = []
        
        # Analyze building patterns
        building_count = sum(1 for idea in session.ideas_generated 
                           if len(idea.contributors) > 1)
        if building_count > len(session.ideas_generated) * 0.3:
            patterns.append({
                'pattern': 'high_collaboration',
                'description': 'Frequent building on each other\'s ideas',
                'strength': building_count / len(session.ideas_generated)
            })
        
        # Analyze contribution balance
        contributor_counts = {}
        for idea in session.ideas_generated:
            for contributor in idea.contributors:
                contributor_counts[contributor] = contributor_counts.get(contributor, 0) + 1
        
        if contributor_counts:
            counts = list(contributor_counts.values())
            if np.std(counts) < np.mean(counts) * 0.3:
                patterns.append({
                    'pattern': 'balanced_contribution',
                    'description': 'All participants contributing equally',
                    'strength': 1.0 - (np.std(counts) / np.mean(counts))
                })
        
        return patterns
    
    def _analyze_energy_flow(self, session) -> Dict[str, Any]:
        """Analyze energy flow throughout session"""
        if not hasattr(session, 'energy_flow') or not session.energy_flow:
            return {'dominant_energy': None, 'transitions': 0}
        
        # Count energy types
        energy_counts = {}
        for _, energy in session.energy_flow:
            energy_value = energy.value if hasattr(energy, 'value') else str(energy)
            energy_counts[energy_value] = energy_counts.get(energy_value, 0) + 1
        
        # Find dominant energy
        dominant_energy = max(energy_counts.items(), key=lambda x: x[1])[0] if energy_counts else None
        
        # Count transitions
        transitions = len(session.energy_flow) - 1
        
        return {
            'dominant_energy': dominant_energy,
            'energy_distribution': energy_counts,
            'transitions': transitions,
            'energy_stability': 1.0 / (1.0 + transitions / 10)  # More transitions = less stable
        }
    
    def _identify_key_innovations(self, session) -> List:
        """Identify key innovative ideas from session"""
        # Filter for high novelty and impact
        innovations = [
            idea for idea in session.ideas_generated
            if hasattr(idea, 'novelty_score') and hasattr(idea, 'impact_potential') and
            idea.novelty_score > 0.7 and idea.impact_potential > 0.7
        ]
        
        # Sort by overall score
        innovations.sort(key=lambda i: i.get_overall_score(), reverse=True)
        
        return innovations[:5]  # Top 5 innovations
    
    def _generate_improvement_suggestions(self, session) -> List[str]:
        """Generate suggestions for improving creative sessions"""
        suggestions = []
        
        # Check productivity
        if hasattr(session, 'get_productivity_score') and session.get_productivity_score() < 0.5:
            suggestions.append("Consider more structured brainstorming techniques")
        
        # Check energy flow
        if hasattr(session, 'energy_flow') and len(session.energy_flow) > 10:
            suggestions.append("Try to maintain more consistent creative energy")
        
        # Check collaboration
        solo_ideas = sum(1 for idea in session.ideas_generated if len(idea.contributors) == 1)
        if solo_ideas > len(session.ideas_generated) * 0.7:
            suggestions.append("Encourage more collaborative building on ideas")
        
        # Check breakthrough rate
        if hasattr(session, 'breakthrough_moments') and len(session.breakthrough_moments) == 0:
            suggestions.append("Push for more ambitious and transformative ideas")
        
        return suggestions
    
    def _assess_collaboration_quality(self, session) -> float:
        """Assess overall collaboration quality"""
        factors = []
        
        # Factor 1: Balanced participation
        contributor_counts = {}
        for idea in session.ideas_generated:
            for contributor in idea.contributors:
                contributor_counts[contributor] = contributor_counts.get(contributor, 0) + 1
        
        if contributor_counts:
            counts = list(contributor_counts.values())
            balance_score = 1.0 - (np.std(counts) / (np.mean(counts) + 1))
            factors.append(balance_score)
        
        # Factor 2: Collaborative building
        collab_ratio = sum(1 for idea in session.ideas_generated 
                          if len(idea.contributors) > 1) / len(session.ideas_generated)
        factors.append(collab_ratio)
        
        # Factor 3: Synergy utilization
        if hasattr(session, 'participants') and len(session.participants) > 1:
            synergy_scores = []
            for i in range(len(session.participants)):
                for j in range(i+1, len(session.participants)):
                    pair = tuple(sorted([session.participants[i], session.participants[j]]))
                    if hasattr(self, 'synergy_matrix') and pair in self.synergy_matrix:
                        synergy_scores.append(self.synergy_matrix[pair].synergy_score)
            
            if synergy_scores:
                factors.append(np.mean(synergy_scores))
        
        return np.mean(factors) if factors else 0.5
    
    def _recommend_next_steps(self, session) -> List[str]:
        """Recommend next steps after session"""
        recommendations = []
        
        # Get top ideas
        top_ideas = sorted(session.ideas_generated, 
                          key=lambda i: i.get_overall_score(), 
                          reverse=True)[:3]
        
        if top_ideas:
            recommendations.append(f"Develop top idea: {top_ideas[0].content[:50]}...")
            recommendations.append("Create implementation plan for high-scoring ideas")
        
        # Check for synthesis opportunities
        if len(session.ideas_generated) > 10:
            recommendations.append("Consider synthesis session to combine related ideas")
        
        # Suggest follow-up based on energy
        if hasattr(session, 'energy_flow') and session.energy_flow:
            last_energy = session.energy_flow[-1][1]
            if hasattr(last_energy, 'value'):
                if last_energy.value == 'DIVERGENT':
                    recommendations.append("Schedule convergent session to refine ideas")
                elif last_energy.value == 'CONVERGENT':
                    recommendations.append("Move to implementation planning")
        
        return recommendations
    
    def _update_participant_profiles(self, session) -> None:
        """Update participant profiles based on session performance"""
        if not hasattr(self, 'participant_profiles'):
            self.participant_profiles = {}
            
        for participant in session.participants:
            if participant not in self.participant_profiles:
                self.participant_profiles[participant] = {}
            
            profile = self.participant_profiles[participant]
            
            # Update contribution stats
            contribution_count = sum(1 for idea in session.ideas_generated 
                                   if participant in idea.contributors)
            profile['total_contributions'] = profile.get('total_contributions', 0) + contribution_count
            
            # Update quality stats
            quality_scores = [
                idea.get_overall_score() for idea in session.ideas_generated
                if participant in idea.contributors
            ]
            if quality_scores:
                avg_quality = np.mean(quality_scores)
                profile['avg_idea_quality'] = (
                    profile.get('avg_idea_quality', avg_quality) + avg_quality
                ) / 2
            
            # Update collaboration stats
            collab_count = sum(1 for idea in session.ideas_generated
                             if participant in idea.contributors and len(idea.contributors) > 1)
            profile['collaboration_tendency'] = collab_count / contribution_count if contribution_count > 0 else 0
