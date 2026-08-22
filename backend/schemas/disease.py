from typing import Optional

from pydantic import BaseModel


class DiseaseResponse(BaseModel):
    success: bool
    plant: Optional[str] = None
    disease: Optional[str] = None
    confidence: Optional[float] = None
    recommendation: Optional[str] = None
    prevention: Optional[str] = None
    model_available: bool
    error: Optional[dict[str, str]] = None
