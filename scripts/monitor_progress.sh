#!/bin/bash
# Simple progress monitor for the minimal foundation experiments

RESULTS_DIR="/home/b/Lost in the MIddle/lost-in-the-middle/Context/results/qa_predictions"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Experiment Progress Monitor${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check oracle pilots
echo -e "${YELLOW}Oracle Pilots:${NC}"

check_file() {
    local filepath="$1"
    local name="$2"

    if [ -f "$filepath" ]; then
        local size=$(stat -c%s "$filepath" 2>/dev/null || echo "0")
        local size_mb=$((size / 1024 / 1024))
        echo -e "  ${GREEN}✓${NC} $name (${size_mb}MB)"
        return 0
    else
        echo -e "  ⏳ $name (pending)"
        return 1
    fi
}

check_file "$RESULTS_DIR/pilot_test.jsonl.gz" "gemma3:4b"
check_file "$RESULTS_DIR/pilot_gemma3_27b.jsonl.gz" "gemma3:27b"
check_file "$RESULTS_DIR/pilot_mistral_small_22b.jsonl.gz" "mistral-small:22b"

echo ""
echo -e "${YELLOW}10-Document Experiments:${NC}"

# gemma3:4b
echo "  gemma3:4b:"
check_file "$RESULTS_DIR/gemma3_4b_10doc_gold_at_0.jsonl.gz" "    Position 0"
check_file "$RESULTS_DIR/gemma3_4b_10doc_gold_at_4.jsonl.gz" "    Position 4"
check_file "$RESULTS_DIR/gemma3_4b_10doc_gold_at_9.jsonl.gz" "    Position 9"

# mistral-small:22b
echo "  mistral-small:22b:"
check_file "$RESULTS_DIR/mistral-small_22b_10doc_gold_at_0.jsonl.gz" "    Position 0"
check_file "$RESULTS_DIR/mistral-small_22b_10doc_gold_at_4.jsonl.gz" "    Position 4"
check_file "$RESULTS_DIR/mistral-small_22b_10doc_gold_at_9.jsonl.gz" "    Position 9"

# gemma3:27b
echo "  gemma3:27b:"
check_file "$RESULTS_DIR/gemma3_27b_10doc_gold_at_0.jsonl.gz" "    Position 0"
check_file "$RESULTS_DIR/gemma3_27b_10doc_gold_at_4.jsonl.gz" "    Position 4"
check_file "$RESULTS_DIR/gemma3_27b_10doc_gold_at_9.jsonl.gz" "    Position 9"

echo ""
echo -e "${YELLOW}Closedbook Baseline:${NC}"
check_file "$RESULTS_DIR/gemma3_4b_closedbook.jsonl.gz" "gemma3:4b closedbook"

echo ""
echo -e "${BLUE}========================================${NC}"

# Check if automation script is running
if pgrep -f "run_minimal_foundation.sh" > /dev/null; then
    echo -e "${GREEN}✓${NC} Automation script is running"
else
    echo -e "${YELLOW}⚠${NC} Automation script is not running"
fi

# Show current gemma3:27b oracle progress if still running
GEMMA27_ORACLE="$RESULTS_DIR/pilot_gemma3_27b.jsonl.gz"
if [ -f "$GEMMA27_ORACLE" ]; then
    # Check if it's still being written to (file size changing)
    size1=$(stat -c%s "$GEMMA27_ORACLE" 2>/dev/null || echo "0")
    sleep 2
    size2=$(stat -c%s "$GEMMA27_ORACLE" 2>/dev/null || echo "0")

    if [ "$size1" != "$size2" ]; then
        size_mb=$((size2 / 1024 / 1024))
        echo ""
        echo -e "${BLUE}ℹ${NC}  gemma3:27b oracle still running (${size_mb}MB so far)"
    fi
fi

echo ""
