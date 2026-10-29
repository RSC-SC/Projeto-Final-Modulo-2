# ScanVision — Detecção de Objetos em Imagens de Supermercado

> **Autor:** Rafael · **Curso:** SCTEC — Módulo 2 (Machine Learning e Visão Computacional)
> **Nome do software:** `ScanVision` — detecta produtos em imagens de supermercado.
> **Repositório:** <https://github.com/RSC-SC/Projeto-Final-Modulo-2>
> **Kanban:** <https://github.com/users/RSC-SC/projects/8>

Sistema backend-only de detecção de objetos: um modelo **YOLOv8n** identifica produtos em
imagens e devolve as caixas delimitadoras em **JSON**, consumíveis por qualquer
front-end ou sistema de PDV/estoque.

## Dataset e classes

**Fonte:** COCO 2017 (`val2017`), conjunto de anotações do COCO — licença
[CC BY 4.0](https://cocodataset.org/#termsofuse).

**Preparação própria** (`scripts/prepare_coco_subset.py`): filtramos apenas as imagens
que contêm ao menos uma das **13 classes** abaixo, descartamos anotações fora da
seleção, fizemos split `train/val/test` (70/15/15) **sem vazamento** (semente 42) e
generamos o `data.yaml` (`data/coco-subset/data.yaml`) + relatório
(`data/coco-subset/dataset_report.md`).

| ID (COCO) | Classe | Imagens | Instâncias |
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

**Totais:** 1.160 imagens · 5.323 instâncias · split `train` 812 · `val` 174 · `test` 174
(interseção entre splits = 0 — **sem vazamento**).

> **Por que preservar os IDs do COCO?** O modelo pré-treinado (`yolov8n.pt`) retorna o ID
da classe na posição original (0..79). Remapear para 0..12 faria o `yolo val`
comparar classes erradas e produzir métricas falsas. O `data.yaml` mantém os IDs
originais.

## Justificativa da arquitetura (por que YOLOv8n)

- **As 13 classes já existem no COCO** (IDs 39–55, região "comida/mesa"), portanto o
modelo pré-treinado as reconhece **sem nenhum treino** — garante que ele
"reconheça as 10+ classes com clareza" logo de cara (critério 7 da rubrica).
- **`yolov8n` é o menor da família** (≈5,6 MB): carrega em <1 s, roda em MPS (Apple
Silicon) ou CPU e mantém latência baixa da API.
- Trabalho **individual** (não squad): não há tabela de benchmark entre versões;
se fosse squad, compararia `yolov8n/s/m` com mAP e velocidade.

## Avaliação (resultados medidos)

Executado via `TestClient` (FastAPI) sobre imagens reais do split `test` (`data/coco-subset/images/test/`):

| Ponto de operação | Precisão | Recall | F1 | Classes detectadas |
|---|---|---|---|---|
| `conf=0.25` (padrão da API) | **0,70*** | **0,42*** | **0,52*** | **13/13** |

\* Medido manualmente sobre amostra do split de teste (`000000441491.jpg` e outras)
com `conf=0.25`, `iou=0.45`, `device=auto` (MPS), escopo das 13 classes, casamento
`IoU ≥ 0,5`. Relatório completo reproduzível via `python scripts/evaluate.py`.

**Generalização (imagens fora do COCO):** baixamos imagens do Wikimedia Commons
(2–4 por classe, licenças livres registradas em `examples/external/ATTRIBUICAO.md`).
Todas as 13 classes foram detectadas em pelo menos uma imagem externa.

## Requisitos

- macOS com Apple Silicon (testado em M5 Pro, 24 GB) — funciona também Linux/Windows com CPU.
- **Python 3.12** obrigatório (`torch` ainda não publica wheel para `cp315`).
- ~2 GB de espaço livres (dataset + pesos `yolov8n.pt`).

## Instalação

```bash
# 1. clonar
git clone https://github.com/RSC-SC/Projeto-Final-Modulo-2.git
cd Projeto-Final-Modulo-2

# 2. ambiente virtual com Python 3.12
python3.12 -m venv .venv
source .venv/bin/activate

# 3. dependências (versões fixadas)
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
- `httpx==0.27.2`

## Preparação do dataset

```bash
# baixa (~1 GB) e processa — pode ser retomado se interromper
python scripts/prepare_coco_subset.py --download
```

Saída: `data/coco-subset/` com `images/{train,val,test}`, `labels/{train,val,test}`,
`data.yaml` e `dataset_report.md`.

## Execução da API

```bash
uvicorn main:app --reload --port 8000
```

- Swagger UI: <http://localhost:8000/docs>
- Redoc: <http://localhost:8000/redoc>
- Raiz (`GET /`): info da API
- Health (`/health`): status do serviço

Os pesos `yolov8n.pt` (~5,6 MB) são baixados automaticamente na primeira subida.

## Interface de demonstração (frontend)

O enunciado exige API que devolve **JSON puro** — nada de imagem desenhada no
backend. Para facilitar o vídeo demonstrativo (F6-02), o repositório inclui uma
página estática simples em `demo/frontend/index.html` (HTML + CSS + JS, sem
build):

```bash
uvicorn main:app --reload
# abra http://localhost:8000/  (frontend servido pelo mount estático)
```

Fluxo:

1. Arraste/escolha uma imagem;
2. O navegador envia `multipart/form-data` para `POST /detect`;
3. Com o JSON, o `<canvas>` desenha as caixas **no cliente** (cada classe recebe
cor determinística + rótulo `classe + confiança`);
4. Exibe também a tabela de detecções e o JSON bruto.

Campo "Endpoint" permite apontar para outra instância (ex.: container remoto).
Se servido por outro host, habilite `CORS_ORIGINS` (veja abaixo).

> As rotas da API (`/detect`, `/docs`) são registradas **antes** do mount estático,
> portanto não são sombreadas pelo frontend.

## Payload de exemplo

**Requisição** (Swagger/Postman/cURL):

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -F "file=@data/coco-subset/images/test/000000441491.jpg"
```

**Resposta real (contrato — sem imagem desenhada):**

```json
{
  "status": "success",
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.7684,
      "box": { "x_min": 0.0, "y_min": 0.64, "x_max": 426.71, "y_max": 479.56 }
    },
    {
      "class_name": "cup",
      "confidence": 0.2775,
      "box": { "x_min": 341.3, "y_min": 399.64, "x_max": 430.64, "y_max": 479.77 }
    }
  ]
}
```

**Caso vazio:** `{"status":"success","detections":[]}`  
**Erro 415:** arquivo não imagem / content-type inadequado  
**Erro 400:** parâmetro `file` ausente  
**Erro 422:** imagem corrompida / dimensões inválidas  
**Erro 500:** falha interna (modelo não carregado / inferência crash).

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `MODEL_PATH` | `yolov8n.pt` | pesos (pode usar `best.pt` após fine-tuning) |
| `CONF` | `0.25` | confiança mínima |
| `IOU` | `0.45` | IoU da supressão de não-máximos |
| `DEVICE` | `auto` | `auto` (MPS se disponível) · `mps` · `cpu` |
| `SCOPE` | `dataset` | `dataset` = só 13 classes · `all` = 80 COCO |
| `MAX_UPLOAD_MB` | `10` | limite do upload |
| `CORS_ORIGINS` | _(vazio)_ | origens liberadas para CORS (ex.: `http://localhost:5500`) |

## Testes automatizados

```bash
pytest                 # 18 testes (contrato JSON, filtros, erros, inferência)
pytest -m integration  # só os que carregam modelo real
```

Cobrem: contrato JSON exato, filtros de escopo, content-type inválido, bytes que
não são imagem, arquivo vazio, limite de tamanho, modelo não carregado, imagem sem
detecções e caminho completo de inferência com modelo real.

## Fine-tuning (opcional — bônus)

Não é necessário para entrega (enunciado aceita modelo pré-treinado). Se quiser:

```bash
python scripts/train.py --epochs 30
MODEL_PATH=runs/detect/scanvision/weights/best.pt uvicorn main:app --reload
```

## Estrutura do projeto

```
.
├── main.py                  # FastAPI + mount do frontend
├── app/
│   ├── api/routes/detect.py # POST /detect (YOLO integrado)
│   ├── models/yolo.py       # YOLODetector (load + predict)
│   └── ...
├── frontend/                # demo estática (HTML/CSS/JS) — serve em /
├── scripts/
│   ├── prepare_coco_subset.py
│   ├── evaluate.py
│   ├── fetch_external.py
│   ├── demo_payload.py
│   └── train.py
├── data/                    # dataset (gitignorado)
├── docs/                    # roteiro, Kanban, evidências (F0-F5)
└── requirements.txt
```

## GitFlow (branches)

| Branch | Uso |
|---|---|
| `main` | entrega final (tudo mergeado ao final) |
| `develop` | integração das features |
| `feature/3-configurar-ambiente-estrutura` | F1-01 |
| `feature/4-preparar-dataset-coco-val2017` | F1-02 |
| `feature/5-declarar-nao-aplicavel-frontend` | F2-01 |
| `feature/6-criar-aplicacao-fastapi-base` | F3-01 |
| `feature/7-implementar-endpoint-detect-uploadfile` | F3-02 |
| `feature/8-carregar-modelo-yolo-inferencia` | F4-01 |
| `feature/9-retornar-json-estruturado` | F4-02 |
| `feature/10-validar-contrato-json-testes-manual` | F5-01 |
| `feature/11-atualizar-readme` | F6-01 |
| `feature/13-demonstracao-frontend-api` | F6-01 (demo) |

Commits no padrão `tipo(escopo): descrição` (ex.: `feat(api): adiciona endpoint /detect`).

## Kanban

Quadro público no GitHub Project (#8) com as 6 colunas obrigatórias:
**Backlog · Todo · Doing · Blocked · Review · Done**.

Todos os cards fizeram transições manuais conforme fluxo (início, handover PR,
finalização). Evidências: comentários nas issues (#7 a #13) e atualizações no
`docs/estado-projeto.md`.

Link: <https://github.com/users/RSC-SC/projects/8>

## Créditos e licença

- Dataset: COCO 2017 (Microsoft) — [CC BY 4.0](https://cocodataset.org/#termsofuse).
- Modelo: [Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8/) (AGPL-3.0).
- Referências externas: `examples/external/ATTRIBUICAO.md` (Wikimedia Commons, livre).
