"""
StadiumVerse AI V2 - Ollama Provider
Local AI provider using Ollama for offline operation
"""

import json
import logging
import time
from typing import Any, AsyncGenerator, Dict, List, Optional
from urllib.parse import urljoin

import aiohttp

from .base import AIMessage, AIProvider, AIResponse, MessageRole

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    """
    Ollama AI provider for local, offline AI processing
    Supports qwen2.5-coder and other Ollama models
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("host", "http://localhost:11434")
        self.model = config.get("model", "qwen2.5-coder:3b")
        self.session: Optional[aiohttp.ClientSession] = None

        # Ollama-specific configuration
        self.keep_alive = config.get("keep_alive", "5m")
        self.num_ctx = config.get("num_ctx", 4096)
        self.repeat_penalty = config.get("repeat_penalty", 1.1)

        logger.info(f"Initialized Ollama provider with model: {self.model}")

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout, headers={"Content-Type": "application/json"}
            )
        return self.session

    async def _close_session(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _messages_to_prompt(self, messages: List[AIMessage]) -> str:
        """Convert messages to a single prompt for Ollama"""
        prompt_parts = []

        for message in messages:
            if message.role == MessageRole.SYSTEM:
                prompt_parts.append(f"System: {message.content}")
            elif message.role == MessageRole.USER:
                prompt_parts.append(f"User: {message.content}")
            elif message.role == MessageRole.ASSISTANT:
                prompt_parts.append(f"Assistant: {message.content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)

    def _extract_confidence_and_reasoning(
        self, content: str
    ) -> tuple[float, str, List[str]]:
        """
        Extract confidence score, reasoning, and alternatives from AI response
        Uses heuristics to parse structured responses
        """
        confidence = 0.7  # Default confidence
        reasoning = ""
        alternatives = []

        lines = content.strip().split("\n")

        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # Look for confidence indicators
            if "confidence" in line_lower:
                try:
                    # Extract number from confidence line
                    import re

                    conf_match = re.search(r"(\d+(?:\.\d+)?)", line)
                    if conf_match:
                        conf_val = float(conf_match.group(1))
                        if conf_val <= 1.0:
                            confidence = conf_val
                        elif conf_val <= 100.0:
                            confidence = conf_val / 100.0
                except ValueError:
                    pass

            # Look for reasoning sections
            if any(
                keyword in line_lower
                for keyword in ["reason", "because", "analysis", "explanation"]
            ):
                # Capture this line and next few lines as reasoning
                reasoning_lines = [line]
                for j in range(i + 1, min(i + 4, len(lines))):
                    if lines[j].strip() and not any(
                        keyword in lines[j].lower()
                        for keyword in ["alternative", "option", "confidence"]
                    ):
                        reasoning_lines.append(lines[j])
                    else:
                        break
                reasoning = " ".join(reasoning_lines).strip()

            # Look for alternatives
            if any(
                keyword in line_lower
                for keyword in ["alternative", "option", "instead", "could also"]
            ):
                alternatives.append(line.strip())

        # Fallback reasoning if not found
        if not reasoning:
            reasoning = "AI analysis based on current stadium conditions and predictive modeling."

        # Fallback alternatives if not found
        if not alternatives:
            alternatives = [
                "Deploy additional volunteers",
                "Adjust crowd flow patterns",
                "Implement backup protocols",
            ]

        return confidence, reasoning, alternatives

    async def generate_completion(
        self,
        messages: List[AIMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> AIResponse:
        """Generate completion using Ollama API"""
        start_time = time.time()

        try:
            session = await self._get_session()
            prompt = self._messages_to_prompt(messages)

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                    "num_ctx": self.num_ctx,
                    "repeat_penalty": self.repeat_penalty,
                },
                "keep_alive": self.keep_alive,
            }

            url = urljoin(self.base_url, "/api/generate")

            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error {response.status}: {error_text}")

                result = await response.json()
                content = result.get("response", "")

                # Calculate metrics
                latency_ms = (time.time() - start_time) * 1000

                # Extract structured information from response
                confidence, reasoning, alternatives = (
                    self._extract_confidence_and_reasoning(content)
                )

                # Estimate token count (rough approximation)
                token_count = len(content.split()) + len(prompt.split())

                return AIResponse(
                    content=content,
                    confidence=confidence,
                    reasoning=reasoning,
                    alternatives=alternatives,
                    token_count=token_count,
                    latency_ms=latency_ms,
                    model_used=self.model,
                    metadata={
                        "provider": "ollama",
                        "prompt_tokens": len(prompt.split()),
                        "completion_tokens": len(content.split()),
                        "total_eval_count": result.get("eval_count", 0),
                        "total_eval_duration": result.get("total_duration", 0),
                    },
                )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Ollama completion error: {e}")

            # Return error response with fallback
            return AIResponse(
                content=f"Unable to process request: {str(e)}",
                confidence=0.0,
                reasoning="Error occurred during AI processing",
                alternatives=[
                    "Retry request",
                    "Check system status",
                    "Use manual override",
                ],
                token_count=0,
                latency_ms=latency_ms,
                model_used=self.model,
                metadata={"error": str(e), "provider": "ollama"},
            )

    async def generate_stream(
        self,
        messages: List[AIMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response using Ollama API"""
        try:
            session = await self._get_session()
            prompt = self._messages_to_prompt(messages)

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                    "num_ctx": self.num_ctx,
                    "repeat_penalty": self.repeat_penalty,
                },
                "keep_alive": self.keep_alive,
            }

            url = urljoin(self.base_url, "/api/generate")

            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    yield f"Error: {error_text}"
                    return

                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            yield f"Streaming error: {str(e)}"

    async def health_check(self) -> bool:
        """Check if Ollama is healthy and the model is available"""
        try:
            session = await self._get_session()

            # Check if Ollama is running
            url = urljoin(self.base_url, "/api/tags")
            async with session.get(url) as response:
                if response.status != 200:
                    return False

                data = await response.json()
                models = data.get("models", [])

                # Check if our model is available
                model_names = [model.get("name", "") for model in models]
                return any(self.model in model_name for model_name in model_names)

        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False

    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        try:
            session = await self._get_session()

            url = urljoin(self.base_url, "/api/show")
            payload = {"model": self.model}

            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "model": self.model,
                        "size": data.get("size", 0),
                        "format": data.get("format", "unknown"),
                        "family": data.get("details", {}).get("family", "unknown"),
                        "parameter_size": data.get("details", {}).get(
                            "parameter_size", "unknown"
                        ),
                        "quantization_level": data.get("details", {}).get(
                            "quantization_level", "unknown"
                        ),
                        "provider": "ollama",
                        "local": True,
                        "offline_capable": True,
                    }
                else:
                    return {
                        "model": self.model,
                        "provider": "ollama",
                        "status": f"Error {response.status}",
                        "local": True,
                        "offline_capable": True,
                    }

        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {
                "model": self.model,
                "provider": "ollama",
                "error": str(e),
                "local": True,
                "offline_capable": True,
            }

    async def close(self):
        """Close the provider and cleanup resources"""
        await self._close_session()

    def __del__(self):
        """Cleanup on deletion"""
        if hasattr(self, "session") and self.session and not self.session.closed:
            # Can't await in __del__, so just log
            logger.warning("OllamaProvider session not properly closed")
