"""
StadiumVerse AI V2 - Base AI Provider Interface
Abstract interface for all AI providers supporting the Living Brain architecture
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import time

class MessageRole(str, Enum):
    """Message roles in AI conversations"""
    SYSTEM = "system"
    USER = "user" 
    ASSISTANT = "assistant"

@dataclass
class AIMessage:
    """AI message structure"""
    role: MessageRole
    content: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class AIResponse:
    """AI response with metadata"""
    content: str
    confidence: float
    reasoning: str
    alternatives: List[str]
    token_count: int
    latency_ms: float
    model_used: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class AIProvider(ABC):
    """
    Abstract base class for all AI providers
    Ensures consistent interface across different LLM providers
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("model", "unknown")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2000)
        self.timeout = config.get("timeout", 30)
        
        # Performance tracking
        self.total_requests = 0
        self.total_tokens = 0
        self.avg_latency_ms = 0.0
        self.error_count = 0
        
    @abstractmethod
    async def generate_completion(
        self,
        messages: List[AIMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate a completion from the AI model
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature override
            max_tokens: Maximum tokens override
            **kwargs: Additional provider-specific parameters
            
        Returns:
            AIResponse with content and metadata
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[AIMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the AI model
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature override
            max_tokens: Maximum tokens override
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Partial response chunks
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the AI provider is healthy and responsive
        
        Returns:
            True if healthy, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model information
        """
        pass
    
    def update_performance_metrics(self, latency_ms: float, token_count: int, success: bool):
        """Update internal performance metrics"""
        self.total_requests += 1
        self.total_tokens += token_count
        
        if success:
            # Update moving average latency
            self.avg_latency_ms = (
                (self.avg_latency_ms * (self.total_requests - 1) + latency_ms) 
                / self.total_requests
            )
        else:
            self.error_count += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "avg_latency_ms": self.avg_latency_ms,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(1, self.total_requests),
            "tokens_per_second": self.total_tokens / max(1, self.avg_latency_ms / 1000),
            "model": self.model
        }
    
    async def generate_agent_response(
        self,
        agent_name: str,
        system_prompt: str,
        user_message: str,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate a response for a specific AI agent
        
        Args:
            agent_name: Name of the agent
            system_prompt: System prompt for the agent
            user_message: User message to process
            context: Additional context for the agent
            **kwargs: Additional parameters
            
        Returns:
            AIResponse with agent's response
        """
        messages = [
            AIMessage(role=MessageRole.SYSTEM, content=system_prompt),
            AIMessage(role=MessageRole.USER, content=user_message)
        ]
        
        if context:
            context_message = f"Additional Context: {context}"
            messages.insert(-1, AIMessage(role=MessageRole.USER, content=context_message))
        
        start_time = time.time()
        
        try:
            response = await self.generate_completion(messages, **kwargs)
            
            # Add agent metadata
            response.metadata.update({
                "agent_name": agent_name,
                "context_provided": context is not None,
                "timestamp": time.time()
            })
            
            self.update_performance_metrics(
                response.latency_ms, 
                response.token_count, 
                True
            )
            
            return response
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.update_performance_metrics(latency_ms, 0, False)
            raise e
    
    async def generate_debate_response(
        self,
        agent_name: str,
        system_prompt: str,
        debate_context: Dict[str, Any],
        **kwargs
    ) -> AIResponse:
        """
        Generate a response for AI debate mode
        
        Args:
            agent_name: Name of the debating agent
            system_prompt: System prompt for the agent
            debate_context: Context about the debate topic
            **kwargs: Additional parameters
            
        Returns:
            AIResponse with agent's debate position
        """
        debate_message = f"""
        DEBATE CONTEXT:
        Topic: {debate_context.get('topic', 'Unknown')}
        Current Situation: {debate_context.get('situation', 'Unknown')}
        Other Agents' Positions: {debate_context.get('other_positions', [])}
        
        Provide your position with:
        1. Clear reasoning
        2. Confidence level (0-100%)
        3. Risk assessment
        4. Alternative actions
        5. Estimated cost/impact
        
        Be specific and actionable.
        """
        
        return await self.generate_agent_response(
            agent_name=agent_name,
            system_prompt=system_prompt,
            user_message=debate_message,
            context=debate_context,
            **kwargs
        )
    
    async def generate_storyteller_response(
        self,
        scenario: Dict[str, Any],
        style: str = "narrative",
        **kwargs
    ) -> AIResponse:
        """
        Generate a storyteller response explaining scenarios in natural language
        
        Args:
            scenario: Scenario data to narrate
            style: Storytelling style (narrative, technical, casual)
            **kwargs: Additional parameters
            
        Returns:
            AIResponse with natural language story
        """
        storyteller_prompt = f"""
        You are the AI Storyteller for StadiumVerse. Transform technical data into engaging narratives.
        
        Style: {style}
        Scenario: {scenario}
        
        Create a natural language explanation that:
        1. Explains what is happening
        2. Describes the impact
        3. Provides clear recommendations
        4. Uses specific numbers and timeframes
        5. Maintains professional but engaging tone
        
        Example format: "Within eight minutes approximately 3,200 supporters are expected to move toward Exit B after the final whistle. If no action is taken, average exit time increases to twenty-two minutes. Opening Exit D now will reduce congestion by forty percent."
        """
        
        return await self.generate_agent_response(
            agent_name="storyteller",
            system_prompt="You are the AI Storyteller, expert at explaining complex scenarios in natural language.",
            user_message=storyteller_prompt,
            context=scenario,
            **kwargs
        )