import argparse
import os
import sys
from jsonparser import qcjson as qj



def main():

    dict_json = qj.dict_json(args.path_json)
    df = qj.create_df(dict_json)
    df_classes = qj.class_cols(df)
    df_final = qj.quality_col(df_classes)
    df_final.to_csv(args.out, index=False)


if __name__ == "__main__":



    parser = argparse.ArgumentParser(

        description="A script to parse json.qc files from EpiAtlas. It returns a dataframe with the IHEC quality metrics"
    )

    parser.add_argument('-p', '--path_json',
                        help='The absolut path to the json.qc files',
                        required=True
                        )

    parser.add_argument('-o', '--out',
                        help='The absolut path to the output files',
                        required=True
                        )
    
    args = parser.parse_args()
    
    main()