"""Detect endpoint for object detection.

Utiliza o modelo YOLO carregado globalmente para inferência sobre a imagem
enviada via UploadFile. Retorna JSON estruturado com detections.
Se não houver detecções, retorna array vazio sem imagem desenhada.
"""

import io
from typing import Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from PIL import Image

from app.models.yolo import CONF as DEFAULT_CONF, detector

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@router.post("/detect")
async def detect(
    file: UploadFile = File(...),
    conf: Optional[float] = Query(
        default=DEFAULT_CONF,
        ge=0.0,
        le=1.0,
        description="Confiança mínima do YOLO para filtrar detecções (default: 0.25)",
    ),
):
    """Detect objects in uploaded image using YOLO model.

    Returns JSON with status and detections array.
    Each detection has class_name, confidence, and box coordinates.

    Query parameter ``conf`` (default 0.25 / env CONF) defines the minimum
    confidence threshold. Deteções abaixo desse valor são filtradas.
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

    # Read and process image with YOLO
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Não foi possível processar a imagem: {exc}",
        )

    detections = detector.predict(image, conf_threshold=conf)

    # Format response without class_id (contract: class_name, confidence, box)
    formatted_detections = [
        {
            "class_name": d["class_name"],
            "confidence": d["confidence"],
            "box": d["box"],
        }
        for d in detections
    ]

    return {"status": "success", "detections": formatted_detections}
