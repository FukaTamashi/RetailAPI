from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config import settings
from server.utils.exception_handler import validation_exception_handler

from api.retail_api.retail_api import retail_router


def _init_router(app: FastAPI) -> None:
    app.include_router(
        retail_router,
        prefix="/api/retailCRM",
        tags=["RetailCRM"]
    )


def _init_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )


def _init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )


def _init_pagination(app: FastAPI) -> None:
    add_pagination(app)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _init_router(app)
    _init_pagination(app)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_middleware(app)
    _init_exception_handlers(app)
    return app


app = create_app()
