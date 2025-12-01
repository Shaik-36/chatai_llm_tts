"""
LLM Service - Call OpenAI Chat API
"""

import httpx
from src.config import settings


async def get_llm_response(user_text: str) -> str:
    """
    Call OpenAI Chat Completions API.
    
    Args:
        user_text: User's input text
    
    Returns:
        Generated response from LLM
    
    Raises:
        Exception: On API errors or parsing failures
    """
    
    url = f"{settings.openai_base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": settings.llm_system_prompt},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": settings.llm_max_tokens,
        "temperature": settings.llm_temperature
    }
    
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    except httpx.HTTPStatusError as e:
        raise Exception(f"OpenAI API error: {e.response.status_code}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid response format: {e}")
    except Exception as e:
        raise Exception(f"LLM service error: {str(e)}")
