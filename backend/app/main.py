from fastapi import FastAPI

from app.api.answers import router as answers_router
from app.api.experiments import router as experiments_router
from app.api.polls import router as polls_router
from app.api.questions import router as questions_router
from app.api.users import router as users_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Polls API", version="0.1.0")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(polls_router)
app.include_router(questions_router)
app.include_router(answers_router)
app.include_router(experiments_router)
