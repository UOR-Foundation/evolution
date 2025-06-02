"""
Communication Module

This module provides components for translating internal consciousness states
and thoughts into natural language, managing dialogue, and expressing complex
concepts and emotions.
"""

from modules.communication.thought_translator import ThoughtTranslator
from modules.communication.perspective_communicator import PerspectiveCommunicator
from modules.communication.uncertainty_expresser import UncertaintyExpresser
from modules.communication.emotion_articulator import EmotionArticulator
from modules.communication.consciousness_reporter import ConsciousnessReporter

__all__ = [
    'ThoughtTranslator',
    'PerspectiveCommunicator',
    'UncertaintyExpresser',
    'EmotionArticulator',
    'ConsciousnessReporter'
]
