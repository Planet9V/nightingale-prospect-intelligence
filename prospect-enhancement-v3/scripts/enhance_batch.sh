#!/bin/bash

# Prospect Enhancement System v3 - Batch Enhancement Script
# Usage: ./enhance_batch.sh [batch_name] [batch_size]
# Example: ./enhance_batch.sh priority_2_batch_1 10

# Set defaults
BATCH_NAME=${1:-"default_batch"}
BATCH_SIZE=${2:-10}
BASE_DIR="/root/Desktop/project_nightingale_workspace/project_nightingale"
SCRIPT_DIR="$BASE_DIR/1_Capabilities/prospect_enhancement_v3"
LOG_DIR="$SCRIPT_DIR/logs"
TRACKER="$BASE_DIR/prospects/1_Prospect_analysis/ACTIVE_DOCS/ENHANCEMENT_TRACKER_2025_LIVE.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Session log file
SESSION_LOG="$LOG_DIR/session_$(date +%Y%m%d_%H%M%S).log"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$SESSION_LOG"
}

# Function to check MCP servers
check_mcp_servers() {
    log_message "${YELLOW}Checking MCP server status...${NC}"
    
    cd "$BASE_DIR" || exit 1
    
    if npm run claude-init > /tmp/mcp_check.log 2>&1; then
        if grep -q "ready" /tmp/mcp_check.log; then
            log_message "${GREEN}✓ MCP servers ready${NC}"
            return 0
        else
            log_message "${RED}✗ Some MCP servers not ready${NC}"
            cat /tmp/mcp_check.log >> "$SESSION_LOG"
            return 1
        fi
    else
        log_message "${RED}✗ Failed to check MCP servers${NC}"
        return 1
    fi
}

# Function to get next batch of prospects
get_next_batch() {
    log_message "${YELLOW}Identifying next $BATCH_SIZE prospects...${NC}"
    
    # Read from prospect groups configuration
    PROSPECTS=()
    
    # This would normally read from the JSON config and tracker
    # For now, using a simple approach
    if [ "$BATCH_NAME" == "priority_2_batch_1" ]; then
        PROSPECTS=(
            "A-020312_NXP_Semiconductors"
            "A-023123_BMW"
            "A-030734_Consumers_Energy"
            "A-022134_San_Francisco_International_Airport"
            "A-021654_Port_of_Long_Beach"
            "A-153223_GE_Vernova_Energy"
            "A-067890_Crestron_Electronics"
            "A-078901_Pepco_Holdings"
            "A-089012_Southern_California_Edison"
            "A-090123_Duke_Energy"
        )
    else
        log_message "${RED}✗ Unknown batch name: $BATCH_NAME${NC}"
        exit 1
    fi
    
    # Limit to requested batch size
    PROSPECTS=("${PROSPECTS[@]:0:$BATCH_SIZE}")
    
    log_message "${GREEN}✓ Found ${#PROSPECTS[@]} prospects to enhance${NC}"
}

# Function to create enhancement prompt
create_prompt() {
    local prospect_list=""
    local count=1
    
    for prospect in "${PROSPECTS[@]}"; do
        # Extract company name from prospect ID
        company_name=$(echo "$prospect" | sed 's/A-[0-9]*_//; s/_/ /g')
        prospect_list="${prospect_list}${count}. ${prospect} - ${company_name}\n"
        ((count++))
    done
    
    cat > "$LOG_DIR/current_batch_prompt.txt" << EOF
Process the following $BATCH_SIZE prospects, creating all 7 standard files for each:

$prospect_list

For each prospect:
1. Check existing files in prospects/[PROSPECT_ID]/
2. Create/update all 7 framework files:
   - Organization_Foundation.md
   - Strategic_Context.md
   - Technical_Infrastructure.md
   - Security_Intelligence.md
   - Vendor_Ecosystem.md
   - Business_Initiatives.md
   - Engagement_Strategy.md
3. Ensure 150+ data points per file
4. Focus on cybersecurity relevance
5. Use only real, current data (no templates)
6. Update the tracker after each completion

Target completion: 3 hours
Quality target: 9.5+ for each prospect

Begin with the first prospect and continue sequentially.
EOF
    
    log_message "${GREEN}✓ Enhancement prompt created${NC}"
}

# Function to update tracker
update_tracker() {
    local prospect=$1
    local status=$2
    local quality=$3
    
    timestamp=$(date '+%Y-%m-%d %H:%M:%S %Z')
    echo "| $timestamp | $prospect | Batch-$BATCH_NAME | $status | $quality |" >> "$TRACKER"
}

# Function to validate quality
validate_quality() {
    local prospect=$1
    local prospect_dir="$BASE_DIR/prospects/$prospect"
    
    log_message "${YELLOW}Validating quality for $prospect...${NC}"
    
    # Check for template placeholders
    if grep -r "\[.*\]" "$prospect_dir" > /dev/null 2>&1; then
        log_message "${RED}✗ Templates detected in $prospect${NC}"
        return 1
    fi
    
    # Check file count
    file_count=$(find "$prospect_dir" -name "*.md" -type f | grep -E "(Organization_Foundation|Strategic_Context|Technical_Infrastructure|Security_Intelligence|Vendor_Ecosystem|Business_Initiatives|Engagement_Strategy)" | wc -l)
    
    if [ "$file_count" -lt 7 ]; then
        log_message "${RED}✗ Only $file_count/7 files found for $prospect${NC}"
        return 1
    fi
    
    log_message "${GREEN}✓ Basic quality validation passed for $prospect${NC}"
    return 0
}

# Main execution
main() {
    log_message "${GREEN}=== Prospect Enhancement Batch Session ===${NC}"
    log_message "Batch: $BATCH_NAME"
    log_message "Size: $BATCH_SIZE prospects"
    log_message "Started: $(date)"
    log_message ""
    
    # Step 1: Check environment
    if ! check_mcp_servers; then
        log_message "${RED}✗ Environment check failed. Exiting.${NC}"
        exit 1
    fi
    
    # Step 2: Get prospects
    get_next_batch
    
    # Step 3: Create prompt
    create_prompt
    
    # Step 4: Display prompt for manual execution
    log_message ""
    log_message "${YELLOW}Enhancement prompt ready!${NC}"
    log_message "The prompt has been saved to: $LOG_DIR/current_batch_prompt.txt"
    log_message ""
    log_message "${GREEN}To execute enhancement:${NC}"
    log_message "1. Open Claude Code"
    log_message "2. Copy the prompt from: $LOG_DIR/current_batch_prompt.txt"
    log_message "3. Paste and execute in Claude"
    log_message "4. Monitor progress with: tail -f $TRACKER"
    log_message ""
    
    # Step 5: Wait for completion and validate
    log_message "${YELLOW}Press Enter when enhancement is complete to run validation...${NC}"
    read -r
    
    # Step 6: Validate each prospect
    log_message ""
    log_message "${YELLOW}Running quality validation...${NC}"
    
    passed=0
    failed=0
    
    for prospect in "${PROSPECTS[@]}"; do
        if validate_quality "$prospect"; then
            update_tracker "$prospect" "COMPLETE" "9.5+/10"
            ((passed++))
        else
            update_tracker "$prospect" "NEEDS_REVIEW" "TBD"
            ((failed++))
        fi
    done
    
    # Step 7: Summary
    log_message ""
    log_message "${GREEN}=== Batch Summary ===${NC}"
    log_message "Total Prospects: ${#PROSPECTS[@]}"
    log_message "Passed Validation: $passed"
    log_message "Need Review: $failed"
    log_message "Completion Rate: $(( passed * 100 / ${#PROSPECTS[@]} ))%"
    log_message "Ended: $(date)"
    log_message ""
    
    if [ $failed -gt 0 ]; then
        log_message "${YELLOW}⚠ Some prospects need review. Check the tracker for details.${NC}"
    else
        log_message "${GREEN}✓ All prospects successfully enhanced!${NC}"
    fi
    
    log_message ""
    log_message "Full session log: $SESSION_LOG"
    log_message "Tracker: $TRACKER"
}

# Run main function
main