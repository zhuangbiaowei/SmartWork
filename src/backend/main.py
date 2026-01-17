from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.file_system import router as file_router

app = FastAPI(
    title="SmartWork API", description="AI 智能体协作平台后端 API", version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router, prefix="/api/files", tags=["files"])


@app.get("/")
async def root():
    return {"message": "SmartWork API Server", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
