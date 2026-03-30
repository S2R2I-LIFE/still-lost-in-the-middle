# Pilot Test Results Summary

**Date**: 2026-03-30
**Phase**: Phase 2 (Implementation) - Pilot Testing
**Dataset**: NaturalQuestions-Open Oracle (single gold document per question)
**Test Size**: 2,655 examples

---

## Executive Summary

Pilot testing revealed a **critical incompatibility** with Qwen models and led to a **model selection revision**. Gemma models perform excellently and are now the primary focus for experiments.

**Key Finding**: All qwen3.5 models are reasoning models that output thinking processes incompatible with the QA evaluation pipeline, resulting in near-zero accuracy. Gemma3:4b achieved 89.15% oracle accuracy, validating the experimental setup.

---

## Pilot Test Results

### Test 1: qwen3.5:4b (Initial Pilot)
**Model**: qwen3.5:4b (3.4GB, ~4B parameters)
**Status**: ❌ Failed
**Accuracy**: 0.11% (3/2,655 correct)
**Output File**: `Context/results/qa_predictions/pilot_test.jsonl.gz`

**Problem Identified**:
- Model outputs to "thinking" field, not "response" field
- Example output: `{"response": "", "thinking": "Thinking Process:\n\n1. **Analyze the Request:..."}`
- Evaluation script tries to match thinking process against gold answer
- Result: Essentially random performance

**Sample Response**:
```
Question: who got the first nobel prize in physics
Model Output: Thinking Process:

1.  **Analyze the Request:**
    *   Task: Write a high-quality answer for the given question.
    *   Constraint: Use *only* the provided search results (some might be irrelevant)....

Gold Answer: Wilhelm Conrad Röntgen
Evaluation: ❌ No match
```

### Test 2: gemma3:4b (Replacement Pilot)
**Model**: gemma3:4b (3.3GB, ~4B parameters)
**Status**: ✅ Success
**Accuracy**: 89.15% (2,365/2,655 correct)
**Output File**: `Context/results/qa_predictions/pilot_gemma3_4b.jsonl.gz`

**Success Factors**:
- Model outputs direct answers to "response" field
- Clean, well-formatted responses
- Compatible with evaluation pipeline
- Strong performance validates experimental setup

**Sample Response**:
```
Question: who got the first nobel prize in physics
Model Output: According to Document [1], Wilhelm Conrad Röntgen received the first Nobel Prize in Physics in 1901.
Gold Answer: Wilhelm Conrad Röntgen
Evaluation: ✅ Correct (89.15% of examples matched)
```

---

## Investigation: Reasoning Models

To understand the scope of the problem, we tested multiple Qwen models:

| Model | Response Field | Thinking Field | Conclusion |
|-------|----------------|----------------|------------|
| qwen3.5:4b | Empty (`""`) | Contains thinking | Reasoning model |
| qwen3.5:9b | Empty (`""`) | Contains thinking | Reasoning model |
| qwen3.5:27b | Empty (`""`) | Contains thinking | Reasoning model |
| qwen3:30b | Empty (`""`) | Contains thinking | Reasoning model |

**Conclusion**: All Qwen models in the user's Ollama installation are reasoning models designed to show their work rather than give direct answers.

---

## Model Selection Revision

### Original Plan (Phase 1)
| Tier | Model | Size | Parameters |
|------|-------|------|------------|
| Large | qwen3.5:27b | 17GB | ~27B |
| Medium | mistral-small:22b | 12GB | ~22B |
| Small | qwen3.5:4b | 3.4GB | ~4B |

**Rationale**: Controlled comparison (qwen 4B vs 27B), size diversity, architectural variety

### Revised Plan (Post-Pilot)
| Tier | Model | Size | Parameters | Oracle Acc |
|------|-------|------|------------|------------|
| Large | gemma3:27b | 17GB | ~27B | TBD |
| Medium | mistral-small:22b | 12GB | ~22B | TBD |
| Small | gemma3:4b | 3.3GB | ~4B | **89.15%** |

**Rationale**:
- ✅ Maintained controlled comparison (gemma3 4B vs 27B)
- ✅ Preserved size diversity (4B, 22B, 27B)
- ✅ Enhanced architectural diversity (Gemma's local/global attention vs Mistral's standard)
- ✅ All models give direct answers (non-reasoning)
- ✅ Pilot validated (gemma3:4b: 89.15% oracle accuracy)

**Added Scientific Value**:
- Gemma's interleaved local/global attention (5:1 ratio) vs Mistral's standard attention
- Hypothesis: Local/global attention may reduce middle-position degradation

---

## Technical Details

### Ollama API Response Format

**Standard Models (Mistral, Gemma)**:
```json
{
  "model": "gemma3:4b",
  "response": "According to Document [1], Wilhelm Conrad Röntgen...",
  "thinking": "",
  "done": true
}
```

**Reasoning Models (Qwen)**:
```json
{
  "model": "qwen3.5:4b",
  "response": "",
  "thinking": "Thinking Process:\n\n1. **Analyze the Request:**...",
  "done": true
}
```

### Code Fix Applied

**File**: `src/lost_in_the_middle/ollama_client.py`

**Original Logic** (Pilot Test 1):
```python
response_text = result.get("response", "")
thinking_text = result.get("thinking", "")

if thinking_text and response_text:
    generated_text = thinking_text + "\n" + response_text
elif thinking_text:
    generated_text = thinking_text  # ← Used for qwen, causing evaluation failure
elif response_text:
    generated_text = response_text
```

This logic was designed to handle both fields, but it meant qwen's thinking process became the "answer."

**Current Status**: No additional code changes needed. Standard models (Gemma, Mistral) work correctly with existing code.

---

## Oracle Dataset Performance Analysis

**Oracle Task**: Each example has ONE document containing the answer.
- **Upper bound**: 100% (all information is present)
- **Expected performance**: 85-95% for good models (accounting for challenging questions)
- **Lower bound**: ~10-20% (parametric knowledge baseline)

**gemma3:4b Performance**: 89.15%
- ✅ Within expected range for strong performance
- ✅ Indicates model can extract information when present
- ✅ Validates experimental pipeline

**Breakdown by Error Type** (sample of failures):
1. Formatting mismatches (e.g., "May 18, 2018" vs "2018-05-18")
2. Partial answers (e.g., missing "in Physics" from "Nobel Prize")
3. Information synthesis errors
4. Edge cases with ambiguous questions

**Implications for Position Bias Testing**:
- High oracle accuracy means model CAN answer when information is accessible
- Position bias experiments will show degradation when answer is buried in middle
- Establishes strong baseline for comparison

---

## Files Updated

### Documentation
- ✅ `Context/models.txt` - Comprehensive model selection revision with rationale
- ✅ `Context/PILOT_RESULTS.md` - This file

### Code
- ✅ `scripts/run_ollama_experiments.sh` - Updated model list (qwen → gemma)

### Results
- ✅ `Context/results/qa_predictions/pilot_test.jsonl.gz` - qwen3.5:4b results (0.11% acc)
- ✅ `Context/results/qa_predictions/pilot_gemma3_4b.jsonl.gz` - gemma3:4b results (89.15% acc)

---

## Next Steps

### Immediate Actions

1. **Run mistral-small:22b Oracle Pilot**
   - Validate medium-tier model works correctly
   - Expected accuracy: 85-95%
   - Establishes second baseline
   ```bash
   /home/b/miniconda3/envs/lost-in-the-middle/bin/python scripts/get_qa_responses_from_ollama.py \
       --model mistral-small:22b \
       --input-path qa_data/nq-open-oracle.jsonl.gz \
       --output-path Context/results/qa_predictions/pilot_mistral_small_22b.jsonl.gz \
       --temperature 0.0 \
       --max-new-tokens 100
   ```

2. **Run gemma3:27b Oracle Pilot**
   - Validate large-tier model works correctly
   - Expected accuracy: 85-95%
   - Establishes third baseline
   ```bash
   /home/b/miniconda3/envs/lost-in-the-middle/bin/python scripts/get_qa_responses_from_ollama.py \
       --model gemma3:27b \
       --input-path qa_data/nq-open-oracle.jsonl.gz \
       --output-path Context/results/qa_predictions/pilot_gemma3_27b.jsonl.gz \
       --temperature 0.0 \
       --max-new-tokens 100
   ```

3. **Compare Oracle Performance**
   - Does larger model (27B) outperform smaller (4B)?
   - Are Gemma models more consistent than Mistral?
   - Establishes baseline for position bias testing

### Full Experiment Execution

Once all three oracle pilots complete successfully:

4. **Run 10-Document Experiments**
   - All 3 models × 3 positions (start, middle, end)
   - Tests basic position bias with manageable context
   - Expected completion: ~6-12 hours

5. **Run 20-Document Experiments**
   - All 3 models × 3 positions
   - Tests stronger position bias signal
   - Expected completion: ~12-24 hours

6. **Run 30-Document Experiments**
   - All 3 models × 3 positions
   - Maximum stress test from original paper
   - Expected completion: ~18-36 hours

7. **Run KV Retrieval Experiments**
   - All 3 models × 3 KV dataset sizes (75, 140, 300)
   - Synthetic task with perfect control
   - Expected completion: ~8-16 hours

8. **Analysis and Visualization**
   - Generate position vs accuracy plots
   - Compare with original paper findings
   - Document whether U-shaped curve persists

---

## Research Questions to Answer

### Primary Questions (Original Paper)
1. **Does the U-shaped performance curve persist in modern models (2024)?**
   - Original paper (2023): GPT-3.5, Claude-1.3, MPT-30B all showed U-shape
   - Our test: Gemma3 (4B, 27B), Mistral-Small (22B)

2. **Does model size affect position bias?**
   - Compare gemma3:4b vs gemma3:27b (same architecture, different scale)
   - Original paper: Larger models showed similar or worse position bias

3. **Do modern extended-context models handle long contexts better?**
   - Gemma3: 128K context window
   - Mistral-Small: 32K context window
   - Original models: 4K-16K

### Secondary Questions (Architectural)
4. **Does interleaved local/global attention reduce position bias?**
   - Gemma3's 5:1 local/global attention
   - Hypothesis: Local attention may help with nearby context, global with distant

5. **How do different architectures compare?**
   - Gemma3 (local/global) vs Mistral (standard attention)
   - Both are decoder-only, instruction-tuned, modern (2024)

6. **Does query-aware contextualization help modern models?**
   - Original finding: Helps encoder-decoder, unclear for decoder-only
   - Test: Standard prompts vs query-aware prompts

---

## Timeline Estimate

**Pilot Testing** (Current Phase):
- ✅ gemma3:4b oracle: Complete (89.15% accuracy)
- ⏳ mistral-small:22b oracle: 2-3 hours
- ⏳ gemma3:27b oracle: 2-3 hours
- **Total**: ~4-6 hours

**Full QA Experiments**:
- 10-doc experiments: 6-12 hours
- 20-doc experiments: 12-24 hours
- 30-doc experiments: 18-36 hours
- **Total**: ~36-72 hours (1.5-3 days continuous)

**KV Retrieval Experiments**:
- All datasets: 8-16 hours
- **Total**: ~8-16 hours

**Analysis and Documentation**:
- Data processing: 2-4 hours
- Visualization: 2-4 hours
- Results writeup: 4-8 hours
- **Total**: ~8-16 hours

**Grand Total**: ~52-110 hours of computation + analysis
**Calendar Time**: ~3-7 days with RTX 4090

---

## Lessons Learned

1. **Always pilot test with simple datasets first**
   - Oracle dataset revealed reasoning model incompatibility immediately
   - Saved days of wasted computation on full experiments

2. **Check API response format assumptions**
   - Assumed all models use "response" field
   - Qwen models use "thinking" field instead
   - Different model families have different behaviors

3. **Document model selection rationale clearly**
   - Original plan didn't anticipate reasoning model issue
   - Flexibility in model selection is valuable
   - Scientific value preserved despite changes

4. **Evaluation pipeline must match model output**
   - Reasoning models incompatible with exact-match evaluation
   - Would need different evaluation for thinking processes
   - Standard models (Gemma, Mistral) work as expected

---

## Recommendations

### For This Experiment
- ✅ Proceed with Gemma3 + Mistral model selection
- ✅ Run remaining oracle pilots before full experiments
- ✅ Monitor for any similar issues with other models
- ⚠ Consider adding gemma2:9b for additional data point (between 4B and 22B)

### For Future Experiments
- 🔍 Investigate reasoning models separately (different research question)
- 🔍 Test query-aware contextualization with Gemma's attention mechanism
- 🔍 Compare with base (non-instruct) models if available
- 🔍 Consider encoder-decoder models (if Ollama support improves)

### For Code Improvements
- ✅ Current ollama_client.py handles both standard and reasoning models
- 💡 Add model type detection (reasoning vs standard) for logging
- 💡 Add response format validation before evaluation
- 💡 Create separate evaluation pipeline for reasoning model outputs

---

**Status**: Pilot phase partially complete. gemma3:4b validated. Awaiting mistral-small:22b and gemma3:27b oracle pilots before proceeding to full experiments.
