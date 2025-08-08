#!/usr/bin/env python3
"""
Enrichment Agent for PSI System
Handles data enrichment using MCP services
"""

import asyncio
import logging
import re
from typing import Dict, Optional

class EnrichmentAgent:
    """Agent responsible for enriching personas with additional data"""
    
    def __init__(self, shared_scratchpad: dict):
        self.scratchpad = shared_scratchpad
        self.logger = logging.getLogger('EnrichmentAgent')
        self.enrichment_cache = self.scratchpad.get('enrichment_cache', {})
    
    async def enrich_persona(self, persona: Dict) -> Dict:
        """Enrich a single persona with additional data"""
        try:
            # Check cache first
            cache_key = f"{persona['full_name']}_{persona['company_name']}"
            if cache_key in self.enrichment_cache:
                cached_data = self.enrichment_cache[cache_key]
                persona.update(cached_data)
                return persona
            
            # For v1.0, we'll use pattern-based email generation
            # In future versions, this would use MCP Jina AI
            enriched_data = {}
            
            # Generate potential email
            if not persona.get('email'):
                email = self.generate_email(persona['full_name'], persona['company_name'])
                if email:
                    enriched_data['email'] = email
                    enriched_data['email_confidence'] = 0.6
            
            # Generate LinkedIn URL pattern
            if not persona.get('linkedin'):
                linkedin = self.generate_linkedin(persona['full_name'])
                if linkedin:
                    enriched_data['linkedin'] = linkedin
                    enriched_data['linkedin_confidence'] = 0.5
            
            # Add enrichment timestamp
            enriched_data['enrichment_attempted'] = True
            
            # Cache the enrichment
            self.enrichment_cache[cache_key] = enriched_data
            
            # Update persona
            persona.update(enriched_data)
            
            return persona
            
        except Exception as e:
            self.logger.error(f"Enrichment failed for {persona.get('full_name')}: {str(e)}")
            persona['enrichment_attempted'] = False
            return persona
    
    def generate_email(self, full_name: str, company_name: str) -> Optional[str]:
        """Generate potential email address"""
        try:
            # Parse name
            name_parts = full_name.strip().split()
            if len(name_parts) < 2:
                return None
            
            first_name = name_parts[0].lower()
            last_name = name_parts[-1].lower()
            
            # Clean company name for domain
            domain = self.generate_domain(company_name)
            if not domain:
                return None
            
            # Common patterns (would be enhanced with MCP in production)
            patterns = [
                f"{first_name}.{last_name}@{domain}",
                f"{first_name[0]}{last_name}@{domain}",
                f"{first_name}@{domain}",
                f"{last_name}@{domain}"
            ]
            
            # Return most likely pattern (first one for v1.0)
            return patterns[0]
            
        except Exception:
            return None
    
    def generate_domain(self, company_name: str) -> Optional[str]:
        """Generate likely domain from company name"""
        # Clean company name
        clean_name = company_name.lower()
        
        # Remove common suffixes
        suffixes = [
            ' corporation', ' corp', ' incorporated', ' inc',
            ' company', ' co', ' llc', ' ltd', ' limited',
            ' group', ' international', ' technologies',
            ' systems', ' solutions', ' services'
        ]
        
        for suffix in suffixes:
            clean_name = clean_name.replace(suffix, '')
        
        # Remove special characters
        clean_name = re.sub(r'[^a-z0-9\s]', '', clean_name)
        clean_name = clean_name.strip()
        
        # Handle multi-word names
        words = clean_name.split()
        if not words:
            return None
        
        # Common domain patterns
        if len(words) == 1:
            domain = f"{words[0]}.com"
        else:
            # Try acronym
            acronym = ''.join(word[0] for word in words)
            # Or concatenated
            concatenated = ''.join(words)
            # Or hyphenated
            hyphenated = '-'.join(words)
            
            # Return most likely (would use MCP validation in production)
            domain = f"{concatenated}.com"
        
        return domain
    
    def generate_linkedin(self, full_name: str) -> Optional[str]:
        """Generate potential LinkedIn URL"""
        try:
            # Parse name
            name_parts = full_name.strip().split()
            if len(name_parts) < 2:
                return None
            
            first_name = name_parts[0].lower()
            last_name = name_parts[-1].lower()
            
            # Common LinkedIn patterns
            patterns = [
                f"linkedin.com/in/{first_name}-{last_name}",
                f"linkedin.com/in/{first_name}{last_name}",
                f"linkedin.com/in/{last_name}{first_name}"
            ]
            
            # Return most likely pattern
            return patterns[0]
            
        except Exception:
            return None
    
    async def batch_enrich(self, personas: list) -> list:
        """Enrich multiple personas efficiently"""
        tasks = []
        batch_size = 5  # Process in small batches
        
        for i in range(0, len(personas), batch_size):
            batch = personas[i:i + batch_size]
            for persona in batch:
                task = self.enrich_persona(persona)
                tasks.append(task)
            
            # Process batch
            enriched_batch = await asyncio.gather(*tasks)
            
            # Small delay to respect rate limits (would be configured for MCP)
            await asyncio.sleep(0.1)
        
        return personas