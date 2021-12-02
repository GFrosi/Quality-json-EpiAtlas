# Quality-json-EpiAtlas
Script to compile and classify the quality of the samples analyzed by the IHEC pipeline from EpiAltas project


# Requiremets

```python > 3.0``` and ```create a env with requirements.txt```


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
  -o OUT, --out OUT     The absolut path to the output table
  
  ```