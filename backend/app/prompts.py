from typing import Optional

def build_prompt(code: str, level: str, language: Optional[str]):
    lang = language or "unknown"
    return f"""
Explain this {lang} code for a {level} developer. Return ONLY valid JSON:

{{
  "summary": "Brief explanation",
  "walkthrough": ["Step 1", "Step 2"],
  "concepts": [{{"concept": "Name", "learn_more_url": "https://exact-working-url.com or null"}}],
  "gotchas": ["What could go wrong and why"],
  "improvements": ["How to make it better"],
  "questions_to_ask": ["Questions for deeper understanding"],
  "risks": [{{"line": 1, "reason": "Security/performance issue"}}]
}}

For learn_more_url:
- Use the curated URL database for verified links
- Set to null if concept not in database 


Code:
```{lang}
{code}
```""".strip()

def build_chat_prompt(question: str, code: str, level: str, language: Optional[str]):
    lang = language or "unknown"
    return f"""
You are helping a {level} developer understand this {lang} code. Answer their question clearly and concisely.

When providing learning resources:
- Do NOT include any URLs or links
- Instead, give specific search terms like "search for 'Pydantic BaseModel tutorial'"
- Mention official documentation sites by name without linking
- Example: "Check the official Pydantic documentation for BaseModel details" 


Format guidelines:
- Use **bold** for important terms
- Keep explanations appropriate for {level} level
- Be specific and practical
- Provide search guidance instead of direct links

Code context:
```{lang}
{code}
```

Question: {question}

Answer:""".strip()