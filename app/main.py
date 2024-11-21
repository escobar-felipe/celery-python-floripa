import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.tasks import add


app = FastAPI(
    title="API",
    description="Documentação API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "api is alive"}


@app.get("/ping")
async def health():
    return {"message": "api alive"}


@app.post("/add")
def enqueue_add(x: int, y: int):
    result = add.delay(x, y)
    return {"task_id": result.id}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
