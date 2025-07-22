from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import lifespan
from .routers.task_router import router as tasks_router
from .routers.auth_router import router as auth_router


app = FastAPI(title="TodoTasks", lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

