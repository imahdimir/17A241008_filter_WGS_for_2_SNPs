
list.of.packages <- c("data.table", "dplyr", "magrittr", "tidyverse", "plinkFile", "genio")

lapply(list.of.packages, library, character.only = TRUE)


data <- read.csv("/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/out/model_data.csv")

colnames(data)

# low quality snp g1+g2 ~ g1^-g2^
model1 <- lm(W1p2_rs28 ~ I1m2_rs28, data = data)
summary(model1)

# high quality snp g1+g2 ~ g1^-g2^
model2 <- lm(W1p2_rs14 ~ I1m2_rs14, data = data)
summary(model2)

# low quality snp g1-g2 ~ g1^-g2^
model3 <- lm(W1m2_rs28 ~ I1m2_rs28, data = data)
summary(model3)

# high quality snp g1-g2 ~ g1^-g2^
model4 <- lm(W1m2_rs14 ~ I1m2_rs14, data = data)
summary(model4)

