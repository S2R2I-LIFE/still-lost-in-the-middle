# Lost in the Middle: How Language Models Use Long Contexts

## Executive Summary

This research investigates a critical limitation in modern large language models (LLMs): while recent models can accept very long input contexts (up to 100K tokens), they struggle to effectively use information throughout that context. The study reveals that LLMs exhibit a **U-shaped performance curve** - they perform best when relevant information appears at the beginning or end of their input, but performance degrades significantly (sometimes by over 20%) when the same information is placed in the middle of long contexts.

This has major implications for retrieval-augmented generation (RAG) systems, search applications, and any use case involving long documents or multiple retrieved passages.

## Key Findings

### The U-Shaped Performance Curve

The most striking finding is the **U-shaped performance pattern** across multiple models and tasks:

- **Primacy bias**: Models perform well when relevant information is at the start of the input
- **Recency bias**: Models perform well when relevant information is at the end of the input
- **Middle degradation**: Performance drops dramatically when relevant information is in the middle

**Quantitative example**: GPT-3.5-Turbo's accuracy on multi-document QA tasks:
- Best case (info at start/end): ~65-70% accuracy
- Worst case (info in middle): ~45% accuracy (with 30 documents)
- Closed-book baseline (no context): 56.1% accuracy

In the worst cases, providing context actually *hurt* performance compared to using no context at all.

### Extended Context ≠ Better Context Usage

Perhaps surprisingly, models with extended context windows (16K, 100K tokens) performed nearly identically to their standard counterparts when both could fit the same input:

- GPT-3.5-Turbo (4K) vs GPT-3.5-Turbo (16K): Nearly superimposed performance curves
- Claude-1.3 (8K) vs Claude-1.3 (100K): Similar patterns

**Implication**: Training models to handle longer contexts doesn't automatically make them better at using that context.

### Architecture Matters (With Caveats)

**Encoder-decoder models** (like Flan-T5, Flan-UL2) showed more robust performance than decoder-only models, but only within their training sequence length:

- Within training length (≤2048 tokens): Nearly flat performance across positions (1.9% variance)
- Beyond training length: U-shaped curve reappears

**Hypothesis**: Bidirectional encoding allows better relative importance estimation between documents.

### Query-Aware Contextualization Impact

Placing the query/question both before and after the context documents had mixed results:

- **Key-value retrieval**: Dramatic improvement - achieved near-perfect performance (e.g., GPT-3.5-Turbo went from 45.6% worst-case to 100%)
- **Multi-document QA**: Minimal impact on overall trends

### Instruction Fine-Tuning Doesn't Fix It

Comparing base models (MPT-30B) with instruction-tuned versions (MPT-30B-Instruct):

- Both exhibited the U-shaped curve
- Instruction tuning slightly reduced worst-case disparity (from ~10% to ~4%)
- Base models showed stronger recency bias, while instruction-tuned models developed primacy bias too

### Model Scale Matters

Analysis of Llama-2 models across sizes:

- **7B models**: Only recency-biased (right side of U-curve)
- **13B and 70B models**: Full U-shaped curve with both primacy and recency bias

The U-shaped pattern only emerges at sufficient model scale.

## Experimental Setup

### Task 1: Multi-Document Question Answering

**Design**:
- Input: A question + k documents (Wikipedia passages, max 100 tokens each)
- Context: Exactly 1 document contains the answer, k-1 are distractors
- Variable: Position of the answer-containing document (beginning, middle, end)
- Variable: Number of total documents (10, 20, 30)

**Dataset**: 2,655 queries from NaturalQuestions-Open with paragraph-length answers

**Distractor selection**: Used Contriever (fine-tuned on MS-MARCO) to retrieve relevant but answer-less passages, ordered by decreasing relevance

**Evaluation metric**: Accuracy - whether any correct answer appears in model output

**Baselines**:
- **Closed-book**: No documents, relying on parametric memory
- **Oracle**: Single document containing the answer

### Task 2: Key-Value Retrieval

**Design**:
- Input: JSON object with k key-value pairs (all random UUIDs) + target key
- Goal: Return the value associated with the specified key
- Variable: Position of target key-value pair in the JSON
- Variable: Number of total pairs (75, 140, 300)

**Rationale**: Minimal testbed for basic retrieval ability, removing confounding linguistic features by using random UUIDs instead of natural language

**Evaluation metric**: Accuracy - whether correct value appears in output

### Models Tested

**Closed (API-based)**:
- GPT-3.5-Turbo (4K context)
- GPT-3.5-Turbo (16K context)
- Claude-1.3 (8K context)
- Claude-1.3 (100K context)

**Open-source**:
- MPT-30B-Instruct (8K context, ALiBi positional embeddings)
- LongChat-13B-16K (16K context, extended LLaMA-13B with condensed rotary embeddings)
- Flan-T5-XXL (512 tokens, encoder-decoder)
- Flan-UL2 (2048 tokens, encoder-decoder)
- Llama-2 family (7B, 13B, 70B - for ablation studies)

**Generation settings**: Greedy decoding (temperature = 0) for reproducibility

## Results Summary

### Multi-Document QA Performance

**GPT-3.5-Turbo (30 documents)**:
- Position 0 (start): ~62% accuracy
- Position 15 (middle): ~42% accuracy
- Position 29 (end): ~70% accuracy
- 28% absolute difference between best and worst

**Claude-1.3** showed similar but slightly less pronounced patterns

**MPT-30B-Instruct** exhibited the strongest U-shape with largest performance drops in the middle

### Key-Value Retrieval Performance

**Claude models**: Near-perfect performance (~100%) across all positions and context lengths

**GPT-3.5-Turbo (300 KV pairs)**:
- Best case: ~85% accuracy
- Worst case (middle): ~45% accuracy

**MPT-30B-Instruct**: Similar U-shaped degradation

**LongChat-13B**: Exhibited unusual behavior - generated code to retrieve keys instead of returning values directly when info was at the start

### Open-Domain QA Case Study

Tested how many retrieved documents actually help performance:

**Finding**: Reader performance saturates far before retrieval recall
- Using 50 documents vs 20 documents: Only ~1-1.5% improvement
- But significantly increased latency and cost

**Implication**: More context isn't always better - there's a point of diminishing returns

## Implications for Practice

### For RAG Systems

1. **Document positioning matters**: Place most relevant documents at the start or end of prompts, not the middle
2. **Reranking is critical**: Push relevant information closer to the boundaries
3. **Truncation strategies**: Consider retrieving fewer, better-ordered documents rather than many documents

### For Long-Context Applications

1. **Don't assume extended context = better usage**: A model with 100K context window doesn't necessarily use it well
2. **Test position-invariance**: When evaluating long-context models, test whether performance remains stable regardless of where information appears
3. **Practical limits exist**: Even if a model *can* take 16K tokens, effectiveness may plateau much earlier

### For Model Development

1. **New evaluation protocols needed**: Position-variance should be a standard benchmark
2. **Architectural considerations**: Encoder-decoder architectures may be more robust (within training lengths)
3. **Query-aware techniques**: For retrieval tasks, bidirectional processing helps

### General Recommendations

- **Design prompts strategically**: Don't assume the model will "find" information anywhere in the context
- **Monitor real-world performance**: The U-shaped curve may explain unexpected failures in production
- **Consider cost-effectiveness**: Adding more context increases cost/latency but may not improve accuracy

## Connection to Psychology: The Serial-Position Effect

The researchers note an interesting parallel to human memory research. In psychology, the **serial-position effect** (Ebbinghaus, 1913; Murdock, 1962) describes how humans better remember the first and last items in a list compared to middle items.

The emergence of this pattern in LLMs is somewhat surprising because Transformer self-attention mechanisms are theoretically equally capable of attending to any token in the context - there's no architectural reason for position to matter. Yet the U-shaped curve persists.

## Limitations and Future Work

### What This Study Didn't Cover

- **Decoding strategies**: Only tested greedy decoding; sampling strategies might behave differently
- **Other task types**: Focused on QA and retrieval; summarization, reasoning, etc. may show different patterns
- **Fine-tuning approaches**: Different instruction-tuning methods might mitigate position bias
- **Prompt engineering**: Alternative prompt formats might improve middle-context usage

### Open Questions

1. Can we train models to be truly position-invariant?
2. Do attention patterns reveal why middle information is ignored?
3. Can architectural modifications (e.g., hybrid encoder-decoder designs) solve this?
4. How do chain-of-thought or reasoning approaches interact with position bias?

## Conclusion

The "Lost in the Middle" phenomenon reveals a fundamental limitation in current language models: **they cannot robustly access information throughout their context windows**. While models advertise long context capabilities, their actual ability to *use* that context degrades significantly based on where information appears.

For practitioners, this means:
- **Be strategic about context organization** - don't treat the context window as a uniform space
- **Question the value of extended contexts** - longer isn't always better
- **Design with position in mind** - place critical information at boundaries

For researchers, this establishes **position-invariance as a key evaluation criterion** for future long-context models. A model that can *accept* 100K tokens but can't reliably use information from the middle is not truly a long-context model.

The research provides both a warning and a roadmap: current models have significant limitations, but understanding these limitations enables better system design and points toward architectural and training improvements that could make LLMs more robust long-context reasoners.

---

**Citation**: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *arXiv preprint arXiv:2307.03172*.
