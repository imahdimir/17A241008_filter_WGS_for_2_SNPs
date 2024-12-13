#!/usr/bin/bash

unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:

sudo apt install plink2
mkdir plink_out

# downlad chr22 imputed data by their ids
# bgen
dx download file-FxY62b8JkF66qV4X0p7KGzgf
# bgi
dx download file-FxZ2f1jJkF6B5yVBPkVvZf1P
# sample
dx download file-Gqy8B4QJ5Yx3jGBky1kyGB50


# qualified_iids.txt
dx download file-Gv28PF0Jq1jyXxZqy8xQF8Fy

# two SNPs for filtering
# project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/med/two_snps_lifted.txt
dx download file-GxJgfgjJq1jbQ91pzP5GB7Qj


cwd=$(pwd)
bgen_fp="$cwd/ukb22828_c22_b0_v3.bgen"
sample_fp="$cwd/ukb22828_c22_b0_v3.sample"
iids="$cwd/qualified_iids.txt"
snps="$cwd/two_snps_20241212.txt"
out_dir="$cwd/plink_out"

plink2 --bgen "$bgen_fp" ref-first --export bgen-1.2 --sample "$sample_fp" --keep "$iids" --extract "$snps" --out "$out_dir/two_snps"
