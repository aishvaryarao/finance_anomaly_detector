from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from backend.routes import upload, transactions, anomalies

load_dotenv()

app = FastAPI(
    title="Finance Anomaly Detector API",
    description="Detect anomalies in financial transactions",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(transactions.router)
app.include_router(anomalies.router)

@app.get("/")
async def root():
    return {
        "message": "Finance Anomaly Detector API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload",
            "transactions": "/api/transactions",
            "anomalies": "/api/anomalies"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)