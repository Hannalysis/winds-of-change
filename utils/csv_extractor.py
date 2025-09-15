import pandas as pd

def extract_to_csv(QUERY, engine, CSV_PATH):
    df = pd.read_sql(QUERY, engine)
    df.to_csv(CSV_PATH, index=False)
    print(f"~📜 Query CSV saved to {CSV_PATH} ~")