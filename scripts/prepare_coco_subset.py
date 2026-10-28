#!/usr/bin/env python3
"""
Prepara subset YOLO a partir do COCO 2017 val2017 filtrando apenas
as 13 classes de alimentos definidas no escopo do projeto.

Classes alvo:
bottle, cup, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

Mapeamento preserva IDs originais do COCO (0..79) para compatibilidade com modelo pré-treinado.
"""

import argparse
import json
import os
import random
import shutil
from pathlib import Path

TARGET_CLASSES = {
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

def main():
    parser = argparse.ArgumentParser(description="Preparar subset COCO val2017 para classes de alimentos")
    parser.add_argument("--coco-root", required=True, help="Raiz do COCO (com annotations/instances_val2017.json e val2017/)")
    parser.add_argument("--out", required=True, help="Diretório de saída (ex: data/coco-subset)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--val", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    args = parser.parse_args()

    random.seed(args.seed)
    coco_root = Path(args.coco_root)
    out = Path(args.out)

    ann_path = coco_root / "annotations" / "instances_val2017.json"
    img_dir = coco_root / "val2017"

    with open(ann_path) as f:
        coco = json.load(f)

    images_by_id = {img["id"]: img for img in coco["images"]}
    anns_by_img = {}
    for ann in coco["annotations"]:
        if ann["category_id"] in TARGET_CLASSES:
            anns_by_img.setdefault(ann["image_id"], []).append(ann)

    img_ids = list(anns_by_img.keys())
    random.shuffle(img_ids)

    n = len(img_ids)
    n_train = int(n * args.train)
    n_val = int(n * args.val)
    splits = {
        "train": img_ids[:n_train],
        "val": img_ids[n_train:n_train + n_val],
        "test": img_ids[n_train + n_val:],
    }

    for split in ["train", "val", "test"]:
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)

    for split, ids in splits.items():
        for img_id in ids:
            img = images_by_id[img_id]
            src_img = img_dir / img["file_name"]
            dst_img = out / "images" / split / img["file_name"]
            if src_img.exists():
                shutil.copy2(src_img, dst_img)

            w, h = img["width"], img["height"]
            label_path = out / "labels" / split / (Path(img["file_name"]).stem + ".txt")
            lines = []
            for ann in anns_by_img[img_id]:
                cat_id = ann["category_id"]
                x, y, bw, bh = ann["bbox"]
                xc = (x + bw / 2) / w
                yc = (y + bh / 2) / h
                nw = bw / w
                nh = bh / h
                lines.append(f"{cat_id} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}")
            label_path.write_text("\n".join(lines) + "\n")

    print(f"Subset gerado em {out}")
    print(f"Imagens: train={len(splits['train'])}, val={len(splits['val'])}, test={len(splits['test'])}")

if __name__ == "__main__":
    main()
