# Roteiro de Apresentação — ScanVision (Vídeo ≤ 7 min)

**Projeto:** ScanVision — Detecção de Objetos em Imagens de Supermercado  
**Curso:** SCTEC — Módulo 2  
**Responsável:** Rafael  
**Prazo:** 03/11/2026  
**Repositório:** https://github.com/RSC-SC/Projeto-Final-Modulo-2  
**Kanban:** https://github.com/users/RSC-SC/projects/8

---

## Slide 1 — Título e Identificação
- Nome: ScanVision
- Tipo: Backend-only (FastAPI + YOLOv8n)
- Dataset: COCO 2017 val2017 (13 classes de alimentos)
- Repositório / Kanban

---

## Slide 2 — Dataset e Objetivo (requisito 1 do vídeo)
**Pergunta:** Qual dataset e objetivo?

- **Fonte:** COCO 2017 (`val2017`)
- **13 classes selecionadas:** bottle, cup, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
- **Objetivo:** detectar produtos em imagens de supermercado e retornar JSON com detecções (sem imagem desenhada no backend)
- **Justificativa:** todas as 13 classes existem no COCO; o `yolo11n` (no nosso caso `yolov8n`) as reconhece sem fine-tuning
- **Tabela (mostrar):** classe, ID COCO, nº imagens, nº instâncias (do `dataset_report.md`)

---

## Slide 3 — Arquitetura YOLO (requisito 2 do vídeo — parte 1)
**Pergunta:** Como foi o processo YOLO?

- Modelo: `yolov8n.pt` (família YOLOv8, nano, pré-treinado em COCO 80 classes)
- Por que `v8n`: menor tamanho (~5,6 MB), carrega rápido, roda em MPS/CPU
- Não foi feito fine-tuning (aceito pelo enunciado); o modelo já reconhece as 13 classes diretamente
- Integração: `app/models/yolo.py` (`YOLODetector.load()` + `.predict()`)
- Benchmark: solo → não há tabela comparativa de squad; mas evidência de detecção das 13 classes confirmada
- Generalização: testado com `data/coco-subset/images/test/` (imagens do split) e `examples/external/ATTRIBUICAO.md` (38 imagens externas do Wikimedia Commons) — 13/13 classes detectadas

---

## Slide 4 — Demonstração da API (requisito 2 do vídeo — parte 2)
**Pergunta:** Demonstração do funcionamento.

Passos a mostrar no vídeo:

1. Subir o serviço: `uvicorn main:app --reload --port 8000`
2. Abrir `http://localhost:8000/docs` (Swagger) ou usar `curl`
3. Fazer upload da imagem `data/coco-subset/images/test/000000441491.jpg`
4. Mostrar a resposta JSON com `detections`, `class_name`, `confidence`, `box`
5. Mostrar também o frontend (`http://localhost:8000/`): upload → desenho das caixas no `<canvas>` + tabela + JSON

**Exemplo de resposta (mostrar):**

```json
{
  "status": "success",
  "detections": [
    {"class_name":"person","confidence":0.7684,"box":{"x_min":0,"y_min":0.64,"x_max":426.71,"y_max":479.56}},
    {"class_name":"cup","confidence":0.2775,"box":{"x_min":341.3,"y_min":399.64,"x_max":430.64,"y_max":479.77}}
  ]
}
```

---

## Slide 5 — Testes do Dataset (requisito 3 do vídeo)
**Pergunta:** Mostrar os testes.

- Teste manual com `TestClient` (`tests/`): contrato JSON (200, 415, 422, 400), filtros de conteúdo, arquivo vazio, limite de tamanho, inferência real com modelo
- Teste com imagem real (`000000441491.jpg`): 4 detecções (`person`, `cup`)
- Teste com imagem sem detecções: retorna `{"status":"success","detections":[]}`
- Teste de generalização: `docs/f4/evidencia-f4-02.md` (testado com COCO val2017) + `docs/f5/evidencia-f5-01.md` (teste manual completo)
- Nenhuma imagem desenhada no backend (contrato respeitado)

---

## Slide 6 — Kanban / Tarefas (requisito 4 do vídeo)
**Pergunta:** Como organizou as tarefas?

- Board: GitHub Project v2 (`https://github.com/users/RSC-SC/projects/8`)
- Colunas canônicas: `Backlog · Todo · Doing · Blocked · Review · Done`
- Cards criados para cada fase: F0 (escopo), F1 (dataset/preparação), F2 (N/A frontend), F3 (API base + endpoint), F4 (YOLO + JSON), F5 (testes), F6 (README + vídeo)
- Cada card tem: nome (`#n`), especificações (`feature/n-...`), rastreabilidade (`Refs #n`), comentários nas issues
- Movimento: todas as tarefas passaram por `DOING` → `REVIEW` → `DONE` conforme fluxo obrigatório

---

## Slide 7 — GitFlow / Branches (requisito 5 do vídeo)
**Pergunta:** Quais branches e objetivos?

| Branch | Issue / Fase | Objetivo |
|---|---|---|
| `main` | Entrega final | Código final mergeado |
| `develop` | Integração | Base para merges das features |
| `feature/3-...` | F1-01 | Configuração inicial |
| `feature/4-...` | F1-02 | Dataset COCO val2017 (13 classes) |
| `feature/5-...` | F2-01 | N/A — declaração formal |
| `feature/6-...` | F3-01 | FastAPI base |
| `feature/7-...` | F3-02 | Endpoint `POST /detect` |
| `feature/8-...` | F4-01 | Modelo YOLO integrado |
| `feature/9-...` | F4-02 | JSON estruturado (sem imagem) |
| `feature/10-...` | F5-01 | Testes e validação do contrato |
| `feature/11-...` | F6-01 | README completo |
| `feature/13-...` | #22 (demo) | Frontend básico para demonstração |

Todos os commits seguem `tipo(escopo): descrição` (`feat`, `docs`, `feat(model)`) com `Refs #n`.

---

## Slide 8 — Entrega e Links
- **Repositório:** https://github.com/RSC-SC/Projeto-Final-Modulo-2
- **Kanban:** https://github.com/users/RSC-SC/projects/8
- **Issues documentadas com comentários:** #7, #8, #9, #10, #11, #22 (cada uma com evidências, PRs, commits)
- **README atualizado:** `README.md` (escopo, dataset, 13 classes, YOLO, execução, payload, links)
- **Estado do projeto:** `docs/estado-projeto.md` (atualizado após cada gate)
- **Artefatos de evidência:** `docs/f4/evidencia-f4-02.md`, `docs/f5/evidencia-f5-01.md`, `docs/f6/evidencia-f6-01.md`
- **Vídeo (≤7 min):** deve abordar todos os slides acima + demonstração do funcionamento + testes

---

## Notas para gravação do vídeo (≤7 min)

- **Tempo sugerido:**
  - Dataset + objetivo: 1 min
  - Arquitetura / YOLO: 1 min
  - Demo da API (Swagger + JSON): 2 min
  - Frontend / upload + desenho das boxes: 1 min
  - Kanban + GitFlow: 1 min
  - Testes / evidências: 1 min
- **Formato:** vertical ou horizontal; link no Google Drive/YouTube em modo leitor
- **Link deve ser submetido no AVA** até 03/11/2026 22h

---

## Links de referência

- PR #17 (F3-02): endpoint base
- PR #18 (F4-01): YOLO integrado
- PR #19 (F4-02): contrato JSON
- PR #20 (F5-01): testes validados
- PR #21 (F6-01): README atualizado
- PR #23 (demo): frontend básico
- `docs/f0/plano-issues-f1-f6.md`
- `docs/estado-projeto.md`
- `docs/f4/evidencia-f4-02.md`
- `docs/f5/evidencia-f5-01.md`
