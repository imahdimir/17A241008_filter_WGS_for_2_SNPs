#!/usr/bin/bash

dx run --instance-type mem1_ssd1_v2_x2 app-cloud_workstation

dx ssh job

unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:


sudo apt install tabix -y


dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz"
dx download "project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22/ukb24310_c22_b791_v1.vcf.gz.tbi"

tabix -h ukb24310_c22_b791_v1.vcf.gz chr22:15825356-15825357 > rs2844970.vcf

sudo apt install vcftools

vcf-validator rs2844970.vcf

awk '/^##fileformat/ {print; print "##reference=GRCH38"; next}1' rs2844970.vcf > rs2844970.vcf
sed '/^##.*$/a #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE' rs2844970.vcf > 1.vcf

tabix ukb24310_c22_b791_v1.vcf.gz chr22:15825356 > rs2844970.vcf
