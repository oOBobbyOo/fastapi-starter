"""
自定义异常。

集中管理业务异常，统一返回格式。
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """应用基类异常。"""

    def __init__(
        self,
        detail: str = "An error occurred",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestException(AppException):
    """请求错误 (400)。"""

    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedException(AppException):
    """未授权 (401)。"""

    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(AppException):
    """禁止访问 (403)。"""

    def __init__(self, detail: str = "Not enough permissions") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(AppException):
    """资源未找到 (404)。"""

    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ConflictException(AppException):
    """资源冲突 (409)。"""

    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class UnprocessableEntityException(AppException):
    """数据验证失败 (422)。"""

    def __init__(self, detail: str = "Validation error") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TooManyRequestsException(AppException):
    """请求过于频繁 (429)。"""

    def __init__(self, detail: str = "Too many requests") -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": "60"},  # 可选: 告诉客户端多久后重试
        )


class InternalServerException(AppException):
    """服务器内部错误 (500)。"""

    def __init__(self, detail: str = "Internal server error") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
