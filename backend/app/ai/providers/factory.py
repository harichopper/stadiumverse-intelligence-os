"""
StadiumVerse AI V2 - AI Provider Factory
Factory pattern for creating AI providers based on configuration
"""

import logging
from typing import Any, Dict

from ...config import settings
from .base import AIProvider
from .ollama_provider import OllamaProvider

logger = logging.getLogger(__name__)


class UnsupportedProviderError(Exception):
    """Raised when an unsupported AI provider is requested"""

    pass


class ProviderConfigurationError(Exception):
    """Raised when AI provider configuration is invalid"""

    pass


def create_ai_provider(provider_config: Dict[str, Any] = None) -> AIProvider:
    """
    Factory function to create AI providers based on configuration

    Args:
        provider_config: Configuration dictionary, defaults to settings if None

    Returns:
        AIProvider: Configured AI provider instance

    Raises:
        UnsupportedProviderError: When provider type is not supported
        ProviderConfigurationError: When configuration is invalid
    """
    if provider_config is None:
        provider_config = {
            "provider": getattr(settings, "LLM_PROVIDER", "ollama"),
            "host": getattr(settings, "OLLAMA_HOST", "http://localhost:11434"),
            "model": getattr(settings, "OLLAMA_MODEL", "qwen2.5-coder:3b"),
            "temperature": getattr(settings, "AI_TEMPERATURE", 0.7),
            "max_tokens": getattr(settings, "AI_MAX_TOKENS", 2000),
            "timeout": getattr(settings, "AI_TIMEOUT", 30),
        }

    provider_type = provider_config.get("provider", "").lower()

    logger.info(f"Creating AI provider: {provider_type}")

    if provider_type == "ollama":
        return _create_ollama_provider(provider_config)
    else:
        # Future providers can be added here
        available_providers = ["ollama"]
        raise UnsupportedProviderError(
            f"Unsupported AI provider: {provider_type}. "
            f"Available providers: {', '.join(available_providers)}"
        )


def _create_ollama_provider(config: Dict[str, Any]) -> OllamaProvider:
    """
    Create and configure Ollama provider

    Args:
        config: Ollama configuration

    Returns:
        OllamaProvider: Configured Ollama provider

    Raises:
        ProviderConfigurationError: When configuration is invalid
    """
    required_keys = ["host", "model"]
    missing_keys = [key for key in required_keys if not config.get(key)]

    if missing_keys:
        raise ProviderConfigurationError(
            f"Missing required Ollama configuration: {', '.join(missing_keys)}"
        )

    # Validate host URL
    host = config["host"]
    if not (host.startswith("http://") or host.startswith("https://")):
        raise ProviderConfigurationError(
            f"Invalid Ollama host URL: {host}. Must start with http:// or https://"
        )

    # Validate model name
    model = config["model"]
    if not model or not isinstance(model, str):
        raise ProviderConfigurationError(
            f"Invalid Ollama model: {model}. Must be a non-empty string"
        )

    # Set defaults for optional parameters
    ollama_config = {
        "host": host,
        "model": model,
        "temperature": config.get("temperature", 0.7),
        "max_tokens": config.get("max_tokens", 2000),
        "timeout": config.get("timeout", 30),
        "keep_alive": config.get("keep_alive", "5m"),
        "num_ctx": config.get("num_ctx", 4096),
        "repeat_penalty": config.get("repeat_penalty", 1.1),
    }

    # Validate numeric parameters
    numeric_params = {
        "temperature": (0.0, 2.0),
        "max_tokens": (1, 32000),
        "timeout": (1, 300),
        "num_ctx": (512, 32768),
        "repeat_penalty": (0.5, 2.0),
    }

    for param, (min_val, max_val) in numeric_params.items():
        value = ollama_config[param]
        if not isinstance(value, (int, float)) or not min_val <= value <= max_val:
            raise ProviderConfigurationError(
                f"Invalid {param}: {value}. Must be between {min_val} and {max_val}"
            )

    try:
        provider = OllamaProvider(ollama_config)
        logger.info(f"Successfully created Ollama provider with model: {model}")
        return provider

    except Exception as e:
        raise ProviderConfigurationError(f"Failed to create Ollama provider: {e}")


async def validate_ai_provider(provider: AIProvider) -> Dict[str, Any]:
    """
    Validate that an AI provider is working correctly

    Args:
        provider: AI provider to validate

    Returns:
        Dict with validation results
    """
    validation_results = {
        "healthy": False,
        "model_info": {},
        "test_response": None,
        "error": None,
        "performance": {},
    }

    try:
        # Health check
        validation_results["healthy"] = await provider.health_check()

        if not validation_results["healthy"]:
            validation_results["error"] = "Provider failed health check"
            return validation_results

        # Get model info
        validation_results["model_info"] = await provider.get_model_info()

        # Test simple completion
        from .base import AIMessage, MessageRole

        test_messages = [
            AIMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            AIMessage(
                role=MessageRole.USER,
                content="Say 'Hello from StadiumVerse AI' and nothing else.",
            ),
        ]

        test_response = await provider.generate_completion(test_messages)
        validation_results["test_response"] = {
            "content": test_response.content[:100],  # First 100 chars
            "confidence": test_response.confidence,
            "latency_ms": test_response.latency_ms,
            "token_count": test_response.token_count,
        }

        # Get performance stats
        validation_results["performance"] = provider.get_performance_stats()

        logger.info("AI provider validation successful")

    except Exception as e:
        validation_results["error"] = str(e)
        logger.error(f"AI provider validation failed: {e}")

    return validation_results


# Global provider instance (singleton pattern)
_global_provider: AIProvider = None


async def initialize_global_provider(
    provider_config: Dict[str, Any] = None,
) -> AIProvider:
    """
    Initialize the global AI provider instance

    Args:
        provider_config: Optional configuration dictionary

    Returns:
        AIProvider: Global provider instance
    """
    global _global_provider

    if _global_provider is None:
        _global_provider = create_ai_provider(provider_config)

        # Validate the provider
        validation = await validate_ai_provider(_global_provider)
        if not validation["healthy"]:
            logger.error(f"Global AI provider validation failed: {validation['error']}")
            raise ProviderConfigurationError(
                f"Global AI provider is unhealthy: {validation['error']}"
            )

        logger.info("Global AI provider created and validated")

    return _global_provider


async def get_global_ai_provider() -> AIProvider:
    """
    Get the global AI provider instance
    Creates one if it doesn't exist

    Returns:
        AIProvider: Global provider instance
    """
    global _global_provider

    if _global_provider is None:
        return await initialize_global_provider()

    return _global_provider


async def shutdown_global_provider():
    """Shutdown and cleanup the global AI provider"""
    global _global_provider

    if _global_provider is not None:
        if hasattr(_global_provider, "close"):
            await _global_provider.close()
        _global_provider = None
        logger.info("Global AI provider shutdown complete")
