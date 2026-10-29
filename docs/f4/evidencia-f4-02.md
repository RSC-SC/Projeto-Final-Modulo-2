# F4-02 — Evidências: JSON Estruturado (sem imagem desenhada)

**Issue:** #9  
**Branch:** `feature/9-retornar-json-estruturado`  
**Commit:** `Refs #9`  
**Data:** 29/10/2026

## Contrato de Resposta (Gherkin US-05 / docs/f0/criterios-aceite-gherkin.md)

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

- ✅ Apenas JSON (sem imagem desenhada / sem campo base64)
- ✅ `detections` é array; vazio quando sem objetos (`[]`)
- ✅ Cada elemento tem `class_name` (string), `confidence` (float 0–1), `box` com coordenadas numéricas
- ✅ Nenhum campo de imagem ou desenho presente na resposta

## Evidência de Teste Manual (FastAPI TestClient)

Executado com `data/coco-subset/images/test/000000441491.jpg`:

```json
{
  "status": "success",
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.7684,
      "box": {"x_min": 0.0, "y_min": 0.64, "x_max": 426.71, "y_max": 479.56}
    },
    {
      "class_name": "person",
      "confidence": 0.3165,
      "box": {"x_min": 247.23, "y_min": 40.7, "x_max": 566.26, "y_max": 479.88}
    },
    {
      "class_name": "cup",
      "confidence": 0.2775,
      "box": {"x_min": 341.3, "y_min": 399.64, "x_max": 430.64, "y_max": 479.77}
    },
    {
      "class_name": "person",
      "confidence": 0.2699,
      "box": {"x_min": 301.52, "y_min": 13.78, "x_max": 637.97, "y_max": 479.09}
    }
  ]
}
```

- Nenhum campo `image` ou `drawn` presente.
- Nenhuma base64.
- Coordenadas são números (não strings).

## Rastreabilidade

- Branch: `feature/9-retornar-json-estruturado`
- Commit esperado: `feat(api): formatar JSON conforme contrato F4-02 (#9)` (`Refs #9`)
- PR: `#` (a ser criado após commit)
- Arquivos vinculados:
  - `app/api/routes/detect.py` (formatação do retorno)
  - `docs/f4/evidencia-f4-02.md` (este arquivo)
