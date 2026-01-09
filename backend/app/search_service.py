import requests
import os
from typing import Optional, List

class WebSearchService:
    def __init__(self):
        self.bing_api_key = os.environ.get("BING_SEARCH_API_KEY")
        self.bing_endpoint = "https://api.bing.microsoft.com/v7.0/search"
    
    def search_for_concept_docs(self, concept: str, language: str = "python") -> Optional[str]:
        """Search for official documentation for a programming concept"""
        
        # Prioritize official docs in search query
        query = f"{concept} {language} official documentation site:docs.python.org OR site:docs.pydantic.dev"
        
        headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
        params = {
            "q": query,
            "count": 3,
            "responseFilter": "Webpages"
        }
        
        try:
            response = requests.get(self.bing_endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            results = response.json()
            
            # Return first result from trusted domains
            trusted_domains = ["docs.python.org", "docs.pydantic.dev", "fastapi.tiangolo.com", "developer.mozilla.org"]
            
            for page in results.get("webPages", {}).get("value", []):
                url = page.get("url", "")
                for domain in trusted_domains:
                    if domain in url:
                        return url
            
            return None
            
        except Exception as e:
            print(f"Search error: {e}")
            return None

def get_search_enhanced_url(concept: str, language: str = "python") -> Optional[str]:
    """Get a URL for a concept using web search"""
    search_service = WebSearchService()
    return search_service.search_for_concept_docs(concept, language)