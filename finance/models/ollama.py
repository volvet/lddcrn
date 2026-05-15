
import os
import json
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import urlopen

from langchain_ollama import ChatOllama

def get_ollama_base_url():
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def list_available_ollama_models(base_url: str | None = None, timeout: float = 5.0) -> list[str]:
    """Return model names available in the local/remote Ollama server.

    This calls Ollama's `/api/tags` endpoint and returns model names only.
    """
    resolved_base_url = base_url or get_ollama_base_url()
    tags_url = urljoin(f"{resolved_base_url.rstrip('/')}/", "api/tags")

    try:
        with urlopen(tags_url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError):
        return []

    models = payload.get("models", [])
    return [model["name"] for model in models if isinstance(model, dict) and "name" in model]


def _resolve_model_name(requested_name: str, available_models: list[str]) -> str:
    """Resolve common local aliases to an available Ollama model name."""
    if requested_name in available_models:
        return requested_name

    candidates: list[str] = []
    if ":" not in requested_name and "-" in requested_name:
        # Common typo/alias: qwen3-8b -> qwen3:8b
        candidates.append(requested_name.replace("-", ":", 1))
    if ":" not in requested_name:
        candidates.append(f"{requested_name}:latest")

    for candidate in candidates:
        if candidate in available_models:
            return candidate

    return requested_name

def get_ollama_model(model_name: str, base_url: str | None = None) -> ChatOllama:
    """Return a ChatOllama instance for the specified model name."""
    resolved_base_url = base_url or get_ollama_base_url()
    available_models = list_available_ollama_models(base_url=resolved_base_url)
    resolved_model_name = _resolve_model_name(model_name, available_models)
    return ChatOllama(model=resolved_model_name, base_url=resolved_base_url)


