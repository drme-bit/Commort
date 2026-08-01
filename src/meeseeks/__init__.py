import os

from dotenv import load_dotenv

from src.meeseeks.GroqMeeseeks import GroqMeeseeks
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.OpenMeeseeks import OpenMeeseeks


def make_meeseeks(provider: str = None) -> MeeseeksModel:
    load_dotenv()
    provider = provider or os.getenv("MEESEEKS_PROVIDER", "groq")

    if provider == "groq":
        return GroqMeeseeks()
    if provider == "openrouter":
        return OpenMeeseeks()

    raise ValueError(f"unknown meeseeks provider: {provider}")
