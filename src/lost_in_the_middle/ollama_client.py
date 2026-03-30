#!/usr/bin/env python3
"""Client for interacting with Ollama API.

This module provides a simple interface for querying Ollama models via their HTTP API.
Ollama must be running locally on the default port (11434).
"""
import json
import logging
import time
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 300  # 5 minutes for long context generation


class OllamaAPIError(Exception):
    """Raised when Ollama API returns an error."""
    pass


class OllamaConnectionError(Exception):
    """Raised when unable to connect to Ollama service."""
    pass


def check_ollama_running() -> bool:
    """Check if Ollama service is running and accessible.

    Returns:
        bool: True if Ollama is running, False otherwise.
    """
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_ollama_models() -> List[str]:
    """Get list of available Ollama models.

    Returns:
        List[str]: List of model names available locally.

    Raises:
        OllamaConnectionError: If unable to connect to Ollama.
        OllamaAPIError: If API returns an error.
    """
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except requests.exceptions.ConnectionError as e:
        raise OllamaConnectionError(
            f"Unable to connect to Ollama at {OLLAMA_BASE_URL}. "
            "Is Ollama running? Try: ollama serve"
        ) from e
    except requests.exceptions.RequestException as e:
        raise OllamaAPIError(f"Error fetching Ollama models: {e}") from e


def query_ollama_model(
    model: str,
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 100,
    top_p: float = 1.0,
    timeout: int = DEFAULT_TIMEOUT,
    retry_attempts: int = 3,
    retry_delay: int = 5,
) -> str:
    """Query an Ollama model with a prompt and return the response.

    Args:
        model: Name of the Ollama model to use (e.g., "qwen3.5:27b").
        prompt: The text prompt to send to the model.
        temperature: Sampling temperature (0.0 = greedy, higher = more random).
        max_tokens: Maximum number of tokens to generate.
        top_p: Nucleus sampling parameter.
        timeout: Request timeout in seconds.
        retry_attempts: Number of times to retry on failure.
        retry_delay: Delay in seconds between retries.

    Returns:
        str: The model's generated response text.

    Raises:
        OllamaConnectionError: If unable to connect to Ollama.
        OllamaAPIError: If API returns an error after all retries.
    """
    if not prompt:
        raise ValueError("Prompt cannot be empty")

    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,  # Get complete response, not streaming
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,  # Ollama's parameter name for max tokens
            "top_p": top_p,
        }
    }

    last_exception = None
    for attempt in range(retry_attempts):
        try:
            logger.debug(f"Querying Ollama model {model} (attempt {attempt + 1}/{retry_attempts})")

            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()

            # Extract the generated text from the response
            # Some models (like reasoning models) use "thinking" field instead of/in addition to "response"
            response_text = result.get("response", "")
            thinking_text = result.get("thinking", "")

            # Combine both fields (reasoning models may use "thinking", regular models use "response")
            if thinking_text and response_text:
                generated_text = thinking_text + "\n" + response_text
            elif thinking_text:
                generated_text = thinking_text
            elif response_text:
                generated_text = response_text
            else:
                generated_text = ""
                logger.warning(f"Ollama returned empty response for model {model}")

            return generated_text

        except requests.exceptions.ConnectionError as e:
            last_exception = OllamaConnectionError(
                f"Unable to connect to Ollama at {OLLAMA_BASE_URL}. "
                "Is Ollama running? Try: ollama serve"
            )
            logger.warning(f"Connection error on attempt {attempt + 1}: {e}")

        except requests.exceptions.Timeout as e:
            last_exception = OllamaAPIError(
                f"Request timed out after {timeout} seconds. "
                "Try increasing timeout or reducing context length."
            )
            logger.warning(f"Timeout on attempt {attempt + 1}: {e}")

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error from Ollama: {e}"
            try:
                error_detail = response.json().get("error", "")
                if error_detail:
                    error_msg += f" - {error_detail}"
            except:
                pass
            last_exception = OllamaAPIError(error_msg)
            logger.warning(f"HTTP error on attempt {attempt + 1}: {error_msg}")

        except (ValueError, json.JSONDecodeError) as e:
            last_exception = OllamaAPIError(f"Invalid JSON response from Ollama: {e}")
            logger.warning(f"JSON decode error on attempt {attempt + 1}: {e}")

        # Wait before retrying (except on last attempt)
        if attempt < retry_attempts - 1:
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    # If we get here, all retries failed
    raise last_exception


def verify_model_available(model: str) -> bool:
    """Check if a specific model is available in Ollama.

    Args:
        model: Name of the model to check.

    Returns:
        bool: True if model is available, False otherwise.
    """
    try:
        available_models = get_ollama_models()
        return model in available_models
    except (OllamaConnectionError, OllamaAPIError):
        return False


def format_model_info(model: str) -> Dict:
    """Get detailed information about a specific model.

    Args:
        model: Name of the model.

    Returns:
        Dict: Model information including size, parameters, etc.

    Raises:
        OllamaConnectionError: If unable to connect to Ollama.
        OllamaAPIError: If API returns an error.
    """
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/show",
            json={"name": model},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        raise OllamaConnectionError(
            f"Unable to connect to Ollama at {OLLAMA_BASE_URL}"
        ) from e
    except requests.exceptions.RequestException as e:
        raise OllamaAPIError(f"Error fetching model info: {e}") from e


if __name__ == "__main__":
    # Simple test/demo of the client
    logging.basicConfig(level=logging.INFO)

    print("Checking if Ollama is running...")
    if check_ollama_running():
        print("✓ Ollama is running")

        print("\nAvailable models:")
        try:
            models = get_ollama_models()
            for model in models:
                print(f"  - {model}")
        except Exception as e:
            print(f"  Error: {e}")

        print("\nTesting query (if you have a model installed)...")
        print("To test, run: python -c 'from lost_in_the_middle.ollama_client import query_ollama_model; print(query_ollama_model(\"qwen3.5:4b\", \"What is 2+2?\", max_tokens=10))'")
    else:
        print("✗ Ollama is not running")
        print("  Start it with: ollama serve")
