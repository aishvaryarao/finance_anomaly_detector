from fastapi import APIRouter, HTTPException, Query
from database.models import Transaction
from typing import List

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.get("/")
async def get_transactions(user_id: int = Query(...), skip: int = 0, limit: int = 100):
    """Get all transactions for a user"""
    try:
        transactions = Transaction.get_by_user(user_id)
        if transactions is None:
            raise HTTPException(status_code=500, detail="Database error")
        
        return {
            "total": len(transactions),
            "transactions": transactions[skip:skip+limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomalies")
async def get_anomalies(user_id: int = Query(...)):
    """Get anomalies for a user"""
    try:
        anomalies = Transaction.get_anomalies(user_id)
        if anomalies is None:
            raise HTTPException(status_code=500, detail="Database error")
        
        return {
            "total": len(anomalies),
            "anomalies": anomalies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_summary(user_id: int = Query(...)):
    """Get transaction summary"""
    try:
        transactions = Transaction.get_by_user(user_id)
        if transactions is None:
            raise HTTPException(status_code=500, detail="Database error")
        
        total_spent = sum(float(t.get("amount", 0)) for t in transactions)
        categories = {}
        for t in transactions:
            cat = t.get("category", "Other")
            categories[cat] = categories.get(cat, 0) + float(t.get("amount", 0))
        
        return {
            "total_spent": total_spent,
            "transaction_count": len(transactions),
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))