from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.deepgram import stream_transcribe
from services.openai import stream_gpt
from services.elevenlabs import stream_tts
import asyncio

router = APIRouter()

@router.websocket('/ws/voice')
async def voice_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive audio stream from client
        async def audio_generator():
            while True:
                data = await websocket.receive_bytes()
                if not data:
                    break
                yield data
        # Stream to Deepgram for transcription
        transcript_gen = stream_transcribe(audio_generator())
        async for transcript in transcript_gen:
            # Stream transcript to OpenAI GPT
            gpt_gen = stream_gpt(transcript)
            async for gpt_reply in gpt_gen:
                # Stream GPT reply to ElevenLabs for TTS
                tts_gen = stream_tts(gpt_reply)
                async for audio_chunk in tts_gen:
                    await websocket.send_bytes(audio_chunk)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.close(code=1011, reason=str(e)) 