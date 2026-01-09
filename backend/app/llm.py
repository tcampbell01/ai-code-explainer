import os
import anthropic

def get_model():
    return os.environ.get("MODEL_NAME", "claude-3-haiku-20240307")

def explain_code(prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model=get_model(),
        max_tokens=2000,
        temperature=0.1,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def chat_with_claude(prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model=get_model(),
        max_tokens=1500,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text
