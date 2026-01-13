import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")



def solve_trajectory(m, q, 
                    x0, y0, z0, I,
                    b_field, e_field, 
                    create_interpolators, rk4, boris, flat_trajectory, deviation_degree, three_dimensional_trajectory, field_plot,
                    Ec0, v_direction, 
                    step, total_t, 
                    output_file, output_graphic, txt_name, file_name, magnet_name, traj_distance, 
                    method, current):

    # define some physical constants
    c = 2.99792458e8      # light speed (m/s)
    gamma = 1.0 + (Ec0 / m)
    conv_v = (np.sqrt(1.0 - 1.0/(gamma**2))) * c  # converted speed (m/s)



    # convert and normalize velocity direction
    ux = v_direction[0]
    uy = v_direction[1]
    uz = v_direction[2]
    u = np.array([ux, uy, uz], dtype=float)
    u_hat = u / np.linalg.norm(u)
    Vx, Vy, Vz = conv_v * u_hat          # x, y and z velocitys (m/s)


    x, y, z = x0, y0, z0       # initial position


    # data import
    df = pd.read_csv(file_name, sep="\t", skiprows=15)   # skiprows=15 only in this case!
    # some adjusts (also only in this case!)
    df.drop(index=[0], inplace=True)
    df = df.dropna(axis=1)
    df = df.set_axis(["x_mm", "y_mm", "z_mm", "Bx_T", "By_T", "Bz_T"], axis=1)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()


    # calls the interpolator function only once, so the code runs faster
    interp_data = create_interpolators(df, current)


    # define arrays to store the results
    num_steps = int(total_t/step)
    x_vals = np.zeros(num_steps)
    y_vals = np.zeros(num_steps)
    z_vals = np.zeros(num_steps)
    Vx_vals = np.zeros(num_steps)
    Vy_vals = np.zeros(num_steps)
    Vz_vals = np.zeros(num_steps)
    t_vals = np.zeros(num_steps)
    Bx_vals = np.zeros(num_steps) 
    By_vals = np.zeros(num_steps)
    Bz_vals = np.zeros(num_steps)


    # main loop
    for i in range(num_steps):
        x_vals[i], y_vals[i], z_vals[i] = x, y, z                             # instant position
        Vx_vals[i], Vy_vals[i], Vz_vals[i] = Vx, Vy, Vz                       # instant velocity
        t_vals[i] = i*step                                                    # instant of time
        Bx_vals[i], By_vals[i], Bz_vals[i] = b_field(x, y, z, interp_data, I)    # instant magnetic field
    

        if method == 'rk4':
            x, y, z, Vx, Vy, Vz = rk4(x, y, z, Vx, Vy, Vz, step, interp_data, b_field, e_field, c, m, q, I)

        elif method == 'boris':
            x, y, z, Vx, Vy, Vz = boris(x, y, z, Vx, Vy, Vz, step, c, q, m, I, e_field, b_field, interp_data)



    # combine data into a single array
    data = np.column_stack((x_vals, y_vals, z_vals, Vx_vals, Vy_vals, Vz_vals, Bx_vals, By_vals, Bz_vals, t_vals))



    df_save = pd.DataFrame(data, columns=['x(m)', 'y(m)', 'z(m)', 'Vx(m/s)', 'Vy(m/s)', 'Vz(m/s)', 'Bx(T)', 'By(T)', 'Bz(T)', 't(s)'])
    df_save = df_save.where(df_save['x(m)'] < traj_distance)
    df_save = df_save.dropna()




    trajectory = df_save[['x(m)', 'y(m)', 'z(m)']]
    




    # save data to file
    if output_file == True:
        df_save.to_csv(f"{txt_name}.csv", index=False, float_format='%.12e')
        simulation_params = {
        'magnet_name': f'{magnet_name}',
        'timestamp': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        'filename': f'{txt_name}',
        '': '',
        'distance traveled[m]': f'{traj_distance}',
        '': '', 
        'particle_mass[MeV/c²]': f'{m}',
        'particle_charge[e]': f'{q}',
        'initial_kinetic_energy[MeV]': f'{Ec0}',
        'initial_position[m]': f'({x0}, {y0}, {z0})',
        'initial_velocity_direction': f'{v_direction}',
        'initial_speed[m/s]': f'{conv_v:.4e}',
        'time_step[s]': f'{step:.2e}',
        'total_time[s]': f'{total_t:.2e}',
        '': '',
        'Data columns': 'x(m), y(m), z(m), Vx(m/s), Vy(m/s), Vz(m/s), Bx(T), By(T), Bz(T), t(s)'
        }
        header_lines = []
        for key, value in simulation_params.items():
            if key == '':
               header_lines.append('')
            elif key == 'Data columns':
                header_lines.append(f'{value}')
            else:
             header_lines.append(f'{key}: {value}')
        header_str = '\n'.join(header_lines)
        np.savetxt(f"{txt_name}.txt", data, 
                fmt='%.12e', delimiter=',', 
                header=header_str,
                 comments='# ',
                 encoding='utf-8')
        

    if output_graphic == True:
        flat_trajectory(df_save, total_t)
        three_dimensional_trajectory(df_save)
        degree_angle01, degree_angle02 = deviation_degree(df_save)
        print(f'The deviation degree (vertical) is approximately {degree_angle01:.2f}° ({degree_angle01})')
        print(f'The deviation degree (horizontal y-axis) is approximately {degree_angle02:.2f}° ({degree_angle02})')



        field_plot(df, I)
           
    

        return trajectory