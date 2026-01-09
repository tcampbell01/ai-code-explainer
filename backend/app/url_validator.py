import requests
from typing import Optional

def validate_url(url: str) -> bool:
    """Check if a URL returns a successful response"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def get_validated_learn_more_url(concept: str) -> Optional[str]:
    """Return a validated URL for a concept, or None if no valid URL found"""
    
    # Common working URLs to try for each concept
    url_candidates = {
        "pydantic": [
            "https://docs.pydantic.dev/",
            "https://pydantic-docs.helpmanual.io/"
        ],
        "basemodel": [
            "https://docs.pydantic.dev/latest/concepts/models/",
            "https://docs.pydantic.dev/"
        ],
        "literal": [
            "https://docs.python.org/3/library/typing.html#typing.Literal",
            "https://docs.python.org/3/library/typing.html"
        ],
        "optional": [
            "https://docs.python.org/3/library/typing.html#typing.Optional",
            "https://docs.python.org/3/library/typing.html"
        ]
    }
    
    concept_lower = concept.lower()
    if concept_lower in url_candidates:
        for url in url_candidates[concept_lower]:
            if validate_url(url):
                return url
    
    return None