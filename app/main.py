from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---- 路由注册 ----
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Health check endpoint
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}
