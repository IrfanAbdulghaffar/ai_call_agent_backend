import httpx
import config

async def stream_gpt(text):
    url = 'https://models.github.ai/inference/chat/completions'
    headers = {
        'Authorization': f'Bearer {config.OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': 'openai/gpt-4.1',
        'temperature': 1,
        'max_tokens': 4096,
        'top_p': 1,
        'messages': [
            {'role': 'user', 'content': text}
        ],
        'stream': True
    }
    async with httpx.AsyncClient() as client:
        async with client.stream('POST', url, headers=headers, json=payload) as resp:
            async for line in resp.aiter_lines():
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    # The response structure may differ; adjust as needed
                    delta = data.get('choices', [{}])[0].get('delta', {}).get('content')
                    if delta:
                        yield delta 