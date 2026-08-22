from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from backend.schemas.disease import DiseaseResponse
from backend.services.disease_service import disease_service
from backend.utils.config import CONFIG
from backend.utils.logger import logger


router = APIRouter(
    prefix="/disease",
    tags=["disease"],
)

SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {"code": code, "message": message},
        },
    )


@router.post("/predict", response_model=DiseaseResponse)
async def predict_disease(file: UploadFile = File(...)) -> DiseaseResponse | JSONResponse:
    if file.content_type not in SUPPORTED_IMAGE_TYPES:
        return error_response(
            "INVALID_IMAGE_TYPE",
            "Only JPEG, PNG, and WebP images are supported.",
            415,
        )

    max_size = int(CONFIG["MAX_IMAGE_SIZE_MB"] * 1024 * 1024)
    image_data = await file.read(max_size + 1)
    if len(image_data) > max_size:
        return error_response(
            "IMAGE_TOO_LARGE",
            f"Image size must not exceed {CONFIG['MAX_IMAGE_SIZE_MB']:g} MB.",
            413,
        )

    try:
        with Image.open(BytesIO(image_data)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError):
        return error_response(
            "INVALID_IMAGE",
            "The uploaded file is not a valid image.",
            400,
        )

    response = disease_service.predict(image_data)
    if not response.model_available:
        return JSONResponse(status_code=503, content=response.model_dump())
    return response
