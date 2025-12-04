"""
Data Models - Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import Optional

# ================================================================
#  Client Message Validations
# ================================================================

class ClientMessage(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, max_length=2000
    )

# ================================================================
#  Server Response Validations
# ================================================================

class ServerMessage(BaseModel):
    type: str  # "audio" or "error"
    audio_data: Optional[str] = None
    llm_text: Optional[str] = None
    error_message: Optional[str] = None
    
    #======= Method to Remove the None Valuse from response =====
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}
