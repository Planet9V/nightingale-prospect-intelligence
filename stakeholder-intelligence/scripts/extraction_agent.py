#!/usr/bin/env python3
"""
Extraction Agent for PSI System
Handles parallel extraction of personas from prospect files
"""

import re
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
import logging

class ExtractionAgent:
    """Agent responsible for extracting personas from prospect files"""
    
    def __init__(self, shared_scratchpad: dict):
        self.scratchpad = shared_scratchpad
        self.logger = logging.getLogger('ExtractionAgent')
        
        # Key files to search for personas
        self.target_files = [
            'Organization_Foundation.md',
            'Engagement_Strategy.md',
            'Business_Initiatives.md',
            'Strategic_Context.md'
        ]
        
        # Patterns for executive extraction
        self.name_patterns = [
            # **Name** - Title format
            r'\*\*([^*]+)\*\*\s*[-–—]\s*([^*\n]+)',
            # ### Name - Title format
            r'###\s+([^-–—\n]+)\s*[-–—]\s*([^\n]+)',
            # #### Name - Title format
            r'####\s+([^-–—\n]+)\s*[-–—]\s*([^\n]+)'
        ]
    
    async def extract_personas(self, prospect_path: Path) -> List[dict]:
        """Extract all personas from a prospect folder"""
        sf_id = self.extract_sf_id(prospect_path.name)
        company_name = self.extract_company_name(prospect_path.name)
        
        if not sf_id:
            self.logger.warning(f"Could not extract SF_ID from {prospect_path.name}")
            return []
        
        # Extract company info
        company_info = await self.extract_company_info(prospect_path)
        self.scratchpad['company_profiles'][sf_id] = company_info
        
        # Find and process relevant files
        personas = []
        for file_pattern in self.target_files:
            file_path = prospect_path / file_pattern
            if file_path.exists():
                file_personas = await self.extract_from_file(
                    file_path, sf_id, company_name, company_info
                )
                personas.extend(file_personas)
        
        # Also check for GTM Part 3 files
        for gtm_file in prospect_path.glob('*GTM*Part*3*.md'):
            file_personas = await self.extract_from_file(
                gtm_file, sf_id, company_name, company_info
            )
            personas.extend(file_personas)
        
        # Deduplicate personas
        unique_personas = self.deduplicate_personas(personas)
        
        # Store in scratchpad
        for persona in unique_personas:
            persona_id = f"{sf_id}_{persona['full_name'].replace(' ', '_')}"
            self.scratchpad['extracted_personas'][persona_id] = persona
        
        return unique_personas
    
    def extract_sf_id(self, folder_name: str) -> Optional[str]:
        """Extract Salesforce ID from folder name"""
        match = re.match(r'^([A-Z]-\d{6})_', folder_name)
        return match.group(1) if match else None
    
    def extract_company_name(self, folder_name: str) -> str:
        """Extract company name from folder name"""
        match = re.match(r'^[A-Z]-\d{6}_(.+)$', folder_name)
        return match.group(1).replace('_', ' ') if match else folder_name
    
    async def extract_company_info(self, prospect_path: Path) -> dict:
        """Extract company information from files"""
        info = {
            'industry': '',
            'sub_industry': '',
            'annual_revenue': '',
            'employee_count': '',
            'headquarters': '',
            'key_products': [],
            'recent_events': []
        }
        
        # Check Organization Foundation first
        org_file = prospect_path / 'Organization_Foundation.md'
        if org_file.exists():
            content = org_file.read_text(encoding='utf-8', errors='ignore')
            
            # Extract industry
            industry_match = re.search(r'(?:Industry|Sector)[:\s]*([^\n]+)', content, re.IGNORECASE)
            if industry_match:
                info['industry'] = industry_match.group(1).strip()
            
            # Extract revenue
            revenue_patterns = [
                r'(?:Annual Revenue|Revenue)[:\s]*\$?([\d.]+\s*[BMK])',
                r'\$?([\d.]+\s*(?:billion|million))\s*(?:in revenue|revenue)'
            ]
            for pattern in revenue_patterns:
                revenue_match = re.search(pattern, content, re.IGNORECASE)
                if revenue_match:
                    info['annual_revenue'] = revenue_match.group(1).strip()
                    break
            
            # Extract employee count
            employee_patterns = [
                r'(?:Employees?|Staff|Workforce)[:\s]*([\d,]+\+?)',
                r'([\d,]+\+?)\s*(?:employees|staff|workers)'
            ]
            for pattern in employee_patterns:
                emp_match = re.search(pattern, content, re.IGNORECASE)
                if emp_match:
                    info['employee_count'] = emp_match.group(1).strip()
                    break
        
        return info
    
    async def extract_from_file(self, file_path: Path, sf_id: str, 
                               company_name: str, company_info: dict) -> List[dict]:
        """Extract personas from a single file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            personas = []
            
            # Apply each pattern
            for pattern in self.name_patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                
                for match in matches:
                    name = match.group(1).strip()
                    title = match.group(2).strip()
                    
                    # Clean up
                    name = re.sub(r'^\*+|\*+$', '', name).strip()
                    title = re.sub(r'^\*+|\*+$', '', title).strip()
                    
                    # Validate
                    if self.is_valid_persona(name, title):
                        # Extract additional context
                        context_start = match.end()
                        context_end = content.find('\n\n', context_start)
                        if context_end == -1:
                            context_end = min(context_start + 1000, len(content))
                        
                        context = content[context_start:context_end]
                        
                        persona = {
                            'sf_id': sf_id,
                            'company_name': company_name,
                            'industry': company_info.get('industry', ''),
                            'sub_industry': company_info.get('sub_industry', ''),
                            'annual_revenue': company_info.get('annual_revenue', ''),
                            'employee_count': company_info.get('employee_count', ''),
                            'headquarters': company_info.get('headquarters', ''),
                            'full_name': name,
                            'title': title,
                            'department': self.extract_department(title),
                            'role_type': self.classify_role(title),
                            'authority_level': self.determine_authority(title),
                            'budget_authority': self.has_budget_authority(title),
                            'veto_power': self.has_veto_power(title),
                            'tenure': self.extract_tenure(context),
                            'previous_role': self.extract_previous_role(context),
                            'education': self.extract_education(context),
                            'key_priorities': self.extract_priorities(context),
                            'pain_points': self.extract_pain_points(context),
                            'source_file': file_path.name,
                            'extraction_confidence': 0.9
                        }
                        
                        personas.append(persona)
            
            return personas
            
        except Exception as e:
            self.logger.error(f"Error extracting from {file_path}: {str(e)}")
            return []
    
    def is_valid_persona(self, name: str, title: str) -> bool:
        """Validate if extracted text represents a real person"""
        # Skip if too short
        if len(name) < 3 or len(title) < 3:
            return False
        
        # Skip non-person keywords
        skip_keywords = [
            'background', 'authority', 'priorities', 'strategy',
            'current', 'former', 'leadership', 'executive',
            'stakeholder', 'position', 'dynamics', 'structure'
        ]
        
        name_lower = name.lower()
        if any(skip in name_lower for skip in skip_keywords):
            return False
        
        # Must have at least one capital letter (proper noun)
        if not any(c.isupper() for c in name):
            return False
        
        # Check for valid title keywords
        title_keywords = [
            'ceo', 'cfo', 'cio', 'cto', 'ciso', 'chief', 'president',
            'vice president', 'vp', 'director', 'manager', 'head',
            'officer', 'chairman', 'board'
        ]
        
        title_lower = title.lower()
        if not any(keyword in title_lower for keyword in title_keywords):
            return False
        
        return True
    
    def classify_role(self, title: str) -> str:
        """Classify role based on title"""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ['ceo', 'chief executive', 'president & ceo']):
            return 'CEO/President'
        elif 'cfo' in title_lower or 'chief financial' in title_lower:
            return 'CFO'
        elif any(term in title_lower for term in ['cio', 'chief information']):
            return 'CIO/CTO'
        elif any(term in title_lower for term in ['cto', 'chief technology']):
            return 'CIO/CTO'
        elif any(term in title_lower for term in ['ciso', 'chief security']):
            return 'CISO'
        elif any(term in title_lower for term in ['coo', 'chief operating']):
            return 'COO'
        elif 'chief' in title_lower:
            return 'Other C-Suite'
        elif any(term in title_lower for term in ['evp', 'executive vice']):
            return 'EVP'
        elif any(term in title_lower for term in ['svp', 'senior vice']):
            return 'SVP'
        elif any(term in title_lower for term in ['vp', 'vice president']):
            return 'VP'
        elif 'director' in title_lower:
            return 'Director'
        elif 'manager' in title_lower:
            return 'Manager'
        elif any(term in title_lower for term in ['chairman', 'board']):
            return 'Board Member'
        else:
            return 'Other'
    
    def determine_authority(self, title: str) -> str:
        """Determine authority level"""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ['ceo', 'president', 'chairman']):
            return 'Ultimate Decision Maker'
        elif any(term in title_lower for term in ['cfo', 'cio', 'cto', 'ciso', 'coo', 'chief']):
            return 'Executive Decision Maker'
        elif any(term in title_lower for term in ['evp', 'executive vice']):
            return 'Senior Decision Maker'
        elif any(term in title_lower for term in ['svp', 'senior vice', 'vp', 'vice president']):
            return 'Decision Influencer'
        elif 'director' in title_lower:
            return 'Technical Influencer'
        else:
            return 'Stakeholder'
    
    def has_budget_authority(self, title: str) -> str:
        """Determine budget authority"""
        title_lower = title.lower()
        budget_roles = [
            'ceo', 'cfo', 'president', 'chief', 'evp', 'svp', 'vp',
            'vice president', 'director', 'procurement', 'purchasing'
        ]
        return 'Yes' if any(term in title_lower for term in budget_roles) else 'No'
    
    def has_veto_power(self, title: str) -> str:
        """Determine veto power"""
        title_lower = title.lower()
        veto_roles = ['ceo', 'cfo', 'president', 'chief executive', 'chairman']
        return 'Yes' if any(term in title_lower for term in veto_roles) else 'No'
    
    def extract_department(self, title: str) -> str:
        """Extract department from title"""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ['finance', 'cfo', 'accounting', 'treasury']):
            return 'Finance'
        elif any(term in title_lower for term in ['technology', 'cto', 'cio', 'it ', 'information']):
            return 'Technology'
        elif any(term in title_lower for term in ['security', 'ciso', 'cyber']):
            return 'Security'
        elif any(term in title_lower for term in ['operations', 'coo', 'supply chain']):
            return 'Operations'
        elif any(term in title_lower for term in ['legal', 'counsel', 'compliance']):
            return 'Legal'
        elif any(term in title_lower for term in ['sales', 'revenue', 'commercial']):
            return 'Sales'
        elif any(term in title_lower for term in ['marketing', 'brand', 'communications']):
            return 'Marketing'
        elif any(term in title_lower for term in ['hr', 'human resources', 'people', 'talent']):
            return 'Human Resources'
        else:
            return 'Executive'
    
    def extract_tenure(self, text: str) -> str:
        """Extract tenure information"""
        patterns = [
            r'(?:Tenure|Since|Joined|Appointed)[:\s]*([^\n,]+)',
            r'(\d{4})\s*-\s*(?:Present|Current)',
            r'(\d+\+?\s*years?)\s*(?:with|at|in)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ''
    
    def extract_previous_role(self, text: str) -> str:
        """Extract previous role"""
        patterns = [
            r'(?:Previous|Former|Previously)[:\s]*([^\n]+)',
            r'(?:Prior to|Before)[^,]+,\s*([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:100]  # Limit length
        return ''
    
    def extract_education(self, text: str) -> str:
        """Extract education"""
        patterns = [
            r'(?:Education|Degree)[:\s]*([^\n]+)',
            r'(B\.?S\.?|M\.?S\.?|M\.?B\.?A\.?|Ph\.?D\.?)[^,\n]*'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:100]  # Limit length
        return ''
    
    def extract_priorities(self, text: str) -> str:
        """Extract key priorities"""
        patterns = [
            r'(?:Priorit(?:y|ies)|Focus|Goals?)[:\s]*([^\n]+)',
            r'(?:Key initiatives?)[:\s]*([^\n]+)'
        ]
        
        priorities = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                priority = match.group(1).strip()
                if 10 < len(priority) < 200:
                    priorities.append(priority)
        
        return '; '.join(priorities[:2])  # Return top 2
    
    def extract_pain_points(self, text: str) -> str:
        """Extract pain points"""
        patterns = [
            r'(?:Pain Points?|Concerns?|Challenges?)[:\s]*([^\n]+)',
            r'(?:Issues?|Problems?)[:\s]*([^\n]+)'
        ]
        
        pains = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pain = match.group(1).strip()
                if 10 < len(pain) < 200:
                    pains.append(pain)
        
        return '; '.join(pains[:2])  # Return top 2
    
    def deduplicate_personas(self, personas: List[dict]) -> List[dict]:
        """Remove duplicate personas"""
        seen = set()
        unique = []
        
        for persona in personas:
            key = (persona['full_name'], persona['company_name'])
            if key not in seen:
                seen.add(key)
                unique.append(persona)
        
        return unique