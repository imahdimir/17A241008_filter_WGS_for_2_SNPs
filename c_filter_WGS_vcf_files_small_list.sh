#!/usr/bin/bash

sudo apt install tabix -y


# selecting the WGS project
dx select --level=VIEW


unset DX_WORKSPACE_ID
dx cd $DX_PROJECT_CONTEXT_ID:


# download the vcf files in parallel first small list

# small list to download
dx download project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/med/download_list_small.txt

# for keeping downloaded files in a separate directory
mkdir wgs

# download the vcf files with dx in parallel into the wgs directory, 10 in parallel
cat download_list_small.txt | xargs -n 1 -P 10 -I {} dx download {} -o wgs


# filter using Tabix for whole set of SNPs & two SNPs, compare the time
dx download project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/med/snps.lifted
dx download project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/med/two_snps_lifted.txt

ls wgs/*.gz | xargs -n 1 basename > list_of_gz_files.txt

mkdir filtered_vcf

sudo apt install parallel -y

parallel "tabix -R wgs/{} ~/snps.lifted > filtered_vcf/{.}" :::: list_of_gz_files.txt
parallel "tabix -R wgs/{} two_snps_lifted.lifted > filtered_vcf/{.}" :::: list_of_gz_files.txt


tabix 1000230_24053_0_0.dragen.hard-filtered.vcf.gz 1 > 1.dragen.hard-filtered.vcf

sudo apt-get install bcftools -y

mkdir sorted_filtered_vcf

# from previous experience in 12A... project, I know vcf files are not sorted
# they need to be sorted before merging

# just 1 file
file=filtered_vcf/1000230_24053_0_0.dragen.hard-filtered.vcf

grep -v "^#" 1.dragen.hard-filtered.vcf | wc -l

# not parallel way
for file in filtered_vcf/*.vcf; do
    bn=$(basename $file)
    bcftools sort -o sorted_filtered_vcf/"sorted_$bn" "$file"
done

# parallel way, by default parallel uses as many CPU cores as possible
ls filtered_vcf/*.vcf | parallel 'bn=$(basename {}); bcftools sort -o sorted_filtered_vcf/"sorted_$bn" "{}"'

# before merging, I need to compress the sorted vcf files and index them
# that way I can merge them in a faster way using bcftools merge

mkdir compressed_sorted_filtered_vcf

# first compress the sorted vcf files
# not parallel way
for file in sorted_filtered_vcf/*.vcf; do
    bn=$(basename $file)
    bgzip -c $file > compressed_sorted_filtered_vcf/$bn.gz
done
# parallel way
ls sorted_filtered_vcf/*.vcf | parallel 'bn=$(basename {}); bgzip -c {} > compressed_sorted_filtered_vcf/$bn.gz'

# not parallel way
for file in compressed_sorted_filtered_vcf/*.gz; do
    bcftools index --csi $file
done

# parallel way
ls compressed_sorted_filtered_vcf/*.gz | parallel 'bcftools index --csi {}'


# now I create the list of files to merge
ls compressed_sorted_filtered_vcf/*.vcf.gz > compressed_sorted_filtered_vcf.txt

# merge all the compressed sorted vcf files
bcftools merge -O z -o merged_compressed_sorted_filtered.vcf.gz -l compressed_sorted_filtered_vcf.txt --threads 72


# convert it to bed so I can check on the genotypes available
sudo apt install plink2

gunzip merged_compressed_sorted_filtered.vcf

# check on the merged file having all the genotypes I want
plink2 --max-alleles 2 --vcf merged_compressed_sorted_filtered.vcf.gz --make-bed --out merged_compressed_sorted_filtered --allow-extra-chr



tabix 1000230_24053_0_0.dragen.hard-filtered.vcf.gz two_snps_lifted > 1000230.vcf

dx download project-GqxPz1QJq1jfPFbKP8Jb8JKp:/projects_data/17A241008_filter_WGS_for_2_SNPs/med/two_snps_lifted.txt
tabix -R wgs/1000265_24053_0_0.dragen.hard-filtered.vcf.gz two_snps_lifted > filter1_by_1/1000265.vcf
