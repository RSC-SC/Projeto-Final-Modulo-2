# F2 - Declarar N/A - Frontend/UI (backend-only)

**Issue vinculada:** #5  
**Fase:** F2  
**Status:** Em andamento  
**Branch:** `feature/5-declarar-nao-aplicavel-frontend`  
**Data:** 27/10/2026  

## N/A - Justificativa

Este projeto é **100% backend-only**. 

### Motivos
- **Produto:** ScanVision - API REST para detecção de objetos em imagens de supermercado (foco em alimentos).
- **Entrega:** Consumida via **Swagger UI** (`/docs`) e ferramentas HTTP (Postman/cURL).
- **Sem interface web/app:** Não há requisitos de UI, páginas, componentes, rotas frontend ou integração com SPA/mobile app.
- **Contrato definido:** Resposta é estritamente **JSON** (`{"status": "success", "detections": [...]}`), conforme PRD (#2).
- **Escopo fora:** Conforme PRD 4.2 "Interface gráfica/frontend" - explícito como fora do escopo.
- **Foco:** Microserviço FastAPI com endpoint `POST /detect` (UploadFile), processamento com YOLO e retorno de detecções estruturadas sem imagem desenhada.

### Escopo desta fase (F2)
Mesmo sendo N/A para frontend, é obrigatório formalizar:
1. **Declaração N/A** com justificativa e escopo (este documento)
2. **UX da API** - Contrato de erros HTTP padronizado, mensagens claras e exemplos reais (ver `docs/ui/ux-api.md`)
3. **Validação de legibilidade** do contrato OpenAPI para consumidor externo

### Confirmação
- [x] Projeto classificado como backend-only
- [x] Não haverá criação de componentes/UI nesta fase
- [x] Contrato de erros/UX da API documentado em `docs/ui/ux-api.md`
- [x] Sem contradição com o contrato da API definido no PRD

## Evidências
- PRD v2.0 (#2): Seção 4.2 - "Fora do Escopo: Interface gráfica/frontend"
- Issue #5: Critérios de aceite (Gherkin)
- Estado do projeto: F1 finalizada, F2 iniciada para declarar N/A

## Handover
Artefatos entregues: `docs/f2/nao-aplicavel-frontend.md`, `docs/ui/ux-api.md`. Próxima fase F3-01 (#6) depende desta declaração.
