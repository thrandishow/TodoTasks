from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import lifespan
from .router import router as tasks_router


app = FastAPI(title="TodoTasks", lifespan=lifespan)
app.include_router(tasks_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
