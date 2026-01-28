import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from scipy.integrate import simpson

from particletracker.fileparser import field_function_from_file
from particletracker.trajectory import solve_trajectory
from particletracker.trajanalysis import show_deviation_degree, show_deviation_in_Z



def finalposition_angle(desired_degree, files, currents, m, q, 
                        x0, y0, z0, v_direction, Ec0, e_field,
                        method, step, total_t, traj_distance):
    data = []
    areas = []

    for file, current in zip(files, currents):
        Ec0 = 2
        print('-'*30)
        print(f'CURRENT CASE: {current} A')
        print('-'*30)

        b_field = field_function_from_file(file, '\t', 17)

        # run the simulation
        traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

        dev_degree = show_deviation_degree(traj, traj_distance)

        print(f' Energy is: {Ec0}')


        while abs(dev_degree) < desired_degree:

            Ec0 = Ec0 - 0.15

            # run the simulation
            traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

            dev_degree = show_deviation_degree(traj, traj_distance)

            print(f' Energy is: {Ec0}')

        if abs(dev_degree) > desired_degree:
            while abs(dev_degree) > desired_degree:

                Ec0 = Ec0 + 0.01                  # run the simulation
                traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

                dev_degree = show_deviation_degree(traj, traj_distance)

                print(f' Energy is: {Ec0}')


        if abs(dev_degree) < desired_degree:
            while abs(dev_degree) < desired_degree:

                Ec0 = Ec0 - 0.001                  # run the simulation
                traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

                dev_degree = show_deviation_degree(traj, traj_distance)

                print(f' Energy is: {Ec0}')

        data += [[current, Ec0]]

        By = traj['By(T)'].tolist()
        factor1 = 10000
        By = [round(x * factor1, 3) for x in By]
        S = traj['S(m)'].tolist()
        factor2 = 100
        S = [round(x * factor2, 3) for x in S]

        area = float(simpson(By, S))  # Simpson's rule
        print(f' Area = {area}')
        
        areas.append(area)

    chart = pd.DataFrame(data, columns=["Current(A)", "Energy(MeV)"])

    return chart, areas, traj, S, By





def finalposition_distance(desired_x, desired_z, files, currents, m, q, 
                            x0, y0, z0, v_direction, Ec0, e_field,
                            method, step, total_t):

    data = []
    areas = []

    for file, current in zip(files, currents):
        print('-'*30)
        print(f'CURRENT CASE: {current} A')
        print('-'*30)

        b_field = field_function_from_file(file, '\t', 17)

        traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

        final_x = show_deviation_in_Z(traj, desired_z)

        print(f' Energy is: {Ec0}')


        while final_x < desired_x:

            Ec0 = Ec0 + 0.1

            traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

            final_x = show_deviation_in_Z(traj, desired_z)

            print(f' Energy is: {Ec0}')

        if final_x > desired_x:
            while final_x > desired_x:

                Ec0 = Ec0 - 0.01               
                traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

                final_x = show_deviation_in_Z(traj, desired_z)

                print(f' Energy is: {Ec0}')


        if final_x < desired_x:
            while final_x < desired_x:

                Ec0 = Ec0 + 0.001          
                traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

                final_x = show_deviation_in_Z(traj, desired_z)

                print(f' Energy is: {Ec0}')


        
        if final_x > desired_x:
            while final_x > desired_x:

                Ec0 = Ec0 - 0.0001        
                traj = solve_trajectory(m, q, 
                                x0, y0, z0, v_direction, Ec0,
                                b_field, e_field,
                                method, step, total_t, 
                                output_file='traj_calculation_results')

                final_x = show_deviation_in_Z(traj, desired_z)

                print(f' Energy is: {Ec0}')


        By = traj['By(T)'].tolist()
        factor1 = 10000
        By = [round(x * factor1, 3) for x in By]
        S = traj['S(m)'].tolist()
        factor2 = 100
        S = [round(x * factor2, 3) for x in S]

        area = float(simpson(By, S))  # Simpson's rule
        print(f' Area = {area}')

        data += [[current, Ec0]]
        areas.append(area)

    chart = pd.DataFrame(data, columns=["Current(A)", "Energy(MeV)"])

    return chart, areas, traj, S, By