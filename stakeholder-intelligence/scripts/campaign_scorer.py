#!/usr/bin/env python3
"""
Campaign Scoring Agent for PSI System
Implements campaign-specific scoring logic
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Tuple

class CampaignScorer:
    """Agent responsible for campaign-specific persona scoring"""
    
    def __init__(self, shared_scratchpad: dict):
        self.scratchpad = shared_scratchpad
        self.logger = logging.getLogger('CampaignScorer')
        self.rules = self.load_campaign_rules()
    
    def load_campaign_rules(self) -> dict:
        """Load campaign rules from YAML configuration"""
        rules_path = Path(__file__).parent.parent / 'configs' / 'campaign_rules.yaml'
        
        try:
            with open(rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load campaign rules: {str(e)}")
            # Return default rules
            return self.get_default_rules()
    
    async def score_persona(self, persona: Dict) -> Dict:
        """Score a persona for all campaigns"""
        scores = {}
        
        # M&A Campaign scoring
        m_a_score, m_a_rationale = self.calculate_m_a_score(persona)
        scores['m_a_score'] = m_a_score
        scores['m_a_rationale'] = m_a_rationale
        
        # Ransomware Campaign scoring
        ransomware_score, ransomware_rationale = self.calculate_ransomware_score(persona)
        scores['ransomware_score'] = ransomware_score
        scores['ransomware_rationale'] = ransomware_rationale
        
        # Overall priority
        scores['overall_priority'] = self.determine_priority(m_a_score, ransomware_score)
        
        # Engagement approach
        scores['engagement_approach'] = self.get_engagement_approach(persona, m_a_score, ransomware_score)
        
        return scores
    
    def calculate_m_a_score(self, persona: Dict) -> Tuple[int, str]:
        """Calculate M&A campaign score"""
        campaign_rules = self.rules.get('m_a_campaign', {})
        base_scores = campaign_rules.get('base_scores', {})
        
        # Start with base score from title
        title = persona.get('title', '')
        score = 0
        rationale_parts = []
        
        # Check exact title match
        for title_pattern, base_score in base_scores.items():
            if title_pattern.lower() in title.lower():
                score = base_score
                rationale_parts.append(f"{title_pattern} role")
                break
        
        # If no exact match, use role type
        if score == 0:
            role_type = persona.get('role_type', 'Other')
            if role_type in base_scores:
                score = base_scores[role_type]
                rationale_parts.append(f"{role_type} position")
            else:
                score = 30  # Default score
        
        # Apply industry adjustments
        industry = persona.get('industry', '')
        industry_adjustments = campaign_rules.get('industry_adjustments', {})
        
        if industry in industry_adjustments:
            adjustments = industry_adjustments[industry]
            for role_pattern, adjustment in adjustments.items():
                if role_pattern.lower() in title.lower():
                    score += adjustment
                    rationale_parts.append(f"{industry} {role_pattern}")
        
        # Apply company size adjustments
        revenue = persona.get('annual_revenue', '')
        if revenue:
            if 'B' in revenue or 'billion' in revenue.lower():
                score += 10
                rationale_parts.append("Large company")
            elif 'M' in revenue and any(float(revenue.replace('M', '').replace('$', '').strip()) > 100 for _ in [1] if revenue.replace('M', '').replace('$', '').strip().replace('.', '').isdigit()):
                score += 5
                rationale_parts.append("Mid-size company")
        
        # Cap score at 100
        score = min(score, 100)
        
        # Generate rationale
        if rationale_parts:
            rationale = "M&A relevance: " + ", ".join(rationale_parts)
        else:
            rationale = "M&A relevance: General stakeholder"
        
        return score, rationale
    
    def calculate_ransomware_score(self, persona: Dict) -> Tuple[int, str]:
        """Calculate ransomware campaign score"""
        campaign_rules = self.rules.get('ransomware_campaign', {})
        base_scores = campaign_rules.get('base_scores', {})
        
        # Start with base score from title
        title = persona.get('title', '')
        score = 0
        rationale_parts = []
        
        # Check exact title match
        for title_pattern, base_score in base_scores.items():
            if title_pattern.lower() in title.lower():
                score = base_score
                rationale_parts.append(f"{title_pattern} role")
                break
        
        # If no exact match, use role type
        if score == 0:
            role_type = persona.get('role_type', 'Other')
            if role_type in base_scores:
                score = base_scores[role_type]
                rationale_parts.append(f"{role_type} position")
            else:
                score = 30  # Default score
        
        # Apply industry adjustments
        industry = persona.get('industry', '')
        industry_adjustments = campaign_rules.get('industry_adjustments', {})
        
        if industry in industry_adjustments:
            adjustments = industry_adjustments[industry]
            for role_pattern, adjustment in adjustments.items():
                if role_pattern.lower() in title.lower():
                    score += adjustment
                    rationale_parts.append(f"{industry} {role_pattern}")
        
        # Apply critical infrastructure boost
        critical_infrastructure = campaign_rules.get('critical_infrastructure_boost', [])
        for ci_entry in critical_infrastructure:
            if isinstance(ci_entry, dict):
                for ci_industry, boost in ci_entry.items():
                    if ci_industry.lower() in industry.lower():
                        score += boost
                        rationale_parts.append("Critical infrastructure")
                        break
        
        # Check for operational keywords
        operational_keywords = ['operations', 'production', 'plant', 'facility', 'manufacturing']
        if any(keyword in title.lower() for keyword in operational_keywords):
            score += 10
            rationale_parts.append("Operational responsibility")
        
        # Cap score at 100
        score = min(score, 100)
        
        # Generate rationale
        if rationale_parts:
            rationale = "Ransomware impact: " + ", ".join(rationale_parts)
        else:
            rationale = "Ransomware impact: General stakeholder"
        
        return score, rationale
    
    def determine_priority(self, m_a_score: int, ransomware_score: int) -> str:
        """Determine overall priority based on campaign scores"""
        max_score = max(m_a_score, ransomware_score)
        
        if max_score >= 90:
            return "Priority 1"
        elif max_score >= 75:
            return "Priority 2"
        elif max_score >= 60:
            return "Priority 3"
        elif max_score >= 40:
            return "Priority 4"
        else:
            return "Priority 5"
    
    def get_engagement_approach(self, persona: Dict, m_a_score: int, ransomware_score: int) -> str:
        """Determine best engagement approach"""
        role_type = persona.get('role_type', '')
        title = persona.get('title', '').lower()
        
        # Determine primary campaign
        if m_a_score > ransomware_score:
            # M&A focused approach
            if 'cfo' in title or 'finance' in title:
                return "Lead with financial risk quantification and M&A valuation impact"
            elif 'legal' in title or 'counsel' in title:
                return "Focus on regulatory compliance and liability in M&A context"
            elif 'corp' in title and 'dev' in title:
                return "Emphasize due diligence process enhancement"
            elif 'ceo' in title or 'president' in title:
                return "Strategic risk management and board-level concerns"
            else:
                return "M&A cybersecurity due diligence best practices"
        else:
            # Ransomware focused approach
            if 'coo' in title or 'operations' in title:
                return "Emphasize operational resilience and business continuity"
            elif 'ciso' in title or 'security' in title:
                return "Technical threat landscape and security solutions"
            elif 'cio' in title or 'it' in title:
                return "IT infrastructure protection and recovery capabilities"
            elif 'ceo' in title or 'president' in title:
                return "Business impact, crisis management, and recovery"
            else:
                return "Ransomware prevention and response strategies"
    
    def get_default_rules(self) -> dict:
        """Return default rules if YAML fails to load"""
        return {
            'm_a_campaign': {
                'base_scores': {
                    'CFO': 100,
                    'CEO': 85,
                    'General Counsel': 85,
                    'VP Finance': 80,
                    'C-Suite': 70,
                    'VP Level': 60,
                    'Director Level': 50,
                    'Other': 30
                }
            },
            'ransomware_campaign': {
                'base_scores': {
                    'COO': 100,
                    'CISO': 95,
                    'CIO': 90,
                    'CTO': 90,
                    'CEO': 85,
                    'C-Suite': 75,
                    'VP Level': 70,
                    'Director Level': 60,
                    'Other': 30
                }
            }
        }