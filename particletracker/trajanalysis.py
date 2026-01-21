import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import math


def plot_2d_trajectory(df, total_t, traj_distance):
        
    condition = df['z(m)'] > (traj_distance-abs(df['z(m)'].iloc[0]))
    result = df.drop(df[condition].index)

    fig = plt.figure(figsize=(15, 15))

    ax1 = fig.add_subplot(321) 
    ax2 = fig.add_subplot(322)
    ax3 = fig.add_subplot(323) 
    ax4 = fig.add_subplot(324)

    tempo = np.linspace(0, total_t, len(result))

    ax1.plot(result['z(m)'], result['x(m)'], 'palevioletred', linewidth=1.5)
    ax1.set_xlabel('Z (m)')
    ax1.set_ylabel('X (m)')
    ax1.grid(True)
    ax1.axis()
    ax1.set_title('ZX trajectory')


    ax2.plot(result['z(m)'], result['y(m)'], 'orange', linewidth=1.5)
    ax2.set_xlabel('Z (m)')
    ax2.set_ylabel('Y (m)')
    ax2.grid(True)
    ax2.axis()
    ax2.set_title('XY trajectory')


    ax3.plot(tempo, result['x(m)'], 'green', linewidth=1.5)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('X (m)')
    ax3.grid(True)
    ax3.axis()
    ax3.set_title('X trajectory')


    ax4.plot(result['z(m)'], result['Bx(T)'], 'teal', linewidth=1.5)
    ax4.set_xlabel('z(m)')
    ax4.set_ylabel('Bx(T)')
    ax4.grid(True)
    ax4.axis()
    ax4.set_title('Bx intensity along Z trajectory')


    plt.tight_layout()
    plt.show()


def plot_3d_trajectory(df, traj_distance):

    condition = df['z(m)'] > (traj_distance-abs(df['z(m)'].iloc[0]))
    result = df.drop(df[condition].index)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=result['z(m)'],
        y=result['y(m)'],
        z=result['x(m)'],
        mode='markers'
    ))
    # set axis ranges properly using axis dicts and df_save columns
    fig.update_layout(
        title='3D Trajectory',
        scene=dict(
            xaxis=dict(title='z (m)'),
            yaxis=dict(title='y (m)'),
            zaxis=dict(title='x (m)'),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600,
        margin=dict(r=20, l=10, b=10, t=40)
    )
    fig.show()



def show_deviation_degree(df, traj_distance):
    condition = df['z(m)'] > (traj_distance-abs(df['z(m)'].iloc[0]))
    result = df.drop(df[condition].index)

    x_list = result['x(m)']
    y_list = result['y(m)']
    z_list = result['z(m)']

    # Get initial and final positions (net displacement)
    x_initial, x_final = x_list.iloc[-3], x_list.iloc[-1]
    y_initial, y_final = y_list.iloc[-3], y_list.iloc[-1]
    z_initial, z_final = z_list.iloc[-3], z_list.iloc[-1]

    # Calculate net displacement
    dx = x_final - x_initial
    dy = y_final - y_initial
    dz = z_final - z_initial

    angle01 = math.atan2(dx, dz) if abs(dx) > 1e-10 or abs(dz) > 1e-10 else 0.0
    angle02 = math.atan2(dy, dz) if abs(dx) > 1e-10 or abs(dy) > 1e-10 else 0.0

    degree_angle01 = math.degrees(angle01)
    degree_angle02 = math.degrees(angle02)

    print(f'The deviation degree (vertical) is approximately {degree_angle01:.2f}° ({degree_angle01})')
    print(f'The deviation degree (horizontal y-axis) is approximately {degree_angle02:.2f}° ({degree_angle02})')

    return degree_angle01

def show_deviation_in_Z(df, final_z):

    for value in df['z(m)']:
        if value < final_z:
            continue
        else:
            Z1 = value
            print(f'Z1 = {Z1}')
            break

    df_invertido_linhas = df.iloc[::-1].reset_index(drop=True)

    for value in df_invertido_linhas['z(m)']:
        if value > final_z:
            continue
        else:
            Z2 = value
            break

    line1 = df[df['z(m)'] == Z1]
    X1 = float(line1['x(m)'])

    line2 =df[df['z(m)'] == Z2]
    X2 = float(line2['x(m)'])

    c1 = (Z2 - final_z) / (Z2 - Z1)
    c2 = (final_z - Z1) / (Z2 - Z1)

    final_x = c1*X1 + c2*X2

    print(f'The final x value is approximately {final_x}')

    return final_x
