"""
StadiumVerse AI V2 - AI Provider System
Abstraction layer for different AI providers with offline-first approach
"""

from .base import AIProvider, AIResponse, AIMessage
from .ollama_provider import OllamaProvider
from .factory import create_ai_provider

__all__ = [
    "AIProvider",
    "AIResponse", 
    "AIMessage",
    "OllamaProvider",
    "create_ai_provider"
]