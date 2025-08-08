# Organa JSON Specification V2
*For Project Nightingale Prospect Intelligence Tracking*

## Overview
The organa.json file (stored as `Master_Intelligence_Profile.json` in each prospect's `05_Organa_Profile` folder) tracks completeness, quality, and metadata for prospect intelligence.

## File Location
```
prospects/A-XXXXXX_Company_Name/05_Organa_Profile/Master_Intelligence_Profile.json
```

## Complete Schema

```json
{
  "prospect_id": "A-XXXXXX_Company_Name",
  "enhancement_version": "3.0",
  "last_updated": "2024-06-15T10:30:00Z",
  "company_info": {
    "legal_name": "Company Legal Name Inc.",
    "common_name": "Company",
    "sector": "Energy|Manufacturing|Transportation|Technology|Food",
    "subsector": "Electric Utility|Oil & Gas|Rail|etc",
    "size": "Large|Medium|Small",
    "revenue": "$X.XB",
    "employees": 12345
  },
  "completeness_scores": {
    "organization_foundation": {
      "score": 10,
      "sections": {
        "legal_structure": {
          "score": 10,
          "data_points": 15,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "financials": {
          "score": 10,
          "data_points": 22,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "leadership": {
          "score": 10,
          "data_points": 45,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "governance": {
          "score": 10,
          "data_points": 18,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 100
    },
    "strategic_context": {
      "score": 10,
      "sections": {
        "recent_news": {
          "score": 10,
          "data_points": 35,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "competitive_landscape": {
          "score": 10,
          "data_points": 28,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "culture_values": {
          "score": 10,
          "data_points": 15,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 78
    },
    "technical_infrastructure": {
      "score": 10,
      "sections": {
        "technology_stack": {
          "score": 10,
          "data_points": 45,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "ot_environment": {
          "score": 10,
          "data_points": 38,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "digital_initiatives": {
          "score": 10,
          "data_points": 22,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 105
    },
    "security_intelligence": {
      "score": 10,
      "sections": {
        "security_posture": {
          "score": 10,
          "data_points": 32,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "incident_history": {
          "score": 10,
          "data_points": 18,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "compliance_status": {
          "score": 10,
          "data_points": 25,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "threat_landscape": {
          "score": 10,
          "data_points": 30,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 105
    },
    "vendor_ecosystem": {
      "score": 10,
      "sections": {
        "current_vendors": {
          "score": 10,
          "data_points": 25,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "contract_details": {
          "score": 10,
          "data_points": 15,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "satisfaction_indicators": {
          "score": 10,
          "data_points": 12,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 52
    },
    "business_initiatives": {
      "score": 10,
      "sections": {
        "active_projects": {
          "score": 10,
          "data_points": 28,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "budget_cycles": {
          "score": 10,
          "data_points": 15,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "rfps_procurements": {
          "score": 10,
          "data_points": 18,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 61
    },
    "engagement_strategy": {
      "score": 10,
      "sections": {
        "value_proposition": {
          "score": 10,
          "data_points": 35,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "stakeholder_matrix": {
          "score": 10,
          "data_points": 40,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "implementation_roadmap": {
          "score": 10,
          "data_points": 25,
          "has_templates": false,
          "last_updated": "2024-06-15"
        },
        "battle_card": {
          "score": 10,
          "data_points": 50,
          "has_templates": false,
          "last_updated": "2024-06-15"
        }
      },
      "total_score": 10,
      "total_data_points": 150
    }
  },
  "overall_metrics": {
    "overall_score": 10.0,
    "total_data_points": 751,
    "has_templates": false,
    "completeness_percentage": 100,
    "files_enhanced": 7,
    "files_pending": 0
  },
  "quality_metrics": {
    "citation_count": 147,
    "named_individuals": 45,
    "specific_technologies": 38,
    "quantified_metrics": 62,
    "recency_score": 9.5,
    "oldest_data_days": 45,
    "actionability_score": 10
  },
  "knowledge_graph_readiness": {
    "nodes": {
      "people": 45,
      "technologies": 38,
      "vendors": 12,
      "threats": 8,
      "initiatives": 15,
      "locations": 23
    },
    "relationships": {
      "reports_to": 35,
      "vendor_of": 12,
      "threatens": 8,
      "implements": 23,
      "located_at": 45
    },
    "total_nodes": 141,
    "total_relationships": 123
  },
  "enhancement_log": [
    {
      "date": "2024-06-15T10:30:00Z",
      "agent": "Agent-1",
      "action": "Full enhancement from templates",
      "changes": [
        "Replaced all template placeholders",
        "Added 751 data points",
        "Reorganized to 7-file structure"
      ],
      "duration_hours": 6.5,
      "mcp_services_used": ["tavily", "jina_ai", "context7"]
    }
  ],
  "research_sources": {
    "web_sources": 89,
    "document_sources": 34,
    "api_sources": 12,
    "database_sources": 8,
    "total_sources": 143
  },
  "validation_status": {
    "last_validated": "2024-06-15T16:45:00Z",
    "validation_passed": true,
    "validation_warnings": [],
    "next_review_date": "2024-09-15"
  }
}
```

## Scoring Methodology

### Score Calculation (1-10 scale)
- **10**: Complete, current, cited, actionable intelligence
- **8-9**: Mostly complete, minor gaps
- **6-7**: Significant content but some templates remain
- **4-5**: Mix of real content and templates
- **2-3**: Mostly templates with minimal real data
- **1**: Templates only or empty

### Data Point Counting
- Each discrete piece of information = 1 point
- Examples:
  - Executive name and title = 2 points
  - Revenue figure with year = 2 points
  - Specific technology vendor = 1 point
  - Threat actor identification = 1 point

### Quality Indicators
- `has_templates`: true if ANY template placeholders remain
- `recency_score`: 10 if all data <30 days, decreases with age
- `actionability_score`: Based on specificity and usefulness for sales

## Usage Examples

### Check Overall Completeness
```python
with open(organa_path) as f:
    data = json.load(f)
    print(f"Overall Score: {data['overall_metrics']['overall_score']}/10")
    print(f"Data Points: {data['overall_metrics']['total_data_points']}")
    print(f"Has Templates: {data['overall_metrics']['has_templates']}")
```

### Identify Enhancement Needs
```python
for file, metrics in data['completeness_scores'].items():
    if metrics['score'] < 9:
        print(f"{file} needs enhancement: {metrics['score']}/10")
```

### Knowledge Graph Export
```python
nodes = data['knowledge_graph_readiness']['nodes']
relationships = data['knowledge_graph_readiness']['relationships']
# Export to graph database format
```

## Validation Rules
1. All scores must be 0-10
2. If `has_templates` is true, max score is 5
3. Total data points should be 700-1000 for complete profile
4. All dates in ISO 8601 format
5. At least one enhancement log entry required

---
*This specification defines the complete tracking system for Project Nightingale prospect intelligence.*