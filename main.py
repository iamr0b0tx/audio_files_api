from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def read_root():
    return {
        "status": 1,
        "data": "pong"
    }
