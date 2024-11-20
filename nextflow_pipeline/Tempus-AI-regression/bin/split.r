#!/usr/bin/env Rscript

library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
dataset_name <- args[1]
dataset_path <- args[2]
slice_column <- args[3]
data <- read.csv(dataset_path)
print(head(data))

slices <- split(data, data[[slice_column]])

for (name in names(slices)) {
  write.csv(slices[[name]], file.path(paste0(name, ".csv")), row.names = FALSE, quote = FALSE)
}