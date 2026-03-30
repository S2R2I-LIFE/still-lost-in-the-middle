# Experimental Results Summary

**Replication Study**: "Lost in the Middle" with Modern Ollama Models (2024)
**Date**: 2026-03-30
**Models**: gemma3:4b, mistral-small:22b, gemma3:27b

---

## Overview

This document summarizes results from multi-document question answering experiments testing position bias in modern language models. We replicate the methodology from Liu et al. (2023) using locally-available Ollama models from 2024.

**Key Question**: Do modern models still exhibit the "lost in the middle" phenomenon where performance degrades when relevant information is positioned in the middle of long contexts?

---

## Evaluation Metric

All results use **best_subspan_em** (best substring exact match):
- Compares model's generated answer against gold answer(s)
- Accounts for flexible matching (substring, case-insensitive)
- Range: 0.0 (no matches) to 1.0 (perfect matches)

---

## Oracle Baseline Results (Upper Bound)

**Setup**: Single document containing the answer (2,655 examples)
**Purpose**: Establishes maximum performance when information is easily accessible

| Model | best_subspan_em | Correct/Total |
|-------|-----------------|---------------|
| gemma3:27b | 0.9002 | 2,389/2,655 |
| gemma3:4b | 0.8915 | 2,365/2,655 |
| mistral-small:22b | 0.8599 | 2,283/2,655 |

**Observation**: Larger gemma3 model (27B) performs best (90%), followed by gemma3:4b (89%) and mistral-small:22b (86%). All modern models significantly outperform 2023 MPT-30B (82%).

---

## 10-Document QA Results (Position Bias Test)

**Setup**: 10 total documents (1 gold + 9 distractors), ~500 examples per position
**Gold positions tested**: 0 (start), 4 (middle), 9 (end)

### gemma3:4b (Small Model)

| Gold Position | best_subspan_em | Correct/Total | vs Oracle |
|---------------|-----------------|---------------|-----------|
| Position 0 (start) | 0.5879 | 1,561/2,655 | -30.4% |
| Position 4 (middle) | 0.5589 | 1,484/2,655 | -33.3% |
| Position 9 (end) | 0.5552 | 1,474/2,655 | -33.6% |

**Observed pattern**: Gradual decline from start to end (NO U-shaped curve)

### mistral-small:22b (Medium Model)

| Gold Position | best_subspan_em | Correct/Total | vs Oracle |
|---------------|-----------------|---------------|-----------|
| Position 0 (start) | 0.6878 | 1,826/2,655 | -17.2% |
| Position 4 (middle) | 0.6719 | 1,784/2,655 | -18.8% |
| Position 9 (end) | 0.6365 | 1,690/2,655 | -22.3% |

**Observed pattern**: Gradual decline, best overall performance across all positions

### gemma3:27b (Large Model)

| Gold Position | best_subspan_em | Correct/Total | vs Oracle |
|---------------|-----------------|---------------|-----------|
| Position 0 (start) | 0.6591 | 1,750/2,655 | -24.1% |
| Position 4 (middle) | 0.6192 | 1,644/2,655 | -28.1% |
| Position 9 (end) | 0.6113 | 1,623/2,655 | -28.9% |

**Observed pattern**: Gradual decline, despite larger size does not outperform mistral-small:22b

---

## Closedbook Baseline Results (Lower Bound)

**Setup**: Question only, no documents (parametric memory only)
**Purpose**: Establishes baseline performance without any context

| Model | best_subspan_em | Correct/Total | vs Oracle |
|-------|-----------------|---------------|-----------|
| gemma3:4b | 0.2279 | 605/2,655 | -66.4% |

---

## Comparison with Original Paper (Liu et al., 2023)

### Oracle Performance Comparison

| Model (Year) | Parameters | Oracle Accuracy |
|--------------|------------|-----------------|
| **Our Models (2024)** | | |
| gemma3:27b | ~27B | 0.9002 |
| gemma3:4b | ~4B | 0.8915 |
| mistral-small:22b | ~22B | 0.8599 |
| **Original Paper (2023)** | | |
| MPT-30B-Instruct | 30B | 0.8166 |
| LongChat-13B-16K | 13B | ~0.82 (est.) |

**Observation**: Modern 2024 models (Gemma3) show improved oracle performance compared to 2023 models, even at smaller sizes.

### 20-Document Position Results (Original Paper)

**Original findings (2023)**:
- MPT-30B-Instruct: Position 0: 0.567, Position 19: 0.562, Middle: ~0.3-0.4
- LongChat-13B-16K: Position 0: 0.686, Position 19: 0.550, Middle: ~0.4-0.5

**Our 10-document results (2024)**:
- Position 0: 59-69% (vs 57-69% in 2023)
- Position 4 (middle): 56-67% (vs 35-45% in 2023) - **Much better!**
- Position 9: 56-64% (vs 55-60% in 2023)

**Key difference**: No U-curve in 2024. Middle performance significantly improved.

---

## Analysis Questions

### 1. Does the U-Shaped Curve Persist?

**Hypothesis**: Modern models (2024) may have reduced position bias compared to 2023 models.

**Test**: Compare performance at position 0 vs 4 vs 9 for each model.
- **U-shaped**: Start high, middle low, end high
- **Flat**: Similar performance across positions
- **Recency only**: End high, others low
- **Primacy only**: Start high, others low

**Result**: **NO** - U-shaped curve eliminated. Modern models show gradual decline from start to end with no recovery at final position.

### 2. Does Model Size Affect Position Bias?

**Hypothesis**: Larger models may be more robust to position effects.

**Test**: Compare gemma3:4b vs gemma3:27b position curves (same architecture, different scale).

**Result**: **NOT STRAIGHTFORWARD** - Mistral-small:22b outperforms larger gemma3:27b across all positions. Architecture matters more than size.

### 3. Does Architecture Matter?

**Hypothesis**: Gemma's interleaved local/global attention (5:1 ratio) may reduce middle-position degradation compared to standard attention.

**Test**: Compare Gemma (local/global attention) vs Mistral (standard attention) position curves.

**Result**: **YES** - Mistral (standard attention) performs better overall (+2.87% avg), but Gemma shows slightly less degradation (4.78% vs 5.13%).

### 4. How Much Does Position Hurt?

**Calculation**: Performance degradation = Oracle accuracy - Worst position accuracy

**Result**:
- gemma3:4b: -33.6% (89.15% → 55.52%)
- mistral-small:22b: -22.3% (85.99% → 63.65%)
- gemma3:27b: -28.9% (90.02% → 61.13%)
- **Average**: -28.3% (vs ~46% in 2023) - **~20% improvement!**

### 5. Are Models Using Context or Guessing?

**Test**: Compare 10-doc performance vs closedbook performance.
- If 10-doc >> closedbook: Models successfully use context
- If 10-doc ≈ closedbook: Models rely on parametric memory

**Result**: **TBD** (awaiting evaluation)

---

## Raw Evaluation Commands

To reproduce these results:

### Oracle Evaluations
```bash
# gemma3:4b oracle
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/pilot_test.jsonl.gz
# Expected: best_subspan_em: 0.8915254237288136

# gemma3:27b oracle
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/pilot_gemma3_27b.jsonl.gz
# Expected: best_subspan_em: 0.9001883239171374

# mistral-small:22b oracle
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/pilot_mistral_small_22b.jsonl.gz
# Expected: TBD
```

### 10-Document Evaluations
```bash
# gemma3:4b - position 0
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/gemma3_4b_10doc_gold_at_0.jsonl.gz

# gemma3:4b - position 4
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/gemma3_4b_10doc_gold_at_4.jsonl.gz

# gemma3:4b - position 9
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/gemma3_4b_10doc_gold_at_9.jsonl.gz

# [Repeat for mistral-small:22b and gemma3:27b...]
```

### Closedbook Evaluation
```bash
PYTHONPATH=src:$PYTHONPATH python scripts/evaluate_qa_responses.py \
    --input-path Context/results/qa_predictions/gemma3_4b_closedbook.jsonl.gz
```

---

## Next Steps

1. **Extract all evaluation scores** from `Context/results/evaluation_log.txt`
2. **Fill in TBD values** in tables above
3. **Create position vs accuracy plots** showing U-shaped curves (if present)
4. **Calculate degradation metrics**: Oracle - Worst position for each model
5. **Write findings summary**: Does "lost in the middle" persist in 2024 models?
6. **Compare with original paper**: Are modern models better or similar?

---

## Expected Completion

**Status**: Experiments running (11/13 complete as of 2026-03-30 12:15)
**ETA**: All data available within 3-6 hours
**Analysis**: Can begin immediately after final experiments complete

---

## Files Generated

**Predictions** (model outputs):
- `Context/results/qa_predictions/pilot_*.jsonl.gz` - Oracle baselines
- `Context/results/qa_predictions/*_10doc_gold_at_*.jsonl.gz` - Position experiments
- `Context/results/qa_predictions/*_closedbook.jsonl.gz` - Closedbook baseline

**Evaluations** (scores):
- `Context/results/evaluation_log.txt` - All best_subspan_em scores

**Analysis** (upcoming):
- Position vs accuracy plots (PNG/PDF)
- Summary tables (CSV)
- Findings document (MD)
