import httpx
import config

async def stream_transcribe(audio_gen):
    url = 'wss://api.deepgram.com/v1/listen'
    headers = {'Authorization': f'Token {config.DEEPGRAM_API_KEY}'}
    async with httpx.AsyncClient() as client:
        async with client.stream('POST', url, headers=headers, data=audio_gen) as resp:
            async for line in resp.aiter_lines():
                # Parse Deepgram's response for transcript text
                # (Assume JSON with 'channel' and 'alternatives')
                import json
                try:
                    data = json.loads(line)
                    transcript = data['channel']['alternatives'][0]['transcript']
                    if transcript:
                        yield transcript
                except Exception:
                    continue 