import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "test-secret-key")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))

# Valeur par défaut POUR LES TESTS
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)
