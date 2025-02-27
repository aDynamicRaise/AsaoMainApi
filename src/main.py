from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from config import settings
from api import router as api_router
from database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(
    title="ASAO Main API",
    lifespan=lifespan,
)

app.include_router(
    api_router,
)


@app.get("/")
def say_hello():
    return {"message" : "Hello, ASAO!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
