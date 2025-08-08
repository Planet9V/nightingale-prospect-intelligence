# Prospect Stakeholder Intelligence (PSI) Standard Operating Procedures v1.0

## Document Control
- **Version**: 1.0
- **Created**: June 18, 2025
- **Status**: Active
- **Classification**: Operational Guide

## Table of Contents
1. [Pre-Operation Checklist](#pre-operation-checklist)
2. [Execution Procedures](#execution-procedures)
3. [Quality Assurance](#quality-assurance)
4. [Troubleshooting](#troubleshooting)
5. [Post-Processing](#post-processing)

## Pre-Operation Checklist

### Environment Verification
```bash
# 1. Verify Python version (must be 3.8+)
python --version

# 2. Check MCP services availability
npm run mcp-verify

# 3. Verify prospect folder access
ls /root/Desktop/project_nightingale_workspace/project_nightingale/prospects/ | wc -l

# 4. Check write permissions for output
touch /root/Desktop/project_nightingale_workspace/project_nightingale/1_Capabilities/Prospect_Stakeholder/outputs/test.txt
rm /root/Desktop/project_nightingale_workspace/project_nightingale/1_Capabilities/Prospect_Stakeholder/outputs/test.txt
```

### Pre-Flight Checks
- [ ] Activity ledger is accessible
- [ ] Previous batch completed successfully
- [ ] No locked files in output directory
- [ ] Sufficient disk space (>1GB)
- [ ] MCP Jina AI service responding

## Execution Procedures

### Step 1: Initialize New Batch
```bash
# 1. Navigate to PSI directory
cd /root/Desktop/project_nightingale_workspace/project_nightingale/1_Capabilities/Prospect_Stakeholder/

# 2. Create new batch entry
echo "Creating new batch entry..."
python scripts/batch_initializer.py --create-new
# This will output: Batch ID: PSI-2025-06-18-XXX
```

### Step 2: Configure Extraction Parameters
```bash
# For full extraction (all prospects, all campaigns)
python scripts/orchestrator.py --config full

# For specific campaign
python scripts/orchestrator.py --config campaign --campaign-type m_a

# For specific prospects
python scripts/orchestrator.py --config selective --prospects "A-001457,A-008302"
```

### Step 3: Execute Main Processing
```bash
# Standard execution
python scripts/orchestrator.py --execute \
    --batch-id PSI-2025-06-18-XXX \
    --parallel-agents 8 \
    --enrichment enabled \
    --output-format excel

# Monitor progress
tail -f logs/psi_execution_[batch-id].log
```

### Step 4: Monitor Execution
During execution, monitor these indicators:
1. **Progress Bar**: Shows prospects processed
2. **Agent Status**: Active/Idle agent count
3. **Error Count**: Should remain <5%
4. **Memory Usage**: Should stay <80% system RAM

### Step 5: Validate Results
```bash
# Run validation script
python scripts/validator.py --batch-id PSI-2025-06-18-XXX

# Check validation report
cat outputs/validation_report_[batch-id].txt
```

## Quality Assurance

### Data Quality Checks

#### Completeness Check
- [ ] All prospects have been processed
- [ ] Minimum 1 persona per prospect
- [ ] Critical fields populated (Name, Title, Company)
- [ ] Campaign scores assigned

#### Accuracy Verification
1. **Sample 10 random records**
   ```bash
   python scripts/qa_sampler.py --batch-id PSI-2025-06-18-XXX --sample 10
   ```

2. **Verify against source**
   - Open source prospect file
   - Confirm persona exists
   - Validate title accuracy
   - Check scoring logic

#### Enrichment Validation
- [ ] Email discovery rate >60%
- [ ] No obviously invalid emails
- [ ] LinkedIn profiles format correct
- [ ] No duplicate personas

### Campaign Scoring Validation

#### M&A Campaign Checks
- CFOs have highest scores (90-100)
- Finance executives properly identified
- Legal/Risk roles included
- Board members captured

#### Ransomware Campaign Checks
- COOs/Operations leaders prioritized
- CISO/Security roles high-scored
- IT leadership included
- Business continuity roles captured

## Troubleshooting

### Common Issues and Solutions

#### Issue: MCP Service Timeout
```bash
# Symptoms: Enrichment failing, timeout errors

# Solution 1: Restart MCP service
npm run mcp-verify

# Solution 2: Reduce batch size
python scripts/orchestrator.py --execute --parallel-agents 4

# Solution 3: Skip enrichment
python scripts/orchestrator.py --execute --enrichment disabled
```

#### Issue: Memory Errors
```bash
# Symptoms: Process killed, out of memory

# Solution 1: Process in smaller batches
python scripts/orchestrator.py --batch-size 20

# Solution 2: Clear scratchpad
rm temp/scratchpad_*.json

# Solution 3: Increase swap space (temporary)
sudo swapon --show
```

#### Issue: Parsing Errors
```bash
# Symptoms: Specific prospects failing

# Solution 1: Check file encoding
file prospects/[problem-folder]/*.md

# Solution 2: Run in debug mode
python scripts/orchestrator.py --debug --prospects [problem-sf-id]

# Solution 3: Manual override
python scripts/manual_entry.py --sf-id [problem-sf-id]
```

#### Issue: Output File Corrupted
```bash
# Symptoms: Excel file won't open

# Solution 1: Use CSV backup
python scripts/converter.py --to-csv --batch-id PSI-2025-06-18-XXX

# Solution 2: Regenerate from cache
python scripts/regenerate_output.py --batch-id PSI-2025-06-18-XXX
```

## Post-Processing

### Step 1: Update Activity Ledger
```bash
# Automatic update
python scripts/ledger_update.py --batch-id PSI-2025-06-18-XXX --status complete

# Manual update (if needed)
echo "| $(date -u +"%Y-%m-%d %H:%M:%S UTC") | v1.0 | Batch PSI-2025-06-18-XXX completed | $USER | 133 prospects processed, 1,247 personas extracted | Complete |" >> activity_ledger.md
```

### Step 2: Generate Summary Report
```bash
# Create execution summary
python scripts/summary_generator.py --batch-id PSI-2025-06-18-XXX

# Review summary
cat outputs/summary_PSI-2025-06-18-XXX.md
```

### Step 3: Archive and Cleanup
```bash
# Archive outputs
cp outputs/PSI_output_[timestamp].xlsx outputs/archive/

# Clean temporary files
rm temp/scratchpad_*.json
rm logs/*_debug.log

# Compress logs
gzip logs/psi_execution_[batch-id].log
```

### Step 4: Distribution
1. **Notify Stakeholders**
   - Email sales leadership with summary
   - Update shared drive with new file
   - Post metrics to dashboard

2. **File Locations**
   - Primary: `outputs/PSI_output_[timestamp].xlsx`
   - Backup: `outputs/PSI_output_[timestamp].csv`
   - Archive: `outputs/archive/`

## Performance Benchmarks

### Expected Performance
- **Small Batch (10 prospects)**: 5-10 minutes
- **Medium Batch (50 prospects)**: 20-30 minutes
- **Full Run (130+ prospects)**: 60-90 minutes

### Performance Optimization
1. **Increase parallel agents** (if RAM allows)
2. **Disable enrichment** for speed
3. **Use SSD** for temp files
4. **Close other applications**

## Maintenance Procedures

### Weekly Maintenance
- [ ] Clean temp directory
- [ ] Archive old outputs
- [ ] Review error logs
- [ ] Update enrichment cache

### Monthly Maintenance
- [ ] Full system test
- [ ] Performance benchmarking
- [ ] Documentation review
- [ ] Stakeholder feedback

## Emergency Procedures

### System Recovery
1. **Stop all processes**
   ```bash
   pkill -f orchestrator.py
   ```

2. **Check system state**
   ```bash
   python scripts/health_check.py
   ```

3. **Restore from checkpoint**
   ```bash
   python scripts/restore_checkpoint.py --latest
   ```

### Data Recovery
- Backups in: `outputs/archive/`
- Checkpoints in: `temp/checkpoints/`
- Logs in: `logs/`

## Escalation Path

### Level 1: Operator Issues
- Check this SOP
- Review logs
- Retry with reduced load

### Level 2: Technical Issues
- Contact Technical Lead
- Provide batch ID and error logs
- Document in activity ledger

### Level 3: System Failures
- Contact Project Nightingale Team
- Initiate disaster recovery
- Executive notification if needed

## Appendix: Quick Reference

### Command Cheat Sheet
```bash
# Full run
python scripts/orchestrator.py --execute --config full

# M&A only
python scripts/orchestrator.py --execute --campaign m_a

# Specific prospects
python scripts/orchestrator.py --execute --prospects "A-001457,A-008302"

# Debug mode
python scripts/orchestrator.py --debug --verbose

# Validation
python scripts/validator.py --batch-id [ID]

# Quick status
tail -f logs/psi_execution_*.log | grep "Progress"
```

### File Locations
- Scripts: `scripts/`
- Configs: `configs/`
- Outputs: `outputs/`
- Logs: `logs/`
- Temp: `temp/`

---
**Remember**: Always update the activity ledger after each run!