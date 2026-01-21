# Trajectory of a particle
The main goal of this project is to calculate the trajectory of a particle under the action of a magnetic field.

## Table of Contents
- [Overview](#Overview)
- [Using](#Using)
- [Particletracker functions](#Particletracker)


## Overview

This project is inspired by a proton accelerator system. Its purpose is to predict the trajectory of a proton as it passes through a magnetic dipole, which is used to alter its path. By adjusting particle and magnet parameters, this code can be applied to predict the motion of any particle in a magnetic field.

## Using
### Installing and running
Before executing the code, ensure that all required Python modules are installed. The dependencies are:
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [plotly](https://plotly.com/python/)
- [datetime](https://docs.python.org/3/library/datetime.html)

If any of these packages are missing, you can install them using *pip*. For example:

`pip install matplotlib numpy pandas plotly`

Once the dependencies are installed, download the main script (main_notebook.ipynb) from this repository. The code is provided as a Jupyter Notebook (.ipynb format), which means it was written for interactive execution.

To run the notebook:
- Open it in your preferred environment, such as Jupyter Notebook, JupyterLab, or VS Code with the Python extension.
- Execute the cells in order to perform the simulation.

## Particletracker

### particletracker.fileparser

**particletracker.fileparser.field_function_from_file**

`field_function_from_file(file_name, separator='\t', data_start=2)`

Parameters:
- **file_name: string**
Complete name of the file to be used (including the extension). The file needs to be in the same folder as the notebook.

- **separator: string**
Character representing the separator of the file to be read. It can be:

|   **Separator**   | **Character** |             **Description**             |
|:-----------------:|:-------------:|:---------------------------------------:|
|       Comma       |      ','      |           Standard CSV format           |
|        Tab        |      '\t'     |           Tab-separated values          |
|     Semicolon     |      ';'      |           European CSV format           |
|        Pipe       |      '\|'     |          Pipe-separated values          |
|       Space       |      ' '      |          Space-separated values         |
|       Colon       |      ':'      |          Colon-separated values         |
|  Multiple spaces  |     '\s+'     |       Regex for one or more spaces      |
|     Whitespace    |     '\s+'     | Any whitespace (spaces, tabs, newlines) |
|   Multiple tabs   |     '\t+'     |             One or more tabs            |
| Mixed spaces/tabs |    '[ \t]+'    |    Any combination of spaces and tabs   |
|    Custom regex   |     custom    |   Any regex patter matching your needs  |

### particletracker.newfield
### particletracker.trajanalysis
### particletracker.trajectory