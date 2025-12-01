"""
LLM Service - OpenAI Chat Completions API

This module is responsible for a single job:
Given input text, call OpenAI's chat completions API
and return the model's text response.

"""

import httpx
from src.config import settings


# Get the response from the LLM (OpenAI)
async def get_llm_response(user_text: str) -> str:
    """
    Calls OpenAI Chat Completions API and returns the response text

    Args: 
        user_text: The validated text from thr client

    Returns:
        Response to the user_text
    """

    # Endpoint URL from base URL in config and as mentioned in OpenAI Specs
    url = f"{settings.openai_base_url}/chat/completions"

    # Header with API Key
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    # Payload according to the OpenAI Spec
    payload = {
        "model": settings.llm_model,
        "messages":[
            {  
                "role"      : "user",
                "content"   : user_text
            }
        ],
        "max_tokens": settings.llm_max_tokens,
        "temperature": settings.llm_temperature
    }


    # Using async to call the OpenAI Chat Completion
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            # Performing the async POST request
            response = await client.post(url, headers=headers, json=payload)

            # If any responses like 2xx, 4xx response raise
            response.raise_for_status()

            # Return the response content
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} {e.response.reason_phrase}")
            print(f"Error details: {e.response.text}")
            # Optionally, re-raise the exception if you want to stop execution here
            # raise
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            # Optionally, re-raise here also
            # raise