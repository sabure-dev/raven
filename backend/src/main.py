import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Raven sneakers shop",
    version="1.0.0",
)


if __name__ == "__main__":
    uvicorn.run(app=app)
