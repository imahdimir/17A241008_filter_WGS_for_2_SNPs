"""
    I am going to prepare the paths to download on the AWS instance for filtering the VCF files based on the individual IDs and SNPs IDs.

    """

import pandas as pd
from pathlib import Path


class Directory :
    proj_csf = '/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF'
    proj_csf = Path(proj_csf)
    pf = proj_csf

    inp_csf = pf / 'inp'
    med_csf = pf / 'med'
    out_csf = pf / 'out'


D = Directory()


class FilePath :
    d = Directory()

    # copied from 14A240924_find_sibs_based_on_kinship_CSF/out
    qualified_iids = d.inp_csf / 'qualified_iids.txt'

    download_list = d.med_csf / 'download_list.txt'
    download_list_small = d.med_csf / 'download_list_small.txt'


FP = FilePath()


class FilePathPattern :
    d = Directory()


FPT = FilePathPattern()


class Var :
    iid = 'IID'
    wgs_folder_name = 'wgs_folder_name'
    wgs_fp = 'wgs_fp'
    tabix_fn = 'tabix_fn'

    ukb_rap_proj_id = 'project-GqxPz1QJq1jfPFbKP8Jb8JKp'
    dragen_wgs_rel_path = '/Bulk/DRAGEN WGS/Whole genome variant call files (VCFs) (DRAGEN) [500k release]'
    dragen_wgs_path_in_proj = f'{ukb_rap_proj_id}:{dragen_wgs_rel_path}'
    wgs_vcf_file_basename_suffix = '_24053_0_0.dragen.hard-filtered.vcf.gz'
    tbi_suffix = '.tbi'

    small_smaple_count = 50
    wgs_vcf_files_dir = '/wgs_vcf_files'


V = Var()


def make_dx_download_list() :
    pass

    ##
    fps_df = pd.read_csv(FP.qualified_iids , header = None , sep = '\t')

    ##
    fps_df = fps_df[[0]]
    fps_df.columns = [V.iid]

    ##
    fps_df[V.iid] = fps_df[V.iid].astype('string')
    fps_df[V.wgs_folder_name] = fps_df[V.iid].str[:2]

    ##
    fps_df = pd.concat([fps_df , fps_df])

    ##
    fps_df = fps_df.sort_values(by = V.iid)

    ##
    # ex:project-GqxPz1QJq1jfPFbKP8Jb8JKp:/Bulk/DRAGEN WGS/Whole genome variant call files (VCFs) (DRAGEN) [500k release]/10/1000230_24053_0_0.dragen.hard-filtered.vcf.gz

    fps_df[V.wgs_fp] = V.dragen_wgs_path_in_proj + '/'
    fps_df[V.wgs_fp] += fps_df[V.wgs_folder_name] + '/'
    fps_df[V.wgs_fp] += fps_df[V.iid] + V.wgs_vcf_file_basename_suffix

    ##
    # add .tbi to the file paths for odd rows
    fps_df.loc[: :2 , V.wgs_fp] += V.tbi_suffix

    ##
    # all qualified VCF files to download
    fps_df[V.wgs_fp].to_csv(FP.download_list , header = False , index = False)

    # small sample of qualified VCF files to download
    _small_fps_df = fps_df[V.wgs_fp].iloc[:V.small_smaple_count]
    _fp = FP.download_list_small
    _small_fps_df.to_csv(_fp , header = False , index = False)

    ##
    fps_df = fps_df.reset_index(drop = True)
    # remove half of the rows to make the tabix list
    fps_df = fps_df.drop(fps_df.index[: :2])
