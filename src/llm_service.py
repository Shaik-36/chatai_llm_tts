"""
LLM Service - Calls OpenAI Chat Endpoint
"""

import httpx
from src.config import settings


async def get_llm_response(user_text: str) -> str:

    #================ Build Parameters to send to Chat Endpoint ==================
    # API DOCs : https://platform.openai.com/docs/api-reference/responses/create

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
    
    #================ POST Message to LLM Endpoint and return response ==================
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    #================================ Handle Exceptions =================================
    except httpx.HTTPStatusError as e:
        raise Exception(f"OpenAI API error: {e.response.status_code}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid response format: {e}")
    except Exception as e:
        raise Exception(f"LLM service error: {str(e)}")
