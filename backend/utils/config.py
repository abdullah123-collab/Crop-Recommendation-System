import os

from dotenv import load_dotenv


load_dotenv()

CONFIG = {
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
    "DISEASE_MODEL_PATH": os.getenv("DISEASE_MODEL_PATH", "models/disease/disease_model.pt"),
    "DISEASE_MODEL_TYPE": os.getenv("DISEASE_MODEL_TYPE", "none"),
    "MAX_IMAGE_SIZE_MB": float(os.getenv("MAX_IMAGE_SIZE_MB", "5")),
}
