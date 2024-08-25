# config.py
"""
Configuration settings for the Solana contract analyzer.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the configuration from environment variables
SOLANA_RPC_ENDPOINT = os.getenv("SOLANA_RPC_ENDPOINT")
LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT")
LLM_API_KEY = os.getenv("LLM_API_KEY")

# Optional: Set default values if environment variables are not set
if SOLANA_RPC_ENDPOINT is None:
    raise ValueError("SOLANA_RPC_ENDPOINT is not set in the environment variables")

if LLM_API_ENDPOINT is None:
    raise ValueError("LLM_API_ENDPOINT is not set in the environment variables")

if LLM_API_KEY is None:
    raise ValueError("LLM_API_KEY is not set in the environment variables")