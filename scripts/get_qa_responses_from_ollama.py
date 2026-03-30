#!/usr/bin/env python3
"""Given a data file with questions and retrieval results, run Ollama models to get responses.

This script adapts the original MPT/LongChat scripts to use Ollama models instead of
HuggingFace models. It maintains the same data format and evaluation compatibility.

Supports any Ollama model (e.g., qwen3.5:27b, mistral-small:22b, qwen3.5:4b).
The retrieval results are used in the exact order that they're given.
"""
import argparse
import dataclasses
import json
import logging
import pathlib
import random
import sys
from copy import deepcopy

from tqdm import tqdm
from xopen import xopen

from lost_in_the_middle.prompting import (
    Document,
    get_closedbook_qa_prompt,
    get_qa_prompt,
)
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
    closedbook,
    prompt_mention_random_ordering,
    use_random_ordering,
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
    all_model_documents = []

    # Fetch all of the prompts
    logger.info(f"Loading examples from {input_path}")
    with xopen(input_path) as fin:
        for line in tqdm(fin, desc="Loading data"):
            input_example = json.loads(line)
            # Get the prediction for the input example
            question = input_example["question"]

            if closedbook:
                documents = []
            else:
                documents = []
                for ctx in deepcopy(input_example["ctxs"]):
                    documents.append(Document.from_dict(ctx))
                if not documents:
                    raise ValueError(f"Did not find any documents for example: {input_example}")

            if use_random_ordering:
                # Randomly order only the distractors (isgold is False), keeping isgold documents
                # at their existing index
                (original_gold_index,) = [idx for idx, doc in enumerate(documents) if doc.isgold is True]
                original_gold_document = documents[original_gold_index]
                distractors = [doc for doc in documents if doc.isgold is False]
                random.shuffle(distractors)
                distractors.insert(original_gold_index, original_gold_document)
                documents = distractors

            if closedbook:
                prompt = get_closedbook_qa_prompt(question)
            else:
                prompt = get_qa_prompt(
                    question,
                    documents,
                    mention_random_ordering=prompt_mention_random_ordering,
                    query_aware_contextualization=query_aware_contextualization,
                )

            prompts.append(prompt)
            examples.append(deepcopy(input_example))
            all_model_documents.append(documents)

    # Get responses for all of the prompts
    logger.info(f"Generating responses for {len(prompts)} prompts using {model_name}")
    logger.info(f"Parameters: temperature={temperature}, top_p={top_p}, max_tokens={max_new_tokens}")

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
        for example, model_documents, prompt, response in zip(examples, all_model_documents, prompts, responses):
            output_example = deepcopy(example)
            # Add some extra metadata to the output example
            output_example["model_prompt"] = prompt
            output_example["model_documents"] = [dataclasses.asdict(document) for document in model_documents]
            output_example["model_answer"] = response
            output_example["model"] = model_name
            output_example["model_temperature"] = temperature
            output_example["model_top_p"] = top_p
            output_example["model_prompt_mention_random_ordering"] = prompt_mention_random_ordering
            output_example["model_use_random_ordering"] = use_random_ordering
            f.write(json.dumps(output_example) + "\n")

    logger.info(f"Successfully wrote {len(responses)} responses to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)
    parser = argparse.ArgumentParser(description="Generate QA responses using Ollama models")

    parser.add_argument(
        "--input-path",
        help="Path to data with questions and documents to use.",
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
        "--closedbook",
        action="store_true",
        help="Run the model in closed-book mode (i.e., don't use documents)."
    )
    parser.add_argument(
        "--prompt-mention-random-ordering",
        action="store_true",
        help="Mention that search results are ordered randomly in the prompt",
    )
    parser.add_argument(
        "--use-random-ordering",
        action="store_true",
        help="Randomize the ordering of the distractors, rather than sorting by relevance.",
    )
    parser.add_argument(
        "--query-aware-contextualization",
        action="store_true",
        help="Place the question both before and after the documents.",
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
        default=100,
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
            args.closedbook,
            args.prompt_mention_random_ordering,
            args.use_random_ordering,
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
