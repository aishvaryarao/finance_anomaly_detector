from fastapi import APIRouter, HTTPException, Query
from database.connection import execute_query

router = APIRouter(prefix="/api/anomalies", tags=["anomalies"])

@router.get("/")
async def get_anomalies(user_id: int = Query(...)):
    """Get all anomalies for a user"""
    try:
        query = """SELECT a.*, t.date, t.description, t.amount 
                   FROM anomalies a
                   JOIN transactions t ON a.transaction_id = t.id
                   WHERE a.user_id = %s
                   ORDER BY a.detected_at DESC"""
        anomalies = execute_query(query, (user_id,))
        
        return {
            "total_anomalies": len(anomalies) if anomalies else 0,
            "anomalies": anomalies or []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report")
async def get_anomaly_report(user_id: int = Query(...)):
    """Get anomaly report"""
    try:
        query = """SELECT COUNT(*) as total_anomalies, 
                          AVG(anomaly_score) as avg_score
                   FROM anomalies
                   WHERE user_id = %s"""
        cursor_result = execute_query(query, (user_id,))
        
        if cursor_result:
            report = cursor_result[0]
            return {
                "total_anomalies_detected": report.get("total_anomalies", 0),
                "average_anomaly_score": report.get("avg_score", 0)
            }
        return {"total_anomalies_detected": 0, "average_anomaly_score": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))