from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.auth import router as signup_router

app = FastAPI()

# Middleware to let the frontend hit the api locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup_router, prefix="/signup", tags=["sign up"])

@app.get("/")
async def root():
    return { "message": "Welcome" }