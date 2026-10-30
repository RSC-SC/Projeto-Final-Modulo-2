# Relatório do dataset (supermercado / COCO subset)

- Fonte: COCO 2017 `val2017` (4952 imagens anotadas no total)
- Classes selecionadas: 13
- Imagens no subset: 1160 (extraídas: 1160)
- Split: train 70% / val 15% / test 15% (seed 42)
- IDs de classe: preservados do COCO (0..79) para compatibilidade com o modelo pré-treinado

| ID | Classe | Imagens | Instâncias |
|---|---|---|---|
| 39 | bottle | 379 | 1013 |
| 41 | cup | 390 | 895 |
| 45 | bowl | 314 | 623 |
| 46 | banana | 103 | 370 |
| 47 | apple | 76 | 236 |
| 48 | sandwich | 98 | 177 |
| 49 | orange | 85 | 285 |
| 50 | broccoli | 71 | 312 |
| 51 | carrot | 81 | 365 |
| 52 | hot dog | 51 | 125 |
| 53 | pizza | 153 | 284 |
| 54 | donut | 62 | 328 |
| 55 | cake | 124 | 310 |

**Total de instâncias**: 5323

Gerado por `scripts/prepare_dataset.py` — não editar manualmente.
