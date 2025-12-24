import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException, status

from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_TYPES = {"image/png", "image/jpeg", "application/pdf"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    stored_name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, stored_name)

    with open(path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "stored_name": stored_name,
        "size": len(content),
        "content_type": file.content_type,
        "uploaded_by": current_user.email,
    }
