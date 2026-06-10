from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List
import shutil
import os
import pandas as pd
from data_processing.parser import parse_csv, parse_pdf
from data_processing.categorizer import TransactionCategorizer
from data_processing.anomaly_detector import AnomalyDetector
from database.models import Transaction, Anomaly, User
from datetime import datetime

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

categorizer = TransactionCategorizer()
detector = AnomalyDetector(contamination=0.1)

@router.post("/")
async def upload_file(file: UploadFile = File(...), user_id: int = Form(...)):
    """Upload and process bank statement"""
    try:
        # Validate file type
        # Validate file type
        if not (
            file.filename.lower().endswith(".csv")
            or file.filename.lower().endswith(".pdf")
            ):
            raise HTTPException(status_code=400, detail="Only CSV and PDF files are allowed")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse file
        # Parse file
        if file.filename.lower().endswith(".csv"):
            df = parse_csv(file_path)
        else:
            df = parse_pdf(file_path)
        
        # Categorize transactions
        df = categorizer.categorize_df(df, desc_column="description")
        
        # Detect anomalies
        df = detector.detect(df, amount_column="amount")
        
        # Save to database
        processed_count = 0
        print("ENTERING SAVE LOOP")
        for _, row in df.iterrows():
            transaction = Transaction(
                user_id=user_id,
                date=row["date"],
                description=row["description"],
                amount=float(row["amount"]),
                category=row["category"],
                is_anomaly=bool(row["is_anomaly"])
            )
            result = transaction.save()
            print("SAVE RESULT:", result)

            processed_count += 1
            
            # If anomaly, also save to anomalies table
            if row["is_anomaly"]:
                anomaly = Anomaly(
                    user_id=user_id,
                    transaction_id=processed_count,
                    anomaly_score=0.95,
                    reason="Unusual spending amount detected"
                )
                anomaly.save()
        
        # Clean up file
        os.remove(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "transactions_processed": processed_count,
            "anomalies_detected": int(df["is_anomaly"].sum())
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))