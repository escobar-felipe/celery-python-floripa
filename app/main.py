from multiprocessing.pool import AsyncResult
from app.celery_app import celery_app
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AddRequest
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
def enqueue_add(request: AddRequest):
    result = add.delay(request.x, request.y)
    return {"task_id": result.id}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        # Tarefa ainda não foi executada
        return {"task_id": task_id, "status": result.state, "result": None}
    elif result.state == "SUCCESS":
        # Tarefa concluída com sucesso
        return {"task_id": task_id, "status": result.state, "result": result.result}
    elif result.state == "FAILURE":
        # Tarefa falhou
        return {
            "task_id": task_id,
            "status": result.state,
            "result": str(result.result),  # Detalhes do erro
            "traceback": result.traceback,  # Stack trace
        }
    else:
        # Outros estados: STARTED, RETRY, REVOKED
        return {"task_id": task_id, "status": result.state, "result": None}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
