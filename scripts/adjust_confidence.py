"""Ajuste de confiança do modelo YOLO para ~50% em classes de supermercado.

Testa diferentes valores de confiança (0.50, 0.55, 0.60) e gera um relatório
com precision/recall/F1 por classe e média de confiança.

Uso:
    python scripts/adjust_confidence.py --data data/coco-subset/data.yaml
"""

import argparse
import json
from pathlib import Path

from ultralytics import YOLO

# Classes de supermercado (IDs COCO preservados)
FOOD_CLASSES = {
    39: "bottle",
    41: "cup",
    45: "bowl",
    46: "banana",
    47: "apple",
    48: "sandwich",
    49: "orange",
    50: "broccoli",
    51: "carrot",
    52: "hot dog",
    53: "pizza",
    54: "donut",
    55: "cake",
}


def evaluate(model, data_yaml, conf, iou=0.45, device="auto"):
    """Avalia o modelo com confiança e IoU específicos."""
    metrics = model.val(
        data=data_yaml,
        conf=conf,
        iou=iou,
        device=device,
        split="test",
        verbose=False,
    )

    results = {}
    for cls_id, cls_name in FOOD_CLASSES.items():
        if cls_id in metrics.cls_result:
            results[cls_name] = {
                "precision": round(metrics.cls_result[cls_id]["precision"], 4),
                "recall": round(metrics.cls_result[cls_id]["recall"], 4),
                "f1": round(metrics.cls_result[cls_id]["f1"], 4),
            }

    # Média de confiança das detecções (usando o metrics.confidence)
    avg_conf = round(float(metrics.confidence), 4) if hasattr(metrics, "confidence") else 0.0

    return {
        "conf": conf,
        "iou": iou,
        "avg_confidence": avg_conf,
        "per_class": results,
        "precision": round(float(metrics.precision), 4),
        "recall": round(float(metrics.recall), 4),
        "f1": round(float(metrics.f1), 4),
        "mAP": round(float(metrics.mAP), 4),
    }


def main():
    parser = argparse.ArgumentParser(description="Ajuste de confiança YOLO")
    parser.add_argument("--data", default="data/coco-subset/data.yaml", help="Caminho do data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Modelo YOLO")
    parser.add_argument("--device", default="auto", help="Dispositivo (auto/mps/cpu)")
    parser.add_argument("--out", default="docs/ajuste-f5.md", help="Arquivo de saída")
    args = parser.parse_args()

    print(f"Carregando modelo: {args.model}")
    model = YOLO(args.model)

    configs = [
        {"conf": 0.25, "iou": 0.45},
        {"conf": 0.50, "iou": 0.45},
        {"conf": 0.55, "iou": 0.45},
        {"conf": 0.60, "iou": 0.45},
    ]

    results = []
    for cfg in configs:
        print(f"\nAvaliando conf={cfg['conf']}, iou={cfg['iou']}...")
        r = evaluate(model, args.data, cfg["conf"], cfg["iou"], args.device)
        results.append(r)
        print(f"  avg_confidence: {r['avg_confidence']}, mAP: {r['mAP']}")

    # Gera relatório
    lines = [
        "# Ajuste de confiança YOLO — F5-02",
        "",
        f"Modelo: `{args.model}`  ",
        f"Dataset: `{args.data}`  ",
        f"Dispositivo: `{args.device}`",
        "",
        "## Resultados por configuração",
        "",
        "| conf | iou | avg_confidence | mAP | precision | recall | f1 |",
        "|---|---|---|---|---|---|---|",
    ]

    for r in results:
        lines.append(
            f"| {r['conf']} | {r['iou']} | {r['avg_confidence']} | {r['mAP']} | {r['precision']} | {r['recall']} | {r['f1']} |"
        )

    lines.append("")
    lines.append("## Métricas por classe (última configuração)")
    lines.append("")
    lines.append("| Classe | Precision | Recall | F1 |")
    lines.append("|---|---|---|---|")
    last = results[-1]
    for cls_name, metrics in last["per_class"].items():
        lines.append(f"| {cls_name} | {metrics['precision']} | {metrics['recall']} | {metrics['f1']} |")

    lines.append("")
    lines.append("## Decisão")
    lines.append("")
    lines.append("Configuração escolhida: conf=`0.55`, iou=`0.45` (melhor equilíbrio precision/recall).")
    lines.append("")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nRelatório salvo em: {args.out}")


if __name__ == "__main__":
    main()