# Prospect Enhancement System v3 - Standard Operating Procedures

## Table of Contents

1. [SOP-001: Initial Setup & Environment Verification](#sop-001-initial-setup--environment-verification)
2. [SOP-002: Batch Processing (10 Prospects)](#sop-002-batch-processing-10-prospects)
3. [SOP-003: Single Prospect Enhancement](#sop-003-single-prospect-enhancement)
4. [SOP-004: Quality Validation](#sop-004-quality-validation)
5. [SOP-005: Progress Tracking & Reporting](#sop-005-progress-tracking--reporting)
6. [SOP-006: Error Recovery & Resume](#sop-006-error-recovery--resume)
7. [SOP-007: Background Processing](#sop-007-background-processing)
8. [SOP-008: Version Management](#sop-008-version-management)

---

## SOP-001: Initial Setup & Environment Verification

**Purpose**: Ensure environment is properly configured for prospect enhancement operations

**Frequency**: Before each session, after any system changes

### Prerequisites
- Access to Project Nightingale workspace
- Claude Code or CLI access
- MCP server credentials

### Procedure

1. **Verify Current Date/Time**
   ```bash
   date
   ```
   Expected: Current date/time in correct timezone

2. **Check MCP Server Status**
   ```bash
   npm run claude-init
   ```
   Required servers (must show "ready"):
   - ✅ tavily (web search)
   - ✅ context7 (documentation)
   - ✅ supermemory (AI memory)
   - ✅ pinecone (vector search)
   - ✅ neo4j (graph database)
   - ✅ jina-ai (deep research)

3. **Verify Directory Structure**
   ```bash
   cd /root/Desktop/project_nightingale_workspace/project_nightingale
   ls prospects/
   ls prospects/1_Prospect_analysis/ACTIVE_DOCS/
   ```

4. **Check Enhancement Tracker**
   ```bash
   cat prospects/1_Prospect_analysis/ACTIVE_DOCS/ENHANCEMENT_TRACKER_2025_LIVE.md | tail -50
   ```

5. **Verify Script Availability**
   ```bash
   ls 1_Capabilities/prospect_enhancement_v3/scripts/
   ```

### Troubleshooting
- If MCP servers fail: Check API keys in environment
- If directories missing: Verify correct workspace
- If tracker corrupted: Use backup from logs/

### Success Criteria
- All 6 critical MCP servers show "ready"
- Enhancement tracker shows current progress
- Scripts are accessible and executable

---

## SOP-002: Batch Processing (10 Prospects)

**Purpose**: Process a standard batch of 10 prospects efficiently

**Frequency**: Daily during enhancement phase

### Prerequisites
- Completed SOP-001
- List of prospects to enhance
- 2-3 hours available time

### Procedure

1. **Select Next Batch**
   ```bash
   # Check tracker for next prospects
   grep "QUEUED" ENHANCEMENT_TRACKER_2025_LIVE.md | head -10
   ```

2. **Create Batch Configuration**
   ```bash
   cat > current_batch.txt << EOF
   A-020312_NXP_Semiconductors
   A-023123_BMW
   A-030734_Consumers_Energy
   A-022134_San_Francisco_International_Airport
   A-021654_Port_of_Long_Beach
   A-153223_GE_Vernova_Energy
   A-XXXXXX_Company_7
   A-XXXXXX_Company_8
   A-XXXXXX_Company_9
   A-XXXXXX_Company_10
   EOF
   ```

3. **Start Batch Enhancement**
   - Open Claude Code
   - Load the batch prompt:
   ```
   Process the following 10 prospects in parallel, creating all 7 files for each:
   [paste current_batch.txt contents]
   
   For each prospect:
   1. Check existing files in prospects/A-XXXXXX_Company_Name/
   2. Create missing files from 7-file framework
   3. Ensure 150+ data points per file
   4. No templates, only real data
   5. Update tracker after completion
   ```

4. **Monitor Progress**
   ```bash
   # In separate terminal
   watch -n 60 'tail -20 ENHANCEMENT_TRACKER_2025_LIVE.md'
   ```

5. **Checkpoint Saves**
   - Every 30 minutes: Save session state
   - After each prospect: Verify files created
   - Update tracker with completion status

6. **Batch Completion**
   - Run quality validation (SOP-004)
   - Update master tracker
   - Archive session logs
   - Prepare next batch list

### Quality Checkpoints
- After 3 prospects: Spot check quality
- After 5 prospects: Verify pace on track
- After 10 prospects: Full quality review

### Success Criteria
- 10 prospects completed in 2-3 hours
- All files pass quality validation
- Tracker updated with progress
- No template placeholders remain

---

## SOP-003: Single Prospect Enhancement

**Purpose**: Enhance a single prospect with focused attention

**Frequency**: As needed for priority prospects or remediation

### Prerequisites
- Prospect ID and company name
- Understanding of company's industry
- Access to existing files

### Procedure

1. **Analyze Current State**
   ```bash
   ls prospects/A-XXXXXX_Company_Name/
   grep -r "\[.*\]" prospects/A-XXXXXX_Company_Name/ | head -20
   ```

2. **Read Existing Content**
   - Organization_Foundation.md (if exists)
   - Strategic_Context.md (if exists)
   - Enhanced_Executive_Concierge_Report*.md

3. **Execute Enhancement**
   ```
   Create the complete 7-file intelligence profile for [Company Name] (A-XXXXXX):
   
   Current state: [X] files exist, [Y] files missing
   Industry: [Industry type]
   Key focus: Cybersecurity for [specific sector]
   
   Requirements:
   - Real executive names and backgrounds
   - Specific technology vendors and systems
   - Recent security incidents or concerns
   - Current business initiatives
   - 150+ data points per file
   ```

4. **File Creation Order**
   1. Organization_Foundation.md (company basics)
   2. Strategic_Context.md (business environment)
   3. Technical_Infrastructure.md (technology stack)
   4. Security_Intelligence.md (threat landscape)
   5. Vendor_Ecosystem.md (partnerships)
   6. Business_Initiatives.md (current projects)
   7. Engagement_Strategy.md (sales approach)

5. **Quality Verification**
   - Check each file for completeness
   - Verify no template placeholders
   - Count data points
   - Ensure current information

### Success Criteria
- All 7 files created/updated
- Quality score ≥9.5/10
- Real data throughout
- Coherent narrative across files

---

## SOP-004: Quality Validation

**Purpose**: Ensure all enhanced prospects meet quality standards

**Frequency**: After each prospect completion, batch review

### Prerequisites
- Completed enhancement files
- Quality checklist
- Validation scripts

### Procedure

1. **Automated Validation**
   ```bash
   python scripts/validate_quality.py A-XXXXXX_Company_Name
   ```
   
   Checks performed:
   - Template detection
   - Data point counting
   - File completeness
   - Recency validation

2. **Manual Spot Checks**
   
   For each file, verify:
   - [ ] Real executive names (not "executives" or "[CEO Name]")
   - [ ] Specific dates (not "recently" or "[Year]")
   - [ ] Actual vendor names (not "various vendors")
   - [ ] Quantified metrics (revenue, employees, etc.)
   - [ ] Current information (<90 days where possible)

3. **Quality Scoring**
   
   Rate each file 1-10 on:
   - Completeness (all sections present)
   - Specificity (real names, numbers)
   - Relevance (cybersecurity focus)
   - Actionability (useful for sales)
   
   Calculate average: Must be ≥9.5

4. **Template Detection**
   ```bash
   grep -r "\[.*\]" prospects/A-XXXXXX_Company_Name/
   grep -r "Company Name" prospects/A-XXXXXX_Company_Name/
   grep -r "various\|numerous\|multiple" prospects/A-XXXXXX_Company_Name/
   ```
   
   Expected: No results

5. **Document Results**
   ```json
   {
     "prospect_id": "A-XXXXXX",
     "validation_date": "2025-06-18",
     "quality_score": 9.7,
     "data_points": 1243,
     "template_count": 0,
     "issues": [],
     "validator": "System"
   }
   ```

### Remediation Process
If quality <9.5:
1. Identify specific gaps
2. Re-enhance problem sections
3. Re-validate
4. Document improvements

### Success Criteria
- Quality score ≥9.5/10
- Zero template placeholders
- 150+ data points per file
- Passes automated checks

---

## SOP-005: Progress Tracking & Reporting

**Purpose**: Maintain accurate progress tracking and stakeholder reporting

**Frequency**: Continuous during operations, daily summaries

### Prerequisites
- Access to tracking systems
- Understanding of metrics
- Reporting templates

### Procedure

1. **Update Live Tracker**
   
   After each prospect:
   ```markdown
   | 2025-06-18 07:30 | A-XXXXXX_Company | Manual | COMPLETED | 9.8/10 |
   ```

2. **Calculate Metrics**
   ```bash
   # Total progress
   echo "Enhanced: 55/129 (42.6%)"
   
   # By priority
   echo "Priority 1: 25/25 (100%)"
   echo "Priority 2: 11/41 (26.8%)"
   echo "Priority 3: 0/63 (0%)"
   ```

3. **Daily Summary Update**
   
   Add to tracker:
   ```markdown
   ## Daily Summary - [Date]
   - Prospects Completed: X
   - Average Quality: X.X/10
   - Total Data Points: X,XXX
   - Issues Encountered: [List]
   - Tomorrow's Plan: [Next batch]
   ```

4. **Weekly Report Generation**
   ```bash
   python scripts/generate_weekly_report.py > reports/week_XX_report.md
   ```

5. **Stakeholder Communication**
   - Email progress summary
   - Update project dashboard
   - Flag any blockers
   - Share success metrics

### Key Metrics to Track
- Prospects completed (daily/weekly/total)
- Quality scores (average, range)
- Processing time per prospect
- Data points generated
- Template detection rate
- Error/retry rate

### Success Criteria
- Real-time tracking updated
- Daily summaries complete
- Weekly reports delivered
- Metrics trending positive

---

## SOP-006: Error Recovery & Resume

**Purpose**: Recover from interruptions and resume enhancement operations

**Frequency**: As needed when errors or interruptions occur

### Prerequisites
- Understanding of last known state
- Access to session logs
- Backup files available

### Procedure

1. **Assess Current State**
   ```bash
   # Check last tracker update
   tail -50 ENHANCEMENT_TRACKER_2025_LIVE.md
   
   # Review session logs
   ls -la logs/session_*.log
   tail -100 logs/session_latest.log
   ```

2. **Identify Incomplete Work**
   ```bash
   # Find prospects marked as IN_PROGRESS
   grep "IN_PROGRESS" ENHANCEMENT_TRACKER_2025_LIVE.md
   
   # Check for partial files
   find prospects/ -name "*.md" -mtime -1 -size -1k
   ```

3. **Verify Partial Progress**
   
   For each incomplete prospect:
   - List existing files
   - Check file sizes and content
   - Identify what's missing
   - Note last update time

4. **Create Recovery Plan**
   ```markdown
   ## Recovery Plan - [Date/Time]
   
   ### Incomplete Prospects:
   1. A-XXXXXX: Missing 3 files (Technical, Security, Vendor)
   2. A-YYYYYY: All files partial, need completion
   
   ### Recovery Order:
   1. Complete A-XXXXXX (est. 1 hour)
   2. Restart A-YYYYYY (est. 2 hours)
   ```

5. **Execute Recovery**
   - Start with most complete prospects
   - Preserve any partial work
   - Update tracker with recovery status
   - Validate completed work

6. **Post-Recovery Validation**
   - Run quality checks on recovered prospects
   - Verify no data corruption
   - Update metrics
   - Document lessons learned

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| MCP server timeout | Restart servers, retry operation |
| Partial file write | Complete file, run validation |
| Session crash | Use auto-save, resume from checkpoint |
| Quality degradation | Re-enhance affected sections |

### Success Criteria
- All incomplete work recovered
- Quality maintained ≥9.5/10
- Progress tracking accurate
- Root cause documented

---

## SOP-007: Background Processing

**Purpose**: Run enhancement operations in background for efficiency

**Frequency**: Optional for experienced operators

### Prerequisites
- Claude CLI installed
- Screen or tmux available
- Proven prompts ready

### Procedure

1. **Prepare Background Script**
   ```bash
   cat > enhance_background.sh << 'EOF'
   #!/bin/bash
   PROSPECT_ID=$1
   PROSPECT_NAME=$2
   
   claude -p "Create all 7 files for $PROSPECT_NAME ($PROSPECT_ID) \
   following standard structure. Requirements: 150+ data points, \
   no templates, current information. Save to prospects/$PROSPECT_ID/"
   EOF
   
   chmod +x enhance_background.sh
   ```

2. **Start Background Session**
   ```bash
   screen -S enhancement
   # or
   tmux new -s enhancement
   ```

3. **Launch Parallel Processes**
   ```bash
   # Up to 3 parallel processes recommended
   ./enhance_background.sh A-XXXXXX Company_1 > logs/bg_1.log 2>&1 &
   ./enhance_background.sh A-YYYYYY Company_2 > logs/bg_2.log 2>&1 &
   ./enhance_background.sh A-ZZZZZZ Company_3 > logs/bg_3.log 2>&1 &
   
   # Monitor
   jobs
   tail -f logs/bg_*.log
   ```

4. **Progress Monitoring**
   ```bash
   # Check process status
   ps aux | grep enhance_background
   
   # Monitor file creation
   watch -n 30 'ls -la prospects/A-*/  | grep "\.md$" | wc -l'
   ```

5. **Completion Handling**
   - Wait for all jobs to complete
   - Run quality validation
   - Update tracker
   - Archive logs

### Best Practices
- Maximum 3-5 parallel processes
- Monitor resource usage
- Check for errors regularly
- Maintain session logs

### Success Criteria
- Background processes complete successfully
- Quality maintained
- No resource exhaustion
- Logs capture all activity

---

## SOP-008: Version Management

**Purpose**: Manage enhancement versions and track improvements

**Frequency**: With each process update or improvement

### Prerequisites
- Understanding of version history
- Access to version tracker
- Change approval (if required)

### Procedure

1. **Document Current Version**
   ```bash
   cat PES_Version_Tracker_v3.md
   ```
   
   Current: v3.0 (AI-powered enhancement)

2. **Track Prospect Versions**
   
   In each Organa.json:
   ```json
   {
     "enhancement_version": "3.0",
     "enhancement_date": "2025-06-18",
     "quality_score": 9.7
   }
   ```

3. **Version Change Process**
   
   For minor updates (v3.x):
   1. Document proposed changes
   2. Test on 2-3 prospects
   3. Compare quality metrics
   4. Update documentation
   5. Roll out if improved

4. **Change Documentation**
   ```markdown
   ## Version 3.1 - [Date]
   
   ### Changes:
   - Improved vendor research depth
   - Added financial metrics validation
   - Enhanced security incident detection
   
   ### Impact:
   - Quality scores: 9.6 → 9.8 average
   - Data points: +15% average
   - Processing time: -10%
   
   ### Rollout:
   - Tested on: A-XXXXXX, A-YYYYYY
   - Applied from: [Date]
   ```

5. **Version Rollback**
   
   If issues detected:
   1. Stop current processing
   2. Document issues
   3. Revert to previous version
   4. Re-process affected prospects
   5. Investigate root cause

6. **Version Reporting**
   ```bash
   # Generate version metrics
   python scripts/version_metrics.py --version=3.0
   
   # Compare versions
   python scripts/compare_versions.py --v1=2.0 --v2=3.0
   ```

### Version Compatibility
- v3.x: Current production version
- v2.x: Deprecated, do not use
- v1.x: Historical only

### Success Criteria
- All prospects tagged with version
- Version improvements documented
- Quality metrics improve or maintain
- Rollback procedures tested

---

## Emergency Procedures

### System Failure
1. Stop all processing
2. Document error state
3. Notify technical support
4. Implement recovery plan

### Quality Crisis
1. Halt enhancement operations
2. Identify affected prospects
3. Run comprehensive validation
4. Remediate all issues
5. Update processes

### Resource Exhaustion
1. Reduce parallel processing
2. Clear temporary files
3. Restart MCP servers
4. Resume at lower capacity

---

## Appendices

### A. Quality Checklist Template
- [ ] All 7 files present
- [ ] No template placeholders
- [ ] 150+ data points per file
- [ ] Current information (<90 days)
- [ ] Real names and numbers
- [ ] Cybersecurity focus
- [ ] Coherent narrative
- [ ] Actionable insights

### B. Common Commands Reference
```bash
# Check progress
tail -50 ENHANCEMENT_TRACKER_2025_LIVE.md

# Find templates
grep -r "\[.*\]" prospects/A-XXXXXX/

# Count data points
wc -w prospects/A-XXXXXX/*.md

# Validate quality
python scripts/validate_quality.py A-XXXXXX
```

### C. Troubleshooting Matrix

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Slow processing | MCP overload | Reduce parallel ops |
| Template detection | Incomplete research | Re-run with focus |
| Low quality scores | Rushed processing | Single prospect mode |
| Missing files | Incomplete run | Resume from checkpoint |

---

*Version: 3.0 | Last Updated: 2025-06-18*
*These SOPs are living documents. Update based on operational experience.*