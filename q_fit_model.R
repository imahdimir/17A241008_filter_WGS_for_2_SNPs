list.of.packages <- c("data.table", "dplyr", "magrittr", "tidyverse", "plinkFile", "genio")

lapply(list.of.packages, library, character.only = TRUE)


data <- read.csv("/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/med/processed_data/model_data.csv")

colnames(data)

# low quality snp g1+g2 ~ g1^-g2^
model1 <- lm(lws ~ lid, data = data)
summary(model1)

# high quality snp g1+g2 ~ g1^-g2^
model2 <- lm(hws ~ hid, data = data)
summary(model2)

# low quality snp g1-g2 ~ g1^-g2^
model3 <- lm(lwd ~ lid, data = data)
summary(model3)

# high quality snp g1-g2 ~ g1^-g2^
model4 <- lm(hwd ~ hid, data = data)
summary(model4)


data <- read.csv("/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/med/processed_data/processed_data_combined.csv")

colnames(data)


# low quality SNP
model1 <- lm(rs2212127_wgs ~ rs2212127_imp, data=data)
summary(model1)

# high quality SNP
model2 <- lm(rs5756437_imp ~ rs5756437_wgs, data=data)
summary(model2)
