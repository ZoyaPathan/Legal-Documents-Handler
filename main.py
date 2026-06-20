from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.database import Base

from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.complaints import router as complaint_router
from app.routers.cases import router as case_router
from app.routers.chat import router as chat_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="LegalConnect API",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(complaint_router)
app.include_router(case_router)
app.include_router(chat_router)
@app.get("/")
def home():
    return {
        "message": "LegalConnect API Running"
    }


@app.get("/")
def home():
    return {
        "message": "LegalConnect API Running"
    }