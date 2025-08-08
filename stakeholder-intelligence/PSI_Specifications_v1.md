# Prospect Stakeholder Intelligence (PSI) Technical Specifications v1.0

## Document Control
- **Version**: 1.0
- **Created**: June 18, 2025
- **Status**: Active
- **Classification**: Technical Specification

## System Requirements

### Hardware Requirements
- **Minimum**:
  - CPU: 4 cores, 2.0 GHz
  - RAM: 8 GB
  - Storage: 10 GB free space
  - Network: Broadband internet

- **Recommended**:
  - CPU: 8+ cores, 3.0 GHz
  - RAM: 16 GB
  - Storage: 50 GB SSD
  - Network: High-speed connection

### Software Requirements
- **Operating System**: Linux/macOS/Windows 10+
- **Python**: 3.8+ with pip
- **Node.js**: 14+ (for MCP services)
- **Required Python Packages**:
  ```
  pandas>=1.3.0
  openpyxl>=3.0.0
  asyncio
  aiofiles>=0.8.0
  pyyaml>=5.4
  jsonschema>=3.2.0
  python-dotenv>=0.19.0
  ```

### MCP Service Requirements
- **Jina AI**: Configured and accessible
- **MCP Server**: Running and verified
- **Authentication**: Valid credentials

## Input Specifications

### Prospect Folder Structure
```
prospects/
├── {SF_ID}_{Company_Name}/
│   ├── Organization_Foundation.md
│   ├── Strategic_Context.md
│   ├── Business_Initiatives.md
│   ├── Engagement_Strategy.md
│   ├── Technical_Infrastructure.md
│   ├── Security_Intelligence.md
│   ├── Vendor_Ecosystem.md
│   └── *_GTM_Part_3_*.md (optional)
```

### SF_ID Format
- Pattern: `^[A-Z]-\d{6}$`
- Examples: `A-001457`, `B-023456`
- Case-sensitive
- Always 8 characters

### Markdown File Structure
```markdown
# Document Title

## Section with Executives
### Executive Name - Title
- Background information
- Tenure: Since 2020
- Previous: Former role
- Education: Degree, University

### Another Executive - Title
Content about this executive...
```

## Output Specifications

### Excel Output Schema

#### Main Sheet: "Stakeholder Intelligence"
| Column Name | Data Type | Required | Description | Example |
|-------------|-----------|----------|-------------|---------|
| SF_ID | String | Yes | Salesforce ID | A-001457 |
| Company_Name | String | Yes | Company name | Boeing Corporation |
| Industry | String | Yes | Primary industry | Aerospace & Defense |
| Sub_Industry | String | No | Industry vertical | Commercial Aviation |
| Annual_Revenue | String | No | Revenue figure | $77.8B |
| Employee_Count | String | No | Number of employees | 170,000+ |
| Headquarters | String | No | HQ location | Arlington, VA |
| Full_Name | String | Yes | Person's full name | Kelly Ortberg |
| Title | String | Yes | Current title | President & CEO |
| Department | String | No | Functional area | Executive |
| Email | String | No | Email address | k.ortberg@boeing.com |
| Phone | String | No | Phone number | +1-555-123-4567 |
| LinkedIn | String | No | LinkedIn profile URL | linkedin.com/in/kortberg |
| Tenure | String | No | Time in role | Since July 2024 |
| Previous_Role | String | No | Previous position | CEO, Rockwell Collins |
| Education | String | No | Educational background | BS, Iowa State |
| Role_Type | String | Yes | Classification | CEO/President |
| Authority_Level | String | Yes | Decision authority | Ultimate Decision Maker |
| Budget_Authority | String | Yes | Budget control | Yes |
| Veto_Power | String | Yes | Veto ability | Yes |
| Reports_To | String | No | Reporting relationship | Board of Directors |
| Team_Size | String | No | Direct reports | 12 |
| M_A_Score | Integer | Yes | M&A campaign score | 85 |
| M_A_Rationale | String | Yes | M&A scoring reason | Financial oversight |
| Ransomware_Score | Integer | Yes | Ransomware score | 95 |
| Ransomware_Rationale | String | Yes | Ransomware reason | Operational impact |
| Key_Priorities | String | No | Top priorities | Safety, Production |
| Pain_Points | String | No | Current challenges | Quality issues |
| Engagement_Approach | String | No | How to engage | Board-level risk |
| Data_Quality_Score | Float | Yes | Confidence score | 0.95 |
| Source_File | String | Yes | Where extracted from | Organization_Foundation.md |
| Extraction_Date | DateTime | Yes | When processed | 2025-06-18 09:15:00 |

#### Summary Sheet: "Batch Summary"
- Total Prospects Processed
- Total Personas Extracted
- Average Personas per Prospect
- Campaign Score Distribution
- Data Quality Metrics
- Processing Time
- Error Summary

### CSV Output Schema
- Same as Excel main sheet
- UTF-8 encoding
- Comma-separated
- Quoted text fields

### JSON Output Schema (Optional)
```json
{
  "batch_id": "PSI-2025-06-18-001",
  "metadata": {
    "version": "1.0",
    "extraction_date": "2025-06-18T09:15:00Z",
    "prospects_processed": 133,
    "total_personas": 1247
  },
  "personas": [
    {
      "sf_id": "A-001457",
      "company": {
        "name": "Boeing Corporation",
        "industry": "Aerospace & Defense",
        "metrics": {}
      },
      "person": {
        "full_name": "Kelly Ortberg",
        "title": "President & CEO",
        "contact": {},
        "background": {}
      },
      "scores": {
        "m_a": {
          "score": 85,
          "factors": ["CEO authority", "M&A oversight"]
        },
        "ransomware": {
          "score": 95,
          "factors": ["Operational impact", "Crisis leader"]
        }
      }
    }
  ]
}
```

## Processing Specifications

### Extraction Rules

#### Name Extraction Patterns
1. **Bold Format**: `**Name** - Title`
2. **Heading Format**: `### Name - Title`
3. **List Format**: `- Name: Title`

#### Title Normalization
- Remove trailing periods
- Standardize abbreviations (VP → Vice President)
- Remove company name suffixes
- Preserve full title hierarchy

#### Role Classification Logic
```python
role_mappings = {
    "CEO/President": ["ceo", "chief executive", "president"],
    "CFO": ["cfo", "chief financial"],
    "CIO/CTO": ["cio", "cto", "chief information", "chief technology"],
    "CISO": ["ciso", "chief security"],
    "COO": ["coo", "chief operating"],
    "EVP": ["evp", "executive vice president"],
    "SVP": ["svp", "senior vice president"],
    "VP": ["vp", "vice president"],
    "Director": ["director"],
    "Manager": ["manager"],
    "Board Member": ["board", "chairman", "trustee"]
}
```

### Campaign Scoring Algorithms

#### M&A Due Diligence Scoring
```python
def calculate_m_a_score(persona, company_context):
    base_scores = {
        "CEO/President": 85,
        "CFO": 100,
        "Corporate Development": 95,
        "General Counsel": 85,
        "Board Member": 80,
        "VP Finance": 75,
        "Controller": 70,
        "VP Strategy": 85
    }
    
    # Industry adjustments
    if company_context.industry == "Private Equity":
        if "Partner" in persona.title:
            base_score += 20
    
    # Size adjustments
    if company_context.revenue > 1000000000:  # $1B+
        base_score += 10
    
    return min(base_score, 100)
```

#### Ransomware Campaign Scoring
```python
def calculate_ransomware_score(persona, company_context):
    base_scores = {
        "COO": 100,
        "CISO": 95,
        "CIO/CTO": 90,
        "VP Operations": 85,
        "IT Director": 80,
        "Security Manager": 75,
        "Business Continuity Manager": 85,
        "Risk Manager": 80
    }
    
    # Industry adjustments
    critical_infrastructure = [
        "Energy", "Healthcare", "Financial Services",
        "Transportation", "Water", "Communications"
    ]
    
    if company_context.industry in critical_infrastructure:
        base_score += 15
    
    return min(base_score, 100)
```

### Data Enrichment Specifications

#### MCP Jina AI Integration
```yaml
jina_config:
  search_patterns:
    email:
      - "{first_name}.{last_name}@{company_domain}"
      - "{first_initial}{last_name}@{company_domain}"
      - "contact {full_name} {company_name} email"
    
    linkedin:
      - "site:linkedin.com/in {full_name} {company_name}"
      - "{full_name} {title} linkedin"
  
  confidence_thresholds:
    email: 0.8
    linkedin: 0.7
    general: 0.6
```

#### Enrichment Priority
1. Email addresses (highest value)
2. Direct phone numbers
3. LinkedIn profiles
4. Additional context/background

### Performance Specifications

#### Processing Targets
- **Extraction Speed**: 1-2 seconds per prospect
- **Enrichment Speed**: 3-5 seconds per persona
- **Scoring Speed**: <0.1 seconds per persona
- **Total Time**: <2 hours for full dataset

#### Concurrency Limits
```yaml
concurrency:
  max_parallel_prospects: 10
  max_enrichment_requests: 5
  max_file_handles: 50
  memory_limit_mb: 4096
```

#### Error Thresholds
- Maximum acceptable error rate: 5%
- File not found: Skip and log
- Parse errors: 3 retry attempts
- Enrichment failures: Continue without

## Quality Assurance Specifications

### Data Validation Rules

#### Required Field Validation
```python
required_fields = {
    "sf_id": r"^[A-Z]-\d{6}$",
    "company_name": r".{2,100}",
    "full_name": r".{3,50}",
    "title": r".{3,100}",
    "role_type": ["CEO/President", "CFO", ...],
    "authority_level": ["Ultimate Decision Maker", ...],
    "m_a_score": range(0, 101),
    "ransomware_score": range(0, 101)
}
```

#### Email Validation
```python
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

#### Data Completeness Targets
- Name completion: 100%
- Title completion: 100%
- Email discovery: >60%
- Phone discovery: >30%
- LinkedIn discovery: >40%

### Output Quality Metrics
```yaml
quality_metrics:
  persona_per_prospect:
    minimum: 1
    target: 5-10
    maximum: 50
  
  data_accuracy:
    title_accuracy: 95%
    company_match: 100%
    role_classification: 90%
  
  enrichment_success:
    email_found: 60%
    valid_emails: 95%
    linkedin_found: 40%
```

## Security Specifications

### Data Handling
- No storage of passwords or credentials
- Email addresses stored in lowercase
- Phone numbers stored without formatting
- No credit card or SSN processing

### Access Control
```yaml
access_control:
  read_permissions:
    - project_nightingale_team
    - sales_leadership
  
  write_permissions:
    - psi_operators
    - system_admins
  
  audit_trail: enabled
  encryption: optional
```

### Privacy Compliance
- GDPR Article 6(1)(f) - Legitimate Interest
- CCPA compliance for California residents
- Data retention: 90 days
- Right to deletion supported

## Version Control Specifications

### Semantic Versioning
- Format: `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Change Documentation
- All changes logged in `version_history.md`
- Git commits for code changes
- Document version in filename
- Backward compatibility notes

## Integration Specifications

### API Endpoints (Future)
```yaml
api_spec:
  base_url: /api/psi/v1
  endpoints:
    - GET /prospects
    - GET /personas/{sf_id}
    - POST /extract
    - GET /batch/{batch_id}
  
  authentication: bearer_token
  rate_limits: 100_requests_per_minute
```

### Export Formats
1. **Excel** (primary)
2. **CSV** (backup)
3. **JSON** (API)
4. **Parquet** (analytics)

---
**Note**: These specifications define the v1.0 implementation. Future versions may extend or modify these requirements.