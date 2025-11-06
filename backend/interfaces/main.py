from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.interfaces.api.routes import router

app = FastAPI(
    title="MetricFlow API",
    description="Turn business data into clear insights — fast.",
    version="0.1.0"
)

# Configure CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)