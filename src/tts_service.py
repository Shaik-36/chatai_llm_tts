"""
TTS Service - Call OpenAI Text-to-Speech API
"""

import httpx
from src.config import settings


async def get_tts_audio(text: str) -> bytes:
    """
    Call OpenAI TTS API to generate audio.
    
    Args:
        text: Text to convert to speech
    
    Returns:
        Audio bytes (MP3 format)
    
    Raises:
        Exception: On API errors
    """
    
    url = "https://api.openai.com/v1/audio/speech"
    
    payload = {
        "model": settings.tts_model,
        "input": text,
        "voice": settings.tts_voice,
        "response_format": "mp3"
    }
    
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.content
    
    except httpx.HTTPStatusError as e:
        raise Exception(f"OpenAI TTS error: {e.response.status_code}")
    except httpx.TimeoutException:
        raise Exception(f"TTS timeout after {settings.request_timeout}s")
    except httpx.ConnectError:
        raise Exception("Cannot connect to OpenAI")
    except Exception as e:
        raise Exception(f"TTS error: {str(e)}")
