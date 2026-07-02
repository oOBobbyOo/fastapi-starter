from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局自定义异常处理器，统一错误返回格式。"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "message": exc.detail, "data": None},
            headers=exc.headers,
        )
