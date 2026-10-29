"""Detect endpoint for object detection."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

router = APIRouter()


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    """Detect objects in uploaded image.

    This endpoint currently returns a stub response as specified in F3-02.
    Full YOLO inference will be implemented in F4.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetro 'file' obrigatório não enviado.",
        )

    # Validate extension
    filename_lower = file.filename.lower()
    if not any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Tipo de arquivo não suportado.",
        )

    # Validate content type
    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Tipo de arquivo não suportado.",
        )

    # For now, return stub response as per F3-02 requirements
    # Full YOLO inference will be implemented in F4-01
    return {"status": "success", "detections": []}
