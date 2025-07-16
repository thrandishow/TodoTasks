import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import get_apps_router
from config.database.db_helper import lifespan


def get_application() -> FastAPI:
    application = FastAPI(title="TodoTasks", lifespan=lifespan)
    application.include_router(get_apps_router())
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
