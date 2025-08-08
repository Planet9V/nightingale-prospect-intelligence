# Prospect Stakeholder Intelligence (PSI) Architecture v1.0

## Document Control
- **Version**: 1.0
- **Created**: June 18, 2025
- **Status**: Active
- **Classification**: Technical Architecture

## System Overview

The PSI system employs a multi-agent, parallel processing architecture designed for scalability, accuracy, and campaign-specific intelligence generation.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PSI ORCHESTRATOR                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Shared Scratchpad                      │   │
│  │  - Company Profiles    - Campaign Scores                │   │
│  │  - Industry Insights   - Enrichment Cache               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
┌───────▼────────┐                              ┌──────▼────────┐
│ EXTRACTION     │                              │ ENRICHMENT    │
│ AGENTS         │                              │ AGENTS        │
├────────────────┤                              ├───────────────┤
│ • File Parser  │                              │ • MCP Jina    │
│ • Pattern Match│                              │ • Email Finder│
│ • Role Extract │                              │ • Data Valid. │
└────────────────┘                              └───────────────┘
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼────────┐     ┌───────▼────────┐
            │ M&A CAMPAIGN   │     │ RANSOMWARE     │
            │ SCORER         │     │ CAMPAIGN SCORER│
            └────────────────┘     └────────────────┘
```

## Component Architecture

### 1. Orchestrator Core
```python
class PSIOrchestrator:
    """
    Central coordination system managing all agents and data flow
    """
    
    Components:
    - Agent Manager: Spawns and monitors parallel agents
    - Resource Manager: Controls concurrent execution limits
    - Data Manager: Maintains shared scratchpad consistency
    - Output Manager: Consolidates and formats results
    
    Key Methods:
    - initialize_system()
    - process_prospects_batch()
    - coordinate_agents()
    - consolidate_results()
```

### 2. Shared Scratchpad Design
```json
{
  "company_profiles": {
    "<sf_id>": {
      "company_name": "string",
      "industry": "string",
      "sub_industry": "string",
      "size_category": "string",
      "key_technologies": ["array"],
      "recent_events": ["array"]
    }
  },
  
  "extracted_personas": {
    "<persona_id>": {
      "sf_id": "string",
      "name": "string",
      "title": "string",
      "department": "string",
      "seniority": "string",
      "contact_info": {},
      "extracted_from": "string",
      "confidence_score": "float"
    }
  },
  
  "enrichment_cache": {
    "<persona_id>": {
      "email_searches": ["array"],
      "linkedin_profile": "string",
      "additional_context": "object"
    }
  },
  
  "campaign_scores": {
    "<persona_id>": {
      "m_a_score": "integer",
      "m_a_factors": ["array"],
      "ransomware_score": "integer",
      "ransomware_factors": ["array"]
    }
  }
}
```

### 3. Agent Architecture

#### Extraction Agents
```python
class ExtractionAgent:
    """
    Parallel agents for parsing prospect files
    """
    
    Responsibilities:
    - Parse markdown files in prospect folders
    - Extract personas using pattern matching
    - Identify roles, titles, and relationships
    - Extract existing contact information
    
    Patterns:
    - Executive sections in Organization_Foundation.md
    - Decision maker profiles in Engagement_Strategy.md
    - Stakeholder lists in GTM documents
```

#### Enrichment Agents
```python
class EnrichmentAgent:
    """
    Agents for data enhancement using external services
    """
    
    MCP Integrations:
    - Jina AI: Document analysis and extraction
    - Web search: Email and LinkedIn discovery
    - Validation: Contact verification
    
    Strategies:
    - Batch similar queries for efficiency
    - Cache results to avoid duplicates
    - Fallback methods for failed enrichments
```

#### Campaign Scoring Agents
```python
class CampaignScoringAgent:
    """
    Specialized agents for campaign-specific scoring
    """
    
    M&A Campaign Logic:
    - CFO/Finance: Base score 100
    - Corporate Development: Base score 90
    - Legal/Risk: Base score 80
    - Industry adjustments: ±20 points
    
    Ransomware Campaign Logic:
    - COO/Operations: Base score 100
    - CISO/Security: Base score 95
    - CIO/IT: Base score 85
    - Industry adjustments: ±20 points
```

## Data Flow Architecture

### 1. Input Processing
```
Prospect Folders → File Discovery → Parallel Parsing → Initial Extraction
                                                          │
                                                          ▼
                                                   Shared Scratchpad
```

### 2. Enrichment Pipeline
```
Extracted Personas → Enrichment Queue → MCP Services → Validation
                           │                              │
                           └─────── Parallel ─────────────┘
                                       │
                                       ▼
                                Enriched Dataset
```

### 3. Scoring Pipeline
```
Enriched Dataset → Campaign Rules → Parallel Scoring → Consolidation
                        │                                    │
                        ├── M&A Scorer                      │
                        └── Ransomware Scorer               │
                                                           ▼
                                                    Final Output
```

## Scalability Design

### Parallel Processing Strategy
1. **Batch Size**: 10-20 prospects per batch
2. **Agent Pool**: 5-10 concurrent agents
3. **Memory Management**: Streaming processing for large files
4. **Error Isolation**: Failed prospects don't block others

### Performance Optimization
```python
# Async processing pattern
async def process_batch(prospects):
    tasks = []
    for prospect in prospects:
        task = asyncio.create_task(
            process_single_prospect(prospect)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return consolidate_results(results)
```

## Integration Architecture

### MCP Service Integration
```yaml
mcp_config:
  jina_ai:
    endpoint: "mcp://jina-ai"
    capabilities:
      - document_extraction
      - entity_recognition
      - email_discovery
    rate_limits:
      requests_per_minute: 60
      batch_size: 10
```

### File System Integration
```python
prospect_structure = {
    "base_path": "/project_nightingale/prospects/",
    "pattern": "^[A-Z]-\d{6}_.*",
    "key_files": [
        "Organization_Foundation.md",
        "Engagement_Strategy.md",
        "*GTM*Part*3*.md"
    ]
}
```

## Security Architecture

### Data Protection
1. **In-Transit**: All MCP communications encrypted
2. **At-Rest**: Output files encrypted if containing PII
3. **Access Control**: Role-based access to outputs
4. **Audit Trail**: All operations logged in activity ledger

### Privacy Compliance
- No storage of unnecessary PII
- Data minimization principles
- Right to deletion support
- Compliance with GDPR/CCPA

## Error Handling Architecture

### Fault Tolerance
```python
error_handling = {
    "file_not_found": "skip_and_log",
    "parsing_error": "retry_with_fallback",
    "enrichment_failure": "proceed_without_enrichment",
    "scoring_error": "apply_default_score"
}
```

### Recovery Mechanisms
1. **Checkpoint System**: Save progress periodically
2. **Partial Results**: Return what succeeded
3. **Error Reporting**: Detailed logs for debugging
4. **Retry Logic**: Automatic retry for transient failures

## Monitoring Architecture

### Key Metrics
```yaml
performance_metrics:
  - prospects_processed_per_hour
  - enrichment_success_rate
  - average_personas_per_prospect
  - scoring_accuracy
  
quality_metrics:
  - data_completeness_score
  - enrichment_coverage
  - campaign_alignment_accuracy
```

### Observability
- Real-time progress tracking
- Performance dashboards
- Quality assurance reports
- Error analysis tools

## Evolution Path

### v1.0 (Current)
- File-based processing
- Basic MCP integration
- Two campaign types

### v2.0 (Planned)
- Database backend
- Advanced MCP features
- Multiple campaign types
- API endpoints

### v3.0 (Future)
- Machine learning scoring
- Real-time processing
- Predictive analytics
- Auto-learning patterns