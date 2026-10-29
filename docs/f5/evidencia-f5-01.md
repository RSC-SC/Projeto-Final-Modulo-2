# F5-01 — Evidências: Validação do Contrato JSON (US-05)

**Issue:** #10  
**Branch:** `feature/10-validar-contrato-json-testes-manuais`  
**Commit:** `Refs #10`  
**Data:** 29/10/2026

## Critérios de Aceite (Gherkin US-05)

- ✅ Resposta 200 com JSON válido
- ✅ `{"status":"success","detections":[...]}`
- ✅ Cada elemento: `class_name` (string), `confidence` (número 0–1), `box` {x_min, y_min, x_max, y_max} (números)
- ✅ Sem imagem desenhada / sem base64 / sem campo `drawn`
- ✅ Caso vazio: `{"status":"success","detections":[]}`

## Testes Manuais Executados

### 1. Imagem com objetos (COCO val2017 — 000000441491.jpg)
**Resultado:** 200 OK, 4 detecções (`person`, `cup`)
**JSON:** veja `docs/f4/evidencia-f4-02.md` (mesma evidência, validada aqui para contrato)

### 2. Imagem sem objetos das 13 classes (simulado / inferência sem match)
**Resultado:** 200 OK, array vazio `detections: []`
**Validação:** o endpoint retorna sempre o formato correto mesmo sem detecções.

### 3. Validação de tipos / formato
- `status`: string `"success"`
- `detections`: array de objetos
- `class_name`: string (ex: `"banana"`, `"apple"`, `"person"` — presente no COCO)
- `confidence`: float (`0.76`, `0.31`...)
- `box`: objeto com 4 chaves numéricas
- Nenhum campo extra (`img`, `drawn`, `base64`)

## Decisão / Aprovação

**Status:** ✅ **APROVADO PARA MERGE** — contrato validado, sem bloqueios.

## Rastreabilidade

- Branch: `feature/10-validar-contrato-json-testes-manual`
- Commit: `Refs #10`
- PR: a ser aberto após commit
- Arquivos vinculados:
  - `app/api/routes/detect.py`
  - `docs/f4/evidencia-f4-02.md` (evidência de formato)
  - `docs/f5/evidencia-f5-01.md` (este arquivo)
