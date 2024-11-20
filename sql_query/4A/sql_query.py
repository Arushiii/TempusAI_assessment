import sqlite3
import pandas as pd

conn = sqlite3.connect("genomic_data_disease_association.db")

# 4A: SQL Query
query = """
WITH diseased_frequency AS (
    SELECT
        variant_id,
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM patients WHERE disease_status = 'diseased') AS diseased_frequency
    FROM
        patients
    WHERE
        disease_status = 'diseased'
    GROUP BY
        variant_id
),
healthy_frequency AS (
    SELECT
        variant_id,
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM patients WHERE disease_status = 'healthy') AS healthy_frequency
    FROM
        patients
    WHERE
        disease_status = 'healthy'
    GROUP BY
        variant_id
),
frequency_comparison AS (
    SELECT
        COALESCE(d.variant_id, h.variant_id) AS variant_id,
        COALESCE(d.diseased_frequency, 0) AS diseased_frequency,
        COALESCE(h.healthy_frequency, 0) AS healthy_frequency,
        ABS(COALESCE(d.diseased_frequency, 0) - COALESCE(h.healthy_frequency, 0)) AS frequency_difference
    FROM
        diseased_frequency d
    FULL OUTER JOIN
        healthy_frequency h
    ON
        d.variant_id = h.variant_id
)
SELECT
    variant_id,
    diseased_frequency,
    healthy_frequency,
    frequency_difference
FROM
    frequency_comparison
ORDER BY
    frequency_difference DESC
LIMIT 5;
"""

results = conn.execute(query).fetchall()
results_df = pd.DataFrame(results, columns=["variant_id", "diseased_frequency", "healthy_frequency", "frequency_difference"])

print("Top 5 Variants Strongly Associated with Disease:")
print(results_df)
results_df.to_csv("/Users/arushishrivastava/Desktop/tempus_coding/TempusAI_assessment/sql_query/data/genomic_data_disease_sample_data/top_5_variants.csv", index=False)

# Close the database connection
conn.close()
