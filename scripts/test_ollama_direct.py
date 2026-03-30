#!/usr/bin/env python3
"""Test Ollama API directly to debug empty responses."""
import json
import requests

# Test 1: Direct API call
print("=" * 60)
print("Test 1: Direct Ollama API call")
print("=" * 60)

payload = {
    "model": "qwen3.5:4b",
    "prompt": "What is 2+2? Answer with just the number.",
    "stream": False,
    "options": {
        "temperature": 0.0,
        "num_predict": 10,
    }
}

print(f"Sending payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=30
    )
    print(f"\nStatus code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    result = response.json()
    generated_text = result.get("response", "")
    print(f"\nExtracted text: '{generated_text}'")
    print(f"Text length: {len(generated_text)}")

except Exception as e:
    print(f"Error: {e}")

# Test 2: Using our client
print("\n" + "=" * 60)
print("Test 2: Using our ollama_client")
print("=" * 60)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lost_in_the_middle.ollama_client import query_ollama_model

try:
    response = query_ollama_model(
        model="qwen3.5:4b",
        prompt="What is 2+2? Answer with just the number.",
        temperature=0.0,
        max_tokens=10,
        timeout=30
    )
    print(f"Client response: '{response}'")
    print(f"Response length: {len(response)}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Longer prompt (like QA)
print("\n" + "=" * 60)
print("Test 3: QA-style prompt")
print("=" * 60)

qa_prompt = """Write a high-quality answer for the given question using only the provided search results (some of which might be irrelevant).

Document [1](Title: Test) This is a test document with some information about the number four.

Question: What is 2+2?
Answer:"""

try:
    response = query_ollama_model(
        model="qwen3.5:4b",
        prompt=qa_prompt,
        temperature=0.0,
        max_tokens=100,
        timeout=30
    )
    print(f"QA response: '{response}'")
    print(f"Response length: {len(response)}")
except Exception as e:
    print(f"Error: {e}")
