from fastapi import Depends, FastAPI

from app.auth import router as auth_router
from app.database import Base, engine
from app.dependencies import get_current_user
from app.models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure File Upload API")
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}
