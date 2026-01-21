import numpy as np

def e_field(x, y, z): 
      Ex = 0
      Ey = 0
      Ez = 0
      return Ex, Ey, Ez


# defines the magnetic field at each point
def b_field(x, y, z, interp_data, I):


    # this transformation is only necessary when the data given is in mm
    x_mm = x * 1000
    y_mm = y * 1000
    z_mm = z * 1000

    point = np.array([x_mm, y_mm, z_mm], dtype=float)

    # Call the function to get field tuple (Bx, By, Bz)
    field_tuple = interp_data(point)

    # Unpack the tuple (assuming it returns Bx, By, Bz in that order)
    Bx, By, Bz = (i * I for i in field_tuple)

    
    return Bx, By, Bz