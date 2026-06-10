import pandas as pd

class TransactionCategorizer:
    def __init__(self):
        self.categories = {
            "Groceries": ["supermarket", "grocery", "whole foods"],
            "Dining": ["restaurant", "cafe", "pizza", "burger"],
            "Transport": ["uber", "lyft", "taxi", "gas", "parking"],
            "Entertainment": ["movie", "cinema", "spotify", "netflix"],
            "Shopping": ["amazon", "mall", "store", "retail"],
        }
    
    def categorize(self, description: str) -> str:
        """Categorize transaction based on description"""
        desc_lower = description.lower()
        for category, keywords in self.categories.items():
            if any(keyword in desc_lower for keyword in keywords):
                return category
        return "Other"
    
    def categorize_df(self, df: pd.DataFrame, desc_column: str = "description") -> pd.DataFrame:
        """Categorize all transactions in dataframe"""
        df["category"] = df[desc_column].apply(self.categorize)
        return df