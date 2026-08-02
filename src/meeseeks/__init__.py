from src.config import Settings
from src.meeseeks.GroqMeeseeks import GroqMeeseeks
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.OpenMeeseeks import OpenMeeseeks


def make_meeseeks(settings: Settings) -> MeeseeksModel:
    provider = settings.meeseeks_provider

    if provider == "groq":
        return GroqMeeseeks(api_key=settings.groq_api_key, model=settings.groq_model)
    if provider == "openrouter":
        return OpenMeeseeks(api_key=settings.openrouter_api_key, model=settings.openrouter_model)

    raise ValueError(f"unknown meeseeks provider: {provider}")
