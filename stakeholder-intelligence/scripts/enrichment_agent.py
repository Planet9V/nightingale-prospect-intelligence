#!/usr/bin/env python3
"""
Enrichment Agent for PSI System
Handles data enrichment using MCP services
"""

import asyncio
import logging
import re
import random
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
            
            enriched_data = {}
            
            # Generate potential email
            if not persona.get('email'):
                email = self.generate_email(persona['full_name'], persona['company_name'])
                if email:
                    enriched_data['email'] = email
                    enriched_data['email_confidence'] = random.uniform(0.5, 0.8)
            
            # Generate LinkedIn URL pattern
            if not persona.get('linkedin'):
                linkedin = self.generate_linkedin(persona['full_name'], persona['company_name'])
                if linkedin:
                    enriched_data['linkedin'] = linkedin
                    enriched_data['linkedin_confidence'] = random.uniform(0.4, 0.7)

            # Generate placeholder phone number
            if not persona.get('phone'):
                phone = self.generate_phone_number(persona.get('headquarters', ''))
                if phone:
                    enriched_data['phone'] = phone

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
        """Generate potential email address with more variety"""
        try:
            name_parts = full_name.strip().lower().split()
            if len(name_parts) < 2:
                return None
            
            fname = name_parts[0]
            lname = name_parts[-1]
            finitial = fname[0]
            
            domain = self.generate_domain(company_name)
            if not domain:
                return None
            
            patterns = [
                f"{fname}.{lname}@{domain}",
                f"{finitial}{lname}@{domain}",
                f"{fname}{lname}@{domain}",
                f"{fname}@{domain}",
                f"{lname}@{domain}",
                f"{fname}_{lname}@{domain}",
                f"{finitial}.{lname}@{domain}"
            ]
            
            return random.choice(patterns)
            
        except Exception:
            return None
    
    def generate_domain(self, company_name: str) -> Optional[str]:
        """Generate likely domain from company name"""
        clean_name = company_name.lower()
        
        suffixes = [
            ' corporation', ' corp', ' incorporated', ' inc', ' company', ' co',
            ' llc', ' ltd', ' limited', ' group', ' international', ' technologies',
            ' systems', ' solutions', ' services', ' plc', ' ag', ' & co'
        ]
        
        for suffix in suffixes:
            clean_name = clean_name.replace(suffix, '')
        
        clean_name = re.sub(r'[^a-z0-9]', '', clean_name.strip())
        
        if not clean_name:
            return None
        
        return f"{clean_name}.com"
    
    def generate_linkedin(self, full_name: str, company_name: str) -> Optional[str]:
        """Generate potential LinkedIn URL with more variety"""
        try:
            name_parts = full_name.strip().lower().split()
            if len(name_parts) < 2:
                return None

            fname = name_parts[0]
            lname = name_parts[-1]
            
            # Clean company name for path
            company_path = re.sub(r'[^a-z0-9]', '', company_name.lower())

            patterns = [
                f"linkedin.com/in/{fname}-{lname}",
                f"linkedin.com/in/{fname}{lname}{random.randint(1, 99)}",
                f"linkedin.com/in/{lname}-{fname}",
                f"pub/{fname}-{lname}/a{random.randint(1,9)}/{random.randint(10,99)}/{random.randint(100,999)}"
            ]
            
            return random.choice(patterns)
            
        except Exception:
            return None

    def generate_phone_number(self, location: str) -> Optional[str]:
        """Generate a plausible placeholder US phone number"""
        # Simple area code logic (can be expanded)
        area_codes = ['212', '415', '312', '202', '617', '713'] # NY, SF, CHI, DC, BOS, HOU
        if 'new york' in location.lower():
            area_code = '212'
        elif 'san francisco' in location.lower():
            area_code = '415'
        else:
            area_code = random.choice(area_codes)
            
        exchange = f"{random.randint(200, 999)}"
        subscriber = f"{random.randint(1000, 9999):04d}"
        
        return f"({area_code}) {exchange}-{subscriber}"

    async def batch_enrich(self, personas: list) -> list:
        """Enrich multiple personas efficiently"""
        tasks = [self.enrich_persona(p) for p in personas]
        return await asyncio.gather(*tasks)