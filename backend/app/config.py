"""
StadiumVerse AI V2 - Configuration Settings
"""

import os


class Settings:
    """Application settings"""

    # AI Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "30"))

    # Brain Configuration
    MIN_INTERVENTION_THRESHOLD = float(os.getenv("MIN_INTERVENTION_THRESHOLD", "0.1"))
    MAX_IMPACT_CALCULATION = (
        os.getenv("MAX_IMPACT_CALCULATION", "true").lower() == "true"
    )
    ROI_ANALYSIS_ENABLED = os.getenv("ROI_ANALYSIS_ENABLED", "true").lower() == "true"
    CARBON_TRACKING = os.getenv("CARBON_TRACKING", "true").lower() == "true"

    # Future Engine Configuration
    BRANCH_CALCULATION_DEPTH = int(os.getenv("BRANCH_CALCULATION_DEPTH", "6"))
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
    SCENARIO_SIMULATION_COUNT = int(os.getenv("SCENARIO_SIMULATION_COUNT", "16"))

    # Stadium Configuration
    STADIUM_CAPACITY = int(os.getenv("STADIUM_CAPACITY", "80000"))
    DIGITAL_FAN_COUNT = int(os.getenv("DIGITAL_FAN_COUNT", "100"))
    VOLUNTEER_COUNT = int(os.getenv("VOLUNTEER_COUNT", "20"))

    # Application Settings
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    STADIUM_COORDINATES = [40.7128, -74.0060]
    AI_UPDATE_INTERVAL = 5.0

# Global settings instance
settings = Settings()
STADIUM_ZONES = {}
