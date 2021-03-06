

# Quality-json-EpiAtlas
Script to compile and classify the quality of the samples analyzed by the IHEC pipeline from EpiAltas project


# Requiremets

```python > 3.0``` and ```create a env with requirements.txt```

## These scripts should be used to improve/complete the csv/json files generated by EpiLaP tool. 


### Usage


#### main.py

```
usage: main.py [-h] -p PATH_JSON -o OUT

A script to parse json.qc files from EpiAtlas. It returns a dataframe with the
IHEC quality metrics

optional arguments:
  -h, --help            show this help message and exit
  -p PATH_JSON, --path_json PATH_JSON
                        The absolut path to the json.qc files
  -o OUT, --out OUT     The absolut path to the output files

```


#### merge_quality.py

```
Command line: python merge_quality.py -q result.csv -e EpiAtlas20_21_predicted_col.csv -o EpiAtlas20-21-quality.csv

```
usage: merge_quality.py [-h] -q QUALITY -e EPILAP -o OUT

A script to merge the quality table from EpiAtlas and the EpiLaP prediction
table

optional arguments:
  -h, --help            show this help message and exit
  -q QUALITY, --quality QUALITY
                        The absolut path to the quality metrics table
  -e EPILAP, --epilap EPILAP
                        The absolut path to the epilap predicted table
  -o OUT, --out OUT     The absolut path to the output table```


#### concat_qc.py

```
Command line: python EpiAtlas20-21-quality.csv EpiAtlas22-quality.csv

A script to concat by columns two dataframes. They were generated by main.py and merge_quality.py scripts. 

```


### get_publish_release_col_IHEC.py

```
Command line: python get_publish_release_col_IHEC.py hg38_2020_match_md5_epiatlas_until_2022.txt hg38_2020-10_report.tsv EpiAtlas20-21-22-quality.csv

A script to add the 'publishing_group' and 'releasing_group' columns to 
the EpiAtlas-quality file (after concat_qc.py, if it is necessary)
```


##########################################################################

          Adding additional metadata information to EpiAtlas QC table / json

##########################################################################


- script_add_keys_harmonizedv8ihec_json
### merge_ihec_metadata_v8_epiatlas.py

```
Command line: python merge_ihec_metadata_v8_epiatlas.py ../metadata/ihec_metadata.csv ../metadata/IHEC_metadata_harmonization.v0.8.csv

A script to generate merge the ihec_metadata.csv and the v8 from "https://github.com/IHEC/epimap-metadata-harmonization"
```


### get_epirr_update.py

```
Command line:  python get_epirr_updated.py ihec_metadata.csv IHEC_metadata_harmonization.v0.8.csv ihec_metadata_plusv8.csv

A script to generate a df with updated metadata information based on EpiRR id, ignoring the version (e.g some EpiRR in ihec_metadata have an older version compared with IHEC_metadata_harmonization.v0.8.csv). The new Updated table can be used to generate an updated EpiAtlas.json file (epiatlas.py - EpiLaP)

```


