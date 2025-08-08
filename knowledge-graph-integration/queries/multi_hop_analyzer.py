#!/usr/bin/env python3
"""
🕵️ NIGHTINGALE MULTI-HOP ANALYSIS ENGINE
Advanced Neo4j multi-hop queries for comprehensive threat intelligence and prospect analysis

Purpose: Execute complex multi-hop queries across the unified Neo4j schema
to provide deep insights for both cybersecurity threat modeling and sales intelligence.

Author: Claude Code - Nightingale Project  
Version: 1.0.0 - Production Ready
Last Updated: August 8, 2025
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from neo4j import GraphDatabase
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class QueryResult:
    """Structured query result with metadata"""
    query_type: str
    parameters: Dict[str, Any]
    results: List[Dict[str, Any]]
    execution_time: float
    node_count: int
    relationship_count: int
    confidence_score: float

class MultiHopAnalyzer:
    """Advanced multi-hop analysis engine for Neo4j graph queries"""
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str, neo4j_database: str = "neo4j"):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.neo4j_database = neo4j_database
        self.driver = None
        self.session = None
        self._connect()
    
    def _connect(self):
        """Establish Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            self.session = self.driver.session(database=self.neo4j_database)
            logger.info("Connected to Neo4j database for multi-hop analysis")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> QueryResult:
        """Execute a Neo4j query with timing and metadata"""
        start_time = datetime.now()
        
        try:
            result = self.session.run(query, parameters or {})
            records = [record.data() for record in result]
            
            # Calculate execution metadata
            execution_time = (datetime.now() - start_time).total_seconds()
            node_count = self._count_nodes_in_results(records)
            relationship_count = self._count_relationships_in_results(records)
            confidence_score = self._calculate_confidence_score(records)
            
            return QueryResult(
                query_type="custom",
                parameters=parameters or {},
                results=records,
                execution_time=execution_time,
                node_count=node_count,
                relationship_count=relationship_count,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def _count_nodes_in_results(self, results: List[Dict]) -> int:
        """Count unique nodes in query results"""
        unique_nodes = set()
        for record in results:
            for key, value in record.items():
                if isinstance(value, dict) and 'element_id' in str(value):
                    unique_nodes.add(str(value))
        return len(unique_nodes)
    
    def _count_relationships_in_results(self, results: List[Dict]) -> int:
        """Count relationships in query results"""
        relationship_count = 0
        for record in results:
            for key, value in record.items():
                if 'relationship' in key.lower() or 'edge' in key.lower():
                    relationship_count += 1
        return relationship_count
    
    def _calculate_confidence_score(self, results: List[Dict]) -> float:
        """Calculate confidence score based on data completeness"""
        if not results:
            return 0.0
        
        total_fields = 0
        populated_fields = 0
        
        for record in results:
            for value in record.values():
                total_fields += 1
                if value and value != 'Unknown' and value != 'None':
                    populated_fields += 1
        
        return (populated_fields / total_fields) if total_fields > 0 else 0.0

    # =============================================================================
    # 1-HOP ANALYSIS - Direct Relationships
    # =============================================================================
    
    def analyze_organization_assets(self, org_id: str) -> QueryResult:
        """1-Hop: Analyze direct organizational assets and relationships"""
        query = """
        MATCH (o:Organization {org_id: $org_id})
        OPTIONAL MATCH (o)-[:OWNS]->(tech:Technology)
        OPTIONAL MATCH (o)-[:EMPLOYS]->(person:Person)
        OPTIONAL MATCH (o)-[:OPERATES_IN_SECTOR]->(sector:Sector)
        OPTIONAL MATCH (o)-[:LOCATED_IN]->(location:Location)
        
        WITH o,
             COUNT(DISTINCT tech) as tech_count,
             COUNT(DISTINCT person) as person_count,
             COLLECT(DISTINCT tech.name) as technologies,
             COLLECT(DISTINCT person.name + ' (' + person.role + ')') as key_personnel,
             sector.name as sector_name,
             location.name as location_name
        
        RETURN o.name as organization,
               o.org_id as org_id,
               o.threat_level as threat_level,
               o.intelligence_priority as priority,
               o.sales_stage as sales_stage,
               o.engagement_score as engagement_score,
               sector_name,
               location_name,
               tech_count,
               person_count,
               technologies[0..10] as top_technologies,
               key_personnel[0..10] as key_personnel
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "1-hop-organization-assets"
        return result
    
    # =============================================================================
    # 2-HOP ANALYSIS - Extended Relationships
    # =============================================================================
    
    def analyze_threat_surface(self, org_id: str) -> QueryResult:
        """2-Hop: Organization → Technology → Vulnerability threat surface analysis"""
        query = """
        MATCH (o:Organization {org_id: $org_id})-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)
        
        WITH o, t, v,
             CASE v.severity
                 WHEN 'Critical' THEN 4
                 WHEN 'High' THEN 3
                 WHEN 'Medium' THEN 2
                 WHEN 'Low' THEN 1
                 ELSE 0
             END as severity_score
        
        RETURN o.name as organization,
               t.name as technology,
               t.category as tech_category,
               COUNT(v) as vulnerability_count,
               COLLECT({
                   cve_id: v.cve_id,
                   severity: v.severity,
                   cvss_score: v.cvss_score,
                   published: v.published
               }) as vulnerabilities,
               AVG(severity_score) as avg_severity_score,
               MAX(severity_score) as max_severity_score,
               SUM(CASE WHEN v.exploited_wild = true THEN 1 ELSE 0 END) as exploited_count
        
        ORDER BY max_severity_score DESC, vulnerability_count DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "2-hop-threat-surface"
        return result
    
    def analyze_vendor_ecosystem(self, org_id: str) -> QueryResult:
        """2-Hop: Organization → Partner → Technology vendor ecosystem analysis"""
        query = """
        MATCH (o:Organization {org_id: $org_id})-[:PARTNERS_WITH|SUPPLIES_TO|DEPENDS_ON]->(partner:Organization)-[:OWNS]->(tech:Technology)
        
        WITH o, partner, tech,
             type(relationship) as relationship_type
        
        RETURN o.name as organization,
               partner.name as partner_name,
               partner.sector as partner_sector,
               COUNT(DISTINCT tech) as shared_technologies,
               COLLECT(DISTINCT tech.name)[0..10] as technologies,
               COLLECT(DISTINCT relationship_type) as relationship_types,
               partner.threat_level as partner_threat_level
        
        ORDER BY shared_technologies DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "2-hop-vendor-ecosystem"
        return result
    
    # =============================================================================
    # 3-HOP ANALYSIS - Complex Threat Patterns
    # =============================================================================
    
    def analyze_apt_targeting_patterns(self, org_id: str) -> QueryResult:
        """3-Hop: Threat → Organization → Technology → Vulnerability targeting analysis"""
        query = """
        MATCH (th:Threat)-[:TARGETS]->(o:Organization {org_id: $org_id})-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)
        WHERE th.type = 'Advanced Persistent Threat'
        
        WITH th, o, t, v,
             CASE v.severity
                 WHEN 'Critical' THEN 4
                 WHEN 'High' THEN 3  
                 WHEN 'Medium' THEN 2
                 WHEN 'Low' THEN 1
                 ELSE 0
             END as severity_score
        
        RETURN th.name as threat_actor,
               th.origin as origin,
               th.motivation as motivation,
               o.name as target_organization,
               COUNT(DISTINCT t) as targeted_technologies,
               COUNT(DISTINCT v) as exploitable_vulnerabilities,
               COLLECT(DISTINCT t.name)[0..5] as key_technologies,
               COLLECT(DISTINCT v.cve_id)[0..10] as key_vulnerabilities,
               AVG(severity_score) as avg_vuln_severity,
               th.threat_score as threat_score,
               th.last_activity as last_observed
        
        ORDER BY threat_score DESC, exploitable_vulnerabilities DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "3-hop-apt-targeting"
        return result
    
    def analyze_supply_chain_risks(self, org_id: str, depth: int = 3) -> QueryResult:
        """3-Hop: Organization → Supplier → Supplier → Threat supply chain risk analysis"""
        query = f"""
        MATCH (o:Organization {{org_id: $org_id}})-[:SUPPLIES_TO*1..{depth}]->(customer:Organization)<-[:TARGETS]-(th:Threat)
        
        WITH o, customer, th,
             length((o)-[:SUPPLIES_TO*]->(customer)) as supply_chain_depth
        
        RETURN o.name as supplier,
               customer.name as ultimate_customer,
               customer.sector as customer_sector,
               supply_chain_depth,
               COUNT(DISTINCT th) as shared_threats,
               COLLECT(DISTINCT th.name)[0..5] as threat_names,
               customer.threat_level as customer_threat_level,
               AVG(th.threat_score) as avg_threat_score
        
        ORDER BY supply_chain_depth ASC, shared_threats DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "3-hop-supply-chain-risk"
        return result
    
    # =============================================================================
    # 4-HOP ANALYSIS - Cross-Sector Intelligence
    # =============================================================================
    
    def analyze_cross_sector_threats(self, org_id: str) -> QueryResult:
        """4-Hop: Threat → Organization → Sector → Organization cross-sector threat analysis"""
        query = """
        MATCH (th:Threat)-[:TARGETS]->(o1:Organization {org_id: $org_id})-[:OPERATES_IN_SECTOR]->(s:Sector)<-[:OPERATES_IN_SECTOR]-(o2:Organization)
        WHERE o1 <> o2
        
        WITH th, o1, s, o2
        OPTIONAL MATCH (th)-[:TARGETS]->(o2)
        
        WITH th, o1, s,
             COUNT(DISTINCT o2) as sector_organizations,
             COUNT(DISTINCT CASE WHEN (th)-[:TARGETS]->(o2) THEN o2 ELSE NULL END) as also_targeted,
             COLLECT(DISTINCT o2.name)[0..10] as peer_organizations
        
        RETURN th.name as threat_actor,
               th.type as threat_type,
               o1.name as primary_target,
               s.name as sector,
               sector_organizations,
               also_targeted,
               ROUND(100.0 * also_targeted / sector_organizations, 2) as sector_targeting_percentage,
               peer_organizations,
               th.threat_score as threat_score
        
        ORDER BY sector_targeting_percentage DESC, also_targeted DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "4-hop-cross-sector-threats"
        return result
    
    # =============================================================================
    # 5-HOP ANALYSIS - Advanced Attack Path Discovery
    # =============================================================================
    
    def analyze_attack_paths(self, org_id: str) -> QueryResult:
        """5-Hop: Threat → Organization → Technology → Vulnerability → Exploit → Impact"""
        query = """
        MATCH path = (th:Threat)-[:TARGETS]->(o:Organization {org_id: $org_id})-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)<-[:EXPLOITS]-(th)
        
        WITH th, o, t, v,
             CASE v.severity
                 WHEN 'Critical' THEN 4
                 WHEN 'High' THEN 3
                 WHEN 'Medium' THEN 2
                 WHEN 'Low' THEN 1
                 ELSE 0
             END as severity_score,
             CASE t.criticality
                 WHEN 'Critical' THEN 1.0
                 WHEN 'High' THEN 0.8
                 WHEN 'Medium' THEN 0.6
                 WHEN 'Low' THEN 0.4
                 ELSE 0.2
             END as criticality_multiplier
        
        WITH th, o, t, v, severity_score, criticality_multiplier,
             (severity_score * criticality_multiplier * th.threat_score / 10.0) as attack_path_score
        
        RETURN th.name as threat_actor,
               o.name as target_organization,
               t.name as vulnerable_technology,
               t.category as tech_category,
               v.cve_id as vulnerability,
               v.severity as vuln_severity,
               t.criticality as tech_criticality,
               ROUND(attack_path_score, 2) as attack_path_score,
               v.exploited_wild as active_exploitation,
               th.last_activity as threat_last_seen
        
        ORDER BY attack_path_score DESC, active_exploitation DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "5-hop-attack-paths"
        return result
    
    # =============================================================================
    # 6-HOP ANALYSIS - Executive Decision Impact Analysis  
    # =============================================================================
    
    def analyze_executive_decision_impact(self, org_id: str) -> QueryResult:
        """6-Hop: Threat → Organization → Person → Decision → Technology → Vulnerability"""
        query = """
        MATCH (th:Threat)-[:TARGETS]->(o:Organization {org_id: $org_id})-[:EMPLOYS]->(p:Person)-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)
        WHERE p.decision_authority IN ['Ultimate', 'High'] 
           OR p.role CONTAINS 'CEO' 
           OR p.role CONTAINS 'CTO' 
           OR p.role CONTAINS 'CISO'
        
        WITH th, o, p, t, v,
             CASE v.severity
                 WHEN 'Critical' THEN 4
                 WHEN 'High' THEN 3
                 WHEN 'Medium' THEN 2  
                 WHEN 'Low' THEN 1
                 ELSE 0
             END as severity_score,
             CASE p.decision_authority
                 WHEN 'Ultimate' THEN 1.0
                 WHEN 'High' THEN 0.8
                 WHEN 'Medium' THEN 0.6
                 ELSE 0.4
             END as decision_weight
        
        WITH th, p, 
             COUNT(DISTINCT t) as impacted_technologies,
             COUNT(DISTINCT v) as executive_vulnerabilities,
             COLLECT(DISTINCT t.name)[0..10] as technologies,
             COLLECT(DISTINCT v.cve_id)[0..10] as vulnerabilities,
             AVG(severity_score * decision_weight) as executive_risk_score
        
        RETURN th.name as threat_actor,
               p.name as executive,
               p.role as position,
               p.decision_authority as authority_level,
               impacted_technologies,
               executive_vulnerabilities,
               technologies,
               vulnerabilities,
               ROUND(executive_risk_score, 2) as executive_risk_score,
               p.cybersecurity_awareness as security_awareness
        
        ORDER BY executive_risk_score DESC, impacted_technologies DESC
        """
        
        result = self.execute_query(query, {'org_id': org_id})
        result.query_type = "6-hop-executive-impact"
        return result
    
    # =============================================================================
    # COMPREHENSIVE MULTI-HOP INTELLIGENCE REPORT
    # =============================================================================
    
    def generate_comprehensive_intelligence_report(self, org_id: str) -> Dict[str, QueryResult]:
        """Generate complete multi-hop intelligence report for an organization"""
        logger.info(f"Generating comprehensive intelligence report for {org_id}")
        
        intelligence_report = {}
        
        try:
            # 1-Hop: Organization assets
            intelligence_report['organization_assets'] = self.analyze_organization_assets(org_id)
            
            # 2-Hop: Threat surface and vendor ecosystem
            intelligence_report['threat_surface'] = self.analyze_threat_surface(org_id)
            intelligence_report['vendor_ecosystem'] = self.analyze_vendor_ecosystem(org_id)
            
            # 3-Hop: APT targeting and supply chain risks
            intelligence_report['apt_targeting'] = self.analyze_apt_targeting_patterns(org_id)
            intelligence_report['supply_chain_risks'] = self.analyze_supply_chain_risks(org_id)
            
            # 4-Hop: Cross-sector threats
            intelligence_report['cross_sector_threats'] = self.analyze_cross_sector_threats(org_id)
            
            # 5-Hop: Attack paths
            intelligence_report['attack_paths'] = self.analyze_attack_paths(org_id)
            
            # 6-Hop: Executive decision impact
            intelligence_report['executive_impact'] = self.analyze_executive_decision_impact(org_id)
            
            logger.info(f"Intelligence report generated successfully with {len(intelligence_report)} analysis types")
            return intelligence_report
            
        except Exception as e:
            logger.error(f"Failed to generate intelligence report: {e}")
            raise
    
    def export_intelligence_report(self, intelligence_report: Dict[str, QueryResult], org_id: str) -> str:
        """Export intelligence report to JSON format"""
        
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'organization_id': org_id,
            'report_version': '1.0.0',
            'analysis_types': list(intelligence_report.keys()),
            'total_execution_time': sum(result.execution_time for result in intelligence_report.values()),
            'analyses': {}
        }
        
        for analysis_type, result in intelligence_report.items():
            export_data['analyses'][analysis_type] = {
                'query_type': result.query_type,
                'parameters': result.parameters,
                'results': result.results,
                'metadata': {
                    'execution_time_seconds': result.execution_time,
                    'node_count': result.node_count,
                    'relationship_count': result.relationship_count,
                    'confidence_score': result.confidence_score,
                    'result_count': len(result.results)
                }
            }
        
        # Export to file
        filename = f"intelligence_report_{org_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Intelligence report exported to {filename}")
        return filename
    
    def close(self):
        """Close Neo4j connections"""
        if self.session:
            self.session.close()
        if self.driver:
            self.driver.close()
        logger.info("Closed Neo4j connections")

def main():
    """Main execution function for multi-hop analysis"""
    # Initialize analyzer with Neo4j credentials
    analyzer = MultiHopAnalyzer(
        neo4j_uri=os.getenv('NEO4J_URI', 'neo4j+s://a7e7ac92.databases.neo4j.io'),
        neo4j_user=os.getenv('NEO4J_USER', 'neo4j'),
        neo4j_password=os.getenv('NEO4J_PASSWORD', 'MRi11OXY-XqofS14p4ShgMMqDOGvcEkBQnA1KDe_Wyc'),
        neo4j_database=os.getenv('NEO4J_DATABASE', 'neo4j')
    )
    
    try:
        # Example: Generate comprehensive intelligence report
        org_id = "ORG-029867"  # Johnson Controls example
        
        logger.info(f"🕵️ Starting comprehensive multi-hop analysis for {org_id}")
        
        # Generate full intelligence report
        intelligence_report = analyzer.generate_comprehensive_intelligence_report(org_id)
        
        # Export report
        report_file = analyzer.export_intelligence_report(intelligence_report, org_id)
        
        # Print summary
        print(f"\n🎯 MULTI-HOP INTELLIGENCE REPORT SUMMARY")
        print(f"=" * 50)
        print(f"Organization ID: {org_id}")
        print(f"Analysis Types: {len(intelligence_report)}")
        print(f"Total Execution Time: {sum(r.execution_time for r in intelligence_report.values()):.2f}s")
        print(f"Report Exported: {report_file}")
        
        for analysis_type, result in intelligence_report.items():
            print(f"\n{analysis_type.upper()}:")
            print(f"  - Query Type: {result.query_type}")
            print(f"  - Results: {len(result.results)} records")
            print(f"  - Execution Time: {result.execution_time:.2f}s") 
            print(f"  - Confidence Score: {result.confidence_score:.2f}")
        
        logger.info("✅ Multi-hop analysis completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Multi-hop analysis failed: {e}")
        raise
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()