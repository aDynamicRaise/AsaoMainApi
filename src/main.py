from contextlib import asynccontextmanager
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api import router as api_router
from database.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    title="ASAO Main API",
    lifespan=lifespan,
)

app.include_router(
    api_router,
)


@app.exception_handler(RequestValidationError)
async def unicorn_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    for error in errors:
        if error['type'] == 'value_error' and error['loc'][1] == 'email':
            error['msg'] = "Неверный формат адреса электронной почты. Адрес должен быть по типу: user@example.com"
        elif error['type'] == 'string_too_short' and error['loc'][1] == 'password':
            error['msg'] = "Пароль должен содержать не менее 4 символов"
        elif error['type'] == 'string_too_long' and error['loc'][1] == 'password':
            error['msg'] = "Пароль должен содержать не более 20 символов"

    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


origins = [ "http://localhost:3000", ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
