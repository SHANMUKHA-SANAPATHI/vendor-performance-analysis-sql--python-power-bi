from sqlalchemy import create_engine
import pandas as pd
import os
import logging
import time

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# MySQL connection
engine = create_engine("mysql+pymysql://root:password@localhost:3306/inventory")

def ingest_db(filepath, table_name, engine, chunksize=50000):
    """Ingest large CSV into database without data loss"""
    first_chunk = True
    total_rows = 0

    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        chunk.to_sql(
            table_name,
            con=engine,
            if_exists="replace" if first_chunk else "append",  # replace once, append later
            index=False,
            method="multi",
            chunksize=chunksize
        )
        total_rows += len(chunk)
        first_chunk = False

    return total_rows

def load_raw_data():
    start = time.time()
    data_folder = r"C:\Users\shanm\Downloads\vendor performance\data"

    for file in os.listdir(data_folder):
        if file.endswith(".csv") and file != "sales.csv":  # skip sales (already loaded)
            table_name = file[:-4].replace(" ", "_")  # table = file name
            filepath = os.path.join(data_folder, file)

            logging.info(f"Attempting to ingest {file} as table {table_name}")
            try:
                row_count = ingest_db(filepath, table_name, engine)
                logging.info(f"{table_name} ingested successfully with {row_count} rows")
            except Exception as e:
                logging.error(f"Failed to ingest {file}: {e}")

    end = time.time()
    total_time = (end - start) / 60
    logging.info("------------- Ingestion Complete -------------")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")

if __name__ == "__main__":
    load_raw_data()
