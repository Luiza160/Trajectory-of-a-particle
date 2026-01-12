import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


# creates the interpolator
def create_interpolators(df):
    
    grade = list(zip(df['x_mm'], df['z_mm']))


    # creates functions to define each field component
    fbx_plano = LinearNDInterpolator(grade, df['Bx_T'], fill_value=0)
    fby_plano = LinearNDInterpolator(grade, df['By_T'], fill_value=0)
    fbz_plano = LinearNDInterpolator(grade, df['Bz_T'], fill_value=0)   


    def interp_func(point):
        # Note: your original code uses only x and z coordinates (2D interpolation)
        point_ = np.array([point[0], point[2]])
        
        return (
            float(fbx_plano(point_)), 
            float(fby_plano(point_)),
            float(fbz_plano(point_))
        )
    

    return interp_func


