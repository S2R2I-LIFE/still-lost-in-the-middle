# Experimental Plan: "Lost in the Middle" Replication with Ollama Models

## Overview

This document specifies the detailed experimental protocol for replicating the "Lost in the Middle" research using locally-available Ollama models. The experiments follow the original paper's methodology while adapting to local inference constraints.

**Status**: Phase 1 (Documentation) - Not yet implemented
**Last Updated**: 2026-03-29

---

## Research Questions

1. **Do modern Ollama models (2024-2025) exhibit the same U-shaped performance curve as 2023 models?**
2. **Does model size (4B vs 22B vs 27B parameters) affect position bias?**
3. **Are the results comparable to the original GPT-3.5-Turbo and Claude-1.3 findings?**
4. **Do query-aware contextualization techniques help Ollama models?**

---

## Experimental Design

### Models Under Test

1. **qwen3.5:27b** (Large tier, 27B parameters)
2. **mistral-small:22b** (Medium tier, 22B parameters)
3. **qwen3.5:4b** (Small tier, 4B parameters)

See `models.txt` for detailed model specifications and rationale.

### Tasks

We replicate two tasks from the original paper:

1. **Multi-Document Question Answering** (Primary task)
2. **Key-Value Retrieval** (Synthetic retrieval task)

---

## Task 1: Multi-Document Question Answering

### Dataset

**Source**: NaturalQuestions-Open
- **Total examples**: 2,655 queries (paragraphs only, no tables/lists)
- **Base dataset**: NQ-Open queries with annotated Wikipedia answers
- **Document format**: Wikipedia passages (chunks ≤100 tokens)

### Document Configurations

Three context length settings:
- **10 total documents**: 1 gold + 9 distractors
- **20 total documents**: 1 gold + 19 distractors
- **30 total documents**: 1 gold + 29 distractors

### Gold Document Positions

For each context length, test multiple positions of the gold (answer-containing) document:

**10 documents** (positions 0-9):
- Position 0 (start)
- Position 4 (early-middle)
- Position 9 (end)

**20 documents** (positions 0-19):
- Position 0 (start)
- Position 4 (early)
- Position 9 (early-middle)
- Position 14 (late-middle)
- Position 19 (end)

**30 documents** (positions 0-29):
- Position 0 (start)
- Position 4 (early)
- Position 9 (early-middle)
- Position 14 (middle)
- Position 19 (late-middle)
- Position 24 (late)
- Position 29 (end)

**Total QA dataset files**: 15 position variants across 3 context lengths

### Baseline Conditions

**Oracle setting**:
- Input: Question + single gold document only
- Purpose: Upper bound on performance
- Dataset: `nq-open-oracle.jsonl.gz`

**Closedbook setting**:
- Input: Question only, no documents
- Purpose: Parametric knowledge baseline
- Implementation: Use standard QA prompts without document context

### Experimental Conditions

**Standard prompting**:
- Query appears before documents
- Format: "Question: [Q]\n\nDocuments:\n[Doc1]\n[Doc2]...\nAnswer:"

**Query-aware contextualization** (optional, Phase 2 extension):
- Query appears both before AND after documents
- Format: "Question: [Q]\n\nDocuments:\n[Doc1]...\nQuestion: [Q]\nAnswer:"
- Tests whether bidirectional context helps

### Available Dataset Files

```
qa_data/
├── nq-open-oracle.jsonl.gz                                    # Oracle baseline
├── 10_total_documents/
│   ├── nq-open-10_total_documents_gold_at_0.jsonl.gz
│   ├── nq-open-10_total_documents_gold_at_4.jsonl.gz
│   └── nq-open-10_total_documents_gold_at_9.jsonl.gz
├── 20_total_documents/
│   ├── nq-open-20_total_documents_gold_at_0.jsonl.gz
│   ├── nq-open-20_total_documents_gold_at_4.jsonl.gz
│   ├── nq-open-20_total_documents_gold_at_9.jsonl.gz
│   ├── nq-open-20_total_documents_gold_at_14.jsonl.gz
│   └── nq-open-20_total_documents_gold_at_19.jsonl.gz
└── 30_total_documents/
    ├── nq-open-30_total_documents_gold_at_0.jsonl.gz
    ├── nq-open-30_total_documents_gold_at_4.jsonl.gz
    ├── nq-open-30_total_documents_gold_at_9.jsonl.gz
    ├── nq-open-30_total_documents_gold_at_14.jsonl.gz
    ├── nq-open-30_total_documents_gold_at_19.jsonl.gz
    ├── nq-open-30_total_documents_gold_at_24.jsonl.gz
    └── nq-open-30_total_documents_gold_at_29.jsonl.gz
```

### Evaluation Metric

**Accuracy**: Does any correct answer (from NQ annotations) appear in model output?
- Binary: 1 if answer present, 0 otherwise
- Allows for flexible answer formats
- Same metric as original paper

### Expected Outputs

For each model × dataset combination:
- **Predictions file**: `[model]_[dataset]_predictions.jsonl.gz`
- **Contains**: Question, gold answer(s), model prediction, correctness score

Example prediction format:
```json
{
  "question": "Who wrote the novel 'Pride and Prejudice'?",
  "answers": ["Jane Austen"],
  "model_prediction": "Jane Austen wrote Pride and Prejudice...",
  "correct": 1,
  "model": "qwen3.5:27b",
  "dataset": "nq-open-10_total_documents_gold_at_0"
}
```

---

## Task 2: Key-Value Retrieval

### Dataset

**Synthetic data**: JSON objects with random UUID key-value pairs
- **Purpose**: Minimal testbed for basic retrieval ability
- **Format**: String-serialized JSON with k key-value pairs
- **Keys/Values**: Random UUIDs (no semantic meaning)

### Context Length Settings

Three KV pair counts:
- **75 key-value pairs** (smallest setting)
- **140 key-value pairs** (medium setting)
- **300 key-value pairs** (largest setting)

### Target Position Manipulation

For each context length, vary position of the target key-value pair throughout the JSON object.

**Note**: Dataset files already contain position-varied examples.

### Available Dataset Files

```
kv_retrieval_data/
├── kv-retrieval-75_keys.jsonl.gz
├── kv-retrieval-140_keys.jsonl.gz
└── kv-retrieval-300_keys.jsonl.gz
```

**Examples per file**: 500 (as per original paper)

### Evaluation Metric

**Accuracy**: Does the correct UUID value appear in model output?
- Binary: 1 if correct value present, 0 otherwise
- Tests pure retrieval capability

### Expected Outputs

For each model × dataset combination:
- **Predictions file**: `[model]_kv-retrieval-[N]_keys_predictions.jsonl.gz`

Example prediction format:
```json
{
  "key": "a3f2c1e5-...",
  "correct_value": "9b7e4d2a-...",
  "model_prediction": "9b7e4d2a-...",
  "correct": 1,
  "model": "mistral-small:22b",
  "num_keys": 140
}
```

---

## Execution Plan

### Phase 2.1: Pilot Run (Validation)

**Purpose**: Verify implementation before full experiments

**Models**: qwen3.5:4b only (fastest inference)

**Datasets**:
- Oracle: `nq-open-oracle.jsonl.gz`
- 10 docs, position 0: `nq-open-10_total_documents_gold_at_0.jsonl.gz`
- KV 75 keys: `kv-retrieval-75_keys.jsonl.gz`

**Success Criteria**:
- Scripts run without errors
- Output format matches expected schema
- Evaluation scripts successfully score predictions
- Results are qualitatively reasonable (oracle >> 10-doc >> closedbook)

**Estimated Time**: 1-2 hours

### Phase 2.2: Medium Run (Core Results)

**Purpose**: Generate main experimental results

**Models**: All three (qwen3.5:4b, mistral-small:22b, qwen3.5:27b)

**Datasets**:
- All multi-doc QA positions (15 files)
- Oracle baseline (1 file)
- All KV retrieval settings (3 files)

**Not included**: Closedbook, query-aware variants (Phase 2.3)

**Estimated Time**: 24-48 hours of continuous inference (model-dependent)

### Phase 2.3: Extended Run (Optional Extensions)

**Additional conditions**:
- Closedbook baseline (QA with no documents)
- Query-aware contextualization (if helpful in pilot)

**Estimated Time**: Additional 12-24 hours

---

## Detailed Execution Protocol

### Pre-Execution Checklist

- [ ] Ollama service is running (`ollama list`)
- [ ] All three models are pulled locally
- [ ] Sufficient disk space for outputs (~5-10GB)
- [ ] Sufficient VRAM/RAM for largest model (24GB+)
- [ ] Git worktree or branch created for code changes (isolate Phase 2 work)

### Per-Model Execution Steps

1. **Verify model availability**:
   ```bash
   ollama list | grep [model_name]
   ```

2. **Run oracle baseline** (sanity check):
   ```bash
   python scripts/get_qa_responses_from_ollama.py \
       --model [model_name] \
       --input-path qa_data/nq-open-oracle.jsonl.gz \
       --output-path Context/results/qa_predictions/[model]_oracle.jsonl.gz \
       --temperature 0.0 \
       --max-new-tokens 100
   ```

3. **Run multi-doc QA experiments** (loop over positions):
   ```bash
   for pos_file in qa_data/10_total_documents/*.jsonl.gz; do
       python scripts/get_qa_responses_from_ollama.py \
           --model [model_name] \
           --input-path "$pos_file" \
           --output-path Context/results/qa_predictions/[model]_$(basename $pos_file) \
           --temperature 0.0 \
           --max-new-tokens 100
   done
   ```

4. **Run KV retrieval experiments**:
   ```bash
   for kv_file in kv_retrieval_data/*.jsonl.gz; do
       python scripts/get_kv_responses_from_ollama.py \
           --model [model_name] \
           --input-path "$kv_file" \
           --output-path Context/results/kv_predictions/[model]_$(basename $kv_file) \
           --temperature 0.0 \
           --max-new-tokens 50
   done
   ```

5. **Evaluate predictions**:
   ```bash
   python scripts/evaluate_qa_responses.py \
       --input-path Context/results/qa_predictions/[model]_*.jsonl.gz \
       --output-path Context/results/evaluation_scores/[model]_qa_scores.csv

   python scripts/evaluate_kv_responses.py \
       --input-path Context/results/kv_predictions/[model]_*.jsonl.gz \
       --output-path Context/results/evaluation_scores/[model]_kv_scores.csv
   ```

### Automation Script (Batch Execution)

See Phase 2 deliverable: `scripts/run_ollama_experiments.sh`

This script will:
- Loop over all models
- Run all QA and KV experiments
- Automatically evaluate results
- Log progress and errors
- Estimate remaining time

---

## Inference Parameters

### Standard Settings (Match Original Paper)

```python
{
    "temperature": 0.0,        # Greedy decoding (deterministic)
    "max_new_tokens": 100,     # For QA (answers are typically short)
    "max_new_tokens": 50,      # For KV (UUIDs are 36 chars)
    "top_p": 1.0,              # Not used with temperature=0
    "top_k": None,             # Not used with temperature=0
    "stop_sequences": ["\n\n"] # Optional: stop at double newline
}
```

### Ollama API Call Format

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3.5:27b",
  "prompt": "[formatted prompt with question and documents]",
  "stream": false,
  "options": {
    "temperature": 0.0,
    "num_predict": 100
  }
}'
```

---

## Output Directory Structure

```
Context/results/
├── qa_predictions/
│   ├── qwen3.5_27b_oracle.jsonl.gz
│   ├── qwen3.5_27b_10_total_documents_gold_at_0.jsonl.gz
│   ├── qwen3.5_27b_10_total_documents_gold_at_4.jsonl.gz
│   ├── ... (all position variants, all models)
│   ├── mistral-small_22b_oracle.jsonl.gz
│   ├── ... (all datasets for mistral)
│   └── qwen3.5_4b_oracle.jsonl.gz
│       └── ... (all datasets for qwen small)
├── kv_predictions/
│   ├── qwen3.5_27b_kv-retrieval-75_keys.jsonl.gz
│   ├── qwen3.5_27b_kv-retrieval-140_keys.jsonl.gz
│   ├── qwen3.5_27b_kv-retrieval-300_keys.jsonl.gz
│   └── ... (all KV settings, all models)
├── evaluation_scores/
│   ├── qwen3.5_27b_qa_scores.csv
│   ├── qwen3.5_27b_kv_scores.csv
│   ├── mistral-small_22b_qa_scores.csv
│   ├── mistral-small_22b_kv_scores.csv
│   ├── qwen3.5_4b_qa_scores.csv
│   └── qwen3.5_4b_kv_scores.csv
├── analysis/
│   ├── position_bias_analysis.ipynb    # Jupyter notebook for analysis
│   ├── plot_u_curve.py                 # Script to generate plots
│   └── comparative_analysis.py         # Compare with original paper
└── summary/
    └── final_results.md                # Final summary report
```

---

## Data Logging Requirements

For each inference run, log:

1. **Model metadata**:
   - Model name and version
   - Parameter count
   - Context window size
   - Ollama version

2. **Runtime metrics**:
   - Start/end timestamps
   - Total inference time
   - Tokens per second (if available)
   - VRAM usage (peak)

3. **Dataset metadata**:
   - Dataset name
   - Number of examples processed
   - Gold position (if applicable)

4. **Error tracking**:
   - Failed examples (if any)
   - Error messages
   - Timeout instances

**Log format**: JSON lines, one entry per dataset run

Example log entry:
```json
{
  "model": "qwen3.5:27b",
  "dataset": "nq-open-10_total_documents_gold_at_0.jsonl.gz",
  "start_time": "2026-03-29T10:00:00Z",
  "end_time": "2026-03-29T12:30:00Z",
  "duration_seconds": 9000,
  "examples_processed": 2655,
  "tokens_per_second": 15.2,
  "peak_vram_gb": 22.4,
  "errors": 0
}
```

---

## Analysis Plan (Phase 3)

After data collection, perform:

1. **Position bias analysis**:
   - Plot accuracy vs. gold position for each model/context length
   - Identify U-shaped curves
   - Calculate best-case vs. worst-case disparity

2. **Model size comparison**:
   - Compare 4B vs 22B vs 27B at same positions
   - Test hypothesis: larger models = less position bias?

3. **Comparison with original paper**:
   - Overlay Ollama results with GPT-3.5-Turbo/Claude-1.3 curves
   - Quantify improvement (if any) in modern models

4. **Context length effects**:
   - Compare 10 vs 20 vs 30 document settings
   - Identify saturation points

5. **KV retrieval analysis**:
   - Compare KV results with QA results
   - Identify models with perfect KV retrieval (like Claude-1.3 in original)

---

## Success Criteria

### Minimum Viable Results

- [ ] All 3 models successfully run on all datasets
- [ ] Evaluation metrics computed for all runs
- [ ] At least one clear U-shaped curve observed (validates replication)
- [ ] Results documented in `results_template.md`

### Complete Results

- [ ] All standard conditions tested (QA + KV, all positions)
- [ ] Closedbook baselines computed
- [ ] Comparison plots with original paper generated
- [ ] Statistical analysis completed (variance, significance)
- [ ] Findings written up in final report

### Extended Results (Optional)

- [ ] Query-aware contextualization tested
- [ ] Additional models tested (if informative)
- [ ] Open-domain QA case study replicated

---

## Risk Mitigation

### Potential Issues and Solutions

**Issue**: Ollama API timeouts on long contexts
- **Solution**: Increase timeout limits, reduce batch size to 1

**Issue**: Out of memory errors
- **Solution**: Run models sequentially, use smaller model first, monitor VRAM

**Issue**: Inconsistent outputs (non-deterministic despite temperature=0)
- **Solution**: Run multiple seeds, check Ollama version, verify settings

**Issue**: Evaluation script failures
- **Solution**: Test with oracle first, check output format matches expected schema

**Issue**: Long execution times (days of inference)
- **Solution**: Prioritize 10-doc and 20-doc settings, skip 30-doc if needed

---

## Timeline Estimate (Phase 2 Implementation)

**Week 1**: Code development
- Days 1-2: Implement `ollama_client.py`
- Days 3-4: Adapt QA and KV experiment scripts
- Days 5-7: Testing, debugging, pilot run

**Week 2**: Data collection
- Days 1-2: qwen3.5:4b (small model, fast)
- Days 3-4: mistral-small:22b (medium)
- Days 5-7: qwen3.5:27b (large model, slow)

**Week 3**: Analysis and reporting
- Days 1-3: Evaluate results, generate plots
- Days 4-5: Compare with original paper
- Days 6-7: Write final report, document findings

**Total**: ~3 weeks for complete Phase 2 execution

---

## Appendix: Dataset Statistics

### Multi-Document QA

| Setting        | Gold Positions Tested | Files | Examples per File |
|----------------|-----------------------|-------|-------------------|
| 10 documents   | 0, 4, 9               | 3     | 2,655             |
| 20 documents   | 0, 4, 9, 14, 19       | 5     | 2,655             |
| 30 documents   | 0, 4, 9, 14, 19, 24, 29 | 7   | 2,655             |
| Oracle         | N/A (single doc)      | 1     | 2,655             |
| **Total**      | -                     | **16**| **42,480 examples**|

### Key-Value Retrieval

| Setting  | Files | Examples per File | Positions Tested |
|----------|-------|-------------------|------------------|
| 75 keys  | 1     | 500               | Varied in data   |
| 140 keys | 1     | 500               | Varied in data   |
| 300 keys | 1     | 500               | Varied in data   |
| **Total**| **3** | **1,500 examples**| -                |

### Total Inference Load

**Per model**:
- QA: 16 datasets × 2,655 examples = 42,480 queries
- KV: 3 datasets × 500 examples = 1,500 queries
- **Total per model**: 43,980 queries

**All 3 models**: 131,940 total queries

At ~15 tokens/sec with ~100 tokens per query:
- ~6.7 seconds per query
- ~295,000 seconds total = ~82 hours continuous inference

**Realistic estimate with overhead**: 4-5 days of wall-clock time

---

## Appendix: Comparison with Original Paper

### Original Experiments (2023)

| Model              | Parameters | Context | QA Datasets | KV Datasets | Query-Aware |
|--------------------|------------|---------|-------------|-------------|-------------|
| GPT-3.5-Turbo      | ~175B      | 4K      | ✓           | ✓           | ✓           |
| GPT-3.5-Turbo (16K)| ~175B      | 16K     | ✓           | ✓           | ✓           |
| Claude-1.3         | Unknown    | 8K      | ✓           | ✓           | ✓           |
| Claude-1.3 (100K)  | Unknown    | 100K    | ✓           | ✓           | ✓           |
| MPT-30B-Instruct   | 30B        | 8K      | ✓           | ✓           | ✓           |
| LongChat-13B (16K) | 13B        | 16K     | ✓           | ✓           | ✓           |

### Our Replication (2026)

| Model              | Parameters | Context | QA Datasets | KV Datasets | Query-Aware |
|--------------------|------------|---------|-------------|-------------|-------------|
| qwen3.5:27b        | 27B        | 32K     | ✓           | ✓           | Optional    |
| mistral-small:22b  | 22B        | 32K     | ✓           | ✓           | Optional    |
| qwen3.5:4b         | 4B         | 8-32K   | ✓           | ✓           | Optional    |

**Key Differences**:
- Smaller models overall (4B-27B vs 13B-175B)
- All open-source, local inference
- Longer context windows (32K vs 4-16K)
- Models from 2024-2025 vs 2023
- Query-aware optional (resource constraints)

---

**End of Experimental Plan**

**Next Steps**:
1. Review and approve this plan
2. Proceed to Phase 2 (Code Implementation)
3. Begin with pilot run validation
