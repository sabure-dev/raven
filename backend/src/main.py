import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from api.v1.routers import all_routers
from core.exceptions import BaseModelException

app = FastAPI(
    title="Raven sneakers shop",
    version="1.0.0",
)


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


for router in all_routers:
    app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app=app)
