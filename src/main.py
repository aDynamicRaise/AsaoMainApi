from fastapi import FastAPI

app = FastAPI(
    title="ASAO Main API",
)


@app.get("/")
def say_hello():
    return {"message" : "Hello, ASAO!"}