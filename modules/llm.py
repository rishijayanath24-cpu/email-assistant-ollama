"""Thin wrapper around the local Ollama HTTP API."""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


class OllamaError(RuntimeError):
    pass


def ask_ollama(prompt: str, temperature: float = 0.4) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(
            f"Could not reach Ollama at {OLLAMA_URL} (is `ollama serve` running "
            f"and is `{MODEL_NAME}` pulled?): {exc}"
        ) from exc
    return response.json().get("response", "").strip()
