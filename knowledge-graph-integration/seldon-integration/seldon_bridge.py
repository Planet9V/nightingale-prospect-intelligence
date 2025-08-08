#!/usr/bin/env python3
"""
🕵️ NIGHTINGALE-SELDON INTEGRATION BRIDGE
Neo4j unified schema integration for Project Seldon intelligence platform

Purpose: Seamless integration between Nightingale prospect intelligence 
and Project Seldon document processing platform with unified Neo4j schema.

Author: Claude Code - Nightingale Project
Version: 1.0.0 - Production Ready
Last Updated: August 8, 2025
"""

import os
import json
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
import yaml
from dataclasses import dataclass
from neo4j import GraphDatabase
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SeldonIntegrationConfig:
    """Configuration for Seldon-Nightingale integration"""
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    neo4j_database: str
    seldon_endpoint: str
    nightingale_data_path: str
    batch_size: int = 100
    enable_real_time: bool = True
    quality_threshold: float = 0.8

class NightingaleSeldonBridge:
    """
    Integration bridge between Nightingale prospect intelligence 
    and Project Seldon document processing platform.
    """
    
    def __init__(self, config: SeldonIntegrationConfig):
        self.config = config
        self.driver = None
        self.session = None
        self._connect_neo4j()
        
    def _connect_neo4j(self):
        """Establish Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_user, self.config.neo4j_password)
            )
            self.session = self.driver.session(database=self.config.neo4j_database)
            logger.info("Successfully connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def initialize_unified_schema(self) -> bool:
        """Initialize the unified Neo4j schema for Seldon integration"""
        try:
            # Load and execute schema
            schema_path = "../schema/unified_schema.cypher"
            with open(schema_path, 'r') as f:
                schema_queries = f.read().split(';')
            
            for query in schema_queries:
                query = query.strip()
                if query and not query.startswith('//'):
                    self.session.run(query)
            
            logger.info("Unified schema initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize schema: {e}")
            return False
    
    def load_prospect_data(self, prospect_data: Dict[str, Any]) -> bool:
        """Load prospect intelligence data into Neo4j"""
        try:
            # Extract organization data
            org_data = self._extract_organization_data(prospect_data)
            
            # Create organization node
            org_query = """
            MERGE (o:Organization {org_id: $org_id})
            SET o += $properties,
                o.updated_at = datetime(),
                o.data_source = 'Nightingale'
            RETURN o.org_id as org_id
            """
            
            result = self.session.run(org_query, {
                'org_id': org_data['org_id'],
                'properties': org_data
            })
            
            # Load related entities
            self._load_personnel(prospect_data.get('personnel', []), org_data['org_id'])
            self._load_technologies(prospect_data.get('technologies', []), org_data['org_id'])
            self._load_threats(prospect_data.get('threats', []), org_data['org_id'])
            self._load_vulnerabilities(prospect_data.get('vulnerabilities', []))
            
            logger.info(f"Successfully loaded prospect data for {org_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load prospect data: {e}")
            return False
    
    def _extract_organization_data(self, prospect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and normalize organization data"""
        foundation = prospect_data.get('Organization_Foundation', {})
        strategic = prospect_data.get('Strategic_Context', {})
        security = prospect_data.get('Security_Intelligence', {})
        
        return {
            'org_id': prospect_data.get('org_id', f"ORG-{hash(foundation.get('name', ''))%100000:05d}"),
            'name': foundation.get('name', 'Unknown'),
            'sector': foundation.get('sector', 'Unknown'),
            'industry': foundation.get('industry', 'Unknown'),
            'headquarters': foundation.get('headquarters', 'Unknown'),
            'revenue': foundation.get('revenue', 0),
            'employees': foundation.get('employees', 0),
            'website': foundation.get('website', ''),
            'description': foundation.get('description', ''),
            'threat_level': security.get('threat_level', 'Unknown'),
            'security_maturity': security.get('security_maturity', 'Unknown'),
            'intelligence_priority': strategic.get('priority', 'Medium'),
            'sales_stage': prospect_data.get('sales_stage', 'Unknown'),
            'engagement_score': prospect_data.get('engagement_score', 0.0),
            'technical_fit': prospect_data.get('technical_fit', 0.0),
            'last_assessment': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat()
        }
    
    def _load_personnel(self, personnel: List[Dict], org_id: str):
        """Load personnel data and relationships"""
        for person in personnel:
            person_query = """
            MERGE (p:Person {person_id: $person_id})
            SET p += $properties,
                p.updated_at = datetime(),
                p.data_source = 'Nightingale'
            WITH p
            MATCH (o:Organization {org_id: $org_id})
            MERGE (o)-[:EMPLOYS {
                position: $position,
                department: $department,
                decision_authority: $decision_authority,
                created_at: datetime()
            }]->(p)
            """
            
            self.session.run(person_query, {
                'person_id': person.get('person_id', f"PER-{hash(person.get('name', ''))%100000:05d}"),
                'org_id': org_id,
                'properties': person,
                'position': person.get('role', 'Unknown'),
                'department': person.get('department', 'Unknown'),
                'decision_authority': person.get('decision_authority', 'None')
            })
    
    def _load_technologies(self, technologies: List[Dict], org_id: str):
        """Load technology data and relationships"""
        for tech in technologies:
            tech_query = """
            MERGE (t:Technology {tech_id: $tech_id})
            SET t += $properties,
                t.updated_at = datetime(),
                t.data_source = 'Nightingale'
            WITH t
            MATCH (o:Organization {org_id: $org_id})
            MERGE (o)-[:OWNS {
                ownership_type: $ownership_type,
                strategic_importance: $importance,
                created_at: datetime()
            }]->(t)
            """
            
            self.session.run(tech_query, {
                'tech_id': tech.get('tech_id', f"TECH-{hash(tech.get('name', ''))%100000:05d}"),
                'org_id': org_id,
                'properties': tech,
                'ownership_type': tech.get('ownership_type', 'Uses'),
                'importance': tech.get('criticality', 'Medium')
            })
    
    def _load_threats(self, threats: List[Dict], org_id: str):
        """Load threat data and targeting relationships"""
        for threat in threats:
            threat_query = """
            MERGE (th:Threat {threat_id: $threat_id})
            SET th += $properties,
                th.updated_at = datetime(),
                th.data_source = 'Nightingale'
            WITH th
            MATCH (o:Organization {org_id: $org_id})
            MERGE (th)-[:TARGETS {
                confidence: $confidence,
                attack_vectors: $attack_vectors,
                last_observed: $last_observed,
                created_at: datetime()
            }]->(o)
            """
            
            self.session.run(threat_query, {
                'threat_id': threat.get('threat_id', f"THR-{hash(threat.get('name', ''))%100000:05d}"),
                'org_id': org_id,
                'properties': threat,
                'confidence': threat.get('confidence', 'Medium'),
                'attack_vectors': threat.get('attack_vectors', []),
                'last_observed': threat.get('last_observed', datetime.now().isoformat())
            })
    
    def _load_vulnerabilities(self, vulnerabilities: List[Dict]):
        """Load vulnerability data"""
        for vuln in vulnerabilities:
            vuln_query = """
            MERGE (v:Vulnerability {vuln_id: $vuln_id})
            SET v += $properties,
                v.updated_at = datetime(),
                v.data_source = 'Nightingale'
            """
            
            self.session.run(vuln_query, {
                'vuln_id': vuln.get('vuln_id', vuln.get('cve_id', f"VULN-{hash(vuln.get('name', ''))%100000:05d}")),
                'properties': vuln
            })
    
    def execute_multi_hop_analysis(self, query_type: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute multi-hop analysis queries"""
        
        query_map = {
            'threat_surface': """
                MATCH (o:Organization {org_id: $org_id})-[:OWNS]->(t:Technology)<-[:AFFECTS]-(v:Vulnerability)<-[:EXPLOITS]-(th:Threat)
                RETURN o.name as organization, 
                       COUNT(DISTINCT t) as technologies,
                       COUNT(DISTINCT v) as vulnerabilities,
                       COUNT(DISTINCT th) as threats,
                       COLLECT(DISTINCT th.name)[0..5] as top_threats
            """,
            
            'supply_chain_risk': """
                MATCH (o1:Organization {org_id: $org_id})-[:SUPPLIES_TO*1..3]->(o2:Organization)<-[:TARGETS]-(th:Threat)
                RETURN o1.name as supplier,
                       o2.name as customer,
                       COUNT(DISTINCT th) as shared_threats,
                       COLLECT(DISTINCT th.name)[0..3] as threat_names
            """,
            
            'executive_exposure': """
                MATCH (o:Organization {org_id: $org_id})-[:EMPLOYS]->(p:Person)<-[:TARGETS]-(th:Threat)
                WHERE p.decision_authority IN ['Ultimate', 'High']
                RETURN p.name as executive,
                       p.role as position,
                       COUNT(DISTINCT th) as direct_threats,
                       COLLECT(DISTINCT th.name) as threat_names
            """,
            
            'sector_correlation': """
                MATCH (o:Organization {org_id: $org_id})-[:OPERATES_IN_SECTOR]->(s:Sector)<-[:OPERATES_IN_SECTOR]-(peer:Organization)<-[:TARGETS]-(th:Threat)
                RETURN s.name as sector,
                       COUNT(DISTINCT peer) as peer_organizations,
                       COUNT(DISTINCT th) as sector_threats,
                       COLLECT(DISTINCT th.name)[0..10] as common_threats
            """
        }
        
        if query_type not in query_map:
            raise ValueError(f"Unknown query type: {query_type}")
        
        try:
            result = self.session.run(query_map[query_type], parameters)
            return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Failed to execute multi-hop analysis: {e}")
            return []
    
    def generate_seldon_intelligence_feed(self, org_id: str) -> Dict[str, Any]:
        """Generate comprehensive intelligence feed for Project Seldon"""
        
        # Comprehensive intelligence aggregation
        intelligence_query = """
        MATCH (o:Organization {org_id: $org_id})
        OPTIONAL MATCH (o)-[:OWNS]->(tech:Technology)
        OPTIONAL MATCH (o)<-[:TARGETS]-(threat:Threat)
        OPTIONAL MATCH (o)-[:EMPLOYS]->(person:Person)
        OPTIONAL MATCH (tech)<-[:AFFECTS]-(vuln:Vulnerability)
        
        WITH o,
             COUNT(DISTINCT tech) as tech_count,
             COUNT(DISTINCT threat) as threat_count,
             COUNT(DISTINCT person) as person_count,
             COUNT(DISTINCT vuln) as vuln_count,
             COLLECT(DISTINCT tech.name)[0..10] as technologies,
             COLLECT(DISTINCT threat.name)[0..10] as threats,
             COLLECT(DISTINCT person.name + ' (' + person.role + ')')[0..10] as key_personnel,
             COLLECT(DISTINCT vuln.cve_id)[0..10] as vulnerabilities
        
        RETURN {
            organization: o.name,
            org_id: o.org_id,
            sector: o.sector,
            threat_level: o.threat_level,
            intelligence_priority: o.intelligence_priority,
            sales_stage: o.sales_stage,
            engagement_score: o.engagement_score,
            technical_fit: o.technical_fit,
            summary: {
                technologies: tech_count,
                threats: threat_count,
                personnel: person_count,
                vulnerabilities: vuln_count
            },
            details: {
                technologies: technologies,
                threats: threats,
                key_personnel: key_personnel,
                vulnerabilities: vulnerabilities
            },
            last_updated: o.updated_at
        } as intelligence_feed
        """
        
        try:
            result = self.session.run(intelligence_query, {'org_id': org_id})
            record = result.single()
            return record['intelligence_feed'] if record else {}
        except Exception as e:
            logger.error(f"Failed to generate Seldon intelligence feed: {e}")
            return {}
    
    def sync_with_seldon(self, org_ids: List[str] = None) -> bool:
        """Synchronize Nightingale data with Project Seldon"""
        try:
            if not org_ids:
                # Get all organizations
                result = self.session.run("MATCH (o:Organization) RETURN o.org_id as org_id")
                org_ids = [record['org_id'] for record in result]
            
            seldon_feeds = []
            for org_id in org_ids:
                feed = self.generate_seldon_intelligence_feed(org_id)
                if feed:
                    seldon_feeds.append(feed)
            
            # Export to Seldon-compatible format
            output_path = f"seldon_intelligence_feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, 'w') as f:
                json.dump({
                    'generated_at': datetime.now().isoformat(),
                    'source': 'Nightingale Prospect Intelligence',
                    'version': '1.0.0',
                    'organization_count': len(seldon_feeds),
                    'organizations': seldon_feeds
                }, f, indent=2, default=str)
            
            logger.info(f"Successfully synchronized {len(seldon_feeds)} organizations with Seldon")
            logger.info(f"Intelligence feed exported to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync with Seldon: {e}")
            return False
    
    def close(self):
        """Close Neo4j connections"""
        if self.session:
            self.session.close()
        if self.driver:
            self.driver.close()
        logger.info("Closed Neo4j connections")

def load_config(config_path: str = "config.yaml") -> SeldonIntegrationConfig:
    """Load integration configuration"""
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return SeldonIntegrationConfig(**config_data)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        # Return default config with environment variables
        return SeldonIntegrationConfig(
            neo4j_uri=os.getenv('NEO4J_URI', 'neo4j+s://a7e7ac92.databases.neo4j.io'),
            neo4j_user=os.getenv('NEO4J_USER', 'neo4j'),
            neo4j_password=os.getenv('NEO4J_PASSWORD', 'MRi11OXY-XqofS14p4ShgMMqDOGvcEkBQnA1KDe_Wyc'),
            neo4j_database=os.getenv('NEO4J_DATABASE', 'neo4j'),
            seldon_endpoint=os.getenv('SELDON_ENDPOINT', 'http://localhost:8000/api/v1'),
            nightingale_data_path=os.getenv('NIGHTINGALE_DATA_PATH', './prospect-database')
        )

def main():
    """Main execution function"""
    logger.info("🕵️ Starting Nightingale-Seldon Integration Bridge")
    
    # Load configuration
    config = load_config()
    
    # Initialize bridge
    bridge = NightingaleSeldonBridge(config)
    
    try:
        # Initialize unified schema
        bridge.initialize_unified_schema()
        
        # Example: Load sample prospect data
        sample_prospect = {
            'org_id': 'ORG-029867',
            'Organization_Foundation': {
                'name': 'Johnson Controls International plc',
                'sector': 'Manufacturing',
                'industry': 'Building Technologies & Solutions',
                'headquarters': 'Cork, Ireland',
                'revenue': 25100000000,
                'employees': 100000,
                'website': 'https://www.johnsoncontrols.com'
            },
            'Strategic_Context': {
                'priority': 'High'
            },
            'Security_Intelligence': {
                'threat_level': 'Medium-High',
                'security_maturity': 'Developing'
            },
            'sales_stage': 'Qualified',
            'engagement_score': 8.5,
            'technical_fit': 9.2
        }
        
        # Load prospect data
        bridge.load_prospect_data(sample_prospect)
        
        # Execute multi-hop analysis
        threat_surface = bridge.execute_multi_hop_analysis('threat_surface', {'org_id': 'ORG-029867'})
        logger.info(f"Threat surface analysis: {threat_surface}")
        
        # Generate Seldon intelligence feed
        intel_feed = bridge.generate_seldon_intelligence_feed('ORG-029867')
        logger.info(f"Generated intelligence feed for Seldon integration")
        
        # Sync with Seldon
        bridge.sync_with_seldon(['ORG-029867'])
        
        logger.info("✅ Nightingale-Seldon integration completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Integration failed: {e}")
        raise
    finally:
        bridge.close()

if __name__ == "__main__":
    main()