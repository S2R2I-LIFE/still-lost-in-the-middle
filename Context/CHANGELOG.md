# Changelog: Lost in the Middle Replication with Ollama

This changelog tracks all modifications made to the original "Lost in the Middle" codebase for the Ollama replication project.

**Repository**: https://github.com/nelson-liu/lost-in-the-middle
**Replication By**: [Your Name]
**Start Date**: 2026-03-29
**Status**: Phase 1 (Documentation) - No code changes yet

---

## Versioning

- **v0.1.0** - Initial documentation (Phase 1)
- **v0.2.0** - Ollama integration implementation (Phase 2)
- **v0.3.0** - Experiment execution (Phase 2)
- **v1.0.0** - Complete replication with results (Phase 3)

---

## [Phase 1 - Documentation] - 2026-03-29

### Added

**Documentation files** (all in `Context/` directory):
- `summary.md` - Semi-technical summary of the original research paper
- `models.txt` - Selected Ollama models with rationale (3 models: small, medium, large)
- `experiment_plan.md` - Detailed experimental protocol and execution plan
- `CHANGELOG.md` - This file, tracking all modifications
- `results_template.md` - Template for documenting findings (to be created)
- `results/` - Directory structure for future experiment outputs (to be created)

**Planning artifacts**:
- Complete experimental design documented
- Dataset inventory completed (15 QA files + 3 KV files + 1 oracle)
- Success criteria defined
- Timeline estimates created

### Modified

None - No code changes in Phase 1.

### Unchanged

All original repository files remain untouched:
- `/src/lost_in_the_middle/` - Core prompting and evaluation code
- `/scripts/` - Original experiment and evaluation scripts
- `/qa_data/` - Multi-document QA datasets
- `/kv_retrieval_data/` - Key-value retrieval datasets
- `requirements.txt` - Original dependencies
- `README.md` - Original documentation

---

## [Phase 2 - Implementation] - 2026-03-29

**Status**: Code implementation complete (awaiting pilot testing)

### Added

**New Python modules**:
- `src/lost_in_the_middle/ollama_client.py`
  - Purpose: Abstraction layer for Ollama API calls
  - Functions:
    - `query_ollama_model()` - Send prompts to Ollama models
    - `get_ollama_models()` - List available models
    - `check_ollama_running()` - Verify Ollama service status
  - Dependencies: `requests` library

**New experiment scripts**:
- `scripts/get_qa_responses_from_ollama.py`
  - Based on: `scripts/get_mpt_responses.py` and `scripts/get_longchat_responses.py`
  - Purpose: Run multi-document QA experiments with Ollama models
  - Changes from original:
    - Replace HuggingFace model loading with Ollama API calls
    - Remove GPU memory management (handled by Ollama)
    - Keep same data loading/prompting logic
    - Add model availability checks

- `scripts/get_kv_responses_from_ollama.py`
  - Based on: `scripts/get_mpt_kv_responses.py` and `scripts/get_longchat_kv_responses.py`
  - Purpose: Run key-value retrieval experiments with Ollama models
  - Changes: Same as QA script above

**New automation scripts**:
- `scripts/run_ollama_experiments.sh`
  - Purpose: Batch execution of all experiments
  - Features:
    - Loop over all models
    - Run all QA and KV datasets
    - Automatic evaluation
    - Progress logging
    - Error handling

**Implementation details**:
- All scripts written and tested (syntax-level)
- Maintains compatibility with original evaluation scripts
- Output format matches original (JSONL with same schema)
- Sequential processing (Ollama limitation - no batching)
- Comprehensive error handling and retry logic
- Progress tracking with tqdm
- Logging for debugging
    - Disk space available
    - Output directories exist

### Modified

**Dependencies** (`requirements.txt`):
- ✅ Added: `requests>=2.31.0` for Ollama HTTP API calls
- Unchanged: All existing dependencies (tqdm, xopen, pydantic, pytest, etc.)
- Note: torch, transformers, vllm not needed for Ollama experiments but kept for compatibility

**Documentation**:
- `README.md`
  - Add section: "Ollama Replication Instructions"
  - Link to: `Context/experiment_plan.md`

### Unchanged

**Core evaluation code** (reused without modification):
- ✅ `scripts/evaluate_qa_responses.py` - QA accuracy evaluation
- ✅ `scripts/evaluate_kv_responses.py` - KV accuracy evaluation
- ✅ `src/lost_in_the_middle/prompting.py` - Prompt templates (used directly)
- ✅ `src/lost_in_the_middle/metrics.py` - Evaluation metrics

**Data files** (all original, untouched):
- ✅ All datasets in `qa_data/` and `kv_retrieval_data/`
- ✅ No data preprocessing needed

**Original experiment scripts** (preserved):
- ✅ `scripts/get_qa_responses_from_mpt.py`
- ✅ `scripts/get_qa_responses_from_longchat.py`
- ✅ `scripts/get_qa_responses_from_llama_2.py`
- ✅ `scripts/get_kv_responses_from_mpt.py`
- ✅ `scripts/get_kv_responses_from_longchat.py`
- All original scripts remain functional and unmodified

---

## [Phase 3 - Analysis] - 2026-03-30

### Completed
- ✅ All 13 experiments executed (34,515 examples)
- ✅ Evaluation completed for all experiments
- ✅ Created comprehensive analysis (FINDINGS.md - 15,000 words)
- ✅ Generated 4 visualization plots (PNG)
- ✅ Filled in all result tables (RESULTS_SUMMARY.md)
- ✅ Updated README with actual findings
- ✅ Prepared research paper appendix

### Key Findings Documented
- U-shaped curve eliminated in 2024 models
- Primacy bias persists, recency bias eliminated
- ~20% less position degradation vs 2023
- Models effectively use context (2.4-2.8× over closedbook)
- Architecture matters more than size for position robustness

**Status**: Not started

### Planned: Added

**Analysis scripts**:
- `Context/results/analysis/position_bias_analysis.ipynb`
  - Purpose: Jupyter notebook for interactive analysis
  - Contents:
    - Load evaluation scores
    - Plot accuracy vs. position (U-curves)
    - Statistical tests
    - Comparison tables

- `Context/results/analysis/plot_u_curve.py`
  - Purpose: Generate publication-quality plots
  - Outputs: PNG/PDF figures for each model/setting

- `Context/results/analysis/comparative_analysis.py`
  - Purpose: Compare Ollama results with original paper
  - Outputs: Comparison tables and overlay plots

**Results documentation**:
- `Context/results/summary/final_results.md`
  - Purpose: Complete findings report
  - Based on: `results_template.md`

### Planned: Data Outputs

**Prediction files** (generated during Phase 2):
- `Context/results/qa_predictions/` - Model predictions for QA tasks
- `Context/results/kv_predictions/` - Model predictions for KV tasks

**Evaluation files**:
- `Context/results/evaluation_scores/` - Accuracy scores per dataset

**Visualizations**:
- U-curve plots (accuracy vs. position)
- Model comparison charts
- Context length effect plots

---

## Migration Guide (From Original to Ollama)

### For Users Running Original Experiments

If you previously ran experiments with the original code:

**What stays the same**:
- Dataset files (no changes)
- Evaluation metrics (same accuracy calculation)
- Prompt formats (preserved from original)
- Output formats (compatible with original evaluation scripts)

**What changes**:
- Model loading: HuggingFace → Ollama API
- GPU management: Manual CUDA → Ollama handles it
- Batch processing: Native batching → Sequential (Ollama limitation)
- Model names: `mpt-30b-instruct` → `qwen3.5:27b` (etc.)

### For Users Extending This Work

To add new models:

1. **Add model to** `Context/models.txt`:
   - Document parameters, context window, rationale

2. **Verify Ollama availability**:
   ```bash
   ollama pull [model_name]
   ollama list
   ```

3. **Run experiments**:
   ```bash
   ./scripts/run_ollama_experiments.sh --model [model_name]
   ```

4. **Update results**:
   - Add new model to `Context/results_template.md`
   - Regenerate analysis plots

---

## Breaking Changes

### None (Phase 1)

No breaking changes - original code is untouched.

### Expected in Phase 2

**API differences from HuggingFace**:
- Ollama uses HTTP API (not Python transformers library)
- No direct control over sampling (temperature only)
- Sequential inference (no native batching)

**Script interface changes**:
- New `--model` parameter accepts Ollama model names (e.g., `qwen3.5:27b`)
- Old HuggingFace model paths won't work with Ollama scripts
- Original scripts remain functional (preserved separately)

---

## Compatibility Notes

### Python Version
- **Original**: Python 3.8+
- **Ollama replication**: Python 3.8+ (same)

### Dependencies
- **Original**: HuggingFace transformers, torch, CUDA
- **Ollama replication**: HuggingFace (for data only), requests, NO torch/CUDA needed

### Operating Systems
- **Original**: Linux (CUDA required)
- **Ollama replication**: Linux, macOS, Windows (Ollama cross-platform)

### Hardware Requirements
- **Original**: NVIDIA GPU with 24GB+ VRAM
- **Ollama replication**:
  - GPU preferred (24GB+ VRAM for largest models)
  - CPU fallback supported (slower)
  - Apple Silicon supported (Metal acceleration)

---

## Testing Strategy

### Phase 1 (Documentation)
- ✓ All documentation files created
- ✓ Experimental design reviewed for completeness
- ✓ Dataset inventory verified

### Phase 2 (Implementation)
Planned tests:
- [ ] Unit tests for `ollama_client.py`
- [ ] Integration test: Ollama API connectivity
- [ ] Pilot run: Oracle dataset with qwen3.5:4b
- [ ] Validation: Output format matches evaluation script expectations
- [ ] Smoke test: All models × 1 small dataset

### Phase 3 (Analysis)
Planned validations:
- [ ] Sanity checks: Oracle > standard conditions > closedbook
- [ ] Reproducibility: Re-run one condition, verify identical results
- [ ] Cross-validation: Compare with original paper's published metrics

---

## Known Issues and Limitations

### Current (Phase 1)
None - documentation phase only.

### Anticipated (Phase 2)

**Ollama limitations**:
- Sequential processing only (no batching) → slower than original
- Less control over generation parameters
- Model-specific quirks (may need per-model adjustments)

**Resource constraints**:
- Large models (27B) may be slow on CPU
- Long contexts (30 docs) may hit memory limits
- Total inference time: days vs. hours (due to sequential processing)

**Comparison limitations**:
- Different models than original (Ollama vs. GPT-3.5/Claude)
- Different architectures (all decoder-only, no encoder-decoder)
- Smaller parameter counts (27B max vs. 175B GPT-3.5)

---

## Future Work

### Immediate (Phase 2)
- Implement Ollama integration
- Run core experiments (QA + KV, all positions)

### Near-term (Phase 3)
- Analyze results
- Compare with original paper
- Document findings

### Long-term (Optional)
- Add encoder-decoder models (if Ollama supports)
- Test reasoning models (e.g., deepseek-r1)
- Replicate open-domain QA case study
- Test query-aware contextualization variants
- Explore position bias mitigation techniques

---

## Acknowledgments

**Original Research**:
- Paper: "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., 2023)
- Repository: https://github.com/nelson-liu/lost-in-the-middle
- Authors: Nelson F. Liu, Kevin Lin, John Hewitt, et al.

**Replication**:
- Uses Ollama for local model inference
- Preserves original experimental design and evaluation metrics
- Extends findings to modern (2024-2025) open-source models

---

## Questions or Issues?

For questions about:
- **Original paper/code**: See https://github.com/nelson-liu/lost-in-the-middle
- **Ollama setup**: See https://ollama.ai/docs
- **This replication**: [Add your contact/issue tracker]

---

**Last Updated**: 2026-03-29 (Phase 1 - Documentation Complete)
**Next Update**: Phase 2 implementation begins
