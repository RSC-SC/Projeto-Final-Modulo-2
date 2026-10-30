# [F5-02] Ajuste de confiança YOLO para ~50% em classes de supermercado

## Objetivo
Ajustar hiperparâmetros/confiança do modelo YOLO (`yolov8n.pt`) para atingir aproximadamente **50% de confiança média** nas classes problemáticas do dataset COCO 2017 `val2017` (ex.: `hot dog`, `donut`, `bowl`, `cup`, `bottle`), sem prejudicar o desempenho das demais 13 classes.

## Contexto
O modelo atual (`yolov8n.pt`) detecta com confiança frequentemente >80% para várias classes. Em um cenário realista de self-checkout, sobreconfiança leva a falsos positivos. A meta de ~50% equilibra precisão e recall para itens de supermercado.

## Escopo técnico

- **Branch:** `feature/26-ajuste-confianca-yolo-50` (base: `develop`)
- **Modelo:** `yolov8n.pt` (Ultralytics YOLO v8n, pré-treinado COCO)
- **Framework:** `ultralytics==8.3.28`
- **Arquivos principais:** `app/models/yolo.py`, `app/main.py`, `scripts/evaluate.py` (ou `scripts/adjust.py` se criado)
- **Dataset:** `data/coco-subset/` (`data.yaml` com IDs COCO preservados: 39 bottle, 41 cup, 45 bowl, 46 banana, 47 apple, 48 sandwich, 49 orange, 50 broccoli, 51 carrot, 52 hot dog, 53 pizza, 54 donut, 55 cake)

### Hiperparâmetros a testar
| Parâmetro | Valor atual | Teste |
|---|---|---|
| `conf` (threshold) | 0.25 (API) / 0.45 (interna) | 0.50, 0.55, 0.60 |
| `iou` (NMS) | 0.45 | 0.45, 0.50, 0.55 |
| `augment` | false | true (se necessário) |
| `device` | `auto` (MPS) | `mps`, `cpu` (fallback) |

### Métricas de avaliação
- **Por classe:** `precision`, `recall`, `f1`, `confidence` média
- **Global:** média de `confidence` das 13 classes
- **Sucesso:** `confidence` média ≥ 50% para ≥ 3 das 13 classes, sem regredir >10% nas demais
- **Contratação:** `POST /detect` continua retornando `200` com JSON válido (`docs/f4/evidencia-f4-02.md`)

## Evidências
- Antes/depois: `docs/f4/evidencia-f4-02.md` (atualizar com iterações)
- Avaliação completa: `docs/f5/evidencia-f5-01.md`
- Registro de iterações: `docs/ajuste-f5.md` (novo)
- Script de avaliação: `scripts/evaluate.py` (ou `scripts/adjust.py` se criado)

## Critérios de aceite
1. PR aprovada (`feature/26-ajuste-confianca-yolo-50` → `develop`)
2. `docs/ajuste-f5.md` com tabela antes/depois
3. `docs/estado-projeto.md` atualizado
4. Nenhum `git revert` necessário — ajuste finalizado em uma única iteração documentada ou com registro claro das tentativas
5. API `/detect` continua funcionando (`200`, JSON estruturado, sem imagem desenhada)

## Dependências
- F4-01 (#8) — YOLO integrado (`DONE`)
- F4-02 (#9) — JSON estruturado (`DONE`)
- F5-01 (#10) — Contrato validado (`DONE`)
- F5-02 (#10/ajuste) — esta tarefa (em desenvolvimento)

## Labels
`fase-5`, `tipo-task`, `modelo`, `ajuste`, `confiança`

---
*Refs #8, #9, #10*
