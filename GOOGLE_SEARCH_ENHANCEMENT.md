# Future Enhancement: Google Custom Search API Integration

## Overview
This document outlines how to integrate Google Custom Search API to dynamically find current, working documentation links for programming concepts.

## Current Implementation
- **Curated URL Database**: Manual list of verified documentation URLs
- **Pros**: Reliable, fast, no API costs
- **Cons**: Requires manual maintenance, limited coverage

## Proposed Enhancement: Google Custom Search API

### Benefits
- **Dynamic Link Discovery**: Automatically find current documentation
- **Broader Coverage**: Support for any programming concept
- **Self-Updating**: Links stay current as documentation moves
- **Cost Effective**: 100 free searches/day, then $5/1000 queries

### Implementation Plan

#### 1. Setup Requirements
```bash
# Google Cloud Console Setup
1. Create project at https://console.cloud.google.com/
2. Enable Custom Search API
3. Create Custom Search Engine at https://cse.google.com/
4. Configure to search only trusted domains:
   - docs.python.org
   - docs.pydantic.dev
   - fastapi.tiangolo.com
   - developer.mozilla.org
   - docs.djangoproject.com
   - flask.palletsprojects.com
```

#### 2. Environment Variables
```env
# Add to .env
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_custom_search_engine_id
```

#### 3. Implementation Code
```python
# backend/app/google_search_service.py
import requests
import os
from typing import Optional, List
from urllib.parse import urlparse

class GoogleSearchService:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        self.engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        # Trusted domains for documentation
        self.trusted_domains = [
            "docs.python.org",
            "docs.pydantic.dev", 
            "fastapi.tiangolo.com",
            "developer.mozilla.org"
        ]
    
    def search_concept_docs(self, concept: str, language: str = "python") -> Optional[str]:
        """Search for official documentation for a programming concept"""
        
        # Construct search query
        query = f"{concept} {language} documentation"
        
        params = {
            "key": self.api_key,
            "cx": self.engine_id,
            "q": query,
            "num": 5  # Get top 5 results
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            
            # Find first result from trusted domain
            for item in results.get("items", []):
                url = item.get("link", "")
                domain = urlparse(url).netloc
                
                if any(trusted in domain for trusted in self.trusted_domains):
                    # Verify URL is accessible
                    if self._verify_url(url):
                        return url
            
            return None
            
        except Exception as e:
            print(f"Search error: {e}")
            return None
    
    def _verify_url(self, url: str) -> bool:
        """Verify that a URL returns a successful response"""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

# Enhanced URL database with fallback to search
def get_enhanced_learn_more_url(concept: str, language: str = "python") -> Optional[str]:
    """
    Get documentation URL with fallback to Google Search
    
    1. Check curated database first (fast, reliable)
    2. If not found, use Google Search API (dynamic)
    3. Cache successful search results
    """
    from .url_database import get_learn_more_url
    
    # Try curated database first
    curated_url = get_learn_more_url(concept)
    if curated_url:
        return curated_url
    
    # Fallback to Google Search
    if os.environ.get("GOOGLE_SEARCH_API_KEY"):
        search_service = GoogleSearchService()
        search_url = search_service.search_concept_docs(concept, language)
        
        if search_url:
            # Cache successful result for future use
            from .url_database import add_verified_url
            add_verified_url(concept, search_url)
            return search_url
    
    return None
```

#### 4. Integration Points
```python
# Update main.py
from .google_search_service import get_enhanced_learn_more_url

# Replace in explain endpoint:
verified_url = get_enhanced_learn_more_url(concept_name, req.language or "python")
```

#### 5. Caching Strategy
```python
# Add to url_database.py
import json
from datetime import datetime, timedelta

CACHE_FILE = "search_cache.json"
CACHE_DURATION = timedelta(days=7)  # Cache for 1 week

def load_search_cache():
    """Load cached search results"""
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_search_cache(cache):
    """Save search results to cache"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached_url(concept: str) -> Optional[str]:
    """Get URL from cache if not expired"""
    cache = load_search_cache()
    entry = cache.get(concept.lower())
    
    if entry:
        cached_time = datetime.fromisoformat(entry['timestamp'])
        if datetime.now() - cached_time < CACHE_DURATION:
            return entry['url']
    
    return None
```

### Cost Analysis
- **Free Tier**: 100 searches/day
- **Paid Tier**: $5 per 1000 searches
- **Expected Usage**: ~10-50 searches/day for new concepts
- **Monthly Cost**: $0-15 depending on usage

### Migration Plan
1. **Phase 1**: Implement Google Search service alongside curated database
2. **Phase 2**: Add caching to reduce API calls
3. **Phase 3**: Monitor usage and costs
4. **Phase 4**: Gradually expand trusted domains

### Monitoring & Maintenance
- Track API usage and costs
- Monitor search result quality
- Update trusted domains list
- Refresh cache periodically
- Fallback to curated database if API fails

### Alternative: Hybrid Approach
Keep curated database for common concepts (90% coverage) and use Google Search only for rare/new concepts to minimize costs.

## Implementation Priority: Low
Current curated database approach covers most use cases effectively. Implement this enhancement only if:
1. Users frequently request links for concepts not in database
2. Maintenance overhead of curated database becomes significant
3. Budget allows for API costs