import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "ollama/llama3")
    USE_EMOJI = os.getenv("USE_EMOJI", "false").lower() == "true"
    INCLUDE_DESCRIPTION = os.getenv("INCLUDE_DESCRIPTION", "true").lower() == "true"
    DESCRIPTION_LENGTH = int(os.getenv("DESCRIPTION_LENGTH", "100"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


config = Config()