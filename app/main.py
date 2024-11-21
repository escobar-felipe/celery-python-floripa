import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API",
    description="Documentação API",
    redoc_url=None,
    openapi_url=None,
    docs_url=None,
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


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
