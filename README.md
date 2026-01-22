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

- Parameters:
    - **file_name: string**
    Complete name of the file to be used (including the extension). The file needs to be in the same folder as the notebook.

    - **separator: string**
    Character representing the separator of the file to be read. If not specified, uses tab separator ('\t'). The separators can be:

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

    - **data_start: integer**
    Line of the file where the data starts (without column names). If not specified, the standard value is 2.

- Returns:
    
    Returns a tuple containing the magnetic field function of each axis (x, y and z, respectively)

### particletracker.newfield

**particletracker.newfield.generate_field_function**

`generate_field_function(fields, I)`

- Parameters:
    - **fields: dictionary**
    A dictionary containing the data to be used to discover the new field. To calculate this, you need two different field maps. The dictionary need to have this structure:

    {'field_functions': [(field_function01), (field_function02)],
    'I(A)': [(current01), (current02)]}

    Where the field function is the function that describes a known magnetic field (can be found using *.fileparser* function) and the current is the current associated with this magnetic field.

    - **I: scalar**
    The current associated with the field you want to calculate.

- Returns:
    
    Returns a tuple containing each axis of the magnetic field function of the new field calculated.

### particletracker.trajanalysis

**particletracker.trajanalysis.plot_2d_trajectory**

`plot_2d_trajectory(df, total_t, traj_distance)`

- Parameters:
    - **df: DataFrame**
    A DataFrame containing the particle's trajectory informations. The DataFrame needs to have at least these columns: 'z(m)', 'y(m)', 'x(m)' and 'Bx(T)'. 

    This DataFrame can be obtained using *.trajectory.solve_trajectory* function.

    - **total_t: scalar**
    A scalar representing total elapsed time of the simulation. 

    - **xpoint, zpoint: scalar**
    A scalar representing the coordinate where the detector is located.

- Returns:

Returns 4 graphs, containing, respectively:

XZ trajectory;

ZY trajectory;

X trajectory;

Bx intensity along Z trajectory

**particletracker.trajanalysis.plot_3d_trajectory**

`plot_3d_trajectory(df, traj_distance)`

- Parameters:

    - **df: DataFrame**
    A DataFrame containing the particle's trajectory informations. The DataFrame needs to have at least these columns: 'z(m)', 'y(m)' and 'x(m)'. 

    - **traj_distance: scalar**
    A scalar representing the total distance traveled by the particle.

- Returns:

Returns an interactive 3D graph, showing the trajectory on all coordinates.

**particletracker.trajanalysis.show_deviation_degree**

`show_deviation_degree(df, traj_distance)`

- Parameters:

    - **df: DataFrame**
    A DataFrame containing the particle's trajectory informations. The DataFrame needs to have at least these columns: 'z(m)', 'y(m)' and 'x(m)'. 

    - **traj_distance: scalar**
    A scalar representing the total distance traveled by the particle.

- Returns:

Returns the deviation degree along XZ axis (horizntal deviation).

**particletracker.trajanalysis.show_deviation_in_Z**

`show_deviation_in_Z(df, final_z)`

- Parameters:

    - **df: DataFrame**
    A DataFrame containing the particle's trajectory informations. The DataFrame needs to have at least these columns: 'z(m)' and 'x(m)'. 

    - **final_z: scalar**
    A scalar representing the Z-coordinate where the detector is located.

- Returns:

Returns the final X-coordinate value, that should correspond to the coordinate of the detector.

### particletracker.trajectory

**particletracker.trajectory.solve_trajectory**

`solve_trajectory(m, q, x0, y0, z0, v_direction, Ec0, b_field, e_field, method, step, total_t, output_file='traj_calculation_results')`

- Parameters:
    - **m: scalar**
    Scalar representing the mass of the particle (unit: MeV/c²).
    
    - **q: scalar**
    Scalar representing the elementary charge of the particle (it can be 1 if the particle id a proton or -1 if the particle is a electron).
    
    - **x0, y0, z0: scalar**
    Three different scalars representing the inital coordinates of the particle's trajectory (unit: m).
    
    - **v_direction: list**
    List representing the velocity vector of the particle. It is used to define the velocity's angulation, not the velocity's magnitude.
    
    - **Ec0: scalar**
    Scalar representing particle's initial energy (unit: MeV).
    
    - **b_field: a**
    
    - **e_field: a**
    
    - **method: string**
    String specifying the iteration method that will be used. It can be 'boris' or 'rk4'.
    
    - **step: scalar**
    Scalar representing the time step that will be used to calculate the iterations. It can be a value (for exalmple $10^{-6}$ seconds) or a ratio (a fraction of the total elapsed time). 
    
    - **total_t: scalar**
    Scalar representing the total elapsed time of the simulation (unit: s)
    
    - **output_file: string**
    String containing the name of the file to be saved. This file contains all the informations about the trajectory of the particle. If not specified, saves with the standard name: 'traj_calculation_results'.

- Returns:

    Returns a DataFrame containing all the trajectory data.

**particletracker.trajectory.rk4**

`rk4(x, y, z, Vx, Vy, Vz, step, b_field, e_field, c, m, q)`



- Parameters:

    - **x, y, z: scalar**


    - **Vx, Vy, Vz: scalar**


    - **step: scalar**
    Scalar representing the time step that will be used to calculate the iterations. It can be a value (for exalmple $10^{-6}$ seconds) or a ratio (a fraction of the total elapsed time).
    
    - **b_field: a**
    
    - **e_field: a**
    
    - **c: scalar**
    Scalar representing the speed of light. The standard value is $2.99792458^8$
    
    - **m: scalar**
    Scalar representing the mass of the particle (unit: MeV/c²).

    - **q: scalar**
    Scalar representing the elementary charge of the particle (it can be 1 if the particle id a proton or -1 if the particle is a electron).

- Returns:

**particletracker.trajectory.boris**

`boris(x, y, z, Vx, Vy, Vz, step, c, q, m, e_field, b_field)`

- Parameters:

    - **x, y, z: scalar**
    
    - **Vx, Vy, Vz: scalar**
    
    - **step: scalar**
    Scalar representing the time step that will be used to calculate the iterations. It can be a value (for exalmple $10^{-6}$ seconds) or a ratio (a fraction of the total elapsed time).
    
    - **c: scalar**
    
    - **q: scalar**
    Scalar representing the elementary charge of the particle (it can be 1 if the particle id a proton or -1 if the particle is a electron).
    
    - **m: scalar**
    Scalar representing the mass of the particle (unit: MeV/c²).

    - **e_field: a**
    
    - **b_field: a**

- Returns: