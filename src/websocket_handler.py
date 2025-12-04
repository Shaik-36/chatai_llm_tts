"""
WebSocket Handler - Orchestrates LLM - TTS Services
"""

import base64
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from src.models import ClientMessage, ServerMessage
from src.llm_service import get_llm_response
from src.tts_service import get_tts_audio

# ================================================================
#  Handle the Websocket Connections Function
# ================================================================

async def handle_websocket(websocket: WebSocket) -> None:
    
    print(f"[WS] 🔗 New connection...!")
    await websocket.accept()
    print(f"[WS] ✅ Connection accepted...!")
    
    try:
        # ================================================================
        #  WebSocket Open Connection Loop
        # ================================================================
        while True:

            #================= Receive Message and Validate =================== 
            try:
                data = await websocket.receive_json()
                message = ClientMessage(**data)
            except ValidationError:
                await send_error(websocket, "Invalid message format")
                continue
            except (WebSocketDisconnect, RuntimeError):
                print(f"[WS] Client disconnected")
                break

            #==================== Call LLM - TTS Services ====================
            try:
                llm_response = await get_llm_response(message.text)
                audio_bytes = await get_tts_audio(llm_response)
                
            #==================== Encode Received Audio =======================
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                response = ServerMessage(
                    type="audio",
                    audio_data=audio_base64,
                    llm_text=llm_response
                )

            #============ Send response to Client (Audio-Encoded) ==============
                await websocket.send_json(response.model_dump())
                print(f"[WS] ✅ Audio Message Sent to Client ")
                
            except Exception as e:
                print(f"[ERROR] Issue with the LLM-TTS Services")
                await send_error(websocket, f"Processing error: {str(e)}")
                continue
    finally:
    #============ Close the WebSocket Connection ==============    
        try:
            await websocket.close()
            print(f"[WS] ✅ WebSocket closed cleanly")
        except:
            pass  # Already closed

# ================================================================
#  Send Error Function - Client
# ================================================================

async def send_error(websocket: WebSocket, error_message: str):
    try:
        error_response = ServerMessage(
            type="error",
            error_message=error_message,
            llm_text=""
        )
        await websocket.send_json(error_response.model_dump())
    except:
        pass  # Connection might be broken
