from fastapi import APIRouter
from backend.schemas.crop import PredictRequest, PredictResponse
from backend.services.crop_service import crop_service

router = APIRouter(
    prefix="/crop",
    tags=["crop"]
)

@router.post("/predict", response_model=PredictResponse)
def predict_crop(data: PredictRequest):
    # Delegate inference logic to the crop_service
    prediction_result = crop_service.predict(data)
    return PredictResponse(**prediction_result)
