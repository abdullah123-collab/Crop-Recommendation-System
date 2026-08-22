import os

from dotenv import load_dotenv


load_dotenv()

CONFIG = {
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
}
