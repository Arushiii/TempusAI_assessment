import sqlite3
import pandas as pd

conn = sqlite3.connect("genomic_data_analysis.db")

# 4B: SQL Query
query = """
WITH transcript_gene_tpm AS (
    SELECT
        t.patient_id,
        tg.ensembl_gene_id,
        t.transcript_tpm
    FROM
        transcripts t
    JOIN
        transcript_gene_map tg
    ON
        t.transcript_code = tg.transcript_code
),
gene_level_tpm AS (
    SELECT
        t.patient_id,
        g.gene_symbol,
        SUM(COALESCE(t.transcript_tpm, 0)) AS total_tpm
    FROM
        transcript_gene_tpm t
    JOIN
        ensembl_gene_map g
    ON
        t.ensembl_gene_id = g.ensembl_gene_id
    GROUP BY
        t.patient_id, g.gene_symbol
)
SELECT
    patient_id,
    gene_symbol,
    LOG2(total_tpm + 1) AS log2_tpm_plus_1
FROM
    gene_level_tpm;

"""

results = conn.execute(query).fetchall()
results_df = pd.DataFrame(results, columns=["patient_id", "gene_symbol", "log2(TPM+1)"])

print(results_df)
results_df.to_csv("/Users/arushishrivastava/Desktop/tempus_coding/TempusAI_assessment/sql_query/data/genomic_sample_data/results.csv", index=False)

# Close the database connection
conn.close()
