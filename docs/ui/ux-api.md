# UX da API - Contrato de Erros e Padronização

**Projeto:** ScanVision - Detecção de Objetos em Imagens de Supermercado  
**Fase:** F2 (N/A Frontend/UI)  
**Issue:** #5  
**Data:** 27/10/2026  

## 1. Objetivo
Garantir que a API FastAPI seja **compreensível para um consumidor externo** (Swagger/Postman/cURL), com mensagens de erro claras, códigos HTTP semânticos e formato JSON **consistente e padronizado**.

## 2. Formato Padrão de Erro

Toda resposta de erro **deve** seguir este formato JSON único:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE_SNAKE_CASE",
    "message": "Mensagem legível para o consumidor",
    "hint": "Dica opcional para correção (quando aplicável)"
  }
}
```

**Regras:**
- `status`: sempre `"error"` em respostas de erro
- `error.code`: código semântico em `UPPER_SNAKE_CASE` (ex: `INVALID_FILE_TYPE`)
- `error.message`: descrição clara e objetiva do erro
- `error.hint`: orientação prática para corrigir (opcional, mas recomendado)

## 3. Códigos HTTP e Cenários

| Código HTTP | Situação | error.code | message (exemplo) | hint (exemplo) |
|-------------|----------|------------|-------------------|----------------|
| **400 Bad Request** | Requisição malformada / campo ausente / parâmetro inválido | `BAD_REQUEST` | "Requisição inválida." | "Verifique o corpo da requisição e os parâmetros obrigatórios." |
| **415 Unsupported Media Type** | Arquivo com tipo MIME não suportado (não é imagem) ou Content-Type inadequado | `UNSUPPORTED_MEDIA_TYPE` | "Tipo de arquivo não suportado." | "Envie uma imagem nos formatos aceitos: image/jpeg, image/png, image/webp." |
| **422 Unprocessable Entity** | Arquivo válido como mídia, mas inválido para processamento (corrompido, sem dimensões válidas, não é imagem válida) ou falha de validação Pydantic | `UNPROCESSABLE_ENTITY` | "Não foi possível processar a imagem enviada." | "Envie uma imagem válida (JPEG/PNG/WebP) com dimensões adequadas." |
| **500 Internal Server Error** | Erro inesperado no servidor (falha ao carregar modelo, erro de inferência não tratado) | `INTERNAL_SERVER_ERROR` | "Erro interno do servidor." | "Tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte." |

## 4. Exemplos Reais de Resposta

### 400 Bad Request - Parâmetro `file` ausente
```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "Parâmetro 'file' obrigatório não enviado.",
    "hint": "Envie uma requisição multipart/form-data com o campo 'file' contendo uma imagem."
  }
}
```

### 415 Unsupported Media Type - Arquivo não é imagem
```json
{
  "status": "error",
  "error": {
    "code": "UNSUPPORTED_MEDIA_TYPE",
    "message": "Tipo de arquivo não suportado.",
    "hint": "Envie uma imagem nos formatos aceitos: image/jpeg, image/png, image/webp."
  }
}
```

### 422 Unprocessable Entity - Imagem corrompida
```json
{
  "status": "error",
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Não foi possível processar a imagem enviada.",
    "hint": "Verifique se o arquivo é uma imagem válida (JPEG/PNG/WebP) e tente novamente."
  }
}
```

### 500 Internal Server Error - Falha inesperada
```json
{
  "status": "error",
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Erro interno do servidor.",
    "hint": "Tente novamente mais tarde."
  }
}
```

## 5. Contrato de Sucesso (Referência)

Para manter consistência, o contrato de sucesso já definido no PRD:

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

**Notas:**
- Apenas JSON, sem imagem desenhada (conforme PRD 4.1)
- Coordenadas `box` em pixels (formato x_min/y_min/x_max/y_max)
- `confidence` entre 0 e 1

## 6. Orientação para Swagger / Uso

- **Swagger UI:** Disponível em `http://localhost:8000/docs` após inicialização. Todos os códigos de erro devem estar documentados com exemplos.
- **cURL exemplo (sucesso):**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@imagem.jpg"
```
- **cURL exemplo (erro - arquivo não imagem):**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@documento.pdf"
```

## 7. Checklist de Validação
- [x] Formato de erro padronizado definido
- [x] Códigos HTTP semânticos (400, 415, 422, 500)
- [x] Exemplos reais para cada cenário
- [x] Contrato de sucesso referenciado e coerente
- [x] Orientação para Swagger/Postman/cURL
- [x] Sem contradição com PRD/OpenAPI-alvo
- [x] Legível para consumidor externo

## 8. Decisões
- **Formato único:** Optou-se por `{"status":"error","error":{"code","message","hint"}}` ao invés de apenas `{"detail": ...}` do FastAPI padrão, garantindo consistência entre todos os erros.
- **Códigos semânticos:** Uso de 400/415/422/500 cobre validação, tipo de mídia, processamento e falhas internas.
- **UX-first:** `hint` adicionado para reduzir fricção do consumidor ao corrigir requisições.
