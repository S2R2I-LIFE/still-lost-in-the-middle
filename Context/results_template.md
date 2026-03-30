# Results: "Lost in the Middle" Replication with Ollama Models

**Status**: Template (Phase 1) - Awaiting experimental data
**Last Updated**: 2026-03-29
**Experiments Run**: None yet (Phase 2 pending)

---

## Executive Summary

[Brief overview of findings - 2-3 paragraphs]

**Key findings**:
- [Finding 1: U-shaped curve presence/absence]
- [Finding 2: Model size effects]
- [Finding 3: Comparison with original paper]
- [Finding 4: Unexpected observations]

**Bottom line**: [One sentence summary of whether modern Ollama models solved the position bias problem]

---

## Table of Contents

1. [Multi-Document Question Answering Results](#multi-document-question-answering-results)
2. [Key-Value Retrieval Results](#key-value-retrieval-results)
3. [Model Size Comparison](#model-size-comparison)
4. [Comparison with Original Paper](#comparison-with-original-paper)
5. [Query-Aware Contextualization Impact](#query-aware-contextualization-impact)
6. [Unexpected Findings](#unexpected-findings)
7. [Practical Recommendations](#practical-recommendations)
8. [Limitations and Future Work](#limitations-and-future-work)

---

## Multi-Document Question Answering Results

### Overall Performance Summary

| Model             | Oracle  | Closedbook | Best Position | Worst Position | Disparity |
|-------------------|---------|------------|---------------|----------------|-----------|
| qwen3.5:27b       | [%]     | [%]        | [%]           | [%]            | [%]       |
| mistral-small:22b | [%]     | [%]        | [%]           | [%]            | [%]       |
| qwen3.5:4b        | [%]     | [%]        | [%]           | [%]            | [%]       |

**Oracle**: Single document containing answer (upper bound)
**Closedbook**: No documents, parametric memory only (lower bound)
**Disparity**: Absolute difference between best and worst position accuracy

### Position Bias Analysis

#### 10 Documents Setting

**Positions tested**: 0 (start), 4 (middle), 9 (end)

| Model             | Position 0 | Position 4 | Position 9 | Avg  | Std Dev |
|-------------------|------------|------------|------------|------|---------|
| qwen3.5:27b       | [%]        | [%]        | [%]        | [%]  | [%]     |
| mistral-small:22b | [%]        | [%]        | [%]        | [%]  | [%]     |
| qwen3.5:4b        | [%]        | [%]        | [%]        | [%]  | [%]     |

**Observations**:
- [Does U-shaped curve appear with only 10 documents?]
- [Which model performs best overall?]
- [Is there primacy or recency bias?]

#### 20 Documents Setting

**Positions tested**: 0, 4, 9, 14, 19

| Model             | Pos 0 | Pos 4 | Pos 9 | Pos 14 | Pos 19 | Avg  | Std Dev |
|-------------------|-------|-------|-------|--------|--------|------|---------|
| qwen3.5:27b       | [%]   | [%]   | [%]   | [%]    | [%]    | [%]  | [%]     |
| mistral-small:22b | [%]   | [%]   | [%]   | [%]    | [%]    | [%]  | [%]     |
| qwen3.5:4b        | [%]   | [%]   | [%]   | [%]    | [%]    | [%]  | [%]     |

**Observations**:
- [Is the U-curve more pronounced than 10-doc setting?]
- [Performance at position 14 (true middle) - worst case?]
- [Do end positions (19) outperform start (0)?]

#### 30 Documents Setting

**Positions tested**: 0, 4, 9, 14, 19, 24, 29

| Model             | Pos 0 | Pos 4 | Pos 9 | Pos 14 | Pos 19 | Pos 24 | Pos 29 | Avg  | Std Dev |
|-------------------|-------|-------|-------|--------|--------|--------|--------|------|---------|
| qwen3.5:27b       | [%]   | [%]   | [%]   | [%]    | [%]    | [%]    | [%]    | [%]  | [%]     |
| mistral-small:22b | [%]   | [%]   | [%]   | [%]    | [%]    | [%]    | [%]    | [%]  | [%]     |
| qwen3.5:4b        | [%]   | [%]   | [%]   | [%]    | [%]    | [%]    | [%]    | [%]  | [%]     |

**Observations**:
- [Most pronounced U-curve?]
- [Does performance degrade compared to 20-doc setting?]
- [Is middle performance (14, 19) below closedbook baseline?]
- [Do models recover at position 29?]

### U-Shaped Curve Visualization

[Insert plot: Accuracy vs. Position for each model, faceted by context length]

**X-axis**: Gold document position
**Y-axis**: Accuracy (%)
**Lines**: One per model
**Facets**: 10-doc, 20-doc, 30-doc settings

**Expected pattern**: U-shape (high at 0 and end, low in middle)
**Actual pattern**: [Describe observed patterns]

### Statistical Analysis

**Best-case vs. Worst-case Performance**:

| Model             | 10-doc | 20-doc | 30-doc | Average Disparity |
|-------------------|--------|--------|--------|-------------------|
| qwen3.5:27b       | [%]    | [%]    | [%]    | [%]               |
| mistral-small:22b | [%]    | [%]    | [%]    | [%]               |
| qwen3.5:4b        | [%]    | [%]    | [%]    | [%]               |

**Significance tests**:
- [Paired t-test: Start vs. Middle positions]
- [Paired t-test: Middle vs. End positions]
- [ANOVA: Effect of position across all models]

**Results**: [Statistically significant position effects? At what p-value?]

---

## Key-Value Retrieval Results

### Overall Performance Summary

| Model             | 75 Keys | 140 Keys | 300 Keys | Average |
|-------------------|---------|----------|----------|---------|
| qwen3.5:27b       | [%]     | [%]      | [%]      | [%]     |
| mistral-small:22b | [%]     | [%]      | [%]      | [%]     |
| qwen3.5:4b        | [%]     | [%]      | [%]      | [%]     |

**Note**: Original Claude-1.3 achieved near-perfect (~100%) on all settings.

### Position-Dependent Performance

[For each key count, analyze accuracy vs. position of target key-value pair]

**Pattern observations**:
- [Do models exhibit U-shaped curves in KV retrieval too?]
- [Is KV retrieval easier than multi-doc QA (should be - it's exact match)?]
- [Which models achieve near-perfect performance?]

### Comparison: KV vs. QA Tasks

| Model             | KV Avg Accuracy | QA Avg Accuracy | Difference |
|-------------------|-----------------|-----------------|------------|
| qwen3.5:27b       | [%]             | [%]             | [%]        |
| mistral-small:22b | [%]             | [%]             | [%]        |
| qwen3.5:4b        | [%]             | [%]             | [%]        |

**Interpretation**:
- [Are models better at simple retrieval than reasoning?]
- [Does position bias affect retrieval differently than QA?]

---

## Model Size Comparison

### Hypothesis: Larger models = less position bias

**Test**: Compare 4B vs. 22B vs. 27B at same positions.

### Accuracy by Model Size (Averaged Across Positions)

| Context Length | qwen3.5:4b | mistral-small:22b | qwen3.5:27b | Size Benefit |
|----------------|------------|-------------------|-------------|--------------|
| 10 documents   | [%]        | [%]               | [%]         | [%]          |
| 20 documents   | [%]        | [%]               | [%]         | [%]          |
| 30 documents   | [%]        | [%]               | [%]         | [%]          |

**Size Benefit**: 27B accuracy - 4B accuracy (positive = larger is better)

### Position Bias by Model Size

**Best-worst disparity**:

| Model             | Parameters | Average Disparity | Rank (1=least biased) |
|-------------------|------------|-------------------|-----------------------|
| qwen3.5:27b       | 27B        | [%]               | [1/2/3]               |
| mistral-small:22b | 22B        | [%]               | [1/2/3]               |
| qwen3.5:4b        | 4B         | [%]               | [1/2/3]               |

**Finding**: [Does larger size reduce position bias? Or is it architecture-dependent?]

### Small Model Behavior (4B)

**Original paper finding**: 7B Llama-2 showed only recency bias (not U-curve)

**Our 4B model**:
- [Recency bias only, or full U-curve?]
- [If U-curve exists, primacy bias emerges at lower scale than expected]
- [Overall performance: acceptable or too degraded?]

### Architecture Comparison (Qwen vs. Mistral)

**Controlled comparison**: qwen3.5:27b vs. mistral-small:22b (similar size)

| Metric                    | qwen3.5:27b | mistral-small:22b | Winner  |
|---------------------------|-------------|-------------------|---------|
| Average accuracy          | [%]         | [%]               | [model] |
| Best-worst disparity      | [%]         | [%]               | [model] |
| Primacy bias (pos 0)      | [%]         | [%]               | [model] |
| Recency bias (last pos)   | [%]         | [%]               | [model] |
| Middle performance        | [%]         | [%]               | [model] |

**Finding**: [Are architectural differences (Qwen vs. Mistral) significant, or is size the dominant factor?]

---

## Comparison with Original Paper

### Multi-Document QA: Ollama vs. GPT-3.5-Turbo

**30 documents setting** (most comparable):

| Model             | Best Position | Worst Position | Disparity | Closedbook |
|-------------------|---------------|----------------|-----------|------------|
| **Original Paper:**|              |                |           |            |
| GPT-3.5-Turbo     | ~70%          | ~42%           | 28%       | 56.1%      |
| Claude-1.3        | ~65%          | ~50%           | 15%       | [unknown]  |
| MPT-30B-Instruct  | ~58%          | ~35%           | 23%       | [unknown]  |
| **Our Replication:**|             |                |           |            |
| qwen3.5:27b       | [%]           | [%]            | [%]       | [%]        |
| mistral-small:22b | [%]           | [%]            | [%]       | [%]        |
| qwen3.5:4b        | [%]           | [%]            | [%]       | [%]        |

**Interpretation**:
- [Are modern Ollama models better than 2023 GPT-3.5?]
- [Has position bias decreased with newer architectures/training?]
- [Do smaller Ollama models (27B) match larger closed models (175B)?]

### Key-Value Retrieval: Ollama vs. Claude-1.3

**300 keys setting** (hardest):

| Model             | Best Position | Worst Position | Average | Perfect? |
|-------------------|---------------|----------------|---------|----------|
| **Original Paper:**|              |                |         |          |
| Claude-1.3        | ~100%         | ~100%          | ~100%   | Yes      |
| GPT-3.5-Turbo     | ~85%          | ~45%           | ~65%    | No       |
| MPT-30B-Instruct  | ~70%          | ~40%           | ~55%    | No       |
| **Our Replication:**|             |                |         |          |
| qwen3.5:27b       | [%]           | [%]            | [%]     | [Y/N]    |
| mistral-small:22b | [%]           | [%]            | [%]     | [Y/N]    |
| qwen3.5:4b        | [%]           | [%]            | [%]     | [Y/N]    |

**Interpretation**:
- [Can any Ollama model achieve Claude-1.3's near-perfect retrieval?]
- [If not, why? Architecture, training data, or scale?]

### Visualization: Original vs. Replication

[Insert overlay plot: Original GPT-3.5/Claude curves vs. Ollama model curves]

**Key**: [Different colors for original vs. new models]
**Expected**: [If modern models improved, curves should be flatter]
**Actual**: [Describe observed pattern]

---

## Query-Aware Contextualization Impact

**Status**: [Tested / Not tested in this phase]

If tested:

### Standard vs. Query-Aware Prompting

**Format comparison**:
- **Standard**: "Question: [Q]\n\nDocuments:\n[Docs]\nAnswer:"
- **Query-aware**: "Question: [Q]\n\nDocuments:\n[Docs]\n\nQuestion: [Q]\nAnswer:"

### Multi-Document QA Results

| Model             | Standard Accuracy | Query-Aware Accuracy | Improvement |
|-------------------|-------------------|----------------------|-------------|
| qwen3.5:27b       | [%]               | [%]                  | [%]         |
| mistral-small:22b | [%]               | [%]                  | [%]         |
| qwen3.5:4b        | [%]               | [%]                  | [%]         |

**Position-specific effects**:
- [Does query-aware help at position 0 (start)?]
- [Does it help in the middle?]
- [Does it help at the end?]

### Key-Value Retrieval Results

| Model             | Standard Accuracy | Query-Aware Accuracy | Improvement |
|-------------------|-------------------|----------------------|-------------|
| qwen3.5:27b       | [%]               | [%]                  | [%]         |
| mistral-small:22b | [%]               | [%]                  | [%]         |
| qwen3.5:4b        | [%]               | [%]                  | [%]         |

**Original paper finding**: Query-aware enabled near-perfect KV retrieval for all models.

**Our finding**: [Replicate this result with Ollama models?]

---

## Unexpected Findings

### Finding 1: [Title]

**Observation**: [What was unexpected?]

**Data**:
- [Supporting statistics or examples]

**Hypothesis**: [Why might this occur?]

**Implications**: [What does this mean for practice or future research?]

### Finding 2: [Title]

[Repeat structure above]

### Finding 3: [Title]

[Repeat structure above]

**Examples of potential unexpected findings**:
- Models generating code instead of answers (like LongChat in original)
- Non-monotonic performance (accuracy increases then decreases)
- Different U-curve shapes across models (asymmetric vs. symmetric)
- Stronger primacy than recency bias (or vice versa)
- Context length saturation effects
- Format sensitivity (JSON vs. text documents)

---

## Practical Recommendations

### For RAG System Designers

**Based on our findings**:

1. **Document Ordering**:
   - [Recommendation based on where to place most relevant documents]
   - [Expected performance gain]

2. **Context Window Usage**:
   - [Optimal number of documents to retrieve]
   - [Point of diminishing returns]

3. **Model Selection**:
   - [Which Ollama models are most reliable for long-context RAG?]
   - [Trade-offs: speed vs. position-invariance]

### For Prompt Engineers

1. **Prompt Structure**:
   - [Use query-aware contextualization? Under what conditions?]
   - [Optimal document formatting]

2. **Context Design**:
   - [How to arrange multi-document inputs]
   - [Warnings about middle positions]

### For Researchers

1. **Evaluation Protocols**:
   - [Always test position variance, not just average accuracy]
   - [Include best-case/worst-case disparity as a metric]

2. **Future Directions**:
   - [Which models/architectures to investigate further]
   - [Open questions from this replication]

---

## Limitations and Future Work

### Limitations of This Study

**Model selection**:
- Smaller parameter counts than original (27B max vs. 175B)
- All decoder-only (no encoder-decoder comparison)
- Limited to Ollama-available models

**Experimental scope**:
- [What conditions were skipped due to time/resource constraints?]
- [Datasets not tested (e.g., open-domain QA case study)]

**Comparison challenges**:
- Different models than original (can't directly overlay curves)
- Different training data (2024-2025 vs. 2023)
- Different inference setups (local vs. API)

**Resource constraints**:
- [Inference time limitations]
- [Single-seed experiments (no variance estimates)]
- [Hardware limitations]

### Future Work

**Immediate extensions**:
1. Test base (non-instruct) models to isolate instruction-tuning effects
2. Replicate open-domain QA case study with Ollama models
3. Test additional model sizes (e.g., 70B if available)

**Medium-term research**:
1. Investigate reasoning models (e.g., deepseek-r1) - does chain-of-thought help?
2. Test encoder-decoder models (if Ollama supports or via HuggingFace)
3. Explore position bias mitigation techniques:
   - Attention modifications
   - Prompt engineering
   - Fine-tuning strategies

**Long-term questions**:
1. Can we train models to be truly position-invariant?
2. What architectural changes would eliminate the U-curve?
3. How does position bias interact with other biases (e.g., format, length)?

---

## Conclusion

[2-3 paragraph summary]

**Main takeaways**:
1. [Do modern Ollama models still show position bias?]
2. [How do they compare to 2023 GPT-3.5/Claude?]
3. [What's the practical impact for RAG systems?]

**Significance**:
- [What does this tell us about LLM progress since 2023?]
- [Are we getting closer to truly long-context models?]

**Final thought**: [One sentence on future outlook]

---

## Appendix: Detailed Tables

### A. Complete Accuracy Matrix (QA)

[Full table with every model × dataset × position combination]

### B. Complete Accuracy Matrix (KV)

[Full table with every model × key count × position combination]

### C. Statistical Test Results

[Detailed ANOVA, t-test results with p-values]

### D. Runtime Statistics

| Model             | Avg Tokens/Sec | Total Inference Time | VRAM Used |
|-------------------|----------------|----------------------|-----------|
| qwen3.5:27b       | [num]          | [hours]              | [GB]      |
| mistral-small:22b | [num]          | [hours]              | [GB]      |
| qwen3.5:4b        | [num]          | [hours]              | [GB]      |

### E. Error Analysis

[Examples of failure modes, common errors, edge cases]

---

## Metadata

**Experiment Dates**: [Start date] - [End date]
**Total Inference Time**: [Hours]
**Total Examples Processed**: [Count]
**Models Tested**: 3 (qwen3.5:27b, mistral-small:22b, qwen3.5:4b)
**Datasets Tested**: 18 (15 QA + 3 KV)
**Ollama Version**: [Version number]
**Hardware**: [GPU/CPU specs]

**Data Availability**:
- Raw predictions: `Context/results/qa_predictions/` and `Context/results/kv_predictions/`
- Evaluation scores: `Context/results/evaluation_scores/`
- Analysis code: `Context/results/analysis/`

**Reproducibility**:
- All code in `/scripts/` directory
- Random seeds: [If applicable]
- Exact model versions: [Ollama model tags]

---

**End of Results Template**

**Instructions for Filling Out**:
1. Run experiments (Phase 2)
2. Populate all [bracketed placeholders] with actual numbers
3. Generate plots and insert into designated sections
4. Write interpretation paragraphs based on observed data
5. Update metadata section with actual runtime/dates
6. Review for completeness and consistency
7. Publish as final results document
