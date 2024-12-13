#!/usr/bin/bash

# 72 core machine for the plink2 conversion faster
dx run --instance-type mem1_ssd1_v2_x72 app-cloud_workstation


unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:


sudo apt install plink2


# download the vcf files for that two SNPs
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/out/rs2844970/rs2844970.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/out/rs144588527/rs144588527.vcf.gz"

plink2 --max-alleles 2 --export bgen-1.2 ref-first --out rs2844970 --vcf rs2844970.vcf.gz
plink2 --max-alleles 2 --export bgen-1.2 ref-first --out rs144588527 --vcf rs144588527.vcf.gz

rm rs2844970.vcf.gz
rm rs144588527.vcf.gz

tar -cf rs2844970.tar rs28*
tar -cf rs144588527.tar rs14*

dx upload rs*.tar
