import numpy as np
from scipy.interpolate import LinearNDInterpolator
import warnings
warnings.filterwarnings("ignore")


# creates the interpolator
def create_interpolators(df, I0):
    
    I0 = float(I0)
    bx = np.array(df["Bx_T"], dtype=float)
    by = np.array(df["By_T"], dtype=float)
    bz = np.array(df["Bz_T"], dtype=float)


    bx_norm = (bx / I0).tolist()
    by_norm = (by / I0).tolist()
    bz_norm = (bz / I0).tolist()


    grade = list(zip(df['x_mm'], df['z_mm']))


    # creates functions to define each field component
    fbx_plano = LinearNDInterpolator(grade, bx_norm, fill_value=0)
    fby_plano = LinearNDInterpolator(grade, by_norm, fill_value=0)
    fbz_plano = LinearNDInterpolator(grade, bz_norm, fill_value=0)   


    def interp_func(point):
        # Note: your original code uses only x and z coordinates (2D interpolation)
        point_ = np.array([point[0], point[2]])
        
        return (
            float(fbx_plano(point_)), 
            float(fby_plano(point_)),
            float(fbz_plano(point_))
        )
    

    return interp_func


