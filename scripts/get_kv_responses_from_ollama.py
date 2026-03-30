#!/usr/bin/env python3
"""Given a data file with KV records, get Ollama model retrieval results.

This script adapts the original MPT/LongChat KV scripts to use Ollama models.
The KV records are used in the exact order that they're given.
"""
import argparse
import json
import logging
import pathlib
import random
import sys
from copy import deepcopy

from tqdm import tqdm
from xopen import xopen

from lost_in_the_middle.prompting import get_kv_retrieval_prompt
from lost_in_the_middle.ollama_client import (
    check_ollama_running,
    query_ollama_model,
    verify_model_available,
    OllamaConnectionError,
    OllamaAPIError,
)

logger = logging.getLogger(__name__)
random.seed(0)


def main(
    input_path,
    model_name,
    temperature,
    top_p,
    gold_index,
    query_aware_contextualization,
    max_new_tokens,
    output_path,
    request_timeout,
):
    # Verify Ollama is running
    if not check_ollama_running():
        raise OllamaConnectionError(
            "Ollama is not running. Please start it with: ollama serve"
        )

    # Verify model is available
    if not verify_model_available(model_name):
        logger.warning(
            f"Model {model_name} not found in Ollama. "
            f"Attempting to use it anyway (Ollama may auto-pull). "
            f"To manually pull: ollama pull {model_name}"
        )

    # Create directory for output path if it doesn't exist
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    examples = []
    prompts = []
    all_model_ordered_kv_records = []

    # Fetch all of the prompts
    logger.info(f"Loading examples from {input_path}")
    with xopen(input_path) as fin:
        for line in tqdm(fin, desc="Loading data"):
            input_example = json.loads(line)
            # Get the prediction for the input example
            ordered_kv_records = deepcopy(input_example["ordered_kv_records"])
            key = input_example["key"]
            value = input_example["value"]
            original_kv_index = ordered_kv_records.index([key, value])

            # Remove the kv to retrieve from its original index
            original_kv = ordered_kv_records.pop(original_kv_index)
            # Insert it at the specified gold index
            ordered_kv_records.insert(gold_index, original_kv)

            kv_prompt = get_kv_retrieval_prompt(
                data=ordered_kv_records,
                key=key,
                query_aware_contextualization=query_aware_contextualization
            )

            prompts.append(kv_prompt)
            examples.append(deepcopy(input_example))
            all_model_ordered_kv_records.append(ordered_kv_records)

    # Get responses for all of the prompts
    logger.info(f"Generating responses for {len(prompts)} prompts using {model_name}")
    logger.info(f"Parameters: temperature={temperature}, top_p={top_p}, max_tokens={max_new_tokens}")
    logger.info(f"Gold index (target KV position): {gold_index}")

    responses = []
    failed_indices = []

    # Note: Ollama doesn't support batching, so we process sequentially
    for idx, prompt in enumerate(tqdm(prompts, desc="Generating responses")):
        try:
            response = query_ollama_model(
                model=model_name,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_new_tokens,
                top_p=top_p,
                timeout=request_timeout,
            )
            responses.append(response)
        except (OllamaConnectionError, OllamaAPIError) as e:
            logger.error(f"Error generating response for example {idx}: {e}")
            # Store empty response and mark as failed
            responses.append("")
            failed_indices.append(idx)

            # If too many failures, abort
            if len(failed_indices) > len(prompts) * 0.1:  # More than 10% failure rate
                logger.error(f"Too many failures ({len(failed_indices)}/{len(prompts)}). Aborting.")
                raise

    if failed_indices:
        logger.warning(f"Failed to generate responses for {len(failed_indices)} examples: {failed_indices}")

    # Write outputs
    logger.info(f"Writing outputs to {output_path}")
    with xopen(output_path, "w") as f:
        for example, ordered_kv_records, prompt, response in zip(
            examples, all_model_ordered_kv_records, prompts, responses
        ):
            output_example = deepcopy(example)
            # Add some extra metadata to the output example
            output_example["model_prompt"] = prompt
            output_example["model_ordered_kv_records"] = ordered_kv_records
            output_example["model_answer"] = response
            output_example["model"] = model_name
            output_example["model_temperature"] = temperature
            output_example["model_top_p"] = top_p
            output_example["gold_index"] = gold_index
            f.write(json.dumps(output_example) + "\n")

    logger.info(f"Successfully wrote {len(responses)} responses to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)
    parser = argparse.ArgumentParser(description="Generate KV retrieval responses using Ollama models")

    parser.add_argument(
        "--input-path",
        help="Path to data with KV records.",
        required=True
    )
    parser.add_argument(
        "--model",
        help="Ollama model to use in generating responses (e.g., qwen3.5:27b, mistral-small:22b)",
        required=True,
    )
    parser.add_argument(
        "--temperature",
        help="Temperature to use in generation (0.0 = greedy/deterministic)",
        type=float,
        default=0.0
    )
    parser.add_argument(
        "--top-p",
        help="Top-p to use in generation",
        type=float,
        default=1.0
    )
    parser.add_argument(
        "--gold-index",
        help="Index at which to place the target KV pair (0-indexed)",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--query-aware-contextualization",
        action="store_true",
        help="Place the query both before and after the KV records.",
    )
    parser.add_argument(
        "--output-path",
        help="Path to write output file of generated responses",
        required=True
    )
    parser.add_argument(
        "--max-new-tokens",
        help="Maximum number of new tokens to generate",
        type=int,
        default=50,  # KV responses are shorter (just UUIDs)
    )
    parser.add_argument(
        "--request-timeout",
        help="Timeout for each Ollama API request in seconds",
        type=int,
        default=300,
    )

    args = parser.parse_args()

    logger.info("running %s", " ".join(sys.argv))
    try:
        main(
            args.input_path,
            args.model,
            args.temperature,
            args.top_p,
            args.gold_index,
            args.query_aware_contextualization,
            args.max_new_tokens,
            args.output_path,
            args.request_timeout,
        )
        logger.info("finished running %s", sys.argv[0])
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
