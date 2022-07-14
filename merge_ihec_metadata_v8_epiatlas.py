import pandas as pd
import sys




def main():

    df_metadata = pd.read_csv(sys.argv[1]) #chipseq
    df_v8 = pd.read_csv(sys.argv[2]) #new version epimap
    df_merged = df_metadata.merge(df_v8, how='left', left_on='epirr_id', right_on='EpiRR')
    df_merged.to_csv('ihec_metadata_plusv9.csv', index=False)



if __name__ == "__main__":



    main()