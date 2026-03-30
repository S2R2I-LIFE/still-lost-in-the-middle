#!/bin/bash
# Complete automation script - runs mistral oracle, then 10-doc experiments, then closedbook
# This script runs everything remaining after gemma3:27b oracle

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$PROJECT_ROOT/Context/results"
PYTHON="/home/b/miniconda3/envs/lost-in-the-middle/bin/python"

# Set PYTHONPATH so all scripts can find the lost_in_the_middle module
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

# Function to check if Ollama is running
check_ollama() {
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        log_error "Ollama is not running!"
        log_error "Please start it with: ollama serve"
        exit 1
    fi
    log_success "Ollama is running"
}

# Function to evaluate QA results
evaluate_qa() {
    local input_path="$1"
    local model_name="$2"

    log_info "Evaluating $model_name results..."

    cd "$PROJECT_ROOT"
    "$PYTHON" scripts/evaluate_qa_responses.py \
        --input-path "$input_path" 2>&1 | tee -a "$RESULTS_DIR/evaluation_log.txt"

    local exit_code=${PIPESTATUS[0]}
    if [ $exit_code -eq 0 ]; then
        log_success "$model_name evaluation complete"
        return 0
    else
        log_error "$model_name evaluation failed with exit code $exit_code"
        return 1
    fi
}

# Start
log_section "MINIMAL FOUNDATION - REMAINING EXPERIMENTS"
log_info "Starting at $(date)"

mkdir -p "$RESULTS_DIR/qa_predictions"
mkdir -p "$RESULTS_DIR/evaluation_scores"

# Check Ollama
check_ollama

# Step 1: Run mistral-small:22b oracle
log_section "STEP 1: Running mistral-small:22b Oracle Pilot"
MISTRAL_ORACLE="$RESULTS_DIR/qa_predictions/pilot_mistral_small_22b.jsonl.gz"

log_info "Processing 2,655 oracle examples with mistral-small:22b..."

"$PYTHON" "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
    --model mistral-small:22b \
    --input-path "$PROJECT_ROOT/qa_data/nq-open-oracle.jsonl.gz" \
    --output-path "$MISTRAL_ORACLE" \
    --temperature 0.0 \
    --max-new-tokens 100

if [ $? -eq 0 ]; then
    log_success "mistral-small:22b oracle pilot complete"
    # Evaluate immediately
    evaluate_qa "$MISTRAL_ORACLE" "mistral-small:22b oracle"
else
    log_error "mistral-small:22b oracle pilot failed"
    exit 1
fi

# Step 2: Run 10-document QA experiments
log_section "STEP 2: Running 10-Document QA Experiments"

MODELS=("gemma3:4b" "mistral-small:22b" "gemma3:27b")

# Check if 10-doc datasets exist
if [ ! -d "$PROJECT_ROOT/qa_data/10_total_documents" ]; then
    log_error "10-document datasets not found at qa_data/10_total_documents/"
    log_info "Please ensure the datasets are available"
    exit 1
fi

# 10-document datasets
QA_10DOC_DATASETS=(
    "nq-open-10_total_documents_gold_at_0.jsonl.gz"
    "nq-open-10_total_documents_gold_at_4.jsonl.gz"
    "nq-open-10_total_documents_gold_at_9.jsonl.gz"
)

# Run experiments
for model in "${MODELS[@]}"; do
    log_info "Starting 10-doc experiments for $model"

    for dataset_name in "${QA_10DOC_DATASETS[@]}"; do
        dataset="$PROJECT_ROOT/qa_data/10_total_documents/$dataset_name"

        # Extract position from filename
        if [[ $dataset_name =~ gold_at_([0-9]+) ]]; then
            position="${BASH_REMATCH[1]}"
        else
            log_error "Could not extract position from $dataset_name"
            continue
        fi

        # Create safe model name for filename
        model_safe=$(echo "$model" | tr ':' '_')
        output_file="$RESULTS_DIR/qa_predictions/${model_safe}_10doc_gold_at_${position}.jsonl.gz"

        log_info "Running $model on 10-doc (gold at position $position)..."
        log_info "Input: $dataset"
        log_info "Output: $output_file"

        "$PYTHON" "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
            --model "$model" \
            --input-path "$dataset" \
            --output-path "$output_file" \
            --temperature 0.0 \
            --max-new-tokens 100

        if [ $? -eq 0 ]; then
            log_success "$model 10-doc position $position complete"
            evaluate_qa "$output_file" "$model 10-doc position $position"
        else
            log_error "$model 10-doc position $position failed"
        fi
    done

    log_success "All 10-doc experiments complete for $model"
done

# Step 3: Run closedbook baseline
log_section "STEP 3: Running Closedbook Baseline"
log_info "Running gemma3:4b with no context..."

"$PYTHON" "$SCRIPT_DIR/get_qa_responses_from_ollama.py" \
    --model gemma3:4b \
    --input-path "$PROJECT_ROOT/qa_data/nq-open-oracle.jsonl.gz" \
    --output-path "$RESULTS_DIR/qa_predictions/gemma3_4b_closedbook.jsonl.gz" \
    --temperature 0.0 \
    --max-new-tokens 100 \
    --closedbook

if [ $? -eq 0 ]; then
    log_success "Closedbook baseline complete"
    evaluate_qa "$RESULTS_DIR/qa_predictions/gemma3_4b_closedbook.jsonl.gz" "gemma3:4b closedbook"
else
    log_error "Closedbook baseline failed"
fi

# Final summary
log_section "EXPERIMENTS COMPLETE"
log_success "All minimal foundation experiments finished at $(date)"

echo ""
log_info "Results summary:"
echo "  Oracle pilots: Context/results/qa_predictions/pilot_*.jsonl.gz"
echo "  10-doc experiments: Context/results/qa_predictions/*_10doc_*.jsonl.gz"
echo "  Closedbook: Context/results/qa_predictions/gemma3_4b_closedbook.jsonl.gz"
echo "  Evaluations: Context/results/evaluation_log.txt"

echo ""
log_success "🎉 Ready for analysis!"
