from datetime import datetime
from database.connection import execute_query

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def save(self):
        """Save user to database"""
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        return execute_query(query, (self.username, self.email))
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        return execute_query(query, (username,))

class Transaction:
    def __init__(self, user_id, date, description, amount, category="Other", is_anomaly=False):
        self.user_id = user_id
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category
        self.is_anomaly = is_anomaly
    
    def save(self):
        """Save transaction to database"""
        query = """INSERT INTO transactions 
                   (user_id, date, description, amount, category, is_anomaly) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        return execute_query(query, (self.user_id, self.date, self.description, 
                                     self.amount, self.category, self.is_anomaly))
    
    @staticmethod
    def get_by_user(user_id):
        """Get all transactions for a user"""
        query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC"
        return execute_query(query, (user_id,))
    
    @staticmethod
    def get_anomalies(user_id):
        """Get anomalies for a user"""
        query = "SELECT * FROM transactions WHERE user_id = %s AND is_anomaly = TRUE"
        return execute_query(query, (user_id,))

class Anomaly:
    def __init__(self, user_id, transaction_id, anomaly_score, reason):
        self.user_id = user_id
        self.transaction_id = transaction_id
        self.anomaly_score = anomaly_score
        self.reason = reason
    
    def save(self):
        """Save anomaly to database"""
        query = """INSERT INTO anomalies 
                   (user_id, transaction_id, anomaly_score, reason) 
                   VALUES (%s, %s, %s, %s)"""
        return execute_query(query, (self.user_id, self.transaction_id, 
                                     self.anomaly_score, self.reason))