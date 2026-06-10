import pandas as pd
import pdfplumber

def parse_csv(file_path: str) -> pd.DataFrame:
    """Parse CSV bank statement"""
    try:
        df = pd.read_csv(file_path)
        # Rename columns to standard format
        df.columns = [col.lower().strip() for col in df.columns]
        
        # Ensure required columns exist
        required = ["date", "description", "amount"]
        if not all(col in df.columns for col in required):
            raise ValueError(f"CSV must contain columns: {required}")
        
        # Convert amount to float
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["amount"])
        
        return df
    except Exception as e:
        raise Exception(f"Error parsing CSV: {str(e)}")

def parse_pdf(file_path: str) -> pd.DataFrame:
    """Parse PDF bank statement"""
    try:
        with pdfplumber.open(file_path) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    tables.append(table)
        
        if not tables:
            raise ValueError("No tables found in PDF")
        
        df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
        df.columns = [col.lower().strip() for col in df.columns]
        
        return df
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")