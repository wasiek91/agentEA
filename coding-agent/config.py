"""Configuration management for the AI Coding Agent."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the agent."""

    # API Configuration - ZMIENIONE NA GEMINI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # ← ZMIANA!
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash-latest")

    # Safety Configuration
    DRY_RUN_MODE = os.getenv("DRY_RUN_MODE", "false").lower() == "true"
    REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "false").lower() == "true"

    # Shell Command Configuration
    SHELL_WHITELIST = [
        "npm", "npx",
        "git",
        "python", "python3", "pip", "pip3",
        "node",
        "aider",
        "ls", "dir", "pwd", "cd",
        "cat", "type", "echo",
        "mkdir", "touch"
    ]

    SHELL_BLACKLIST = [
        "rm", "rmdir",
        "del", "erase",
        "format",
        "dd",
        "mkfs",
        ":(){:|:&};:",  # Fork bomb
        "sudo rm -rf",
        "chmod 777"
    ]

    # Agent Configuration
    MAX_ITERATIONS = 10
    VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"
    LANGUAGE = os.getenv("LANGUAGE", "pl")  # pl = Polski, en = English

    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.GEMINI_API_KEY:  # ← ZMIANA!
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "  # ← ZMIANA!
                "Please set it in your .env file."
            )
        return True