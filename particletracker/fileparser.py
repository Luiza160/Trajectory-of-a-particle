import numpy as np
import pandas as pd
import re
from scipy.interpolate import LinearNDInterpolator

import warnings
warnings.filterwarnings("ignore")

def field_function_from_file(file_name, separator='\t', data_start=2):

    # data import
    df = pd.read_csv(file_name, sep=separator, skiprows=(data_start-1))
    # some adjusts
    df = df.dropna(axis=1)
    df = df.set_axis(["x_mm", "y_mm", "z_mm", "Bx_T", "By_T", "Bz_T"], axis=1)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()

    df['x_mm'] = df['x_mm'].apply(lambda x:x/1000)
    df['y_mm'] = df['y_mm'].apply(lambda x:x/1000)
    df['z_mm'] = df['z_mm'].apply(lambda x:x/1000)

    Bx_values = np.array(df["Bx_T"], dtype=float)
    By_values = np.array(df["By_T"], dtype=float)
    Bz_values = np.array(df["Bz_T"], dtype=float)

    count_y = df.value_counts(df['y_mm'])

    if count_y.shape[0] == 1:

        grid = list(zip(df['x_mm'], df['z_mm']))

        # creates functions to define each field component
        fbx = LinearNDInterpolator(grid, Bx_values, fill_value=0)
        fby = LinearNDInterpolator(grid, By_values, fill_value=0)
        fbz = LinearNDInterpolator(grid, Bz_values, fill_value=0)   


        def interp_func(point):
            point_ = np.array([point[0], point[2]])

            return (float(fbx(point_)),
                    float(fby(point_)),
                    float(fbz(point_)))
        
        return interp_func


    else:

        grid = list(zip(df['x_mm'], df['y_mm'], df['z_mm']))

        # creates functions to define each field component
        fbx = LinearNDInterpolator(grid, Bx_values, fill_value=0)
        fby = LinearNDInterpolator(grid, By_values, fill_value=0)
        fbz = LinearNDInterpolator(grid, Bz_values, fill_value=0)   


        def interp_func(point):
            point_ = np.array([point[0], point[1], point[2]])

            return (float(fbx(point_)),
                    float(fby(point_)),
                    float(fbz(point_)))
        
        return interp_func


