#!/usr/bin/bash

# re-filter the population level WGS data for two new SNPs

dx run --instance-type mem1_ssd1_v2_x8 app-cloud_workstation
dx ssh job-GvzpgxjJq1jk2237Y19P5Yy7

unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:

sudo apt install tabix -y
sudo apt install plink2
sudo apt install vcftools
sudo apt install bcftools -y

path="project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, pVCF format [500k release]/chr22"

lq="rs2212127"
lq_pos="chr22:15708497-15708497"

b1="ukb24310_c22_b785_v1.vcf.gz"

# download population vcf files & theire associated index files
dx download "$path/$b1"
dx download "$path/$b1.tbi"

# low quality SNP
# psition on GRCH38 assembly from dbSNP database using RSID on the https://genome.ucsc.edu/cgi-bin/hgTables

tabix -h $b1 $lq_pos > $lq.vcf

bcftools query -f '%CHROM\t%POS\n' $lq.vcf
#> chr22 15708497
vcf-validator $lq.vcf
#> The header tag 'reference' not present. (Not required but highly recommended.)
plink2 --vcf $lq.vcf --freq --out "$lq"_allele_counts
#> CHROM  ID      REF     ALT     ALT_FREQS       OBS_CT
# 22      .       A       C,G,T   1.3354e-06,0.907349,1.60247e-05 748842
lq_split="$lq"_split.vcf.gz
bcftools norm -m- $lq.vcf -Oz -o $lq_split
#> Lines   total/split/realigned/skipped:  1/1/0/0
bcftools query -f '%CHROM\t%POS\n' $lq_split
#chr22   15708497
#chr22   15708497
#chr22   15708497

plink2 --vcf $lq_split --freq --out "$lq_split"_allele_counts
##CHROM  ID      REF     ALT     ALT_FREQS       OBS_CT
#22      .       A       C       1.3354e-06      748842
#22      .       A       G       0.907349        748842
#22      .       A       T       1.60247e-05     748842

#Filter out rare variants based on allele frequency. We'll use a threshold of 1% (0.01)
lq_com="$lq"_common
bcftools view -i 'AF>=0.01' $lq_split -Oz -o "$lq_com".vcf.gz

plink2 --vcf "$lq_com".vcf.gz --freq --out "$lq_com"_allele_counts
# #CHROM  ID      REF     ALT     ALT_FREQS       OBS_CT
# 22      .       A       G       0.907349        748842

plink2 --export bgen-1.2 ref-first --out $lq_com --vcf "$lq_com".vcf.gz

dx upload "$lq_com".bgen "$lq_com".sample


hq="rs5756437"
hq_pos="chr22:36979627-36979627"

b2="ukb24310_c22_b1849_v1.vcf.gz"

dx download "$path/$b2"
dx download "$path/$b2.tbi"

tabix -h $b2 $hq_pos > $hq.vcf

bcftools query -f '%CHROM\t%POS\n' $hq.vcf
# chr22   36979627

plink2 --vcf $hq.vcf --freq --out "$hq"_allele_counts
##CHROM  ID      REF     ALT     ALT_FREQS       OBS_CT
# 22      .       G       A       0.136076        981062

plink2 --export bgen-1.2 ref-first --out $hq --vcf $hq.vcf

dx upload "$hq".bgen "$hq".sample

# terminate the instance
dx-set-timout 0h
