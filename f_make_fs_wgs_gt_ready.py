"""


    """

import numpy as np
import pandas as pd
from pathlib import Path
from bgen_reader import open_bgen
import numpy as np


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

    rs28 = 'rs2844970'
    rs14 = 'rs144588527'
    rs28 = d.out_csf / rs28 / f'{rs28}.bgen'
    rs28_vcf = d.out_csf / f'rs2844970.vcf'
    fixed_rs28_vcf = d.out_csf / f'fixed_rs2844970.vcf'

    rs14 = d.out_csf / rs14 / f'{rs14}.bgen'
    rs14_vcf = d.out_csf / f'rs144588527.vcf'
    fixed_rs14_vcf = d.out_csf / f'fixed_rs144588527.vcf'

    imp = d.inp_csf / 'imputed_data/two_snps.bgen'
    fs = d.inp_csf / 'ukb_rel_with_infType_fs.csv'
    qualified_ids = d.inp_csf / 'qualified_iids.txt'


FP = FilePath()


class Var :
    iid = 'IID'
    id1 = 'ID1'
    id2 = 'ID2'


V = Var()


##
def prepare_wgs_gt() :
    """ """

    ##
    bgn = open_bgen(FP.rs28)

    ##
    sample = bgn.samples
    len(sample)

    ##
    df_iid = pd.DataFrame({
            V.iid : sample
            })

    ##
    nd_gt = bgn.read()
    nd_gt.shape

    ##
    nd_rs28 = nd_gt[: , 1 , :]
    nd_rs28

    ##
    nd_rs28 = np.argmax(nd_rs28 , axis = 1)

    ##
    df_gt = pd.DataFrame(nd_rs28 , columns = [FP.rs28.stem])

    df_gt.value_counts()

    ##
    df_rs_28 = pd.concat([df_iid , df_gt] , axis = 1)

    ##

    ##
    bgn_14 = open_bgen(FP.rs14)

    ##
    sample_14 = bgn_14.samples

    ##
    df_iid_14 = pd.DataFrame({
            V.iid : sample_14
            })

    ##
    nd_gt_14 = bgn_14.read()
    nd_gt_14.shape

    ##
    nd_rs14 = nd_gt_14[: , 0 , :]
    nd_rs14

    ##
    nd_rs14 = np.argmax(nd_rs14 , axis = 1)

    ##
    df_gt_14 = pd.DataFrame(nd_rs14 , columns = [FP.rs14.stem])

    ##
    df_rs_14 = pd.concat([df_iid_14 , df_gt_14] , axis = 1)

    ##

    ##
    df_wgs_gt = pd.merge(df_rs_28 , df_rs_14 , on = V.iid)

    ##


    ##
    bgn_imp = open_bgen(FP.imp)

    ##
    sample_imp = bgn_imp.samples
    sample_imp

    ##
    df_iid_imp = pd.DataFrame({
            V.iid : sample_imp
            })

    df_iid_imp[V.iid] = df_iid_imp[V.iid].str.split('_').str[1]

    ##
    nd_imp = bgn_imp.read()

    ##
    nd_rs28_imp = nd_imp[: , 0]

    ##
    nd_rs28_imp = np.argmax(nd_rs28_imp , axis = 1)

    ##
    df_rs28_gt_imp = pd.DataFrame(nd_rs28_imp , columns = [FP.rs28.stem])

    ##
    df_28_imp = pd.concat([df_iid_imp , df_rs28_gt_imp] , axis = 1)

    ##

    ##
    nd_rs14_imp = nd_imp[: , 1 , :]

    ##
    nd_rs14_imp = np.argmax(nd_rs14_imp , axis = 1)

    ##
    df_rs14_gt_imp = pd.DataFrame(nd_rs14_imp , columns = [FP.rs14.stem])

    ##
    df_14_imp = pd.concat([df_iid_imp , df_rs14_gt_imp] , axis = 1)

    ##


    ##
    df_imp = pd.merge(df_28_imp , df_14_imp , on = V.iid)

    ##


    ##
    df_fs = pd.read_csv(FP.fs)

    ##
    df_fs = df_fs[[V.id1 , V.id2]]

    ##
    df_fs = df_fs.astype('string')

    ##

    ##
    df_q_ids = pd.read_csv(FP.qualified_ids ,
                           header = None ,
                           dtype = 'string' ,
                           sep = '\t')

    ##

    ##
    msk = df_fs[V.id1].isin(df_q_ids[0])
    msk &= df_fs[V.id2].isin(df_q_ids[0])

    df_fs = df_fs[msk]

    ##

    ##
    df_gt = pd.merge(df_fs , df_wgs_gt , left_on = V.id1 , right_on = V.iid)

    df_gt = df_gt.drop(columns = V.iid)

    ##
    df_gt = df_gt.rename(columns = {
            FP.rs28.stem : 'w' + '_1_' + FP.rs28.stem
            })
    df_gt = df_gt.rename(columns = {
            FP.rs14.stem : 'w' + '_1_' + FP.rs14.stem
            })

    ##
    df_gt = pd.merge(df_gt , df_imp , left_on = V.id2 , right_on = V.iid)

    df_gt = df_gt.drop(columns = V.iid)

    df_gt = df_gt.rename(columns = {
            FP.rs28.stem : 'w' + '_2_' + FP.rs28.stem
            })
    df_gt = df_gt.rename(columns = {
            FP.rs14.stem : 'w' + '_2_' + FP.rs14.stem
            })

    ##
    df_gt = pd.merge(df_gt , df_imp , left_on = V.id1 , right_on = V.iid)

    ##
    df_gt = df_gt.drop(columns = V.iid)

    ##
    df_gt = df_gt.rename(columns = {
            FP.rs28.stem : 'i' + '_1_' + FP.rs28.stem
            })
    df_gt = df_gt.rename(columns = {
            FP.rs14.stem : 'i' + '_1_' + FP.rs14.stem
            })

    ##
    df_gt = pd.merge(df_gt , df_wgs_gt , left_on = V.id2 , right_on = V.iid)

    df_gt = df_gt.drop(columns = V.iid)

    ##
    df_gt = df_gt.rename(columns = {
            FP.rs28.stem : 'i' + '_2_' + FP.rs28.stem
            })

    df_gt = df_gt.rename(columns = {
            FP.rs14.stem : 'i' + '_2_' + FP.rs14.stem
            })

    ##
    df_gt1 = df_gt.copy()

    ##
    df_gt1['W1p2_rs28'] = df_gt1['w_1_rs2844970'] + df_gt1['w_2_rs2844970']
    df_gt1['W1p2_rs14'] = df_gt1['w_1_rs144588527'] + df_gt1['w_2_rs144588527']

    ##
    df_gt1['W1m2_rs28'] = df_gt1['w_1_rs2844970'] - df_gt1['w_2_rs2844970']
    df_gt1['W1m2_rs14'] = df_gt1['w_1_rs144588527'] - df_gt1['w_2_rs144588527']

    df_gt1['I1m2_rs28'] = df_gt1['i_1_rs2844970'] - df_gt1['i_2_rs2844970']
    df_gt1['I1m2_rs14'] = df_gt1['i_1_rs144588527'] - df_gt1['i_2_rs144588527']

    ##

    ##


    ##
    df_gt1.to_csv(D.out_csf / 'model_data.csv' , index = False)

    ##
    df_gt2 = df_gt1.copy()

    ##
    cols = df_gt2.columns

    ##
    cols

    ##
    c2k = ['w_1_rs2844970' , 'w_2_rs2844970' , 'i_1_rs2844970' ,
           'i_2_rs2844970']

    df_gt2 = df_gt2[c2k]

    ##
    for col in df_gt2.columns :
        print(df_gt2[col].value_counts())
        print(df_gt2[col].mean())

    ##
    df_gt2.describe()

    ##


    ##


    ##



    ##



    ##



    ##


    ##


    ##


    ##
