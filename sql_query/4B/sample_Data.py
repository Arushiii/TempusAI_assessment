import pandas as pd
import sqlite3
import random
import os

# Database and data generation
conn = sqlite3.connect("genomic_data_analysis.db")

def generate_gene_names(num_genes=100):
    """
    Randomly generates gene names that look similar to real gene symbols.
    """
    prefixes = ["BRCA", "TP", "EGFR", "MYC", "CDKN", "PTEN", "RB", "KRAS", "APC", "PIK3", 
                "AKT", "CCND", "CTNNB", "SMAD", "VHL", "NF", "BRAF", "NOTCH", "ATM", "MET",
                "FGFR", "ERBB", "KIT", "ALK", "IDH", "NTRK", "CDK", "MDM", "ABL", "JAK",
                "FLT", "RET", "PDGF", "SDH", "MEN", "HRAS", "TSC", "MLH", "MSH", "CHEK", 
                "WT", "CDH", "SRC", "GATA", "MTOR", "P", "FOXP", "RBM", "RUNX", "ETV", 
                "CIC", "FUBP", "TERT", "NFE", "ARID", "EZH", "SMAR", "IKZF", "STAT", "ZBTB", 
                "ASXL", "BCOR", "CREB", "KDM", "SETD", "WHSC", "DNMT", "STAG", "RAD", "EP", 
                "CTCF", "AR", "BRD", "GNAS", "IRF", "IKB", "ELF", "FOXA", "FOXL", "MCL", 
                "MECOM", "MGA", "PIK", "PIM"]
    
    if len(prefixes) < num_genes:
        prefixes.extend(['GENE'] * (num_genes - len(prefixes)))
    
    gene_names = []
    for i in range(num_genes):
        prefix = random.choice(prefixes)
        suffix = str(random.randint(1, 99))  
        gene_name = f"{prefix}{suffix}"
        gene_names.append(gene_name)
        prefixes.remove(prefix)
    
    return gene_names



# Step 1: Generate ensembl_gene_map with gene names and chromosomes
gene_ids = [f"ENSG{str(i).zfill(11)}" for i in range(10000000000, 10000000100)]
gene_symbols = generate_gene_names(100)
chromosomes = [f"chr{random.choice(list(range(1, 23)) + ['X', 'Y'])}" for _ in range(100)]

ensembl_gene_map_data = [
    {"ensembl_gene_id": gene_id, "gene_symbol": symbol, "chromosome": chrom}
    for gene_id, symbol, chrom in zip(gene_ids, gene_symbols, chromosomes)
]
ensembl_gene_map_df = pd.DataFrame(ensembl_gene_map_data)
ensembl_gene_map_df.to_sql("ensembl_gene_map", conn, if_exists="replace", index=False)

# Step 2: Generate transcript_gene_map
transcript_codes = [f"ENST{str(i).zfill(11)}" for i in range(20000000000, 20000000150)]
transcript_gene_map_data = [
    {"transcript_code": transcript_code, "ensembl_gene_id": random.choice(gene_ids)}
    for transcript_code in transcript_codes
]
transcript_gene_map_df = pd.DataFrame(transcript_gene_map_data)
transcript_gene_map_df.to_sql("transcript_gene_map", conn, if_exists="replace", index=False)

# Step 3: Generate transcripts with TPM values
patient_ids = [f"p{i}" for i in range(1, 101)]
transcripts_data = [
    {
        "patient_id": random.choice(patient_ids),
        "transcript_code": random.choice(transcript_codes),
        "transcript_tpm": random.uniform(0, 100) if random.random() > 0.1 else None  # 10% chance for null
    }
    for _ in range(200)
]
transcripts_df = pd.DataFrame(transcripts_data)
transcripts_df.to_sql("transcripts", conn, if_exists="replace", index=False)

# Save data
data_folder = "/Users/arushishrivastava/Desktop/tempus_coding/TempusAI_assessment/sql_query/data/genomic_sample_data"
os.makedirs(data_folder, exist_ok=True)

ensembl_gene_map_csv_path = os.path.join(data_folder, "ensembl_gene_map.csv")
transcript_gene_map_csv_path = os.path.join(data_folder, "transcript_gene_map.csv")
transcripts_csv_path = os.path.join(data_folder, "transcripts.csv")

ensembl_gene_map_df.to_csv(ensembl_gene_map_csv_path, index=False)
transcript_gene_map_df.to_csv(transcript_gene_map_csv_path, index=False)
transcripts_df.to_csv(transcripts_csv_path, index=False)

file_paths = {
    "ensembl_gene_map.csv": os.path.abspath(ensembl_gene_map_csv_path),
    "transcript_gene_map.csv": os.path.abspath(transcript_gene_map_csv_path),
    "transcripts.csv": os.path.abspath(transcripts_csv_path),
}

print("Data saved successfully:")
for name, path in file_paths.items():
    print(f"{name}: {path}")

conn.close()
