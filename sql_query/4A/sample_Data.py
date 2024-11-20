import pandas as pd
import sqlite3
import random
import os

# Create the SQLite database connection
conn = sqlite3.connect("genomic_data_disease_association.db")

# Step 1: Generate sample data for 'variants' table with realistic IDs
variants_data = [
    {
        "variant_id": f"rs{random.randint(100000, 999999)}",  # Realistic dbSNP-style variant ID
        "chromosome": f"chr{random.choice(list(range(1, 23)) + ['X', 'Y'])}",
        "position": random.randint(1, 1000000),
        "reference_allele": random.choice(["A", "T", "C", "G"]),
        "alternate_allele": random.choice(["A", "T", "C", "G"]),
    }
    for _ in range(50)
]
variants_df = pd.DataFrame(variants_data).drop_duplicates(subset=["variant_id"])
variants_df.to_sql("variants", conn, if_exists="replace", index=False)

# Step 2: Generate sample data for 'patients' table
patient_ids = [f"p{i}" for i in range(1, 201)]  # 200 patients
variant_ids = variants_df["variant_id"].tolist()
patients_data = []

# Ensure that variants link to the 'variants' table
for patient_id in patient_ids:
    variant_id = random.choice(variant_ids)
    disease_status = (
        "diseased" if variant_id in random.sample(variant_ids, k=15) and random.random() < 0.7 else "healthy"
    )
    patients_data.append({"patient_id": patient_id, "variant_id": variant_id, "disease_status": disease_status})

patients_df = pd.DataFrame(patients_data)
patients_df.to_sql("patients", conn, if_exists="replace", index=False)

# Step 3: Save data to CSV files for reference
data_folder = "/Users/arushishrivastava/Desktop/tempus_coding/TempusAI_assessment/sql_query/data/genomic_data_disease_sample_data"
os.makedirs(data_folder, exist_ok=True)

variants_csv_path = os.path.join(data_folder, "variants.csv")
patients_csv_path = os.path.join(data_folder, "patients.csv")

variants_df.to_csv(variants_csv_path, index=False)
patients_df.to_csv(patients_csv_path, index=False)

file_paths = {
    "variants.csv": os.path.abspath(variants_csv_path),
    "patients.csv": os.path.abspath(patients_csv_path),
}

print("Data saved successfully:")
for name, path in file_paths.items():
    print(f"{name}: {path}")

conn.close()
