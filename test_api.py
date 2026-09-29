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
    
    print(f"Base: {base}")
    print(f"Model: {model}")
    print(f"Key length: {len(key) if key else 'None'}")
    
    url = base.rstrip('/')
    if not url.endswith('/v1/messages'):
        url += '/v1/messages'
        
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 100,
        'temperature': 0
    }
    
    headers = {
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    test_api()
