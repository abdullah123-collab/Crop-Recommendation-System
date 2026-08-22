from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.schemas.disease import DiseaseResponse
from backend.services.disease_service import disease_service


router = APIRouter(
    prefix="/disease",
    tags=["disease"],
)


@router.post("/predict", response_model=DiseaseResponse)
async def predict_disease() -> DiseaseResponse | JSONResponse:
    response = disease_service.predict()
    if not response.model_available:
        return JSONResponse(status_code=503, content=response.model_dump())
    return response
