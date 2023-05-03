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

From Anaconda you can do that in a graphical way:

* open Anaconda Navigator
* go to the Environments tab
* click the Update Index... button
* select "All" instead of "Installed" in the menu
* search for the aforementioned packages and select them for the installation
* click on Apply for installing them

If you are not using Anaconda, you can install them with:

```
pip install -U tabula-py
pip install -U openpyxl
```

## Installation

Just download the main file `RNT-analyisis.py` from this repository.

## Usage

### Prerequisites

A RNT file as PDF named as `RNT_YYYYMM.pdf` (for example `RNT_202305.pdf`) and a XLSX file with a column with IPFidentification codes from the workers (if some codes are missing, these data will not be looked for in the RNT PDF).

### With graphical interface

Just double click on the `RNT-analyisis.py` file.

A prompt should ask you for the RNT PDF file. The RNT file has to be named like `RNT_YYYYMM.pdf` for example `RNT_202209.pdf`. Once chosen that, another prompt should ask you for the XLSX spreadsheet with the workers' data (IPF and name).

A new file will be created with a name like `analysis_RNT_YYYYMM.xlsx` for example `analysis_RNT_202209.xlsx`.

### With command line

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

## Running on example files

In this repository, you can find an example of RNT PDF file here [RNT_202012.pdf](RNT_202012.pdf) and an example of initial XLSX file here [analysis_RNT_202011.xlsx](analysis_RNT_202011.xlsx).

As you can see, the XLSX file has to have at least the IPF column. For convenience, we would recommend to have also columns like CAS, name, work position etc.

In the RNT PDF you will see IPFs starting with 10, to which a DNI number follows; starting with 20, to which a passport number follows (usually temporary before getting a NIE); and 60, to which a NIE number follows.

When you run the script launching:

```
python3 RNT-analyisis.py RNT_202012.pdf  analysis_RNT_202011.xlsx
```

A new file will be created, with the name `analysis_RNT_202012.xlsx`. In this file you will find all the content of the original XLSX file but also a new column with the yearly salary estimated from the content of the `RNT_202012.pdf` file. Using the example PDF, you will get wrong numbers, likely due to the censoring we performed on the PDF.

Also you will get an output text like this:

```
        I.P.F. C.A.F.
0  1099999999E  NULAS
```

This means that this worker exists in the PDF but has not been found in the XLSX file.

