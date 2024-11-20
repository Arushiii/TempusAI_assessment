import sqlite3
import pandas as pd

conn = sqlite3.connect("genomic_data_disease_association.db")
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = conn.execute(query).fetchall()
print("Tables in the database:", tables)


table_name = "variants"  
query = f"PRAGMA table_info({table_name});"
schema = conn.execute(query).fetchall()

print(f"Schema of table '{table_name}':")
for column in schema:
    print(column)