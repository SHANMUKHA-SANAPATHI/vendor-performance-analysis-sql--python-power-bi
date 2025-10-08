from sqlalchemy import create_engine
import pandas as pd
import pymysql
import os
import logging
import time
from injestion_db import injest_db 

# ------------------ Setup Logging ------------------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# ------------------ Database Connection ------------------
db_user = "root"
db_password = "password"
db_host = "localhost"
db_port = "3306"
db_name = "inventory"

engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/inventory}")

# ------------------ Create Vendor Summary ------------------
def create_vendor_summary(engine):
    query = """
    WITH FreightSummary AS (
        SELECT VendorNumber, SUM(Freight) AS FreightCost
        FROM Vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT 
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Volume,
            pp.Price AS ActualPrice,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Volume, pp.Price
    ),
    SalesSummary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales 
        GROUP BY VendorNo, Brand
    )
    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """
    return pd.read_sql_query(query, con=engine)

# ------------------ Clean Data ------------------
def clean_data(df):
    numeric_cols = [
        'Volume', 'TotalPurchaseQuantity', 'TotalPurchaseDollars',
        'TotalSalesQuantity', 'TotalSalesDollars', 'TotalSalesPrice', 'TotalExciseTax'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)

    for col in ['VendorName', 'Description']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)

    return df

# ------------------ Main ------------------
if __name__ == '__main__':
    start_time = time.time()
    try:
        logging.info("Creating Vendor Summary Table...")
        summary_df = create_vendor_summary(engine)

        logging.info("Cleaning Data...")
        clean_df = clean_data(summary_df)

        if clean_df.empty:
            logging.warning("No data to ingest — vendor summary is empty.")
        else:
            logging.info("Ingesting Data...")
            injest_db(clean_df, 'vendor_sales_summary', engine)

        logging.info("Completed Successfully")
    except Exception as e:
        logging.exception(f"Error during ingestion: {e}")
    finally:
        logging.info(f"Execution Time: {time.time() - start_time:.2f} seconds")
