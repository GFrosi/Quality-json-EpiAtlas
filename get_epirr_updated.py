import pandas as pd
import numpy as np
import sys


def map_dict_bio(df_epi_ihec, list_of_dict):

    list_col = ['EpiRR', 'EpiRR_status', 'age',
       'biomaterial_type', 'cell_type', 'donor_age_unit', 'donor_id',
       'donor_life_stage', 'health_state', 'line', 'markers', 'project',
       'sample_ontology_curie', 'sex', 'tissue_type', 'donor_health_status',
       'donor_health_status_ontology_curie', 'disease',
       'disease_ontology_curie']

    df_final = df_epi_ihec.copy()

    for col,dict_i in zip(list_col, list_of_dict):

        df_final[col] = df_final['epirr_id'].map(dict_i).fillna(df_final[col])

    df_final.to_csv('../script_add_keys_harmonizedv8ihec_json/ihec_metadata_plusv8_UPDATED.csv', index=False)


def generate_dict(df_merge):


    list_col = ['EpiRR', 'EpiRR_status', 'age',
       'biomaterial_type', 'cell_type', 'donor_age_unit', 'donor_id',
       'donor_life_stage', 'health_state', 'line', 'markers', 'project',
       'sample_ontology_curie', 'sex', 'tissue_type', 'donor_health_status',
       'donor_health_status_ontology_curie', 'disease',
       'disease_ontology_curie']

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


def main():

    df_epiatlas = pd.read_csv(sys.argv[1]) #3074
    df_ihec = pd.read_csv(sys.argv[2]) #2655 (v8)
    df_epi_ihec = pd.read_csv(sys.argv[3]) #epiatlas + v8 info 
    df_merge = create_dict_bio(df_epi_ihec, df_ihec)
    list_of_dict = generate_dict(df_merge)

    map_dict_bio(df_epi_ihec, list_of_dict)
    # print("Updated csv saved!")

    


if __name__ == "__main__":



    main()