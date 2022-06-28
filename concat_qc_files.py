import pandas as pd
import sys


"""Run this script after qc_json (main.py) and merge quality"""

def drop_cols(df_epi_20_21):
    """Receives a df including error and max cols
    (EpiLaP). Returns a df without error and max cols"""

    df_epi_20_21 = df_epi_20_21.drop(['error', 'max'], axis=1)
    
    return df_epi_20_21


def concat_dfs(df_epi_20_21, df_epi_22):
    """Receives two dfs, and returns a 
    concatenated df by columns including all
    QC metrics"""

    df_epi_20_21 = drop_cols(df_epi_20_21)

    cols = ['Sample', 'md5sum', 'epirr_id', 'uuid', 'track_type',
       'data_generating_centre', 'class', 'Predicted_CT', 'chromatin_acc',
       'ctcf', 'ep300', 'h3k27ac', 'h3k27me3', 'h3k36me3', 'h3k4me1',
       'h3k4me3', 'h3k9ac', 'h3k9me3', 'input', 'mrna_seq', 'polr2a',
       'polr2aphosphos5', 'rna_seq', 'smrna_seq', 'wgb_seq', 'index', 'PBC1',
       'PBC2', 'NRF', 'PBC1_ctrl', 'PBC2_ctrl', 'NRF_ctrl', 'reproducibility',
       'NSC', 'RSC', 'FRiP', 'JSD', 'Library_complexity', 'IDR', 'Enrichment',
       'Fingerprint', 'Quality']

    df_epi_20_21 = df_epi_20_21[cols]
    df_epi_22 = df_epi_22[cols]

    return pd.concat([df_epi_20_21,df_epi_22])



def main():

    df_epi_20_21 = pd.read_csv(sys.argv[1]) #EpiAtlas20-21-quality.csv
    df_epi_22 = pd.read_csv(sys.argv[2]) #epilap_qc_2022.csv
    df_qc = concat_dfs(df_epi_20_21, df_epi_22)
    df_qc.to_csv('EpiAtlas20-21-22-quality.csv') #output


if __name__ == "__main__":


    main()