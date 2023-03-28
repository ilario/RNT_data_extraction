# RNT_data_extraction
Extracting data from PDF of Relación Nominal de Trabajadores (RNT) from Spanish Seguridad Social, written in Python

## Requirements

### Python
Obviously, you will need Python.

In Linux you surely already have it.

In the other operating systems you can [install Anaconda](https://www.anaconda.com/products/distribution#Downloads), for example.

### Virtual environment

If you know what a virtual environment is, means that you need it: you should use it.

If you don't know what it is, but you develop and use custom Python stuff: use it.

Otherwise, don't worry, you can go on without using it.

### Python's additional packages

You will need to install the following additional packages:

* tabula-py
* openpyxl

From Anaconda you can do that in a graphical way.

If you are not using Anaconda, you can install them with:

```
pip install -U tabula-py
pip install -U openpyxl
```

## Installation

Just download the main file `RNT-analyisis.py` from this repository.

## Usage

Execute the `RNT-analyisis.py` file providing as the first argument the PDF of the RNT and as a second argument a XLSX spreadsheet.

The filename of the PDF have to follow this format: `RNT_YYYYMM.pdf`, for example `RNTs/2023/RNT_202301.pdf`.

The spreadsheet needs to have at least a `CAS` and a `IPF` columns for the worker's identification. The other columns and their content will be preserved. For example, the gender and position columns can be added for analyzing the presence of inequalities in the salaries across genders and positions.

The python script will create a new column with the estimated gross salary. It will not show salaries over some threshold, around 48k. This will be stored in a new XLSX file named `analysis_RNT_YYYYMM.xlsx` with the year and month from the input PDF file.

The typical way to use the script is something like this:

```
...create a analysis_RNT_202111.xlsx file with at least the CAS and IPF columns of the workers...
python3 RNT-analyisis.py RNTs/2021/RNT_202112.pdf  analysis_RNT_202111.xlsx
python3 RNT-analyisis.py RNTs/2022/RNT_202201.pdf  analysis_RNT_202112.xlsx
python3 RNT-analyisis.py RNTs/2022/RNT_202202.pdf  analysis_RNT_202201.xlsx
python3 RNT-analyisis.py RNTs/2022/RNT_202203.pdf  analysis_RNT_202202.xlsx
```

where each command takes the output of the previous one and add a column for the newly processed RNT.
