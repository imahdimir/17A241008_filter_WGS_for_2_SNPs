#!/usr/bin/bash

unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:

sudo apt install tabix -y
sudo apt install plink2


# download the vcf files for that two SNPs
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz.tbi"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b1594_v1.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b1594_v1.vcf.gz.tbi"

tabix -h ukb24310_c22_b791_v1.vcf.gz chr22:15825356 > rs2844970.vcf
tabix -h ukb24310_c22_b1594_v1.vcf.gz chr22:31887974 > rs144588527.vcf

plink2 --max-alleles 2 --vcf rs2844970.vcf --make-bed --out rs2844970
plink2 --max-alleles 2 --vcf rs144588527.vcf --make-bed --out rs144588527

bgzip -@ 72 rs2844970.vcf
bgzip -@ 72 rs144588527.vcf

tar -czvf plink_out_rs2844970.tar.gz rs2844970.bed rs2844970.bim rs2844970.fam rs2844970.log
tar -czvf plink_out_rs144588527.tar.gz rs144588527.bed rs144588527.bim rs144588527.fam rs144588527.log

dx upload dx upload plink_out_rs*
dx upload rs*.vcf.gz
