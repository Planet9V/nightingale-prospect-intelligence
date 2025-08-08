// 🕵️ NIGHTINGALE UNIFIED NEO4J SCHEMA FOR PROJECT SELDON
// Comprehensive knowledge graph schema for prospect intelligence and threat analysis
// Version: 1.0.0 - Production Ready
// Last Updated: August 8, 2025

// =============================================================================
// NODE TYPES - Core Entities
// =============================================================================

// ORGANIZATIONS - Primary entities for prospect intelligence
CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.org_id IS UNIQUE;
CREATE INDEX organization_name IF NOT EXISTS FOR (o:Organization) ON (o.name);
CREATE INDEX organization_sector IF NOT EXISTS FOR (o:Organization) ON (o.sector);

// PEOPLE - Key stakeholders and decision makers
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE;
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX person_role IF NOT EXISTS FOR (p:Person) ON (p.role);

// TECHNOLOGIES - IT/OT infrastructure and systems
CREATE CONSTRAINT technology_id IF NOT EXISTS FOR (t:Technology) REQUIRE t.tech_id IS UNIQUE;
CREATE INDEX technology_name IF NOT EXISTS FOR (t:Technology) ON (t.name);
CREATE INDEX technology_category IF NOT EXISTS FOR (t:Technology) ON (t.category);

// THREATS - Threat actors, campaigns, and TTPs
CREATE CONSTRAINT threat_id IF NOT EXISTS FOR (th:Threat) REQUIRE th.threat_id IS UNIQUE;
CREATE INDEX threat_name IF NOT EXISTS FOR (th:Threat) ON (th.name);
CREATE INDEX threat_type IF NOT EXISTS FOR (th:Threat) ON (th.type);

// VULNERABILITIES - Security weaknesses and exposures
CREATE CONSTRAINT vulnerability_id IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.vuln_id IS UNIQUE;
CREATE INDEX vulnerability_cve IF NOT EXISTS FOR (v:Vulnerability) ON (v.cve_id);
CREATE INDEX vulnerability_severity IF NOT EXISTS FOR (v:Vulnerability) ON (v.severity);

// SECTORS - Critical infrastructure sectors
CREATE CONSTRAINT sector_id IF NOT EXISTS FOR (s:Sector) REQUIRE s.sector_id IS UNIQUE;
CREATE INDEX sector_name IF NOT EXISTS FOR (s:Sector) ON (s.name);

// LOCATIONS - Geographic information
CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.location_id IS UNIQUE;
CREATE INDEX location_name IF NOT EXISTS FOR (l:Location) ON (l.name);

// DOCUMENTS - Intelligence reports and documentation
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.doc_id IS UNIQUE;
CREATE INDEX document_type IF NOT EXISTS FOR (d:Document) ON (d.type);

// =============================================================================
// RELATIONSHIP TYPES - Core Connections
// =============================================================================

// ORGANIZATIONAL RELATIONSHIPS
// OWNS - Asset ownership (Organization owns Technology)
// EMPLOYS - Personnel relationships (Organization employs Person)
// PARTNERS_WITH - Business partnerships (Organization partners_with Organization)
// COMPETES_WITH - Competitive relationships (Organization competes_with Organization)
// SUPPLIES_TO - Supply chain relationships (Organization supplies_to Organization)

// TECHNOLOGICAL RELATIONSHIPS  
// USES - Technology usage (Organization uses Technology)
// DEPENDS_ON - Dependencies (Technology depends_on Technology)
// CONNECTS_TO - Network connections (Technology connects_to Technology)
// HOSTS - Hosting relationships (Technology hosts Technology)

// THREAT RELATIONSHIPS
// TARGETS - Threat targeting (Threat targets Organization/Technology)
// EXPLOITS - Vulnerability exploitation (Threat exploits Vulnerability)
// AFFECTS - Impact relationships (Vulnerability affects Technology)
// MITIGATES - Security controls (Technology mitigates Vulnerability)

// GEOGRAPHIC RELATIONSHIPS
// LOCATED_IN - Physical location (Organization/Person located_in Location)
// OPERATES_IN - Operational presence (Organization operates_in Location)

// INTELLIGENCE RELATIONSHIPS
// DOCUMENTED_IN - Documentation links (Entity documented_in Document)
// ANALYZED_BY - Analysis relationships (Entity analyzed_by Person)

// =============================================================================
// SAMPLE SCHEMA IMPLEMENTATION
// =============================================================================

// Create sample sector nodes
CREATE (energy:Sector {
    sector_id: "SECT-001",
    name: "Energy",
    description: "Electric utilities, oil & gas, renewable energy",
    criticality: "Critical",
    regulation: "NERC, DOE",
    created_at: datetime(),
    updated_at: datetime()
});

CREATE (manufacturing:Sector {
    sector_id: "SECT-002", 
    name: "Manufacturing",
    description: "Industrial manufacturing and production facilities",
    criticality: "Critical",
    regulation: "EPA, OSHA",
    created_at: datetime(),
    updated_at: datetime()
});

// Create sample organization with comprehensive properties
CREATE (johnson_controls:Organization {
    org_id: "ORG-029867",
    name: "Johnson Controls International plc",
    sector: "Manufacturing",
    industry: "Building Technologies & Solutions",
    headquarters: "Cork, Ireland",
    revenue: 25100000000,
    employees: 100000,
    stock_symbol: "JCI",
    website: "https://www.johnsoncontrols.com",
    description: "Global leader in building technologies and solutions",
    founded: 1885,
    ceo: "George Oliver",
    threat_level: "Medium-High",
    security_maturity: "Developing",
    intelligence_priority: "High",
    last_assessment: date("2025-08-08"),
    created_at: datetime(),
    updated_at: datetime(),
    // Prospect intelligence specific fields
    sales_stage: "Qualified",
    engagement_score: 8.5,
    decision_timeline: "Q4 2025",
    budget_authority: "Confirmed",
    technical_fit: 9.2,
    competitive_position: "Strong",
    relationship_strength: 7.8
});

// Create technology nodes for infrastructure mapping
CREATE (hvac_systems:Technology {
    tech_id: "TECH-001",
    name: "HVAC Control Systems",
    category: "Industrial Control",
    vendor: "Johnson Controls",
    version: "Multiple",
    criticality: "High",
    internet_facing: false,
    security_controls: ["Network Segmentation", "Access Control"],
    vulnerabilities_count: 3,
    last_scan: date("2025-08-01"),
    created_at: datetime(),
    updated_at: datetime()
});

// Create person nodes for stakeholder mapping
CREATE (george_oliver:Person {
    person_id: "PER-001",
    name: "George Oliver",
    role: "Chairman & CEO",
    department: "Executive",
    email: "confidential",
    phone: "confidential", 
    linkedin: "https://linkedin.com/in/george-oliver-jci",
    decision_authority: "Ultimate",
    influence_score: 10,
    technical_background: "Engineering",
    cybersecurity_awareness: "High",
    engagement_history: "None",
    preferred_contact: "Executive Assistant",
    created_at: datetime(),
    updated_at: datetime()
});

// Create threat nodes for risk assessment
CREATE (apt1:Threat {
    threat_id: "THR-001",
    name: "APT1 (Comment Crew)",
    type: "Advanced Persistent Threat",
    origin: "China",
    motivation: "Espionage",
    sophistication: "High",
    active_since: date("2004-01-01"),
    last_activity: date("2025-07-15"),
    target_sectors: ["Manufacturing", "Energy", "Technology"],
    ttps: ["Spear Phishing", "Lateral Movement", "Data Exfiltration"],
    mitre_groups: ["G0006"],
    threat_score: 8.5,
    created_at: datetime(),
    updated_at: datetime()
});

// Create vulnerability nodes
CREATE (cve_2024_1234:Vulnerability {
    vuln_id: "CVE-2024-1234",
    cve_id: "CVE-2024-1234",
    name: "HVAC Remote Code Execution",
    description: "Buffer overflow in HVAC control protocol",
    severity: "Critical",
    cvss_score: 9.8,
    vector: "Network",
    complexity: "Low",
    published: date("2024-03-15"),
    patched: true,
    patch_date: date("2024-04-01"),
    exploited_wild: true,
    created_at: datetime(),
    updated_at: datetime()
});

// =============================================================================
// RELATIONSHIP CREATION - Multi-Hop Analysis Foundation
// =============================================================================

// Organization relationships
MATCH (jc:Organization {name: "Johnson Controls International plc"})
MATCH (manuf:Sector {name: "Manufacturing"})
CREATE (jc)-[:OPERATES_IN_SECTOR {
    primary: true,
    percentage: 100,
    since: date("1885-01-01"),
    created_at: datetime()
}]->(manuf);

// Personnel relationships  
MATCH (jc:Organization {name: "Johnson Controls International plc"})
MATCH (go:Person {name: "George Oliver"})
CREATE (jc)-[:EMPLOYS {
    position: "Chairman & CEO",
    since: date("2017-09-01"),
    reporting_to: null,
    decision_authority: "Ultimate",
    created_at: datetime()
}]->(go);

// Technology relationships
MATCH (jc:Organization {name: "Johnson Controls International plc"})  
MATCH (hvac:Technology {name: "HVAC Control Systems"})
CREATE (jc)-[:OWNS {
    ownership_type: "Developed",
    deployment_scale: "Global",
    strategic_importance: "Core",
    created_at: datetime()
}]->(hvac);

// Threat targeting relationships
MATCH (apt:Threat {name: "APT1 (Comment Crew)"})
MATCH (jc:Organization {name: "Johnson Controls International plc"})
CREATE (apt)-[:TARGETS {
    confidence: "Medium",
    first_observed: date("2023-01-01"),
    last_observed: date("2025-07-15"),
    attack_vectors: ["Email", "Web Application"],
    success_probability: 0.4,
    created_at: datetime()
}]->(jc);

// Vulnerability relationships
MATCH (vuln:Vulnerability {cve_id: "CVE-2024-1234"})
MATCH (hvac:Technology {name: "HVAC Control Systems"})
CREATE (vuln)-[:AFFECTS {
    impact_level: "Critical",
    affected_versions: "All < 2024.1",
    patch_available: true,
    workaround_available: false,
    created_at: datetime()
}]->(hvac);

// =============================================================================
// MULTI-HOP QUERY EXAMPLES
// =============================================================================

// 1-HOP: Direct relationships (Organization → Technology)
// MATCH (o:Organization)-[r:OWNS]->(t:Technology) 
// WHERE o.name = "Johnson Controls International plc"
// RETURN o.name, r, t.name

// 2-HOP: Organization → Technology → Vulnerability  
// MATCH (o:Organization)-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)
// WHERE o.name = "Johnson Controls International plc"
// RETURN o.name, t.name, v.cve_id, v.severity

// 3-HOP: Threat → Organization → Technology → Vulnerability
// MATCH (th:Threat)-[:TARGETS]->(o:Organization)-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)
// WHERE th.name = "APT1 (Comment Crew)"
// RETURN th.name, o.name, t.name, v.cve_id

// 4-HOP: Cross-sector threat analysis
// MATCH (th:Threat)-[:TARGETS]->(o1:Organization)-[:OPERATES_IN_SECTOR]->(s:Sector)<-[:OPERATES_IN_SECTOR]-(o2:Organization)
// WHERE th.name = "APT1 (Comment Crew)" AND o1 <> o2
// RETURN th.name, s.name, COUNT(DISTINCT o2) as potential_targets

// 5-HOP: Supply chain risk analysis
// MATCH (o1:Organization)-[:SUPPLIES_TO]->(o2:Organization)-[:USES]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)<-[:EXPLOITS]-(th:Threat)
// RETURN o1.name as supplier, o2.name as customer, t.name as technology, v.cve_id, th.name as threat

// 6-HOP: Executive decision maker threat exposure
// MATCH (th:Threat)-[:TARGETS]->(o:Organization)-[:EMPLOYS]->(p:Person)-[:DECISION_AUTHORITY]->(dec:Decision)-[:AFFECTS]->(t:Technology)
// WHERE p.role CONTAINS "CEO" OR p.role CONTAINS "CTO"
// RETURN th.name, o.name, p.name, p.role, t.name

// =============================================================================
// PROJECT SELDON INTEGRATION QUERIES
// =============================================================================

// Intelligence aggregation query for Project Seldon
// MATCH (o:Organization)
// OPTIONAL MATCH (o)-[:OWNS]->(tech:Technology)
// OPTIONAL MATCH (o)<-[:TARGETS]-(threat:Threat)  
// OPTIONAL MATCH (o)-[:EMPLOYS]->(person:Person)
// OPTIONAL MATCH (tech)<-[:AFFECTS]-(vuln:Vulnerability)
// WITH o, 
//      COUNT(DISTINCT tech) as tech_count,
//      COUNT(DISTINCT threat) as threat_count,
//      COUNT(DISTINCT person) as person_count,
//      COUNT(DISTINCT vuln) as vuln_count,
//      COLLECT(DISTINCT threat.name)[0..5] as top_threats
// RETURN o.org_id, o.name, o.sector, o.threat_level, o.intelligence_priority,
//        tech_count, threat_count, person_count, vuln_count, top_threats
// ORDER BY o.intelligence_priority DESC, threat_count DESC

// Real-time threat landscape analysis
// MATCH (th:Threat)-[:TARGETS]->(o:Organization)-[:OPERATES_IN_SECTOR]->(s:Sector)
// WHERE th.last_activity >= date("2025-01-01")
// WITH s.name as sector, COUNT(DISTINCT o) as orgs_targeted, COUNT(DISTINCT th) as active_threats
// RETURN sector, orgs_targeted, active_threats
// ORDER BY active_threats DESC, orgs_targeted DESC

// =============================================================================
// SCHEMA MAINTENANCE
// =============================================================================

// Add timestamp triggers for data lineage
// CREATE OR REPLACE FUNCTION update_timestamp() 
// SET updated_at = datetime();

// Performance optimization indexes
CREATE INDEX org_threat_level IF NOT EXISTS FOR (o:Organization) ON (o.threat_level);
CREATE INDEX org_intelligence_priority IF NOT EXISTS FOR (o:Organization) ON (o.intelligence_priority);
CREATE INDEX tech_criticality IF NOT EXISTS FOR (t:Technology) ON (t.criticality);
CREATE INDEX threat_last_activity IF NOT EXISTS FOR (th:Threat) ON (th.last_activity);
CREATE INDEX vuln_severity IF NOT EXISTS FOR (v:Vulnerability) ON (v.severity);

// =============================================================================
// END UNIFIED SCHEMA
// =============================================================================

// This schema supports:
// 1. Complete prospect intelligence (129+ organizations)
// 2. Multi-hop threat analysis (1-6 degrees)
// 3. Supply chain risk assessment 
// 4. Executive decision maker mapping
// 5. Real-time threat landscape monitoring
// 6. Project Seldon unified intelligence platform integration
// 7. Sales funnel enablement with relationship scoring
// 8. Cybersecurity threat modeling with APT correlation