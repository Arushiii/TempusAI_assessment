#!/usr/bin/env Rscript

library(tidyverse)

# Get all file arguments passed to the script
args <- commandArgs(trailingOnly = TRUE)

# Check if any files are provided
if (length(args) == 0) {
  stop("No files provided as arguments. Usage: script.R file1 file2 file3 ...")
}

# Read all files into a list of data frames and combine them
merged_df <- args %>%
  lapply(read.csv) %>%
  bind_rows()

print(merged_df)

write.csv(merged_df, file = "merged_regression_results.csv", append = FALSE, quote = FALSE, sep = ",", row.names=FALSE)