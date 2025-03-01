import uvicorn
from fastapi import FastAPI

from api.v1.routers import all_routers

app = FastAPI(
    title="Raven sneakers shop",
    version="1.0.0",
)

for router in all_routers:
    app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app=app)
