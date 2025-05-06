import logging
from contextlib import asynccontextmanager
from logging import Filter
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status
from taskiq_fastapi import init

from api.v1.routers import all_routers
from core.exceptions import BaseModelException
from core.tasks.task_app import broker


class NoBaseModelExceptionFilter(Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.exc_info:
            _, exc, _ = record.exc_info
            if isinstance(exc, BaseModelException):
                return False
            return True


@asynccontextmanager
async def taskiq_lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()


def create_app(
        routers: Optional[List] = None,
        exception_handlers: Optional[dict] = None,
        middleware: Optional[List] = None,
        dependencies: Optional[List] = None,
        **kwargs
) -> FastAPI:
    kwargs.setdefault("lifespan", taskiq_lifespan)

    app_kwargs = {
        "title": "Raven sneakers shop",
        "version": "1.0.0",
        **kwargs
    }

    app = FastAPI(**app_kwargs)

    @app.exception_handler(Exception)
    async def universal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, BaseModelException):
            status_code = exc.status_code
            detail = exc.message
            headers = {"WWW-Authenticate": "Bearer"} if status_code == 401 else None
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Internal server error"
            headers = None

        return JSONResponse(
            status_code=status_code,
            content={"detail": detail},
            headers=headers
        )

    if exception_handlers:
        for exc_class, handler in exception_handlers.items():
            app.add_exception_handler(exc_class, handler)

    if middleware:
        for m in middleware:
            app.add_middleware(m)

    if dependencies:
        app.dependency_overrides.update(dependencies)

    routers = routers or all_routers
    for router in routers:
        app.include_router(router, prefix="/api/v1")

    configure_logging()

    return app


def configure_logging():
    logging.getLogger("uvicorn.error").addFilter(NoBaseModelExceptionFilter())
    logging.getLogger("uvicorn.access").addFilter(NoBaseModelExceptionFilter())


app = create_app()
init(broker, app)

if __name__ == "__main__":
    uvicorn.run(app=app)
