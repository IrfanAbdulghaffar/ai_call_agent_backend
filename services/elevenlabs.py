import httpx
import config

VOICE_ID = 'your_voice_id'  # TODO: Replace with your actual ElevenLabs voice ID

async def stream_tts(text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream'
    headers = {
        'xi-api-key': config.ELEVENLABS_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
    }
    payload = {
        'text': text,
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    }
    async with httpx.AsyncClient() as client:
        async with client.stream('POST', url, headers=headers, json=payload) as resp:
            async for chunk in resp.aiter_bytes():
                yield chunk 