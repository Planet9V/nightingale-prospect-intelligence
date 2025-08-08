# Prospect Stakeholder Intelligence (PSI) Capability

## Overview
The Prospect Stakeholder Intelligence (PSI) capability is an advanced, AI-driven system for extracting, enriching, and scoring key decision makers and influencers from Project Nightingale prospect data. It provides campaign-specific targeting intelligence for M&A Due Diligence and Ransomware campaigns.

## Quick Start

### Prerequisites
- Python 3.8+
- Access to Project Nightingale prospects folder
- MCP services configured (Jina AI for enrichment)

### Basic Usage
```bash
# Run extraction for all prospects
python scripts/orchestrator.py --campaign all --output outputs/

# Run for specific campaign
python scripts/orchestrator.py --campaign m_a --output outputs/

# Run for specific prospects
python scripts/orchestrator.py --prospects A-001457,A-008302 --campaign ransomware
```

## Key Features

### 1. Multi-Campaign Intelligence
- **M&A Due Diligence**: Targets financial decision makers (CFO, Corp Dev, Legal)
- **Ransomware**: Targets operational decision makers (COO, CISO, IT)

### 2. Comprehensive Persona Coverage
- C-Suite Executives
- Senior Management (VPs, Directors)
- Key Influencers (Managers, Technical Leads)
- Industry-Specific Roles

### 3. Intelligent Scoring
- Campaign-specific relevance scoring
- Industry-adjusted targeting
- Role-based prioritization
- Influence network mapping

### 4. Data Enrichment
- MCP Jina AI integration for missing emails
- Cross-reference learning
- Pattern recognition
- Automated data completion

## Output Format

The system generates a comprehensive Excel file with:
- Salesforce ID and company information
- Complete persona details (name, title, contact)
- Campaign-specific scores and rationale
- Engagement recommendations
- Data quality indicators

## Architecture

- **Orchestrator**: Manages parallel processing
- **Campaign Agents**: Specialized scoring for each campaign
- **Data Enrichment**: MCP service integration
- **Shared Scratchpad**: Cross-prospect learning

## Documentation

- [Charter](PSI_Charter_v1.md) - Business purpose and value
- [Architecture](PSI_Architecture_v1.md) - Technical design
- [SOP](PSI_SOP_v1.md) - Operational procedures
- [Specifications](PSI_Specifications_v1.md) - Technical requirements

## Tracking

- [Activity Ledger](activity_ledger.md) - All system activities
- [Batch Tracker](batch_tracker.md) - Processing batch details
- [Version History](version_history.md) - Capability evolution

## Version
Current Version: **v1.0**
Released: June 18, 2025

## Support
For issues or enhancements, please update the activity ledger and contact the Project Nightingale team.

## License
Internal Use Only - Project Nightingale