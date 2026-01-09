import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ExplainRequest, ExplainResponse, ChatRequest, ChatResponse
from .prompts import build_prompt, build_chat_prompt
from .llm import explain_code, chat_with_claude
from .url_database import get_learn_more_url

load_dotenv()

app = FastAPI(title="AI Code Explainer")

# Allow your frontend dev server to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    # quick “backend engineer” guardrail
    if "ANTHROPIC_API_KEY" not in os.environ or not os.environ["ANTHROPIC_API_KEY"]:
        raise HTTPException(status_code=500, detail="Server not configured (missing ANTHROPIC_API_KEY).")

    prompt = build_prompt(req.code, req.level, req.language)

    try:
        raw = explain_code(prompt)
        print(f"Raw response: {raw[:500]}...")  # Debug log
        
        # Extract JSON from response (Claude sometimes adds explanatory text)
        json_start = raw.find('{')
        json_end = raw.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            print(f"No JSON found in response: {raw}")
            raise HTTPException(status_code=502, detail="No valid JSON found in response.")
        
        json_str = raw[json_start:json_end]
        print(f"Extracted JSON: {json_str[:200]}...")
        
        data = json.loads(json_str)
        
        # Add verified URLs to concepts
        if "concepts" in data:
            for concept_item in data["concepts"]:
                if isinstance(concept_item, dict) and "concept" in concept_item:
                    concept_name = concept_item["concept"]
                    verified_url = get_learn_more_url(concept_name)
                    concept_item["learn_more_url"] = verified_url
        
        return ExplainResponse(**data)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise HTTPException(status_code=502, detail="Model returned invalid JSON. Try again.")
    except Exception as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if "ANTHROPIC_API_KEY" not in os.environ or not os.environ["ANTHROPIC_API_KEY"]:
        raise HTTPException(status_code=500, detail="Server not configured (missing ANTHROPIC_API_KEY).")

    prompt = build_chat_prompt(req.question, req.code, req.level, req.language)

    try:
        raw = chat_with_claude(prompt)
        print(f"Chat response: {raw[:200]}...")  # Debug log
        return ChatResponse(answer=raw)
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
