from typing import Optional, Dict

# Curated database of verified documentation URLs
VERIFIED_URLS: Dict[str, str] = {
    # Python Core
    "python": "https://docs.python.org/3/",
    "literal": "https://docs.python.org/3/library/typing.html#typing.Literal",
    "list": "https://docs.python.org/3/library/typing.html#typing.List",
    "optional": "https://docs.python.org/3/library/typing.html#typing.Optional",
    "typing": "https://docs.python.org/3/library/typing.html",
    "dict": "https://docs.python.org/3/library/stdtypes.html#dict",
    "str": "https://docs.python.org/3/library/stdtypes.html#str",
    "int": "https://docs.python.org/3/library/functions.html#int",
    "bool": "https://docs.python.org/3/library/functions.html#bool",
    
    # Pydantic
    "pydantic": "https://docs.pydantic.dev/",
    "basemodel": "https://docs.pydantic.dev/latest/concepts/models/",
    "field": "https://docs.pydantic.dev/latest/concepts/fields/",
    "validator": "https://docs.pydantic.dev/latest/concepts/validators/",
    
    # FastAPI
    "fastapi": "https://fastapi.tiangolo.com/",
    "httpexception": "https://fastapi.tiangolo.com/tutorial/handling-errors/",
    
    # JavaScript/Web
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "html": "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "css": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "json": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON",
    
    # Common Programming Concepts
    "recursion": "https://docs.python.org/3/glossary.html#term-recursion",
    "function": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    "class": "https://docs.python.org/3/tutorial/classes.html",
    "loop": "https://docs.python.org/3/tutorial/controlflow.html#for-statements",
    "variable": "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator",
}

def get_learn_more_url(concept: str) -> Optional[str]:
    """
    Get a verified documentation URL for a programming concept.
    
    Args:
        concept: The programming concept to look up
        
    Returns:
        A verified URL or None if no URL is available
    """
    concept_key = concept.lower().strip()
    return VERIFIED_URLS.get(concept_key)

def add_verified_url(concept: str, url: str) -> None:
    """
    Add a new verified URL to the database.
    
    Args:
        concept: The programming concept
        url: The verified documentation URL
    """
    VERIFIED_URLS[concept.lower().strip()] = url

def list_available_concepts() -> list[str]:
    """Return a list of all concepts with available URLs."""
    return list(VERIFIED_URLS.keys())