"""


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

    # copied from 6A240625_liftover_GRCH37_2_GRCH38
    lifted_snps = d.inp_csf / 'snps.lifted'
    two_snps = d.inp_csf / 'one_low_one_high_quality_snp_on_chr22.txt'
    many_high_and_low_quality_snps_on_chr22 = d.inp_csf / 'many_high_and_low_quality_snps_on_chr22.txt'

    two_snps_lifted = d.med_csf / 'two_snps_lifted.txt'
    dragen_coords = d.inp_csf / 'dragen_pvcf_coordinates.csv'


FP = FilePath()


class FilePathPattern :
    d = Directory()


FPT = FilePathPattern()


class Var :
    start_pos = 'starting_position'
    chro = 'chromosome'
    filename = 'filename'


V = Var()


##
def prepare_lifted_snps() :
    """ """

    ##
    snps_df = pd.read_csv(FP.lifted_snps , sep = '\t' , header = None)

    ##
    two_snps_df = pd.read_csv(FP.two_snps , sep = '\t' , header = None)

    ##
    two_snps_lifted_loc = snps_df[snps_df[3].isin(two_snps_df[1])]

    ##
    _df = two_snps_lifted_loc
    _df = _df[[0 , 1 , 2]]
    _df.to_csv(FP.two_snps_lifted , sep = '\t' , index = False , header = False)

    ##
    df_coords = pd.read_csv(FP.dragen_coords)

    ##
    msk = df_coords[V.chro].eq('chr22')

    df_coords1 = df_coords[msk]

    ##
    _2_snps = two_snps_lifted_loc
    _2_snps = _2_snps[[0 , 1 , 2]]

    ##
    s1 = _2_snps[1].astype('int').iloc[0]
    s1

    ##
    s2 = _2_snps[1].astype('int').iloc[1]
    s2

    ##
    df_coords1[V.start_pos] = df_coords1[V.start_pos].astype('int')

    msk = df_coords1[V.start_pos].le(s1)
    df1 = df_coords1[msk]
    df1 = df1.sort_values(V.start_pos)

    ##
    b0 = df1[V.filename].iloc[-1]
    b0

    ##
    msk = df_coords1[V.start_pos].le(int(s2))
    df2 = df_coords1[msk]

    df2 = df2.sort_values(V.start_pos)

    ##
    b1 = df2[V.filename].iloc[-1]
    b1

    ##


    ##

    msk = df_coords1[V.start_pos].ge(s2)
    df3 = df_coords1[msk]

    ##
    b0 , b1


##
def prepare_many_lifted_snps() :
    """ """

    ##
    snps_df = pd.read_csv(FP.lifted_snps , sep = '\t' , header = None)

    ##
    many_snps_df = pd.read_csv(FP.many_high_and_low_quality_snps_on_chr22 ,
                               sep = '\t' ,
                               header = None)

    selected_snps = ['rs4302301' , 'rs5752355']

    many_snps_df = many_snps_df[many_snps_df[1].isin(selected_snps)]

    ##
    many_snps_loc = snps_df[snps_df[3].isin(many_snps_df[1])]

    ##
    # [low quality SNP, high quality SNP]

    ##
    print(many_snps_loc)

    """ out:   
               0         1         2          3
    67252  chr22  15732362  15732363  rs4302301
    68822  chr22  26608937  26608938  rs5752355

    """

    # now I have the location of the two SNPs in the lifted format
    # low q: 15732362, high q: 26608937

    ## now find the files that contain these SNPs

    df_coords = pd.read_csv(FP.dragen_coords)

    ##
    msk = df_coords[V.chro].eq('chr22')

    df_coords1 = df_coords[msk]

    ##
    _2_snps = many_snps_loc
    _2_snps = _2_snps[[0 , 1 , 2]]

    ##
    s1 = _2_snps[1].astype('int').iloc[0]
    s1
    # 15732362

    ##
    s2 = _2_snps[1].astype('int').iloc[1]
    s2
    # 26608937

    ##
    df_coords1[V.start_pos] = df_coords1[V.start_pos].astype('int')

    msk = df_coords1[V.start_pos].le(s1)
    df1 = df_coords1[msk]
    df1 = df1.sort_values(V.start_pos)

    ##
    b0 = df1[V.filename].iloc[-1]

    print(b0)

    """
    ukb24310_c22_b786_v1.vcf.gz
    
    """

    ##
    msk = df_coords1[V.start_pos].le(int(s2))
    df2 = df_coords1[msk]

    df2 = df2.sort_values(V.start_pos)

    ##
    b1 = df2[V.filename].iloc[-1]
    b1

    print(b1)

    """
    ukb24310_c22_b1330_v1.vcf.gz
    
    """

    ##

    ##

    # new low quality SNP the previous didn't find in the WGS data

    ##
    snps_df = pd.read_csv(FP.lifted_snps , sep = '\t' , header = None)

    ##
    many_snps_df = pd.read_csv(FP.many_high_and_low_quality_snps_on_chr22 ,
                               sep = '\t' ,
                               header = None)

    selected_snps = ['rs5752355']

    many_snps_df = many_snps_df[many_snps_df[1].isin(selected_snps)]

    ##
    many_snps_loc = snps_df[snps_df[3].isin(many_snps_df[1])]

    print(many_snps_loc)

    ##
    df_coords = pd.read_csv(FP.dragen_coords)

    ##
    msk = df_coords[V.chro].eq('chr22')

    df_coords1 = df_coords[msk]

    ##
    _2_snps = many_snps_loc
    _2_snps = _2_snps[[0 , 1 , 2]]

    ##
    s1 = _2_snps[1].astype('int').iloc[0]
    s1

    ##
    s1 = 36979627

    ##
    df_coords1[V.start_pos] = df_coords1[V.start_pos].astype('int')

    msk = df_coords1[V.start_pos].le(s1)
    df1 = df_coords1[msk]
    df1 = df1.sort_values(V.start_pos)

    ##
    b0 = df1[V.filename].iloc[-1]
    print(b0)

    ##



    ##


    ##


    ##


    ##


    ##
