#!/usr/bin/env Rscript

library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
slice_file <- args[1]
x_var <- args[2]
y_var <- args[3]

data <- read.csv(slice_file)
print(head(data))

dataset_name <- tools::file_path_sans_ext(basename(slice_file))

formula <- as.formula(paste(y_var, "~", x_var))
print(formula)

# Fit the linear regression model
model <- lm(formula, data = data)


# View the model summary
model_summary <- summary(model)


# Extract coefficients into a data frame
coef_df <- as.data.frame(model_summary$coefficients)
colnames(coef_df) <- c("Estimate", "Std.Error", "t.value", "Pr(>|t|)")
coef_df$Term <- rownames(coef_df)
coef_df <- coef_df %>%
  mutate(Dataset = dataset_name)


# Extract additional metrics into another data frame
metrics_df <- data.frame(
  R_Squared = model_summary$r.squared,
  Adjusted_R_Squared = model_summary$adj.r.squared,
  F_Statistic = model_summary$fstatistic[1],
  P_Value = pf(model_summary$fstatistic[1], 
               model_summary$fstatistic[2], 
               model_summary$fstatistic[3], 
               lower.tail = FALSE),
  Dataset = dataset_name
)


#write.csv(coef_df, paste0("regression_coefficients_", dataset_name, ".csv"), row.names = FALSE, quote = FALSE)
write.csv(metrics_df, paste0("regression_metrics_", dataset_name, ".csv"), row.names = FALSE, quote = FALSE)

