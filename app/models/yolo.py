"""YOLO model loader and inference wrapper for ScanVision.

Carrega um modelo da família YOLO (ultralytics) e expõe inferência
sobre imagens PIL, retornando detecções estruturadas.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from PIL import Image
from ultralytics import YOLO

logger = logging.getLogger(__name__)

# Modelo padrão: YOLOv8 nano (pré-treinado no COCO, inclui as 13 classes de
# alimentos alvo). O arquivo de pesos é baixado automaticamente na primeira
# execução caso não exista localmente.
DEFAULT_MODEL_NAME = "yolov8n.pt"


class YOLODetector:
    """Wrapper around ultralytics YOLO para detecção de objetos."""

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        self.model_name = model_name
        self.model: Optional[YOLO] = None
        self._loaded = False

    def load(self) -> None:
        """Carrega o modelo YOLO em memória."""
        if self._loaded:
            logger.info("YOLO model já carregado: %s", self.model_name)
            return
        logger.info("Carregando modelo YOLO: %s", self.model_name)
        self.model = YOLO(self.model_name)
        self._loaded = True
        logger.info("Modelo YOLO carregado com sucesso: %s", self.model_name)

    def predict(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Executa inferência sobre uma imagem PIL e retorna detecções."""
        if not self._loaded or self.model is None:
            raise RuntimeError("YOLO model não carregado. Chame load() primeiro.")

        results = self.model(image)
        detections: List[Dict[str, Any]] = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                detections.append(
                    {
                        "class_id": cls_id,
                        "class_name": self.model.names[cls_id],
                        "confidence": round(conf, 4),
                        "box": {
                            "x_min": round(float(xyxy[0]), 2),
                            "y_min": round(float(xyxy[1]), 2),
                            "x_max": round(float(xyxy[2]), 2),
                            "y_max": round(float(xyxy[3]), 2),
                        },
                    }
                )

        return detections

    def is_loaded(self) -> bool:
        return self._loaded


# Instância singleton usada pelo restante da aplicação.
detector = YOLODetector()
