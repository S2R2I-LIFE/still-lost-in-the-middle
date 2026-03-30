#!/bin/bash
# Batch execution script for "Lost in the Middle" replication with Ollama models
# This script runs all QA and KV experiments across all selected models

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$PROJECT_ROOT/Context/results"

# Models to test (as specified in Context/models.txt)
# Updated 2026-03-30: Replaced Qwen models (reasoning models) with Gemma models (direct answers)
MODELS=(
    "gemma3:27b"         # Large tier (17GB, ~27B params)
    "mistral-small:22b"  # Medium tier (12GB, ~22B params)
    "gemma3:4b"          # Small tier (3.3GB, ~4B params) - pilot tested: 89.15% oracle accuracy
)

# Inference parameters (matching original paper)
TEMPERATURE=0.0
TOP_P=1.0
MAX_TOKENS_QA=100
MAX_TOKENS_KV=50
TIMEOUT=300

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Ollama is running
check_ollama() {
    log_info "Checking if Ollama is running..."
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        log_success "Ollama is running"
        return 0
    else
        log_error "Ollama is not running. Please start it with: ollama serve"
        return 1
    fi
}

# Check if a model is available
check_model() {
    local model=$1
    log_info "Checking if model $model is available..."
    if ollama list | grep -q "$model"; then
        log_success "Model $model is available"
        return 0
    else
        log_warning "Model $model not found. Attempting to pull..."
        ollama pull "$model" || {
            log_error "Failed to pull model $model"
            return 1
        }
        log_success "Successfully pulled model $model"
        return 0
    fi
}

# Create output directories
setup_directories() {
    log_info "Setting up output directories..."
    mkdir -p "$RESULTS_DIR/qa_predictions"
    mkdir -p "$RESULTS_DIR/kv_predictions"
    mkdir -p "$RESULTS_DIR/evaluation_scores"
    log_success "Directories created"
}

# Run QA experiments for a single model
run_qa_experiments() {
    local model=$1
    local model_slug=$(echo "$model" | tr ':' '_')  # Replace : with _ for filenames

    log_info "Running QA experiments for model: $model"

    # Oracle baseline
    log_info "  Running oracle baseline..."
    python "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
        --model "$model" \
        --input-path "$PROJECT_ROOT/qa_data/nq-open-oracle.jsonl.gz" \
        --output-path "$RESULTS_DIR/qa_predictions/${model_slug}_oracle.jsonl.gz" \
        --temperature $TEMPERATURE \
        --top-p $TOP_P \
        --max-new-tokens $MAX_TOKENS_QA \
        --request-timeout $TIMEOUT

    # 10 documents setting
    for file in "$PROJECT_ROOT/qa_data/10_total_documents"/*.jsonl.gz; do
        filename=$(basename "$file" .jsonl.gz)
        log_info "  Running: $filename"
        python "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
            --model "$model" \
            --input-path "$file" \
            --output-path "$RESULTS_DIR/qa_predictions/${model_slug}_${filename}.jsonl.gz" \
            --temperature $TEMPERATURE \
            --top-p $TOP_P \
            --max-new-tokens $MAX_TOKENS_QA \
            --request-timeout $TIMEOUT
    done

    # 20 documents setting
    for file in "$PROJECT_ROOT/qa_data/20_total_documents"/*.jsonl.gz; do
        filename=$(basename "$file" .jsonl.gz)
        log_info "  Running: $filename"
        python "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
            --model "$model" \
            --input-path "$file" \
            --output-path "$RESULTS_DIR/qa_predictions/${model_slug}_${filename}.jsonl.gz" \
            --temperature $TEMPERATURE \
            --top-p $TOP_P \
            --max-new-tokens $MAX_TOKENS_QA \
            --request-timeout $TIMEOUT
    done

    # 30 documents setting
    for file in "$PROJECT_ROOT/qa_data/30_total_documents"/*.jsonl.gz; do
        filename=$(basename "$file" .jsonl.gz)
        log_info "  Running: $filename"
        python "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
            --model "$model" \
            --input-path "$file" \
            --output-path "$RESULTS_DIR/qa_predictions/${model_slug}_${filename}.jsonl.gz" \
            --temperature $TEMPERATURE \
            --top-p $TOP_P \
            --max-new-tokens $MAX_TOKENS_QA \
            --request-timeout $TIMEOUT
    done

    log_success "QA experiments completed for $model"
}

# Run KV experiments for a single model
run_kv_experiments() {
    local model=$1
    local model_slug=$(echo "$model" | tr ':' '_')

    log_info "Running KV experiments for model: $model"

    # Note: KV experiments require specifying gold_index
    # The original datasets already have varied positions, but we need to run
    # the script with different gold_index values to test position effects

    # For now, we'll run with gold_index=0 (start position)
    # A complete run would test multiple positions (0, middle, end)

    for file in "$PROJECT_ROOT/kv_retrieval_data"/*.jsonl.gz; do
        filename=$(basename "$file" .jsonl.gz)

        # Extract number of keys from filename (e.g., kv-retrieval-75_keys.jsonl.gz -> 75)
        num_keys=$(echo "$filename" | grep -oP '\d+')

        log_info "  Running: $filename (gold_index=0)"
        python "$SCRIPT_DIR/get_kv_responses_from_ollama.py" \
            --model "$model" \
            --input-path "$file" \
            --output-path "$RESULTS_DIR/kv_predictions/${model_slug}_${filename}_gold0.jsonl.gz" \
            --temperature $TEMPERATURE \
            --top-p $TOP_P \
            --max-new-tokens $MAX_TOKENS_KV \
            --gold-index 0 \
            --request-timeout $TIMEOUT
    done

    log_success "KV experiments completed for $model"
}

# Evaluate QA results for a model
evaluate_qa() {
    local model=$1
    local model_slug=$(echo "$model" | tr ':' '_')

    log_info "Evaluating QA results for $model..."

    # The original evaluate script processes all prediction files
    # We'll call it with the pattern for this model's predictions
    python "$SCRIPT_DIR/evaluate_qa_responses.py" \
        --input-path "$RESULTS_DIR/qa_predictions/${model_slug}_*.jsonl.gz" \
        > "$RESULTS_DIR/evaluation_scores/${model_slug}_qa_evaluation.txt" 2>&1 || {
        log_warning "Evaluation failed for $model (may need manual review)"
    }

    log_success "QA evaluation completed for $model"
}

# Evaluate KV results for a model
evaluate_kv() {
    local model=$1
    local model_slug=$(echo "$model" | tr ':' '_')

    log_info "Evaluating KV results for $model..."

    python "$SCRIPT_DIR/evaluate_kv_responses.py" \
        --input-path "$RESULTS_DIR/kv_predictions/${model_slug}_*.jsonl.gz" \
        > "$RESULTS_DIR/evaluation_scores/${model_slug}_kv_evaluation.txt" 2>&1 || {
        log_warning "Evaluation failed for $model (may need manual review)"
    }

    log_success "KV evaluation completed for $model"
}

# Main execution function
main() {
    log_info "===== Lost in the Middle - Ollama Replication ====="
    log_info "Starting batch experiments"
    log_info "Start time: $(date)"

    # Pre-flight checks
    check_ollama || exit 1
    setup_directories

    # Check all models are available
    for model in "${MODELS[@]}"; do
        check_model "$model" || {
            log_error "Model $model not available and couldn't be pulled. Exiting."
            exit 1
        }
    done

    # Run experiments for each model
    for model in "${MODELS[@]}"; do
        log_info "=========================================="
        log_info "Starting experiments for model: $model"
        log_info "=========================================="

        # Run QA experiments
        run_qa_experiments "$model" || {
            log_error "QA experiments failed for $model"
            continue
        }

        # Run KV experiments
        run_kv_experiments "$model" || {
            log_error "KV experiments failed for $model"
            continue
        }

        # Evaluate results
        evaluate_qa "$model"
        evaluate_kv "$model"

        log_success "All experiments completed for $model"
    done

    log_info "===== All experiments completed ====="
    log_info "End time: $(date)"
    log_info "Results saved to: $RESULTS_DIR"
}

# Usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help        Show this help message"
    echo "  --qa-only     Run only QA experiments"
    echo "  --kv-only     Run only KV experiments"
    echo "  --model NAME  Run for specific model only (e.g., qwen3.5:4b)"
    echo ""
    echo "Examples:"
    echo "  $0                           # Run all experiments"
    echo "  $0 --qa-only                 # Run only QA experiments"
    echo "  $0 --model qwen3.5:4b        # Run for single model"
}

# Parse command line arguments
RUN_QA=true
RUN_KV=true
SPECIFIC_MODEL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            usage
            exit 0
            ;;
        --qa-only)
            RUN_KV=false
            shift
            ;;
        --kv-only)
            RUN_QA=false
            shift
            ;;
        --model)
            SPECIFIC_MODEL="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Override models list if specific model requested
if [ -n "$SPECIFIC_MODEL" ]; then
    MODELS=("$SPECIFIC_MODEL")
fi

# Run main function
main
