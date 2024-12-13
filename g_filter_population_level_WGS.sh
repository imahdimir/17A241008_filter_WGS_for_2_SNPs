#!/usr/bin/bash

dx run --instance-type mem1_ssd1_v2_x72 app-cloud_workstation


unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:

sudo apt install tabix -y
sudo apt install plink2
sudo apt install vcftools
sudo apt install bcftools -y


# download vcf files for that two SNPs
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz.tbi"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b1594_v1.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b1594_v1.vcf.gz.tbi"

tabix -h ukb24310_c22_b791_v1.vcf.gz chr22:15825356-15825357 > rs2844970.vcf
tabix -h ukb24310_c22_b1594_v1.vcf.gz chr22:31887974-31887975 > rs144588527.vcf

bgzip -@ 72 rs*.vcf

plink2 --max-alleles 2 --export bgen-1.2 ref-first --out rs2844970 --vcf rs2844970.vcf.gz --write-snps
plink2 --max-alleles 2 --export bgen-1.2 ref-first --out rs144588527 --vcf rs144588527.vcf.gz --write-snps

find . -type f -name 'rs28*' ! -name '*.gz' -print0 | tar --null -cvf rs2844970.tar --files-from -
find . -type f -name 'rs14*' ! -name '*.gz' -print0 | tar --null -cvf rs144588527.tar --files-from -

dx upload rs*.tar
dx upload rs*.vcf.gz

# terminate the instance
dx-set-timout 0h
