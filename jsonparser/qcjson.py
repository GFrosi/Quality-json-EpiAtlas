import json
import sys
import os
import pandas as pd
import numpy as np
from tqdm import tqdm


def dict_json(path):
    '''It receives a root path 
    with json files and returns 
    a dict of dict per json file'''

    list_files = [file for file in os.listdir(path) if file.endswith('.json')] #just json files
    dict_epi = {} 
    
    for ele in tqdm(list_files):
        to_open = open(os.path.join(path,ele))
        json_f = json.load(to_open)
        k = ele #.split('4.')[1].split('.qc')[0] #getting EpiRR and UUID
        dict_epi[k] = {} #dict of dict per json file (sample)
                
        for dset in json_f:
            
            if 'overlap_reproducibility_qc' in dset:    #dict
                dict_epi[k]['reproducibility'] = json_f[dset].get('reproducibility') #get value reproducibility
               
            elif 'ctl_pbc_qc' in dset: #list of dict
                for i in json_f[dset]:
                    dict_epi[k]['PBC1_ctrl'] = i.get('PBC1')
                    dict_epi[k]['PBC2_ctrl'] = i.get('PBC2')
                    dict_epi[k]['NRF_ctrl'] = i.get('NRF')

            elif 'pbc_qc' == dset:
                for i in json_f[dset]: #list of dict
                    dict_epi[k]['PBC1'] = i.get('PBC1')
                    dict_epi[k]['PBC2'] = i.get('PBC2')
                    dict_epi[k]['NRF'] = i.get('NRF')

            elif 'xcor_score' in dset:
                for i in json_f[dset]:
                    dict_epi[k]['NSC'] = i.get('NSC')
                    dict_epi[k]['RSC'] = i.get('RSC')
                   
            elif 'jsd_qc' in dset:
                for i in json_f[dset]:
                    dict_epi[k]['JSD'] = i.get('jsd')
                  
            elif 'frip_macs2' in dset:
                dict_epi[k]['FRiP'] = json_f[dset]['rep1']['FRiP']
                

    return dict_epi


def create_df(dict_epi):
    '''It receives a dict 
    of dict and returns a 
    df'''

    df = pd.DataFrame.from_dict(dict_epi, orient='index').reset_index()

    return df


def class_cols(df):

    
    df1 = df.copy()
    list_lib_com = []
    list_idr = []
    list_enrich = []
    list_finger = []
    list_frip = []

    for index, row in df1.iterrows():

        #Library complexity conditional
        if (row['PBC1'] < 0.5) and (row['PBC2'] < 1) and (row['NRF'] < 0.5):
            list_lib_com.append('BAD')

        elif (0.5 <= row['PBC1'] < 0.8) and (1 <= row['PBC2'] < 3) and (0.5 <= row['NRF'] < 0.8):
            print('ACCEPTABLE PBC1:', row['PBC1'], 'PBC2:',row['PBC2'], 'NRF:', row['NRF'])
            list_lib_com.append('ACCEPTABLE')

        elif (0.8 <= row['PBC1'] < 0.9) and (3 <= row['PBC2'] < 10) and (0.8 <= row['NRF'] < 0.9):
            print('GOOD PBC1:', row['PBC1'], 'PBC2:',row['PBC2'], 'NRF:', row['NRF'])
            list_lib_com.append('GOOD')

        elif (row['PBC1'] >= 0.9) and (row['PBC2'] >= 10) and (row['NRF'] >= 0.9):
            print('IDEAL PBC1:', row['PBC1'], 'PBC2:',row['PBC2'], 'NRF:', row['NRF'])
            list_lib_com.append('IDEAL')

        else:
            print('ELSE PBC1:', row['PBC1'], 'PBC2:',row['PBC2'], 'NRF:', row['NRF'])
            list_lib_com.append('NOT IDENTIFIED')

        #IDR conditional
        if row['reproducibility'] == 'pass':
            list_idr.append('IDEAL')

        else:
            list_idr.append('BAD')

        #Enrichment conditional
        if row['NSC'] >= 1 and row['RSC'] >= 1: 
            list_enrich.append('IDEAL')

        else:
            list_enrich.append('BAD')
    
        #fingerprint conditional
        if row['JSD'] >= 0.5 : 
            list_finger.append('IDEAL')

        else:
            list_finger.append('BAD') 

        #FRiP conditional
        if row['FRiP'] >= 0.1 : 
            list_frip.append('IDEAL')

        else:
            list_frip.append('BAD') 
    

    #creating columns
    df1['Library_complexity'] = list_lib_com
    df1['IDR'] = list_idr
    df1['Enrichment'] = list_enrich
    df1['Fingerprint'] = list_finger
    df1['FRiP_quality'] = list_frip


    return df1


def quality_col(df1):
    '''It receives a df1 
    with subclasses of quality
    and returns a new df including
    the quality control col'''

    df2 = df1.copy()

    df2['Quality'] = np.where((df2['Library_complexity'] == 'IDEAL') &
    (df2['IDR'] == 'IDEAL') &
    (df2['Enrichment'] == 'IDEAL') &
    (df2['FRiP_quality'] == 'IDEAL') &
    (df2['Fingerprint'] == 'IDEAL'), 'IDEAL',
    np.where((df2['Library_complexity'] == 'GOOD') &
    (df2['IDR'] == 'IDEAL') &
    (df2['Enrichment'] == 'IDEAL') &
    (df2['FRiP_quality'] == 'IDEAL') &
    (df2['Fingerprint'] == 'IDEAL'), 'GOOD',
    np.where((df2['Library_complexity'] == 'ACCEPTABLE') &
    (df2['IDR'] == 'IDEAL') &
    (df2['Enrichment'] == 'IDEAL') &
    (df2['FRiP_quality'] == 'IDEAL') &
    (df2['Fingerprint'] == 'IDEAL'), 'ACCEPTABLE',
    np.where((df2['Library_complexity'] == 'NOT IDENTIFIED') &
    (df2['IDR'] == 'IDEAL') &
    (df2['Enrichment'] == 'IDEAL') &
    (df2['FRiP_quality'] == 'IDEAL') &
    (df2['Fingerprint'] == 'IDEAL'), 'TO CHECK', 'BAD'))))
    

    return df2


