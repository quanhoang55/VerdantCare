# ==========================================================================
# PURPOSE: CREATE FASTAPI APP
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoint.v1 import api_v1_router
from app.core.config import settings
from app.core.error import register_exception_handlers
from app.core.logging import get_logger, setup_logging

# Logger
logger = get_logger(__name__)

# ==========================================================================
# CORE LOGIC & FUNCTIONS
# ==========================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    logger.info("Starting %s (%s)", settings.APP_NAME, settings.ENV)
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    setup_logging(settings.LOG_LEVEL)

    # Init FastAPI App
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error Register
    register_exception_handlers(app)
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["Health"])
    async def heath() -> dict[str, str]:
        return {"status": "ok"}

    return app


# ==========================================================================
# FASTAPI APP
# ==========================================================================
app = create_app()
