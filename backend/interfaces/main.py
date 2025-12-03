from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.interfaces.api.routes import router

load_dotenv()

app = FastAPI(
    title="MetricFlow API",
    description="Turn business data into clear insights — fast.",
    version="0.1.0"
)

# Configure CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://metricflow-frontend-bucket.s3-website-us-east-1.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "MetricFlow API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}