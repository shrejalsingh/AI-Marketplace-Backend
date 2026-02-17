from dotenv import load_dotenv
import os

"""
Application configuration module.

Loads environment variables and defines
application-level configuration constants.
"""

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

# Embedding model configuration
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
