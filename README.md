# ScanVision — Detecção de Alimentos de Supermercado (COCO 2017 val2017)

> **Projeto Final — Módulo 2 — SCTEC — Machine Learning e Visão Computacional**
> **Responsável:** Rafael  
> **Prazo:** 03/11/2026  
> **Repositório:** https://github.com/RSC-SC/Projeto-Final-Modulo-2  
> **Kanban:** https://github.com/users/RSC-SC/projects/8

## Objetivo

Detectar objetos (foco em alimentos de supermercado) em imagens utilizando modelo YOLO, com retorno exclusivamente em JSON estruturado (sem imagem desenhada).

## Dataset

- **COCO 2017** (`val2017`)
- **13 classes de alimentos** selecionadas: bottle, cup, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
- Todas presentes e validadas no COCO 2017

## Arquitetura

- **Modelo:** YOLOv8 nano (`yolov8n.pt`) — pré-treinado no COCO (80 classes), carregado via `ultralytics`
- **API:** FastAPI (`main:app`) com endpoint `POST /detect`
- **Inferência:** `app/models/yolo.py` (`YOLODetector.load()` / `.predict()`)
- **Formato de retorno:** apenas JSON (`status`, `detections` com `class_name`, `confidence`, `box` {x_min, y_min, x_max, y_max})
- **Sem imagem desenhada / sem base64**

## Instalação

```bash
# Criar ambiente
python -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt
```

Principais pacotes (`requirements.txt`):
- `fastapi==0.115.0`
- `uvicorn[standard]==0.30.6`
- `python-multipart==0.0.12`
- `ultralytics==8.3.28`
- `torch>=2.3.0`
- `pillow==10.4.0`
- `numpy==1.26.4`

## Execução

```bash
uvicorn main:app --reload --port 8000
```

- **Swagger:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc
- **Root:** `GET /`

## Endpoint de Detecção

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -F "file=@imagem.jpg"
```

### Exemplo de Payload (Sucesso)

```json
{
  "status": "success",
  "detections": [
    {
      "class_name": "banana",
      "confidence": 0.92,
      "box": {
        "x_min": 120,
        "y_min": 80,
        "x_max": 240,
        "y_max": 200
      }
    }
  ]
}
```

### Caso Sem Detecções

```json
{"status": "success", "detections": []}
```

### Códigos de Erro (Contratos Padronizados)

| HTTP | Código | Situação |
|---|---|---|
| 400 | `BAD_REQUEST` | Arquivo `file` ausente |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Tipo/extensão não suportado |
| 422 | `UNPROCESSABLE_ENTITY` | Imagem inválida / corrompida |
| 500 | `INTERNAL_SERVER_ERROR` | Falha interna (modelo/inferência) |

Todos os erros seguem `{"status":"error","error":{"code":"...","message":"...","hint":"..."}}`.

## Estrutura do Projeto (GitFlow)

```text
main/              ← release final
  └── develop/     ← integração (merge das features)
        ├── feature/6-criar-aplicacao-fastapi-base
        ├── feature/7-implementar-endpoint-detect-uploadfile
        ├── feature/8-carregar-modelo-yolo-inferencia
        ├── feature/9-retornar-json-estruturado
        └── feature/10-validar-contrato-json-testes-manual
```

## Evidências / Rastros

- **F0 (Escopo):** `docs/f0/plano-issues-f1-f6.md`, `docs/f0/prd.md`, `docs/f0/user-stories.md`
- **F1 (Dados):** `scripts/prepare_coco_subset.py`, `data/coco-subset/`
- **F2 (N/A):** `docs/f2/nao-aplicavel-frontend.md`
- **F3 (API):** `app/main.py`, `app/api/routes/detect.py`
- **F4 (YOLO):** `app/models/yolo.py`, `docs/f4/evidencia-f4-02.md`
- **F5 (Testes):** `docs/f5/evidencia-f5-01.md`
- **Estado:** `docs/estado-projeto.md` (atualizado a cada gate)

## Entrega

- **Submissão:** GitHub `main` + PR final + vídeo demonstrativo (≤7 min)
- **Documentação completa:** este README + `docs/estado-projeto.md`
