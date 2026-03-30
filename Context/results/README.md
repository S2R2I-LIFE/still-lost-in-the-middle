# Results Directory

This directory contains all experimental outputs from the "Lost in the Middle" replication with Ollama models.

**Status**: Empty (Phase 1 - Documentation Only)
**Created**: 2026-03-29
**Populated**: TBD (Phase 2 - Experiment Execution)

---

## Directory Structure

```
results/
├── qa_predictions/         Model predictions for multi-document QA tasks
├── kv_predictions/         Model predictions for key-value retrieval tasks
├── evaluation_scores/      Accuracy scores and metrics
├── analysis/              Analysis scripts, notebooks, and visualizations
├── summary/               Final summary reports and findings
└── README.md              This file
```

---

## Subdirectory Descriptions

### qa_predictions/

**Purpose**: Store model predictions for all multi-document question answering experiments.

**File format**: `[model_name]_[dataset]_predictions.jsonl.gz`

**Example files** (to be created in Phase 2):
- `qwen3.5_27b_oracle.jsonl.gz`
- `qwen3.5_27b_10_total_documents_gold_at_0.jsonl.gz`
- `qwen3.5_27b_10_total_documents_gold_at_4.jsonl.gz`
- `mistral-small_22b_30_total_documents_gold_at_14.jsonl.gz`
- ... (48 total files: 3 models × 16 datasets)

**Content format**: JSON lines with:
```json
{
  "question": "Question text",
  "answers": ["correct answer 1", "correct answer 2"],
  "model_prediction": "Model's generated answer",
  "correct": 1 or 0,
  "model": "model_name",
  "dataset": "dataset_name",
  "position": gold_document_position,
  "num_documents": total_document_count
}
```

**Total files expected**: ~48 (3 models × 16 QA datasets)

---

### kv_predictions/

**Purpose**: Store model predictions for key-value retrieval experiments.

**File format**: `[model_name]_kv-retrieval-[N]_keys_predictions.jsonl.gz`

**Example files** (to be created in Phase 2):
- `qwen3.5_27b_kv-retrieval-75_keys.jsonl.gz`
- `qwen3.5_27b_kv-retrieval-140_keys.jsonl.gz`
- `qwen3.5_27b_kv-retrieval-300_keys.jsonl.gz`
- ... (9 total files: 3 models × 3 key counts)

**Content format**: JSON lines with:
```json
{
  "key": "target_uuid_key",
  "correct_value": "expected_uuid_value",
  "model_prediction": "Model's retrieved value",
  "correct": 1 or 0,
  "model": "model_name",
  "num_keys": 75/140/300,
  "position": key_position_in_json
}
```

**Total files expected**: 9 (3 models × 3 KV datasets)

---

### evaluation_scores/

**Purpose**: Store computed accuracy scores and aggregate metrics.

**File format**: CSV or JSON with summary statistics.

**Example files** (to be created in Phase 2):
- `qwen3.5_27b_qa_scores.csv`
- `qwen3.5_27b_kv_scores.csv`
- `all_models_comparison.csv`
- `position_bias_summary.json`

**Content format** (CSV example):
```csv
model,dataset,position,num_documents,accuracy,total_examples,correct_count
qwen3.5:27b,10_total_documents_gold_at_0,0,10,0.72,2655,1912
qwen3.5:27b,10_total_documents_gold_at_4,4,10,0.68,2655,1806
...
```

**Metrics to track**:
- Accuracy per position
- Best/worst position accuracy
- Average accuracy across positions
- Standard deviation (position variance)
- Comparison with baselines (oracle, closedbook)

**Total files expected**: ~10 (per-model scores + aggregate comparisons)

---

### analysis/

**Purpose**: Store analysis scripts, Jupyter notebooks, and generated visualizations.

**Expected files** (to be created in Phase 2-3):

**Scripts**:
- `position_bias_analysis.ipynb` - Interactive analysis notebook
- `plot_u_curve.py` - Generate U-shaped curve plots
- `comparative_analysis.py` - Compare with original paper
- `statistical_tests.py` - Significance testing

**Notebooks**:
- `exploratory_analysis.ipynb` - Initial data exploration
- `model_comparison.ipynb` - Cross-model comparison
- `error_analysis.ipynb` - Failure mode analysis

**Visualizations** (generated):
- `u_curve_10_docs.png` - U-curve plot for 10-document setting
- `u_curve_20_docs.png` - U-curve plot for 20-document setting
- `u_curve_30_docs.png` - U-curve plot for 30-document setting
- `model_size_comparison.png` - 4B vs 22B vs 27B comparison
- `original_vs_replication.png` - Overlay with original paper results
- `kv_retrieval_heatmap.png` - KV accuracy heatmap

**Data files**:
- `processed_results.pkl` - Preprocessed data for analysis
- `statistical_test_results.json` - Test outputs (p-values, etc.)

---

### summary/

**Purpose**: Store final summary reports and documentation of findings.

**Expected files** (to be created in Phase 3):
- `final_results.md` - Complete results report (filled-in `results_template.md`)
- `executive_summary.md` - 1-2 page summary for quick reference
- `comparison_with_original.md` - Detailed comparison with 2023 paper
- `practical_recommendations.md` - Actionable insights for practitioners

**Optional**:
- `presentation_slides.pdf` - If presenting results
- `blog_post.md` - Public-facing summary

---

## Data Flow

```
Phase 2: Experiment Execution
┌─────────────────┐
│  Run Ollama     │
│  Experiments    │
└────────┬────────┘
         │
         ├──> qa_predictions/     (Model outputs for QA)
         └──> kv_predictions/     (Model outputs for KV)

Phase 2: Evaluation
┌─────────────────┐
│  Evaluate       │
│  Predictions    │
└────────┬────────┘
         │
         └──> evaluation_scores/  (Accuracy metrics)

Phase 3: Analysis
┌─────────────────┐
│  Analyze        │
│  Results        │
└────────┬────────┘
         │
         ├──> analysis/           (Plots, notebooks, tests)
         └──> summary/            (Final reports)
```

---

## File Naming Conventions

### Predictions

**Pattern**: `[model]_[dataset]_predictions.jsonl.gz`

**Model names**:
- `qwen3.5_27b` (replace `:` with `_` for filenames)
- `mistral-small_22b`
- `qwen3.5_4b`

**Dataset names**:
- QA: `oracle`, `10_total_documents_gold_at_0`, `20_total_documents_gold_at_14`, etc.
- KV: `kv-retrieval-75_keys`, `kv-retrieval-140_keys`, `kv-retrieval-300_keys`

### Scores

**Pattern**: `[model]_[task]_scores.csv`

**Task names**: `qa`, `kv`, or `combined`

### Plots

**Pattern**: `[plot_type]_[setting].png`

**Examples**:
- `u_curve_30_docs.png`
- `model_comparison_all.png`
- `position_bias_heatmap.png`

---

## Size Estimates

**Predictions** (compressed JSONL):
- QA predictions: ~48 files × ~5MB = ~240MB
- KV predictions: ~9 files × ~1MB = ~9MB
- **Subtotal**: ~250MB

**Evaluation scores** (CSV):
- Per-model scores: ~10 files × ~100KB = ~1MB
- **Subtotal**: ~1MB

**Analysis** (notebooks, scripts, plots):
- Notebooks: ~10 files × ~500KB = ~5MB
- Plots: ~20 files × ~200KB = ~4MB
- Data files: ~5MB
- **Subtotal**: ~14MB

**Summary** (reports):
- Markdown reports: ~5 files × ~500KB = ~2.5MB
- **Subtotal**: ~2.5MB

**Total estimated size**: ~270MB

---

## Access and Usage

### Reading Predictions

```python
import gzip
import json

with gzip.open('qa_predictions/qwen3.5_27b_oracle.jsonl.gz', 'rt') as f:
    for line in f:
        example = json.loads(line)
        print(example['question'], example['model_prediction'])
```

### Loading Scores

```python
import pandas as pd

scores = pd.read_csv('evaluation_scores/qwen3.5_27b_qa_scores.csv')
print(scores.groupby('position')['accuracy'].mean())
```

### Running Analysis

```bash
# Generate U-curve plots
python analysis/plot_u_curve.py --input evaluation_scores/*.csv --output analysis/

# Run statistical tests
python analysis/statistical_tests.py --scores evaluation_scores/all_models_comparison.csv

# Launch interactive notebook
jupyter notebook analysis/position_bias_analysis.ipynb
```

---

## Verification Checklist (Phase 2)

After running experiments, verify:

- [ ] All expected prediction files exist (57 total: 48 QA + 9 KV)
- [ ] Prediction files are non-empty and properly formatted (JSON lines)
- [ ] Evaluation scores computed for all predictions
- [ ] No missing data (all 2655 examples per QA dataset, 500 per KV dataset)
- [ ] Accuracy values are reasonable (between 0 and 1)
- [ ] Oracle accuracy > standard > closedbook (sanity check)

---

## Cleanup

**Do NOT delete**:
- Prediction files (primary data)
- Evaluation scores (derived metrics)
- Final summary reports

**Safe to delete** (regenerable):
- Intermediate analysis files (`.pkl`, cached data)
- Draft notebooks (after finalizing)
- Temporary plots (after selecting final versions)

**To regenerate**:
```bash
# Re-evaluate predictions
python scripts/evaluate_qa_responses.py --input-path results/qa_predictions/*.jsonl.gz

# Re-run analysis
python analysis/plot_u_curve.py --input evaluation_scores/*.csv
```

---

## Backup Recommendations

**Critical data** (backup before Phase 3):
- `qa_predictions/` - Cannot be regenerated without re-running expensive inference
- `kv_predictions/` - Same as above

**Regenerable** (can skip backup):
- `evaluation_scores/` - Can be recomputed from predictions
- `analysis/` - Can be regenerated from scores

**Suggested backup**:
```bash
# Compress and archive predictions
tar -czf predictions_backup_$(date +%Y%m%d).tar.gz qa_predictions/ kv_predictions/

# Upload to cloud storage or external drive
```

---

## Status Tracking

**Phase 1 (Documentation)**: ✅ Complete
- Directory structure created
- README written
- Templates prepared

**Phase 2 (Experiments)**: ⏳ Pending
- [ ] Pilot run completed
- [ ] All QA predictions generated
- [ ] All KV predictions generated
- [ ] All predictions evaluated

**Phase 3 (Analysis)**: ⏳ Pending
- [ ] Analysis notebooks created
- [ ] Plots generated
- [ ] Statistical tests run
- [ ] Final report written

---

**Last Updated**: 2026-03-29 (Phase 1 - Directory Created)
**Next Update**: Phase 2 begins (experiment execution)
