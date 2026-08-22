from pathlib import Path
from typing import Any, Optional

from backend.schemas.disease import DiseaseResponse
from backend.utils.config import CONFIG
from backend.utils.logger import logger


class DiseaseService:
    def __init__(self, model_path: Optional[str] = None) -> None:
        configured_path = model_path or CONFIG["DISEASE_MODEL_PATH"]
        path = Path(configured_path)
        self.model_path = path if path.is_absolute() else Path(__file__).resolve().parents[2] / path
        self.model: Optional[Any] = None

    @property
    def model_available(self) -> bool:
        return self.model is not None or self.model_path.is_file()

    def load_model(self) -> bool:
        if not self.model_path.is_file():
            logger.info("Disease model is not available")
            return False

        return False

    def predict(self, image: Any = None) -> DiseaseResponse:
        if not self.model_available and not self.load_model():
            return DiseaseResponse(
                success=False,
                model_available=False,
                error={
                    "code": "MODEL_UNAVAILABLE",
                    "message": "Disease analysis model is not available yet.",
                },
            )

        raise NotImplementedError("Disease inference is not implemented yet")


disease_service = DiseaseService()
