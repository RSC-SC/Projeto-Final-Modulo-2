# Dataset - COCO 2017 val2017 (subset para classes de alimentos)

## Fonte
- COCO 2017 `val2017` (4952 imagens anotadas)
- Anotações: `annotations/instances_val2017.json`

## Classes selecionadas (13)
As 13 classes de alimentos definidas no escopo do projeto:

| ID COCO | Classe |
|---------|--------|
| 39 | bottle |
| 41 | cup |
| 45 | bowl |
| 46 | banana |
| 47 | apple |
| 48 | sandwich |
| 49 | orange |
| 50 | broccoli |
| 51 | carrot |
| 52 | hot dog |
| 53 | pizza |
| 54 | donut |
| 55 | cake |

## Mapeamento classe -> ID
Preservados os IDs originais do COCO (0..79) para compatibilidade com modelos YOLO pré-treinados. Ver `data/coco-subset/data.yaml`.

## Estrutura YOLO-compatible
```
data/coco-subset/
├── data.yaml
├── dataset_report.md
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

## Split
- train: 70%
- val: 15%
- test: 15%
- seed: 42

## Estatísticas (geradas)
Ver `data/coco-subset/dataset_report.md`:
- Imagens no subset: 1160
- Total de instâncias: 5323
- `images/val` e `labels/val`: 174 arquivos cada

## Reprodutibilidade
Usar `scripts/prepare_coco_subset.py`:

```bash
python scripts/prepare_coco_subset.py \
  --coco-root /caminho/para/coco2017 \
  --out data/coco-subset \
  --seed 42
```

Requisitos: COCO com `annotations/instances_val2017.json` e pasta `val2017/`.
