#!/usr/bin/env python3
"""
Prospect Stakeholder Intelligence (PSI) Orchestrator v1.0
Main execution controller for parallel persona extraction and campaign scoring
"""

import os
import sys
import asyncio
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import argparse
import logging
from typing import Dict, List, Tuple, Optional
import re
from concurrent.futures import ThreadPoolExecutor
import yaml

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from scripts.extraction_agent import ExtractionAgent
from scripts.enrichment_agent import EnrichmentAgent
from scripts.campaign_scorer import CampaignScorer
from scripts.output_generator import OutputGenerator
from scripts.batch_manager import BatchManager

class PSIOrchestrator:
    """Main orchestrator for PSI system"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path)
        self.batch_manager = BatchManager()
        self.shared_scratchpad = {
            'company_profiles': {},
            'extracted_personas': {},
            'enrichment_cache': {},
            'campaign_scores': {}
        }
        self.setup_logging()
        
    def load_config(self, config_path: str = None) -> dict:
        """Load configuration from file or defaults"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'prospects_dir': Path(__file__).parent.parent.parent / 'prospect-database',
            'output_dir': Path(__file__).parent.parent / 'outputs',
            'parallel_agents': 8,
            'enrichment_enabled': True,
            'campaigns': ['m_a', 'ransomware'],
            'batch_size': 10,
            'error_threshold': 0.05
        }
    
    def setup_logging(self):
        """Configure logging"""
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'psi_execution_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('PSIOrchestrator')
    
    async def process_prospects(self, prospect_list: List[str] = None) -> dict:
        """Main processing pipeline"""
        self.logger.info("Starting PSI processing")
        
        # Initialize batch
        batch_id = self.batch_manager.create_batch()
        self.logger.info(f"Created batch: {batch_id}")
        
        try:
            # Discovery phase
            prospects = self.discover_prospects(prospect_list)
            self.logger.info(f"Found {len(prospects)} prospects to process")
            
            # Process in batches
            all_results = []
            for i in range(0, len(prospects), self.config['batch_size']):
                batch = prospects[i:i + self.config['batch_size']]
                self.logger.info(f"Processing batch {i//self.config['batch_size'] + 1}")
                
                # Parallel extraction
                extraction_results = await self.parallel_extraction(batch)
                
                # Enrichment phase (if enabled)
                if self.config['enrichment_enabled']:
                    extraction_results = await self.parallel_enrichment(extraction_results)
                
                # Campaign scoring
                scored_results = await self.campaign_scoring(extraction_results)
                
                all_results.extend(scored_results)
                
                # Update batch progress
                self.batch_manager.update_progress(batch_id, len(all_results), len(prospects))
            
            # Generate output
            output_file = self.generate_output(all_results, batch_id)
            
            # Finalize batch
            self.batch_manager.complete_batch(batch_id, len(all_results), output_file)
            
            self.logger.info(f"Processing complete. Output: {output_file}")
            return {
                'batch_id': batch_id,
                'prospects_processed': len(prospects),
                'personas_extracted': len(all_results),
                'output_file': str(output_file)
            }
            
        except Exception as e:
            self.logger.error(f"Processing failed: {str(e)}")
            self.batch_manager.fail_batch(batch_id, str(e))
            raise
    
    def discover_prospects(self, prospect_list: List[str] = None) -> List[Path]:
        """Discover prospect folders to process"""
        prospects_dir = Path(self.config['prospects_dir'])
        
        if prospect_list:
            # Process specific prospects
            prospects = []
            for sf_id in prospect_list:
                matches = list(prospects_dir.glob(f"{sf_id}_*"))
                if matches:
                    prospects.append(matches[0])
                else:
                    self.logger.warning(f"Prospect {sf_id} not found")
            return prospects
        else:
            # Process all prospects
            pattern = re.compile(r'^[A-Z]-\d{6}_')
            prospects = [
                p for p in prospects_dir.iterdir()
                if p.is_dir() and pattern.match(p.name)
            ]
            return sorted(prospects)
    
    async def parallel_extraction(self, prospects: List[Path]) -> List[dict]:
        """Extract personas in parallel"""
        extraction_agent = ExtractionAgent(self.shared_scratchpad)
        
        async def extract_single(prospect_path: Path) -> List[dict]:
            try:
                self.logger.debug(f"Extracting from {prospect_path.name}")
                return await extraction_agent.extract_personas(prospect_path)
            except Exception as e:
                self.logger.error(f"Extraction failed for {prospect_path.name}: {str(e)}")
                return []
        
        # Run extractions in parallel
        tasks = [extract_single(p) for p in prospects]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_personas = []
        for persona_list in results:
            all_personas.extend(persona_list)
        
        return all_personas
    
    async def parallel_enrichment(self, personas: List[dict]) -> List[dict]:
        """Enrich personas with additional data"""
        enrichment_agent = EnrichmentAgent(self.shared_scratchpad)
        
        # Batch enrichment for efficiency
        enriched_personas = []
        batch_size = 5  # MCP rate limiting
        
        for i in range(0, len(personas), batch_size):
            batch = personas[i:i + batch_size]
            
            tasks = [
                enrichment_agent.enrich_persona(persona)
                for persona in batch
            ]
            
            enriched_batch = await asyncio.gather(*tasks)
            enriched_personas.extend(enriched_batch)
            
            # Brief pause to respect rate limits
            await asyncio.sleep(0.5)
        
        return enriched_personas
    
    async def campaign_scoring(self, personas: List[dict]) -> List[dict]:
        """Apply campaign-specific scoring"""
        scorer = CampaignScorer(self.shared_scratchpad)
        
        scored_personas = []
        for persona in personas:
            scores = await scorer.score_persona(persona)
            persona.update(scores)
            scored_personas.append(persona)
        
        return scored_personas
    
    def generate_output(self, personas: List[dict], batch_id: str) -> Path:
        """Generate output files"""
        generator = OutputGenerator()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        version = "v1.0"
        output_file = self.config['output_dir'] / f'PSI_output_{version}_{timestamp}.xlsx'
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate Excel output
        generator.create_excel(personas, output_file, batch_id)
        
        # Also create CSV backup
        csv_file = output_file.with_suffix('.csv')
        generator.create_csv(personas, csv_file)
        
        return output_file

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='PSI Orchestrator')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--prospects', help='Comma-separated list of SF IDs')
    parser.add_argument('--campaign', choices=['all', 'm_a', 'ransomware'], 
                       default='all', help='Campaign type to process')
    parser.add_argument('--no-enrichment', action='store_true', 
                       help='Skip enrichment phase')
    parser.add_argument('--parallel-agents', type=int, default=8,
                       help='Number of parallel agents')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = PSIOrchestrator(args.config)
    
    # Override config with command line args
    if args.no_enrichment:
        orchestrator.config['enrichment_enabled'] = False
    if args.parallel_agents:
        orchestrator.config['parallel_agents'] = args.parallel_agents
    if args.campaign != 'all':
        orchestrator.config['campaigns'] = [args.campaign]
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse prospect list
    prospect_list = None
    if args.prospects:
        prospect_list = [p.strip() for p in args.prospects.split(',')]
    
    # Run processing
    try:
        result = asyncio.run(orchestrator.process_prospects(prospect_list))
        print(f"\nProcessing complete!")
        print(f"Batch ID: {result['batch_id']}")
        print(f"Prospects processed: {result['prospects_processed']}")
        print(f"Personas extracted: {result['personas_extracted']}")
        print(f"Output file: {result['output_file']}")
    except Exception as e:
        print(f"\nProcessing failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()