# Quality-json-EpiAtlas
Script to compile and classify the quality of the samples analyzed by the IHEC pipeline from EpiAltas project


# Requiremets

```python > 3.0``` and ```create a env with requirements.txt```


### Usage

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