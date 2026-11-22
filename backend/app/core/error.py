# ==========================================================================
# PURPOSE: CONFIG ERRORS
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

# Logger
logger = get_logger(__name__)


# ==========================================================================
# CONFIG
# ==========================================================================
class AppError(Exception):
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Any = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class BadRequestError(AppError):
    def __init__(self, message: str = "Invalid request", details: Any = None):
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class ForbiddenError(AppError):
    def __init__(
        self, message: str = "You do not have permission to perform this action"
    ):
        super().__init__(message, code="FORBIDDEN", status_code=403)


class NotFoundError(AppError):
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", code="NOT_FOUND", status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, code="CONFLICT", status_code=409)


class RateLimitError(AppError):
    def __init__(self, message: str = "Too many requests"):
        super().__init__(message, code="RATE_LIMITED", status_code=429)


class ExternalServiceError(AppError):
    def __init__(self, service: str = "External service"):
        super().__init__(
            f"{service} is currently unavailable",
            code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
        )


# ==========================================================================
# REGISTER FUNCTION
# ==========================================================================
def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        if exc.status_code >= 500:
            logger.error(
                "AppError [%s] on %s %s: %s",
                exc.code,
                request.method,
                request.url.path,
                exc.message,
            )
        else:
            logger.warning(
                "Client error [%s] (%s) on %s %s: %s",
                exc.code,
                exc.status_code,
                request.method,
                request.url.path,
                exc.message,
            )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        simplified = [
            {
                "field": ".".join(
                    str(loc) for loc in err.get("loc", []) if loc != "body"
                ),
                "message": err.get("msg", "Invalid value"),
            }
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": simplified,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(
            "Unhandled exception on %s %s", request.method, request.url.path
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                }
            },
        )
