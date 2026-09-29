import toml
import os
import requests
from pathlib import Path

def test_api():
    path = Path('.streamlit/secrets.toml')
    secrets = toml.loads(path.read_text()) if path.exists() else {}
    
    key = os.environ.get('ANTHROPIC_API_KEY') or secrets.get('ANTHROPIC_API_KEY') or secrets.get('anthropic_api_key')
    base = os.environ.get('ANTHROPIC_BASE_URL') or secrets.get('ANTHROPIC_BASE_URL') or 'https://api.anthropic.com'
    model = os.environ.get('ANTHROPIC_MODEL') or secrets.get('ANTHROPIC_MODEL') or secrets.get('anthropic_model') or 'cc/claude-opus-5'
    
    url = base.rstrip('/')
    if not url.endswith('/v1/chat/completions'):
        if url.endswith('/v1'):
            url += '/chat/completions'
        else:
            url += '/v1/chat/completions'
            
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 100,
        'temperature': 0
    }
    
    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"OpenAI Format URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    test_api()
