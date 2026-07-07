"""
StadiumVerse AI V2 - AI Provider System
Abstraction layer for different AI providers with offline-first approach
"""

from .base import AIMessage, AIProvider, AIResponse
from .factory import create_ai_provider
from .ollama_provider import OllamaProvider

__all__ = [
    "AIProvider",
    "AIResponse",
    "AIMessage",
    "OllamaProvider",
    "create_ai_provider",
]
