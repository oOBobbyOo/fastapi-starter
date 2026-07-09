from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局自定义异常处理器，统一错误返回格式。"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """处理自定义应用异常。"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "data": None,
                "message": exc.detail,
                "type": exc.__class__.__name__,
            },
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """处理未捕获的异常。"""
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "data": None,
                "message": "Internal server error",
                "type": "InternalServerError",
            },
        )
