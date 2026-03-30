# Model Specifications: 4B Parameter Models for Position Bias Testing

**Document Purpose**: Comprehensive technical specifications for the 4-billion parameter models used in the "Lost in the Middle" replication study.

**Last Updated**: 2026-03-30
**Models Covered**: qwen3.5:4b, gemma3:4b

---

## Table of Contents

1. [Qwen3.5:4b Specifications](#qwen35-4b-specifications)
2. [Gemma3:4b Specifications](#gemma3-4b-specifications)
3. [Direct Comparison](#direct-comparison-qwen35-vs-gemma3-4b)
4. [Relevance to Position Bias Research](#relevance-to-position-bias-research)

---

# Qwen3.5:4b Specifications

## Model Overview

| Attribute | Value |
|-----------|-------|
| **Model Name** | Qwen3.5-4B |
| **Ollama Tag** | `qwen3.5:4b` |
| **Organization** | Alibaba Cloud (Qwen Team) |
| **Model Family** | Qwen 3.5 |
| **Release Date** | 2024-2025 |
| **Model Type** | Dense Decoder-Only Transformer |
| **License** | Apache 2.0 (or Qwen License - verify before commercial use) |
| **Download Size** | 3.4 GB (Ollama) |

---

## Architecture Specifications

### Core Architecture

| Component | Specification |
|-----------|---------------|
| **Parameters** | ~4 billion (dense, all active) |
| **Architecture Type** | Decoder-only transformer |
| **Number of Layers** | ~32-40 (estimated, not publicly confirmed) |
| **Hidden Dimension** | ~2,048-3,072 (estimated) |
| **Intermediate Size** | ~8,192-11,008 (FFN expansion) |
| **Number of Attention Heads** | ~32 (estimated) |
| **KV Heads (GQA)** | ~8 (estimated, Grouped-Query Attention) |
| **Head Dimension** | ~64-96 (estimated) |
| **Context Window** | 32,768 tokens (32K native) |
| **Max Position Embeddings** | 32,768 |

### Attention Mechanism

**Type**: Grouped-Query Attention (GQA)
- Reduces memory usage by sharing key-value heads
- Balances quality vs efficiency
- Better than Multi-Query Attention for quality
- More efficient than standard Multi-Head Attention

**Attention Pattern**: Standard full attention
- Each token can attend to all previous tokens
- No sliding window or local attention restrictions
- Global context access at all layers

### Positional Encoding

**Type**: Rotary Position Embedding (RoPE) with extensions
- Base frequency: Enhanced for long-context (likely using YaRN or similar)
- Supports extrapolation beyond training length
- Optimized for 32K+ context windows

**Key Features**:
- Relative position encoding (not absolute)
- Enables length extrapolation
- Better long-range dependency modeling

### Activation Functions

**Type**: SwiGLU (Swish-Gated Linear Unit)
- Standard in modern LLaMA-style models
- Better than ReLU or GELU for transformers
- Gated activation for improved expressiveness

### Normalization

**Type**: RMSNorm (Root Mean Square Layer Normalization)
- Pre-normalization (applied before attention/FFN)
- More stable than LayerNorm
- Faster computation
- Standard in efficient transformer designs

---

## Tokenization

| Attribute | Specification |
|-----------|---------------|
| **Tokenizer Type** | BPE (Byte-Pair Encoding) or SentencePiece |
| **Vocabulary Size** | ~151,000 - 152,000 tokens |
| **Special Tokens** | System, User, Assistant delimiters for chat |
| **Multilingual Support** | Strong (Chinese, English, + many others) |
| **Code Support** | Yes (trained on code data) |

**Tokenization Efficiency**:
- Optimized for Chinese (1-2 characters per token avg)
- Competitive with English (subword tokenization)
- Efficient code tokenization

**Special Features**:
- Native support for structured conversations
- Function calling / tool use tokens (in instruct variants)

---

## Training Details

### Training Data

**Corpus Size**: Multi-trillion tokens (exact size not publicly disclosed)

**Data Composition** (estimated):
- Web crawl data (Common Crawl, etc.)
- Books and academic papers
- Code repositories (GitHub, etc.)
- Multilingual text (emphasis on Chinese + English)
- Conversational data
- Structured data (tables, lists, JSON, etc.)

**Data Curation**:
- Quality filtering (deduplication, toxicity filtering)
- Balanced language representation
- Domain diversity (STEM, humanities, arts, etc.)

**Cutoff Date**: Training data up to ~2024 (verify for specific version)

### Training Infrastructure

| Attribute | Specification |
|-----------|---------------|
| **Training Framework** | Likely Megatron-LM or custom |
| **Precision** | BF16 (Brain Float 16) or Mixed Precision |
| **Distributed Training** | Multi-node, multi-GPU (likely 100s-1000s of GPUs) |
| **Training Duration** | Weeks to months (not publicly disclosed) |
| **Compute** | Estimated petaFLOP-days (exact not disclosed) |

### Training Hyperparameters

| Hyperparameter | Value (Estimated) |
|----------------|-------------------|
| **Batch Size** | 2-4 million tokens per batch |
| **Learning Rate** | 1e-4 to 3e-4 (with warmup and decay) |
| **Optimizer** | AdamW |
| **Weight Decay** | 0.1 |
| **Gradient Clipping** | 1.0 |
| **Training Steps** | ~500K - 1M steps |
| **Warmup Steps** | ~5-10K steps |

### Instruction Fine-Tuning

**Qwen3.5:4b is instruction-tuned** (not a base model):
- Supervised fine-tuning on instruction-response pairs
- Reinforcement Learning from Human Feedback (RLHF) or variants
- Optimized for following user instructions
- Chat-optimized dialogue format

**Instruction Data**:
- Human-written examples
- Synthetic data from larger models
- Multilingual instruction sets
- Safety-filtered and aligned

---

## Performance Benchmarks

### Standard Benchmarks (Estimated for 4B scale)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| **MMLU** (Massive Multitask Language Understanding) | ~50-60% | 5-shot, measures general knowledge |
| **GSM8K** (Math Word Problems) | ~40-55% | 8-shot, grade school math |
| **HumanEval** (Code Generation) | ~30-45% | Pass@1, Python coding |
| **CMMLU** (Chinese MMLU) | ~55-65% | Multilingual capability |
| **C-Eval** (Chinese Evaluation) | ~50-60% | Chinese language understanding |

**Note**: Exact scores vary by version and prompt format. These are estimates based on typical 4B model performance.

### Qwen-Specific Strengths

- ✅ Strong multilingual capability (especially Chinese)
- ✅ Good reasoning for size class
- ✅ Effective instruction following
- ✅ Competitive coding ability
- ✅ Long-context handling (32K window)

---

## Capabilities and Limitations

### Capabilities

**What Qwen3.5:4b is good at**:
- General question answering in multiple languages
- Following complex instructions
- Code understanding and generation (Python, JavaScript, etc.)
- Document summarization (within 32K context)
- Translation between languages
- Basic reasoning and math (grade school level)
- Structured output generation (JSON, markdown, etc.)

### Limitations

**Known limitations**:
- ⚠️ **Size constraint**: 4B is relatively small - less capable than 7B+ models
- ⚠️ **Factual accuracy**: Can hallucinate or provide outdated information
- ⚠️ **Complex reasoning**: Struggles with multi-step reasoning beyond simple cases
- ⚠️ **Specialized domains**: Limited depth in specialized fields (law, medicine, etc.)
- ⚠️ **Context usage**: May not effectively use all 32K tokens (see "Lost in the Middle" research)
- ⚠️ **Arithmetic**: Better than GPT-2, but not calculator-accurate
- ⚠️ **Position bias**: Likely exhibits primacy/recency bias (subject of this research)

### Safety Considerations

- Trained with safety filtering and alignment
- May still generate harmful content if prompted adversarially
- Should be used with content moderation in production
- Not suitable for making critical decisions without human oversight

---

## Hardware Requirements

### Inference Requirements

| Configuration | Requirement |
|---------------|-------------|
| **Memory (FP16)** | ~8 GB VRAM/RAM |
| **Memory (8-bit quantized)** | ~4-5 GB VRAM/RAM |
| **Memory (4-bit quantized)** | ~2-3 GB VRAM/RAM |
| **Recommended GPU** | NVIDIA RTX 3060+ (12GB), RTX 4070+ |
| **Minimum GPU** | GTX 1660 (6GB) with quantization |
| **CPU Inference** | Possible but slow (~1-3 tokens/sec) |

### Inference Speed (Estimated)

| Hardware | Tokens/Second | Notes |
|----------|---------------|-------|
| **RTX 4090** | 40-60 tok/s | Full precision, batch=1 |
| **RTX 4070** | 25-35 tok/s | Full precision |
| **RTX 3060 (12GB)** | 15-25 tok/s | Full precision |
| **CPU (16 cores)** | 1-3 tok/s | Very slow, not recommended |
| **Apple M2 Max** | 20-30 tok/s | Metal acceleration |

**Note**: Speed varies with context length, batch size, and quantization.

---

## Use Cases

### Intended Applications

**Qwen3.5:4b is designed for**:
- Chatbots and conversational AI
- Content generation and editing
- Code assistance and completion
- Educational tools and tutoring
- Multilingual translation and localization
- Information extraction and summarization
- Research and experimentation (like this study!)

### Production Considerations

**When to use Qwen3.5:4b**:
- ✅ Cost-sensitive applications (smaller = cheaper)
- ✅ Low-latency requirements (faster than larger models)
- ✅ Multilingual support needed
- ✅ Edge deployment (fits on consumer GPUs)

**When to use larger models instead**:
- ❌ Complex reasoning required
- ❌ High factual accuracy critical
- ❌ Specialized domain expertise needed
- ❌ Maximum quality regardless of cost

---

## Model Variants

### Available Versions

| Variant | Description |
|---------|-------------|
| **qwen3.5:4b** | Instruction-tuned (chat-optimized) |
| **qwen3.5:4b-base** | Base model (if available - pre-instruction tuning) |
| **qwen3.5:4b-q8** | 8-bit quantized version |
| **qwen3.5:4b-q4** | 4-bit quantized version |

**Note**: Availability depends on Ollama library. Check `ollama list` for installed variants.

---

## Licensing and Usage

### License

**Primary License**: Apache 2.0 or Qwen Research License
- ✅ Commercial use typically allowed
- ✅ Modification and distribution allowed
- ⚠️ Verify specific license terms before commercial deployment

**Attribution**: Credit to Alibaba Cloud / Qwen Team recommended

### Terms of Use

- Check Qwen's official model card for latest terms
- Some jurisdictions or use cases may have restrictions
- Responsible AI guidelines apply

---

## References and Resources

**Official Resources**:
- Model Card: https://huggingface.co/Qwen (check for Qwen3.5-4B specific card)
- Technical Report: Search for "Qwen Technical Report" (if published)
- GitHub: https://github.com/QwenLM/Qwen (official repo)
- Blog: Qwen team blog posts on model releases

**Community Resources**:
- Ollama: https://ollama.com/library/qwen3.5
- HuggingFace Hub: Model weights and documentation
- Research papers citing Qwen models

---

# Gemma3:4b Specifications

## Model Overview

| Attribute | Value |
|-----------|-------|
| **Model Name** | Gemma 3 - 4B |
| **Ollama Tag** | `gemma3:4b` |
| **Organization** | Google DeepMind |
| **Model Family** | Gemma 3 |
| **Release Date** | 2024-2025 |
| **Model Type** | Dense Decoder-Only Transformer with Hybrid Attention |
| **License** | Gemma Terms of Use (check Google's license) |
| **Download Size** | 3.3 GB (Ollama) |

---

## Architecture Specifications

### Core Architecture

| Component | Specification |
|-----------|---------------|
| **Parameters** | ~4 billion (dense, all active) |
| **Architecture Type** | Decoder-only transformer with hybrid attention |
| **Number of Layers** | ~26-32 (estimated, with 5:1 local:global ratio) |
| **Local Attention Layers** | ~21-26 (5/6 of total layers) |
| **Global Attention Layers** | ~5 (1/6 of total layers) |
| **Hidden Dimension** | ~2,048-3,072 (estimated) |
| **Intermediate Size** | ~8,192-11,008 (FFN expansion) |
| **Number of Attention Heads** | ~32 (estimated) |
| **KV Heads (GQA/MQA)** | ~4-8 (estimated, likely MQA or GQA) |
| **Head Dimension** | ~64-96 (estimated) |
| **Context Window** | 128,000 tokens (128K native) |
| **Max Position Embeddings** | 128,000+ |

### Attention Mechanism - CRITICAL DIFFERENCE

**Type**: **Interleaved Local/Global Attention (5:1 ratio)**

This is the most important architectural difference from Qwen!

#### Local Attention Layers (5 out of every 6 layers)

**Pattern**: Sliding window / local attention
- Each token can only attend to a **limited window** of nearby tokens
- Window size: Likely 2048-4096 tokens (not publicly confirmed)
- Reduces KV cache memory requirements
- Faster inference (O(n×window) instead of O(n²))
- **Position bias implication**: Cannot see distant context!

**Example**: In a 10-document context (10,000 tokens):
- Token at position 8000 (middle document) can only attend to ~positions 6000-10,000
- Cannot access information from position 1000 (early documents)
- Relies on global layers to connect distant information

#### Global Attention Layers (1 out of every 6 layers)

**Pattern**: Full attention
- Each token can attend to **all previous tokens** (like standard transformer)
- Enables long-range connections
- Higher memory cost (KV cache for full sequence)
- **Position bias implication**: Should be position-invariant!

**Example**: In a 10-document context:
- Token at position 8000 can attend to ALL positions 0-8000
- Can retrieve information from any document
- Provides "global view" of context

#### Attention Interleaving Pattern

**5:1 Ratio** means:
```
Layer 1:  Local attention  (sliding window)
Layer 2:  Local attention  (sliding window)
Layer 3:  Local attention  (sliding window)
Layer 4:  Local attention  (sliding window)
Layer 5:  Local attention  (sliding window)
Layer 6:  Global attention (full context)
Layer 7:  Local attention  (sliding window)
...
```

**Rationale**:
- Local layers handle most processing (faster, less memory)
- Global layers periodically "sync" long-range information
- Balances efficiency (local) with capability (global)

**Hypothesis for Position Bias**:
- **If local attention dominates**: Strong position bias (can't access distant tokens)
- **If global attention compensates**: Reduced position bias (periodic full-context access)
- **Net effect**: Unknown! This is why testing is valuable!

### Positional Encoding

**Type**: Rotary Position Embedding (RoPE) with modifications

**Configuration**:
- **Local attention layers**: Standard RoPE
- **Global attention layers**: RoPE with **base frequency 1,000,000** (1M)
  - Much higher than standard (10,000)
  - Enables 128K+ context window
  - Better long-range position discrimination

**Key Features**:
- Relative position encoding
- Enhanced for ultra-long contexts (128K)
- Different RoPE configs for local vs global layers

### Activation Functions

**Type**: GeGLU or SwiGLU (Gated Linear Units)
- Standard in modern efficient transformers
- Better than ReLU or GELU
- Gated activation for expressiveness

### Normalization

**Type**: RMSNorm (Root Mean Square Layer Normalization)
- Pre-normalization architecture
- Faster than LayerNorm
- More stable training

**Additional**: QK-Normalization
- Normalizes queries and keys in attention
- Improves training stability
- Reduces attention score magnitude issues

---

## Tokenization

| Attribute | Specification |
|-----------|---------------|
| **Tokenizer Type** | SentencePiece (Gemini 2.0 tokenizer) |
| **Vocabulary Size** | 262,000 tokens (262K) |
| **Special Tokens** | System, User, Model delimiters for chat |
| **Multilingual Support** | Good (100+ languages) |
| **Code Support** | Yes (trained on code data) |

**Tokenization Efficiency**:
- Large vocabulary → efficient encoding
- Supports many languages with single tokenizer
- Optimized for English and code (Google's focus)
- Good Chinese support (but not as specialized as Qwen)

**Comparison with Qwen**:
- Gemma: 262K vocab (larger)
- Qwen: ~151K vocab (smaller)
- Same text may tokenize to different lengths!

---

## Training Details

### Training Data

**Corpus Size**: Multi-trillion tokens (exact size not publicly disclosed)

**Data Composition** (estimated):
- Web data (Google's web index - high quality)
- Books and academic papers
- Code repositories (GitHub, etc.)
- Multilingual text (100+ languages)
- Conversational data
- Structured data
- Scientific and technical documents

**Data Curation**:
- Google's quality filtering (very stringent)
- Safety filtering (toxicity, bias reduction)
- Deduplication at scale
- Balanced across domains and languages

**Cutoff Date**: Training data up to ~2024

### Training Infrastructure

| Attribute | Specification |
|-----------|---------------|
| **Training Framework** | Google's internal infrastructure (JAX/Flax) |
| **Precision** | BF16 (Brain Float 16) |
| **Distributed Training** | TPU v4/v5 pods (1000s of chips) |
| **Training Duration** | Weeks to months |
| **Compute** | Estimated petaFLOP-days (Google-scale) |

### Training Hyperparameters

| Hyperparameter | Value (Estimated) |
|----------------|-------------------|
| **Batch Size** | Multi-million tokens per batch |
| **Learning Rate** | 1e-4 to 3e-4 (with schedules) |
| **Optimizer** | AdamW or custom Google optimizer |
| **Weight Decay** | 0.1 |
| **Gradient Clipping** | 1.0 |
| **Training Steps** | ~500K - 1M steps |
| **Warmup Steps** | ~10K steps |

### Instruction Fine-Tuning

**Gemma3:4b is instruction-tuned**:
- Supervised fine-tuning (SFT) on instruction-response pairs
- Reinforcement Learning from Human Feedback (RLHF)
- Safety alignment (Google's responsible AI standards)
- Optimized for helpfulness, harmlessness, honesty

**Instruction Data**:
- Human-written examples (Google annotators)
- Synthetic data from Gemini models
- Multilingual instruction sets
- Heavy safety filtering

---

## Multimodal Capabilities

### Vision-Language Integration

**Gemma 3 includes multimodal capabilities** (text + images):
- Frozen **SigLIP vision encoder**
- Processes images as **256 compact "soft tokens"**
- Combined with text tokens in transformer input
- Native vision-language understanding

**Note**: For text-only experiments (like this research), vision encoder is not used.

### Pan & Scan Algorithm

**High-resolution image handling**:
- Adaptive algorithm for varying aspect ratios
- Processes high-resolution images efficiently
- Splits images into tiles if needed
- Not relevant for text-only tasks

---

## Performance Benchmarks

### Standard Benchmarks (Estimated for 4B scale)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| **MMLU** | ~55-65% | 5-shot, general knowledge |
| **GSM8K** | ~45-60% | 8-shot, math reasoning |
| **HumanEval** | ~35-50% | Pass@1, Python coding |
| **MATH** | ~25-35% | Higher-level mathematics |
| **BIG-Bench** | Varies | Google's comprehensive benchmark |

**Note**: Gemma models often perform above their size class due to Google's training quality.

### Gemma-Specific Strengths

- ✅ Strong safety and alignment (Google standards)
- ✅ Good factual accuracy (quality training data)
- ✅ Multimodal capability (vision + language)
- ✅ Ultra-long context (128K tokens)
- ✅ Efficient inference (local/global attention)

---

## Capabilities and Limitations

### Capabilities

**What Gemma3:4b is good at**:
- General question answering (multilingual)
- Following instructions safely and accurately
- Code understanding and generation
- Long-document processing (128K context)
- Vision-language tasks (if using multimodal variant)
- Reasoning tasks (above average for 4B size)
- Structured output generation

### Limitations

**Known limitations**:
- ⚠️ **Size constraint**: 4B is small - less capable than 9B/27B variants
- ⚠️ **Local attention gaps**: 5/6 of layers have limited context view
- ⚠️ **Complex reasoning**: Still struggles with multi-hop reasoning
- ⚠️ **Specialized knowledge**: Limited depth in niche domains
- ⚠️ **Position bias**: Unknown! Subject of this research
  - Could be worse (local attention can't see distant context)
  - Could be better (global layers provide periodic full access)
- ⚠️ **Arithmetic**: Not calculator-accurate
- ⚠️ **Hallucination**: Can generate plausible but false information

### Safety Considerations

- Heavily aligned with Google's AI Principles
- Strong content filtering and safety guardrails
- May refuse harmful or ambiguous requests
- More conservative than some open models
- Suitable for production with appropriate monitoring

---

## Hardware Requirements

### Inference Requirements

| Configuration | Requirement |
|---------------|-------------|
| **Memory (FP16)** | ~8 GB VRAM/RAM |
| **Memory (8-bit quantized)** | ~4-5 GB VRAM/RAM |
| **Memory (4-bit quantized)** | ~2-3 GB VRAM/RAM |
| **Recommended GPU** | NVIDIA RTX 3060+ (12GB), RTX 4070+ |
| **Minimum GPU** | GTX 1660 (6GB) with quantization |
| **CPU Inference** | Possible but slow |

### Inference Speed (Estimated)

| Hardware | Tokens/Second | Notes |
|----------|---------------|-------|
| **RTX 4090** | 40-65 tok/s | Faster due to local attention |
| **RTX 4070** | 25-40 tok/s | Full precision |
| **RTX 3060 (12GB)** | 15-30 tok/s | Full precision |
| **CPU (16 cores)** | 1-3 tok/s | Not recommended |
| **Google TPU** | Optimized | Best performance (if accessible) |

**Note**: Gemma may be slightly faster than Qwen due to local attention (less KV cache).

---

## Use Cases

### Intended Applications

**Gemma3:4b is designed for**:
- Research and education (like this study!)
- Responsible AI applications
- Long-document analysis (128K context)
- Multimodal applications (text + vision)
- Safety-critical applications (strong alignment)
- Edge deployment (efficient architecture)

### Production Considerations

**When to use Gemma3:4b**:
- ✅ Safety and alignment critical
- ✅ Long-context tasks (up to 128K tokens)
- ✅ Efficient inference needed (local attention)
- ✅ Multimodal capability desired
- ✅ Google ecosystem integration

**When to use other models**:
- ❌ Maximum multilingual performance (Qwen better for Chinese)
- ❌ Largest possible context (Qwen 3.5 has 262K/1M)
- ❌ Full global attention needed (Qwen uses standard attention)

---

## Model Variants

### Available Versions

| Variant | Description |
|---------|-------------|
| **gemma3:4b** | Instruction-tuned, text-only |
| **gemma3:4b-vision** | Multimodal (text + vision) |
| **gemma3:4b-base** | Base model (pre-instruction tuning, if available) |
| **gemma3:4b-q8** | 8-bit quantized |
| **gemma3:4b-q4** | 4-bit quantized |

**Note**: Check Ollama library for available variants.

---

## Licensing and Usage

### License

**Primary License**: Gemma Terms of Use (Google)
- ✅ Commercial use allowed (with conditions)
- ✅ Research use encouraged
- ⚠️ Review Google's terms for specific restrictions
- ⚠️ May have usage caps or reporting requirements

**Attribution**: Credit to Google DeepMind required

### Terms of Use

- Read official Gemma Terms of Use before deployment
- Some use cases may require Google approval
- Responsible AI guidelines strongly encouraged
- Commercial use: verify latest terms

---

## References and Resources

**Official Resources**:
- Model Card: https://ai.google.dev/gemma (official Gemma site)
- Technical Report: "Gemma 3 Technical Report" (if published)
- GitHub: https://github.com/google-deepmind/gemma (if available)
- Blog: Google AI Blog posts on Gemma releases

**Community Resources**:
- Ollama: https://ollama.com/library/gemma3
- HuggingFace Hub: Model weights and documentation
- Research papers on Gemma architecture

---

# Direct Comparison: Qwen3.5 vs Gemma3 (4B)

## Side-by-Side Specifications

| Feature | Qwen3.5:4b | Gemma3:4b | Advantage |
|---------|------------|-----------|-----------|
| **Parameters** | ~4B | ~4B | Tie |
| **Download Size** | 3.4 GB | 3.3 GB | Gemma (slightly smaller) |
| **Context Window** | 32K tokens | 128K tokens | **Gemma** (4× larger) |
| **Vocabulary** | ~151K | 262K | **Gemma** (larger vocab) |
| **Attention Type** | Standard (global) | Hybrid (5:1 local:global) | Different approaches |
| **Attention Pattern** | All layers see full context | Only 1/6 layers see full context | **Qwen** (more global) |
| **Multilingual** | Excellent (esp. Chinese) | Good (100+ languages) | **Qwen** (Chinese), Gemma (breadth) |
| **Training Data** | Alibaba corpus | Google corpus | Different (hard to compare) |
| **Multimodal** | No (text-only in 4B) | Yes (vision + text) | **Gemma** |
| **RoPE Base Freq** | Standard (enhanced) | 1M (in global layers) | **Gemma** (long context) |
| **Organization** | Alibaba (China) | Google (USA) | Preference-dependent |
| **License** | Apache 2.0 / Qwen | Gemma Terms of Use | Qwen (more permissive) |

---

## Key Differences Summary

### Architecture

**Qwen3.5:4b**:
- Standard transformer with full attention at all layers
- Every layer can access entire context
- More memory usage (larger KV cache)
- Standard RoPE with extensions

**Gemma3:4b**:
- Hybrid local/global attention (5:1 ratio)
- Only 1/6 of layers see full context
- Less memory usage (KV cache only for global layers)
- Different RoPE configs for local vs global

### Training Philosophy

**Qwen**:
- Broad multilingual focus
- Strong Chinese capability
- Open research orientation
- Alibaba Cloud ecosystem

**Gemma**:
- Safety and alignment focus
- Google's quality standards
- Multimodal capability
- Responsible AI emphasis

### Performance Trade-offs

**Qwen3.5:4b**:
- ✅ Better for tasks needing full context access
- ✅ More consistent attention across positions
- ✅ Superior Chinese language handling
- ⚠️ Higher memory usage
- ⚠️ Potentially slower inference

**Gemma3:4b**:
- ✅ Much longer context window (128K vs 32K)
- ✅ More memory-efficient (local attention)
- ✅ Potentially faster inference
- ✅ Multimodal capability
- ⚠️ Only 1/6 of layers see full context
- ⚠️ Position bias effects unknown

---

# Relevance to Position Bias Research

## Why This Comparison is Scientifically Valuable

### Research Question

**"Do different attention architectures affect position bias in long-context tasks?"**

### Hypotheses to Test

#### Hypothesis 1: Local Attention Exacerbates Position Bias

**Prediction for Gemma3:4b**:
- Stronger position bias than Qwen3.5:4b
- Local attention layers cannot access distant information
- Model relies on infrequent global layers to connect documents
- **Expected result**: More pronounced U-shaped curve, worse middle performance

**Test**: Compare accuracies at middle positions (14-19 in 30-doc setting)

#### Hypothesis 2: Global Attention Compensates

**Prediction for Gemma3:4b**:
- Weaker position bias than Qwen3.5:4b
- Global layers every 6 layers provide "reset" to full context
- Periodic global access prevents information loss
- **Expected result**: Flatter curve, better middle performance

**Test**: Compare best-worst disparity between models

#### Hypothesis 3: Attention Type Doesn't Matter (Universal Bias)

**Prediction**:
- Both models show similar U-shaped curves
- Position bias is fundamental to decoder-only transformers
- Architecture is less important than scale
- **Expected result**: Curves overlap, similar accuracies

**Test**: Statistical significance of differences in position effects

---

## Experimental Controls

### What's Controlled (Same)

- ✅ **Parameter count**: Both ~4B
- ✅ **Model type**: Both decoder-only transformers
- ✅ **Training era**: Both 2024-2025 (recent)
- ✅ **Instruction-tuning**: Both are instruction-tuned
- ✅ **Task**: Same datasets, same evaluation
- ✅ **Inference settings**: Same temperature, max_tokens

### What's Different (Test Variables)

- **Attention architecture**: Standard vs hybrid local/global
- **Context window**: 32K vs 128K (but we only use ~3K)
- **Training data**: Alibaba vs Google corpus
- **Organization**: Different training philosophies
- **Tokenization**: Different vocabulary sizes

### Confounding Variables

**Potential confounds to consider**:
- Different training data may include different position patterns
- Different instruction-tuning approaches
- Different model widths/depths (for same 4B param count)
- Vocabulary differences → different token counts for same text

**Mitigation**: Focus on relative patterns (U-curve shape) rather than absolute accuracies

---

## Key Metrics to Compare

| Metric | What It Measures | Hypothesis |
|--------|------------------|------------|
| **Oracle Accuracy** | Overall capability | Should be similar (both 4B) |
| **Best Position Accuracy** | Peak performance | May favor start or end |
| **Worst Position Accuracy** | Weakest position | Likely middle positions |
| **Best-Worst Disparity** | Position bias magnitude | Gemma might be higher (local attention) OR lower (global rescue) |
| **Middle Position Avg** | Positions 14-19 (30-doc) | Critical test of local vs global attention |
| **U-Curve Shape** | Symmetric vs asymmetric | Different attention may create asymmetry |
| **Primacy vs Recency** | Start vs end bias | Local attention might favor recency |

---

## Expected Findings

### Scenario A: Gemma Shows Stronger Bias

**If Gemma3:4b has worse middle performance**:
- **Conclusion**: Local attention exacerbates position bias
- **Mechanism**: Limited context window in 5/6 layers prevents accessing middle documents
- **Implication**: Standard full attention is better for position-invariance

**Supporting evidence**:
- Higher best-worst disparity
- Lower middle position accuracies
- More pronounced U-curve

### Scenario B: Gemma Shows Weaker Bias

**If Gemma3:4b has better middle performance**:
- **Conclusion**: Periodic global attention compensates effectively
- **Mechanism**: Every 6th layer "rescues" middle information
- **Implication**: Hybrid attention is a solution to position bias!

**Supporting evidence**:
- Lower best-worst disparity
- Flatter performance curve
- Better middle position accuracies

### Scenario C: No Significant Difference

**If both models show similar patterns**:
- **Conclusion**: Position bias is fundamental, not architecture-dependent (at 4B scale)
- **Mechanism**: Decoder-only design inherently creates position preferences
- **Implication**: Need different solutions (training, prompting, or larger models)

**Supporting evidence**:
- Similar U-curve shapes
- No statistical difference in position effects
- Both show primacy/recency bias

---

## Publication Potential

### Why This Comparison is Novel

- ✅ First study (to our knowledge) comparing standard vs hybrid attention on position bias
- ✅ Controlled comparison (same scale, different architecture)
- ✅ Tests a specific architectural hypothesis (local/global attention)
- ✅ Replicates important prior work (Liu et al., 2023)
- ✅ Uses modern models (2024-2025, not 2023)

### Potential Contributions

1. **If attention type matters**: Provides guidance for future model design
2. **If local attention is worse**: Caution against efficiency optimizations that harm capability
3. **If global attention helps**: Supports hybrid architectures as solution
4. **Regardless of outcome**: Extends "Lost in the Middle" findings to modern models

### Possible Venues

- NeurIPS, ICLR, ACL workshops
- EMNLP (empirical methods)
- arXiv preprint + blog post
- Model analysis / interpretability venues

---

## Conclusion

These two 4B models provide an **ideal controlled experiment** for understanding position bias:

- **Same scale** (4B parameters)
- **Different architectures** (standard vs hybrid attention)
- **Different organizations** (Alibaba vs Google)
- **Both modern** (2024-2025)

The results will shed light on:
1. Whether attention architecture affects position bias
2. How local vs global attention impacts context usage
3. Whether modern models (2024-2025) have improved over 2023 models
4. Practical guidance for model selection and deployment

**This comparison is the scientific core of the replication study.**

---

**Document Version**: 1.0
**Last Updated**: 2026-03-30
**Status**: Models tested, experiments pending
**Next Update**: After pilot test results for both models

