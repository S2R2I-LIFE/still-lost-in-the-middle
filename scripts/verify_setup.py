#!/usr/bin/env python3
"""Verify that the Ollama setup is working correctly."""
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lost_in_the_middle.ollama_client import (
    check_ollama_running,
    get_ollama_models,
    query_ollama_model,
)

def main():
    print("=" * 60)
    print("Ollama Setup Verification")
    print("=" * 60)

    # Check 1: Ollama running
    print("\n[1/4] Checking if Ollama is running...")
    if check_ollama_running():
        print("✓ Ollama is running")
    else:
        print("✗ Ollama is NOT running")
        print("  Please start it with: ollama serve")
        return False

    # Check 2: List models
    print("\n[2/4] Checking available models...")
    try:
        models = get_ollama_models()
        if models:
            print(f"✓ Found {len(models)} model(s):")
            for model in models:
                print(f"  - {model}")
        else:
            print("⚠ No models found")
            print("  Pull a model with: ollama pull qwen3.5:4b")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # Check 3: Test query
    print("\n[3/4] Testing model query...")
    try:
        # Use the first available model
        test_model = models[0]
        print(f"  Using model: {test_model}")
        response = query_ollama_model(
            model=test_model,
            prompt="What is 2+2? Answer with just the number.",
            max_tokens=10,
            timeout=30
        )
        print(f"✓ Model responded: {response.strip()}")
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return False

    # Check 4: Check data files
    print("\n[4/4] Checking data files...")
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'qa_data')
    oracle_file = os.path.join(data_dir, 'nq-open-oracle.jsonl.gz')

    if os.path.exists(oracle_file):
        print(f"✓ Oracle dataset found: {oracle_file}")
    else:
        print(f"✗ Oracle dataset not found: {oracle_file}")
        return False

    print("\n" + "=" * 60)
    print("✓ All checks passed! Ready to run experiments.")
    print("=" * 60)
    print("\nNext step: Run pilot test with:")
    print(f"  python scripts/get_qa_responses_from_ollama.py \\")
    print(f"      --model {test_model} \\")
    print(f"      --input-path qa_data/nq-open-oracle.jsonl.gz \\")
    print(f"      --output-path Context/results/qa_predictions/pilot_test.jsonl.gz")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
