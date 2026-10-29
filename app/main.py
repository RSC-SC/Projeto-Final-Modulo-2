"""FastAPI application for ScanVision - Object Detection API.

This module creates and configures the FastAPI application instance
with error handlers following the standardized error contract.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import detect
from app.models.yolo import detector


app = FastAPI(
    title="ScanVision - Object Detection API",
    description="Detecção de Objetos em Imagens de Supermercado (foco em alimentos)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(detect.router)


@app.on_event("startup")
async def startup_event():
    """Carrega o modelo YOLO no startup da aplicação."""
    detector.load()


@app.get("/")
async def root():
    """Serve o frontend de demonstração (upload + canvas)."""
    return FileResponse("demo/frontend/index.html")


def error_response(
    status_code: int,
    code: str,
    message: str,
    hint: str | None = None,
):
    """Create standardized error response following API contract."""
    content = {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
        },
    }
    if hint is not None:
        content["error"]["hint"] = hint
    return JSONResponse(status_code=status_code, content=content)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with standardized error format."""
    if exc.status_code == status.HTTP_400_BAD_REQUEST:
        return error_response(
            status_code=400,
            code="BAD_REQUEST",
            message=str(exc.detail) if exc.detail else "Requisição inválida.",
            hint="Verifique o corpo da requisição e os parâmetros obrigatórios.",
        )
    elif exc.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE:
        return error_response(
            status_code=415,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="Tipo de arquivo não suportado.",
            hint="Envie uma imagem nos formatos aceitos: image/jpeg, image/png, image/webp.",
        )
    elif exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        return error_response(
            status_code=422,
            code="UNPROCESSABLE_ENTITY",
            message="Não foi possível processar a imagem enviada.",
            hint="Envie uma imagem válida (JPEG/PNG/WebP) com dimensões adequadas.",
        )
    else:
        return error_response(
            status_code=exc.status_code,
            code="HTTP_ERROR",
            message=str(exc.detail) if exc.detail else "Erro na requisição.",
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with standardized format."""
    return error_response(
        status_code=422,
        code="UNPROCESSABLE_ENTITY",
        message="Não foi possível processar a requisição.",
        hint="Verifique os dados enviados e tente novamente.",
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions without exposing stack traces."""
    return error_response(
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="Erro interno do servidor.",
        hint="Tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte.",
    )

# Mount frontend estático no / (após rotas para não sombrear API)
app.mount("/", StaticFiles(directory="demo/frontend", html=True), name="frontend")
