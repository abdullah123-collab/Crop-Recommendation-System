from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, description="Nitrogen content in soil (N)")
    phosphorus: float = Field(..., ge=0, description="Phosphorus content in soil (P)")
    potassium: float = Field(..., ge=0, description="Potassium content in soil (K)")
    temperature: float = Field(..., ge=-20, le=60, description="Temperature in °C")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity in %")
    ph: float = Field(..., ge=0, le=14, description="pH value of the soil")
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")

class PredictResponse(BaseModel):
    recommended_crop: str
    confidence_score: float
    message: str
    top_3_predictions: List[str]
