from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routers import auth, user_router
from app import config


app = FastAPI(
    title="Bantr API",
    description="A mini FastAPI application",
    version="0.1.0"
)
app.add_middleware(SessionMiddleware, secret_key="secret-string")

# Base.metadata.create_all(bind=engine)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Bantr API"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

settings = config.Settings()

app.include_router(auth.router)
app.include_router(user_router.router)


