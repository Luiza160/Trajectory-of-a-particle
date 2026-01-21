import pandas as pd
import numpy as np

def generate_field_function(fields, I):
    b_field_1 = fields['field_functions'][0]
    b_field_2 = fields['field_functions'][1]
    I_1 = fields['I(A)'][0]
    I_2 = fields['I(A)'][1]

    def new_function(point):
        c1 = (I_2 - I) / (I_2 - I_1)
        c2 = (I - I_1) / (I_2 - I_1)

        point_ = np.array([point[0], point[1], point[-1]])

        return (c1*(b_field_1(point_)[0]) + c2*(b_field_2(point_)[0]),
                c1*(b_field_1(point_)[1]) + c2*(b_field_2(point_)[1]),
                c1*(b_field_1(point_)[2]) + c2*(b_field_2(point_)[2]))
    
    return new_function