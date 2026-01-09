from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Level = Literal["beginner", "intermediate", "expert"]

class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50_000)
    language: Optional[str] = None
    level: Level = "beginner"

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    code: str = Field(..., min_length=1, max_length=50_000)
    language: Optional[str] = None
    level: Level = "beginner"

class ChatResponse(BaseModel):
    answer: str

class RiskItem(BaseModel):
    line: int
    reason: str

class ConceptWithLink(BaseModel):
    concept: str
    learn_more_url: Optional[str] = None

class ExplainResponse(BaseModel):
    summary: str
    walkthrough: List[str]
    concepts: List[ConceptWithLink]
    gotchas: List[str]
    improvements: List[str]
    questions_to_ask: List[str]
    risks: List[RiskItem] = []
