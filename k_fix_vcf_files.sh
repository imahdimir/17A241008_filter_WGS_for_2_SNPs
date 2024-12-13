#!/usr/bin/bash


f1=/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/out/rs2844970.vcf
f1_out=/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/out/fixed_rs2844970.vcf

f2=/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/out/rs144588527.vcf
f2_out=/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF/out/fixed_rs144588527.vcf

awk '/^##fileformat/ {print; print "##reference=GRCH38"; next}1' $f1 > $f1_out
awk '/^##fileformat/ {print; print "##reference=GRCh38"; next}1' $f2 > $f2_out
