import numpy as np
import pandas as pd
from pathlib import Path
from bgen_reader import open_bgen


class Var :
    iid = 'IID'
    id1 = 'ID1'
    id2 = 'ID2'
    inf_type = 'infType'

    imp = '_imp'
    wgs = '_wgs'

    rs22 = 'rs2212127'
    rs57 = 'rs5756437'

    hw1 = 'hw1'
    hw2 = 'hw2'
    lw1 = 'lw1'
    lw2 = 'lw2'

    hi1 = 'hi1'
    hi2 = 'hi2'
    li1 = 'li1'
    li2 = 'li2'

    # high quality SNP, WGS sum
    hws = 'hws'
    # low quality SNP, WGS sum
    lws = 'lws'
    # high quality SNP, WGS difference
    hwd = 'hwd'
    # low quality SNP, WGS difference
    lwd = 'lwd'

    # high quality SNP, imputed difference
    hid = 'hid'
    # low quality SNP, imputed difference
    lid = 'lid'


class Directory :
    proj_csf = '/Users/mmir/Library/CloudStorage/Dropbox/git/17A241008_filter_WGS_for_2_SNPs_CSF'
    proj_csf = Path(proj_csf)
    pf = proj_csf

    inp_csf = pf / 'inp'
    med_csf = pf / 'med'
    out_csf = pf / 'out'

    proccessed_data = med_csf / 'processed_data'


class FilePath :
    d = Directory()
    v = Var()

    impupted_data = d.med_csf / 'imputed_two_snps_20241212'
    two_imputed_sns_bgn = impupted_data / 'two_snps.bgen'

    processed_imputed_data = d.proccessed_data / 'processed_imputed_data.parquet'

    wgs_data = d.med_csf / 'wgs'
    wgs_rs22 = wgs_data / (v.rs22 + '_common.bgen')
    wgs_rs57 = wgs_data / (v.rs57 + '.bgen')

    wgs_rs22_processed = d.proccessed_data / 'df_wgs_rs22.parquet'
    wgs_rs57_processed = d.proccessed_data / 'df_wgs_rs57.parquet'

    processed_data = d.proccessed_data / 'processed_data_combined.parquet'
    processed_data_csv = d.proccessed_data / 'processed_data_combined.csv'

    rels = d.inp_csf / 'ukb_rel_with_infType_fs.csv'

    model_data = d.proccessed_data / 'model_data.csv'


def process_imputed_data_to_fit_the_model() :
    pass

    ##
    d = Directory()
    fp = FilePath()
    v = Var()

    ##
    bgn = open_bgen(fp.two_imputed_sns_bgn)

    ##
    sample = bgn.samples
    len(sample)

    ##
    _dct = {
            v.iid : sample
            }

    df_iid = pd.DataFrame(_dct)

    ##
    df_iid[v.iid] = df_iid[v.iid].str.split('_').str[1]

    ##
    nd_gt = bgn.read()
    nd_gt.shape

    ##
    # low quality SNP haplotypes
    nd_lq_snp = nd_gt[: , 0 , :]
    nd_lq_snp

    ##
    nd_lq_snp = np.argmax(nd_lq_snp , axis = 1)

    ##
    df_gt = pd.DataFrame(nd_lq_snp , columns = [v.rs22])
    df_gt.value_counts()

    ##
    df_lq = pd.concat([df_iid , df_gt] , axis = 1)

    ##
    nd_hq = nd_gt[: , 1 , :]
    nd_hq

    ##
    nd_hq = np.argmax(nd_hq , axis = 1)

    ##
    df_gt = pd.DataFrame(nd_hq , columns = [v.rs57])
    df_gt.value_counts()

    ##
    df_hq = pd.concat([df_iid , df_gt] , axis = 1)

    ##

    # merge low and high quality SNP genotypes
    df_imp = pd.merge(df_lq , df_hq , on = v.iid)

    ##
    df_imp.to_parquet(fp.processed_imputed_data , index = False)

    ##


def process_wgs_data_to_fit_the_model() :
    pass

    ##
    d = Directory()
    fp = FilePath()
    v = Var()

    ##
    # WGS data process, low quality SNP
    bgn = open_bgen(fp.wgs_rs22)
    sample = bgn.samples

    ##
    _dct = {
            v.iid : sample
            }

    df_iid = pd.DataFrame(_dct)

    ##
    nd_gt = bgn.read()
    nd_gt.shape

    ##
    nd_snp = nd_gt[: , 0 , :]
    nd_snp

    ##
    nd_snp = np.argmax(nd_snp , axis = 1)

    ##
    df_gt = pd.DataFrame(nd_snp , columns = [v.rs22])
    df_gt.value_counts()

    ##
    df_wgs_1 = pd.concat([df_iid , df_gt] , axis = 1)

    ##
    df_wgs_1.to_parquet(fp.wgs_rs22_processed , index = False)

    ##
    # high quality SNP
    bgn = open_bgen(fp.wgs_rs57)
    sample = bgn.samples

    ##
    _dct = {
            v.iid : sample
            }

    df_iid = pd.DataFrame(_dct)

    ##
    nd_gt = bgn.read()
    nd_gt.shape

    ##
    nd_snp = nd_gt[: , 0 , :]
    nd_snp

    ##
    nd_snp = np.argmax(nd_snp , axis = 1)

    ##
    df_gt = pd.DataFrame(nd_snp , columns = [v.rs57])
    df_gt.value_counts()

    ##
    df_wgs_2 = pd.concat([df_iid , df_gt] , axis = 1)

    ##
    df_wgs_2.to_parquet(fp.wgs_rs57_processed , index = False)

    ##


def combine_imputed_and_wgs_data() :
    pass

    ##
    d = Directory()
    fp = FilePath()
    v = Var()

    ##
    df_imp = pd.read_parquet(fp.processed_imputed_data)
    df_wgs_1 = pd.read_parquet(fp.wgs_rs22_processed)
    df_wgs_2 = pd.read_parquet(fp.wgs_rs57_processed)

    ##
    df = pd.merge(df_imp , df_wgs_1 , on = v.iid , suffixes = ('_imp' , '_wgs'))

    ##
    df = pd.merge(df , df_wgs_2 , on = v.iid , suffixes = ('_imp' , '_wgs'))

    ##
    df.to_parquet(fp.processed_data , index = False)

    ##


def process_combined_data() :
    pass

    ##
    d = Directory()
    fp = FilePath()
    v = Var()

    ##
    df = pd.read_csv(fp.rels)

    ##
    msk = df[v.inf_type].eq('FS')
    df = df[msk]

    ##
    df = df[[v.id1 , v.id2]]

    ##
    df = df.astype('string')

    ##
    df = df.drop_duplicates()

    ##
    df_gt = pd.read_parquet(fp.processed_data)

    ##
    # I assume ref allele is inverted in the WGS data
    # so I will invert the genotypes
    df_gt[v.rs22 + v.wgs] = 2 - df_gt[v.rs22 + v.wgs]
    df_gt[v.rs57 + v.wgs] = 2 - df_gt[v.rs57 + v.wgs]

    ##
    df[v.hw1] = df[v.id1].map(df_gt.set_index(v.iid)[v.rs57 + v.wgs])
    df[v.hw2] = df[v.id2].map(df_gt.set_index(v.iid)[v.rs57 + v.wgs])
    df[v.lw1] = df[v.id1].map(df_gt.set_index(v.iid)[v.rs22 + v.wgs])
    df[v.lw2] = df[v.id2].map(df_gt.set_index(v.iid)[v.rs22 + v.wgs])

    df[v.hi1] = df[v.id1].map(df_gt.set_index(v.iid)[v.rs57 + v.imp])
    df[v.hi2] = df[v.id2].map(df_gt.set_index(v.iid)[v.rs57 + v.imp])
    df[v.li1] = df[v.id1].map(df_gt.set_index(v.iid)[v.rs22 + v.imp])
    df[v.li2] = df[v.id2].map(df_gt.set_index(v.iid)[v.rs22 + v.imp])

    ##
    msk = df_gt[v.iid].eq('4401653')
    df_gt[msk]

    ##
    df[v.hws] = df[v.hw1] + df[v.hw2]
    df[v.lws] = df[v.lw1] + df[v.lw2]
    df[v.hwd] = df[v.hw1] - df[v.hw2]
    df[v.lwd] = df[v.lw1] - df[v.lw2]
    df[v.hid] = df[v.hi1] - df[v.hi2]
    df[v.lid] = df[v.li1] - df[v.li2]

    ##
    df.to_csv(fp.model_data , index = False)

    ##
    df_gt.describe()

    ##


def genotypes() :
    pass

    ##
    d = Directory()
    fp = FilePath()
    v = Var()

    ##
    df = pd.read_parquet(fp.processed_data)

    ##
    df[v.rs22 + v.wgs] = 2 - df[v.rs22 + v.wgs]
    df[v.rs57 + v.wgs] = 2 - df[v.rs57 + v.wgs]

    ##
    df.to_csv(fp.processed_data_csv , index = False)

    ##


    ##


    ##
