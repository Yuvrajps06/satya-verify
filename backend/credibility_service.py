from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class CredibilityService:
    def __init__(self):
        # Predefined credibility scores for known Indian sources
        self.source_ratings = {
            'factcheck.pib.gov.in': 95,
            'pib.gov.in': 95,
            'altnews.in': 90,
            'boomlive.in': 90,
            'thehindu.com': 85,
            'ptinews.com': 88,
            'thequint.com': 82,
            'indiatoday.in': 80,
            'ndtv.com': 80,
            'timesofindia.indiatimes.com': 75,
            'hindustantimes.com': 78,
            'indianexpress.com': 82,
            # Government sources
            'rbi.org.in': 95,
            'mohfw.gov.in': 95,
            'eci.gov.in': 95,
            'mygov.in': 90,
            # Lower credibility
            'opindia.com': 50,
            'postcard.news': 45,
        }
    
    def get_domain_from_url(self, url: str) -> str:
        """
        Extract domain from URL
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www.
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return url.lower()
    
    def calculate_source_credibility(self, source_url: str, source_name: str = '') -> float:
        """
        Calculate credibility score for a source
        """
        domain = self.get_domain_from_url(source_url)
        
        # Check if we have a rating for this domain
        for known_domain, score in self.source_ratings.items():
            if known_domain in domain:
                logger.info(f"Found credibility score for {domain}: {score}")
                return score
        
        # Default credibility for unknown sources
        default_score = 60
        
        # Adjust based on TLD and patterns
        if domain.endswith('.gov.in'):
            default_score = 90  # Government sources
        elif domain.endswith('.edu'):
            default_score = 85  # Educational sources
        elif domain.endswith('.org.in') or domain.endswith('.org'):
            default_score = 75  # NGO sources
        elif any(word in domain for word in ['fake', 'satire', 'parody']):
            default_score = 20  # Satirical sources
        
        logger.info(f"Using default credibility score for {domain}: {default_score}")
        return default_score
    
    def analyze_source_reputation(self, source_data: Dict) -> Dict:
        """
        Analyze and enhance source data with credibility metrics
        """
        source_url = source_data.get('source_url', '')
        source_name = source_data.get('source_name', '')
        
        credibility = self.calculate_source_credibility(source_url, source_name)
        
        # Determine reputation category
        if credibility >= 85:
            reputation = 'Highly Trusted'
        elif credibility >= 70:
            reputation = 'Trusted'
        elif credibility >= 50:
            reputation = 'Moderate'
        else:
            reputation = 'Questionable'
        
        return {
            **source_data,
            'credibility_score': credibility,
            'reputation_category': reputation
        }
    
    def get_trusted_sources_list(self) -> List[Dict]:
        """
        Return list of trusted sources for display
        """
        sources = []
        for domain, score in sorted(self.source_ratings.items(), key=lambda x: x[1], reverse=True):
            if score >= 80:  # Only highly trusted
                sources.append({
                    'domain': domain,
                    'credibility_score': score,
                    'specialization': self._get_specialization(domain)
                })
        return sources
    
    def _get_specialization(self, domain: str) -> List[str]:
        """
        Get specialization areas for a domain
        """
        specializations = {
            'factcheck.pib.gov.in': ['Government', 'Politics', 'Health', 'General'],
            'altnews.in': ['Politics', 'Social Media', 'Religion'],
            'boomlive.in': ['Politics', 'Health', 'Technology'],
            'thehindu.com': ['Politics', 'Economy', 'General News'],
            'ptinews.com': ['General News', 'Breaking News'],
            'rbi.org.in': ['Finance', 'Banking', 'Economy'],
            'mohfw.gov.in': ['Health', 'Medical', 'COVID-19'],
            'eci.gov.in': ['Elections', 'Politics', 'Democracy'],
        }
        return specializations.get(domain, ['General'])
