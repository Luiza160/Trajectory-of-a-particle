import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


# Runge-Kutta 4th order method
def rk4(x, y, z, Vx, Vy, Vz, step, b_field, e_field, c, m, q, I): 

    conv_m = m * 1.78266e-30      # converted mass (Kg)
    conv_q = q * 1.60218e-19        # converted charge (C)
    const = conv_q/conv_m


    def acceleration(x, y, z, Vx, Vy, Vz, b_field, e_field):
        Bx, By, Bz = b_field([x, y, z])
        Ex, Ey, Ez = e_field([x, y, z])

        V2 = Vx**2 + Vy**2 + Vz**2    # squared velocity

        # checks if particle's velocity is closer to light's (won't be)
        if V2 >= c**2:
            gamma_local = 1.0e10 
        else:
            gamma_local = 1.0 / np.sqrt(1.0 - V2/c**2)


        # applies Lorentz factor to Newton-Lorentz equations (defined at readme section)
        # defines instant acceleration based on instant velocitys and fields
        ax = (const/gamma_local)*((Ex+Vy*Bz-Vz*By) - Vx * (gamma_local**2)/(gamma_local + 1) * (Vx*Ex+Vy*Ey+Vz*Ez))
        ay = (const/gamma_local)*((Ey+Vz*Bx-Vx*Bz) - Vy * (gamma_local**2)/(gamma_local + 1) * (Vx*Ex+Vy*Ey+Vz*Ez))
        az = (const/gamma_local)*((Ez+Vx*By-Vy*Bx) - Vz * (gamma_local**2)/(gamma_local + 1) * (Vx*Ex+Vy*Ey+Vz*Ez))

    
        return ax, ay, az


    # k1
    ax1, ay1, az1 = acceleration(x, y, z, Vx, Vy, Vz, b_field, e_field)

    k1_x = Vx        
    k1_y = Vy        
    k1_z = Vz         
    k1_Vx = ax1     
    k1_Vy = ay1      
    k1_Vz = az1        

    # k2 
    x2 = x + 0.5*step * k1_x
    y2 = y + 0.5*step * k1_y
    z2 = z + 0.5*step * k1_z
    Vx2 = Vx + 0.5*step * k1_Vx
    Vy2 = Vy + 0.5*step * k1_Vy
    Vz2 = Vz + 0.5*step * k1_Vz

    ax2, ay2, az2 = acceleration(x2, y2, z2, Vx2, Vy2, Vz2, b_field, e_field)
    k2_x = Vx2   
    k2_y = Vy2
    k2_z = Vz2
    k2_Vx = ax2
    k2_Vy = ay2
    k2_Vz = az2

    # k3 
    x3 = x + 0.5*step * k2_x
    y3 = y + 0.5*step * k2_y
    z3 = z + 0.5*step * k2_z
    Vx3 = Vx + 0.5*step * k2_Vx
    Vy3 = Vy + 0.5*step * k2_Vy
    Vz3 = Vz + 0.5*step * k2_Vz

    ax3, ay3, az3 = acceleration(x3, y3, z3, Vx3, Vy3, Vz3, b_field, e_field)
    k3_x = Vx3
    k3_y = Vy3
    k3_z = Vz3
    k3_Vx = ax3
    k3_Vy = ay3
    k3_Vz = az3

    # k4
    x4 = x + step * k3_x
    y4 = y + step * k3_y
    z4 = z + step * k3_z
    Vx4 = Vx + step * k3_Vx
    Vy4 = Vy + step * k3_Vy
    Vz4 = Vz + step * k3_Vz

    ax4, ay4, az4 = acceleration(x4, y4, z4, Vx4, Vy4, Vz4, b_field, e_field)
    k4_x = Vx4
    k4_y = Vy4
    k4_z = Vz4
    k4_Vx = ax4
    k4_Vy = ay4
    k4_Vz = az4

    # general solution
    new_x = x + (step/6.0) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
    new_y = y + (step/6.0) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
    new_z = z + (step/6.0) * (k1_z + 2*k2_z + 2*k3_z + k4_z)
    new_Vx = Vx + (step/6.0) * (k1_Vx + 2*k2_Vx + 2*k3_Vx + k4_Vx)
    new_Vy = Vy + (step/6.0) * (k1_Vy + 2*k2_Vy + 2*k3_Vy + k4_Vy)
    new_Vz = Vz + (step/6.0) * (k1_Vz + 2*k2_Vz + 2*k3_Vz + k4_Vz)

    return new_x, new_y, new_z, new_Vx, new_Vy, new_Vz




def boris(x, y, z, Vx, Vy, Vz, dt, c, q, m, e_field, b_field):


    conv_m = m * 1.78266e-30      # converted mass (Kg)
    conv_q = q * 1.60218e-19        # converted charge (C)


    # ---- fields at current position (x^n) ----
    Ex, Ey, Ez = e_field([x, y, z])
    Bx, By, Bz = b_field([x, y, z])

    # ---- momentum at time n: p^n = gamma m v ----
    v2 = Vx*Vx + Vy*Vy + Vz*Vz
    # numerical safety: clamp beta^2 to < 1
    beta2 = min(v2 / (c*c), 0.999999999999)
    gamma = 1.0 / ( (1.0 - beta2) ** 0.5 )
    px = gamma * conv_m * Vx
    py = gamma * conv_m * Vy
    pz = gamma * conv_m * Vz

    # ---- half electric kick: p^- = p^n + q E Δt/2 ----
    half_qdt = 0.5 * q * dt
    px_minus = px + half_qdt * Ex
    py_minus = py + half_qdt * Ey
    pz_minus = pz + half_qdt * Ez

    # ---- gamma^- from p^- (time-centered for B-rotation) ----
    pminus2 = px_minus*px_minus + py_minus*py_minus + pz_minus*pz_minus
    gamma_minus = (1.0 + pminus2 / (conv_m*conv_m*c*c)) ** 0.5

    # ---- rotation in B using t and s ----
    # t = (q B Δt) / (2 m γ^-)
    inv = 0.5 * conv_q * dt / (conv_m * gamma_minus)
    tx = inv * Bx
    ty = inv * By
    tz = inv * Bz

    # p' = p^- + p^- × t
    ppx = px_minus + (py_minus * tz - pz_minus * ty)
    ppy = py_minus + (pz_minus * tx - px_minus * tz)
    ppz = pz_minus + (px_minus * ty - py_minus * tx)

    # s = 2 t / (1 + |t|^2)
    t2 = tx*tx + ty*ty + tz*tz
    sx = 2.0 * tx / (1.0 + t2)
    sy = 2.0 * ty / (1.0 + t2)
    sz = 2.0 * tz / (1.0 + t2)

    # p^+ = p^- + p' × s
    px_plus = px_minus + (ppy * sz - ppz * sy)
    py_plus = py_minus + (ppz * sx - ppx * sz)
    pz_plus = pz_minus + (ppx * sy - ppy * sx)

    # ---- second half electric kick: p^{n+1} ----
    px_new = px_plus + half_qdt * Ex
    py_new = py_plus + half_qdt * Ey
    pz_new = pz_plus + half_qdt * Ez

    # ---- recover v^{n+1} from p^{n+1} ----
    pnew2 = px_new*px_new + py_new*py_new + pz_new*pz_new
    gamma_new = (1.0 + pnew2 / (conv_m*conv_m*c*c)) ** 0.5
    inv_gm = 1.0 / (gamma_new * conv_m)

    Vx_new = px_new * inv_gm
    Vy_new = py_new * inv_gm
    Vz_new = pz_new * inv_gm

    # ---- position update ----
    x_new = x + Vx_new * dt
    y_new = y + Vy_new * dt
    z_new = z + Vz_new * dt

    return x_new, y_new, z_new, Vx_new, Vy_new, Vz_new


def solve_trajectory(m, q, 
                 x0, y0, z0, v_direction, Ec0,
                 b_field, e_field,
                 method, step, total_t, 
                 output_file='traj_calculation_results'):


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
        Bx_vals[i], By_vals[i], Bz_vals[i] = b_field([x, y, z])               # instant magnetic field
    

        if method == 'rk4':
            x, y, z, Vx, Vy, Vz = rk4(x, y, z, Vx, Vy, Vz, step, b_field, e_field, c, m, q)

        elif method == 'boris':
            x, y, z, Vx, Vy, Vz = boris(x, y, z, Vx, Vy, Vz, step, c, q, m, e_field, b_field)


    # combine data into a single array
    data = np.column_stack((x_vals, y_vals, z_vals, Vx_vals, Vy_vals, Vz_vals, Bx_vals, By_vals, Bz_vals, t_vals))


    trajectory = pd.DataFrame(data, columns=['x(m)', 'y(m)', 'z(m)', 'Vx(m/s)', 'Vy(m/s)', 'Vz(m/s)', 'Bx(T)', 'By(T)', 'Bz(T)', 't(s)'])
    trajectory = trajectory.dropna()
    

    '''# save data to file
    header = {
    'timestamp': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
    'filename': f'{output_file}',
    '': '', 
    'particle_mass[MeV/c²]': f'{m}',
    'particle_charge[u.a]': f'{q}',
    'initial_kinetic_energy[MeV]': f'{Ec0}',
    'initial_position[m]': f'({x0}, {y0}, {z0})',
    'initial_velocity_direction': f'{v_direction}',
    'initial_speed[m/s]': f'{conv_v:.4e}',
    'total_time[s]': f'{total_t:.2e}',
    '': '',
    'Data columns': 'x(m), y(m), z(m), Vx(m/s), Vy(m/s), Vz(m/s), Bx(T), By(T), Bz(T), t(s)',
    '': '',
    '=============== :BEGIN DATA': '==============='
    }
    header_lines = []
    for key, value in header.items():
        if key == '':
            header_lines.append('')
        elif key == 'Data columns':
            header_lines.append(f'{value}')
        else:
            header_lines.append(f'{key}: {value}')
    header_str = '\n'.join(header_lines)
    np.savetxt(f"{output_file}.traj", data, 
            fmt='%.12e', delimiter=',', 
            header=header_str,
                comments='# ',
                encoding='utf-8')'''

    return trajectory