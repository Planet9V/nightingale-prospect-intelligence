#!/usr/bin/env python3
"""
Enrichment Agent for PSI System
Handles data enrichment using the Perplexity API
"""

import asyncio
import logging
import os
import re
from openai import OpenAI
from typing import Dict, Optional

class EnrichmentAgent:
    """Agent responsible for enriching personas with additional data via Perplexity."""
    
    def __init__(self, shared_scratchpad: dict):
        self.scratchpad = shared_scratchpad
        self.logger = logging.getLogger('EnrichmentAgent')
        self.enrichment_cache = self.scratchpad.get('enrichment_cache', {})

        # Initialize Perplexity API client
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not api_key:
            self.logger.error("PERPLEXITY_API_KEY environment variable not set.")
            raise ValueError("PERPLEXITY_API_KEY is required for the EnrichmentAgent.")
            
        self.client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

    async def _call_perplexity_api(self, prompt: str) -> Optional[str]:
        """Sends a prompt to the Perplexity API and returns the response."""
        try:
            self.logger.info(f"Querying Perplexity API for: {prompt[:100]}...")
            response = self.client.chat.completions.create(
                model="llama-3-sonar-large-32k-online",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            self.logger.info("Successfully received response from Perplexity API.")
            return content
        except Exception as e:
            self.logger.error(f"Perplexity API call failed: {e}")
            return None

    def _construct_prompt(self, full_name: str, company_name: str) -> str:
        """Constructs a detailed prompt for the Perplexity API."""
        return (
            f"As an expert research analyst, please find and consolidate publicly available professional information for '{full_name}', "
            f"who is associated with the company '{company_name}'. Focus on details relevant to a business-to-business sales context. "
            "I am looking for the following specific details:\n"
            "- Official Job Title\n"
            "- Corporate Email Address (if publicly available)\n"
            "- Corporate Direct-Dial Phone Number (if publicly available)\n"
            "- LinkedIn Profile URL\n"
            "- A brief summary of their key responsibilities and professional background.\n\n"
            "Please structure the output clearly with labels for each piece of information. If a piece of information is not found, please state 'Not Found'."
        )

    async def enrich_persona(self, persona: Dict) -> Dict:
        """Enriches a single persona by querying the Perplexity API."""
        full_name = persona.get('full_name', '')
        company_name = persona.get('company_name', '')

        if not full_name or not company_name:
            self.logger.warning("Persona is missing full_name or company_name, skipping enrichment.")
            return persona

        cache_key = f"{full_name}_{company_name}"
        if cache_key in self.enrichment_cache:
            self.logger.info(f"Found in cache. Skipping API call for {full_name}.")
            persona.update(self.enrichment_cache[cache_key])
            return persona

        prompt = self._construct_prompt(full_name, company_name)
        
        # For this re-architecture step, we are not yet parsing the response.
        # We are just making the call and will add parsing in the next step.
        # In a real run, this would be a live API call. For testing in an environment
        # without an API key, this call will fail gracefully.
        api_response = await self._call_perplexity_api(prompt)

        enriched_data = {
            'enrichment_attempted': True,
            'api_response_raw': api_response # Storing raw response for now
        }

        # Parse the API response to extract structured data
        if api_response:
            parsed_data = self._parse_api_response(api_response)
            enriched_data.update(parsed_data)
        
        self.enrichment_cache[cache_key] = enriched_data
        persona.update(enriched_data)
        
        return persona

    def _parse_api_response(self, response_text: str) -> Dict[str, str]:
        """Parses the raw text response from the API to extract key details."""
        parsed_data = {}

        # Regex to find a label and capture the text on the same line until the end
        def extract_value(label):
            pattern = re.compile(f"^{label}\\s*:\\s*(.*)$", re.MULTILINE | re.IGNORECASE)
            match = pattern.search(response_text)
            if match:
                value = match.group(1).strip()
                return value if value.lower() != 'not found' else ""
            return ""

        parsed_data['title'] = extract_value("Official Job Title")
        parsed_data['email'] = extract_value("Corporate Email Address")
        parsed_data['phone'] = extract_value("Corporate Direct-Dial Phone Number")
        parsed_data['linkedin'] = extract_value("LinkedIn Profile URL")
        
        # For the summary, we'll take a more broad approach
        summary_match = re.search(r"summary of their key responsibilities.*?:\n(.*?)(?=\n\n|\Z)", response_text, re.DOTALL | re.IGNORECASE)
        if summary_match:
            parsed_data['summary'] = summary_match.group(1).strip()

        return parsed_data

    async def batch_enrich(self, personas: list) -> list:
        """Enrich multiple personas efficiently."""
        tasks = [self.enrich_persona(p) for p in personas]
        return await asyncio.gather(*tasks)