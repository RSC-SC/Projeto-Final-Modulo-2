"""YOLO model loader and inference wrapper for ScanVision.

Carrega um modelo da família YOLO (ultralytics) e expõe inferência
sobre imagens PIL, retornando detecções estruturadas.

Configurações via variáveis de ambiente:
- CONF: confiança mínima (default: 0.25)
- IOU: threshold de supressão não-máxima (default: 0.45)
- DEVICE: dispositivo inferência (auto/mps/cpu, default: auto)
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from PIL import Image
from ultralytics import YOLO

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "yolov8n.pt"
DEFAULT_CONF = 0.25
DEFAULT_IOU = 0.45

# Lê configurações do ambiente (fallback para valores padrão)
CONF = float(os.environ.get("CONF", DEFAULT_CONF))
IOU = float(os.environ.get("IOU", DEFAULT_IOU))
DEVICE = os.environ.get("DEVICE", "auto")


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

    def predict(self, image: Image.Image, conf_threshold: float = CONF) -> List[Dict[str, Any]]:
        """Executa inferência sobre uma imagem PIL e retorna detecções filtradas.

        Args:
            image: Imagem PIL.
            conf_threshold: Limiares de confiança mínimo; detecções abaixo desse valor
                são excluídas.
        """
        if not self._loaded or self.model is None:
            raise RuntimeError("YOLO model não carregado. Chame load() primeiro.")

        # Passar confiança para o inferidor YOLO (yolov8/ultralytics suporta conf)
        results = self.model.predict(
            image,
            conf=conf_threshold,
            device="cpu",
            classes=[39, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
            verbose=False
        )
        detections: List[Dict[str, Any]] = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                # Refiltrar via conf_threshold novamente (proteção extra)
                if conf < conf_threshold:
                    continue
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
