import pandas as pd
import numpy as np
import sys


def map_new_celltype(df_map, df_newct):
    """Receives two dfs (df map - generated
    by map_dict_bio funcion), and a df
    including the new CellType terms.
    Returns a df with updated info"""

    #dict new cell_types
    dict_ct = dict(zip(df_newct['sample_ontology_term'], df_newct['final'].str.lower()))
    #mapping new cell_types
    df_map['cell_type'] = df_map['sample_ontology_term'].map(dict_ct)
    # df_map.to_csv('../script_add_keys_harmonizedv8ihec_json/ihec_metadata_dfreeze_wgbs_plusv9_UPDATED_newCT.csv', index=False)
    df_map.to_csv('ihec_metadata_dfreeze_wgbs_plusv9_UPDATED_newCT.csv', index=False)


def map_dict_bio(df_epi_ihec, list_col, list_of_dict):
    """Receives a df and a list of dict. Returns
    the desired fields (cols) with updated metadata
    info"""


    df_final = df_epi_ihec.copy()

    for col,dict_i in zip(list_col, list_of_dict):

        df_final[col] = df_final['epirr_id'].map(dict_i).fillna(df_final[col])

    # df_final.to_csv('../script_add_keys_harmonizedv8ihec_json/ihec_metadata_dfreeze_wgbs_plusv9_UPDATED.csv', index=False)
    df_final.to_csv('ihec_metadata_dfreeze_wgbs_plusv9_UPDATED.csv', index=False)

    return df_final


def generate_dict(df_merge, list_col):
    """Receives a df and returns
    a list of dicts."""


    list_of_dict = []

    for col in list_col:

        name_dict = 'dict_' + col
        name_dict = {k:v for k,v in zip(df_merge['epirr_id'], df_merge[col])}
        list_of_dict.append(name_dict)

    return list_of_dict
        
        
def create_dict_bio(df_epi_ihec, df_ihec):
    """Receives two dfs and returns a dict
    with epirr_id as keys and biomaterial_type
    as values"""

    #generating df with epirr no match version
    df_nan = filter_epirr_to_update(df_epi_ihec)
    df_nan['EPIRR_no_v'] = df_nan['epirr_id'].str.split('.').str[0] #from epiatlas

    #df ihec no version to merge with df nan
    df_ihec['EpiRR_IHEC_no_v'] = df_ihec['EpiRR'].str.split('.').str[0]

    #merging dfs to get the biomaterial info
    df_merge = df_nan.merge(df_ihec, how='left', left_on='EPIRR_no_v', right_on='EpiRR_IHEC_no_v')
    df_merge = df_merge.rename(columns={col:col.split('_y')[0] for col in df_merge.columns})
    df_merge = df_merge.loc[:, ~df_merge.columns.str.contains('_x')]

    #saving to check
    # df_merge.to_csv('../script_add_keys_harmonizedv8ihec_json/ihec_metadata_plusv8_525_biomaterial_updated.csv', index=False)

    return df_merge


def filter_epirr_to_update(df_epi_ihec):
    """Receives a df (ihec_metadata_plus_v8)
    and return a filtered df by biomaterial_type
    column containing nan values"""

    return df_epi_ihec[df_epi_ihec['biomaterial_type'].isnull()] #column completly filled in v8


def merge_version_metadata(df_epiatlas, df_ihec):

    df_epi_ihec = df_epiatlas.merge(df_ihec, how='left', left_on='epirr_id', right_on='EpiRR')
    df_epi_ihec.to_csv('ihec_metadata_dfreze_wgbs_plusv9.csv', index=False)

    return df_epi_ihec



def main():

    df_epiatlas = pd.read_csv(sys.argv[1]) #3074 #ihec metadata
    df_ihec = pd.read_csv(sys.argv[2]) #2655 (v8) #update to use v9
    list_col = list(df_ihec.columns)
    # df_epi_ihec = pd.read_csv(sys.argv[3]) #epiatlas + v8 info (run first merge_ihec_metadata_v8)
    df_epi_ihec = merge_version_metadata(df_epiatlas, df_ihec)
    df_newct = pd.read_csv(sys.argv[3]) #df including old sample_ontology_terms and final col (new celltypes)
    df_merge = create_dict_bio(df_epi_ihec, df_ihec)
    list_of_dict = generate_dict(df_merge, list_col)
    df_map = map_dict_bio(df_epi_ihec, list_col ,list_of_dict)

    map_new_celltype(df_map, df_newct)
    # print("Updated csv saved!")

    


if __name__ == "__main__":



    main()
