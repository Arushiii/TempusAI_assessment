import sqlite3
import pandas as pd

conn = sqlite3.connect("genomic_data_analysis.db")
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = conn.execute(query).fetchall()
print("Tables in the database:", tables)


table_name = "ensembl_gene_map"  
query = f"PRAGMA table_info({table_name});"
schema = conn.execute(query).fetchall()

print(f"Schema of table '{table_name}':")
for column in schema:
    print(column)