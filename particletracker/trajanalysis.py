import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import math


def plot_2d_trajectory(result, total_t):
    
        fig = plt.figure(figsize=(15, 15))

        ax1 = fig.add_subplot(321) 
        ax2 = fig.add_subplot(322)
        ax3 = fig.add_subplot(323) 
        ax4 = fig.add_subplot(324)

        tempo = np.linspace(0, total_t, len(result))

        ax1.plot(result['x(m)'], result['y(m)'], 'palevioletred', linewidth=1.5)
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.grid(True)
        ax1.axis()
        ax1.set_title('XY trajectory')


        ax2.plot(result['x(m)'], result['z(m)'], 'orange', linewidth=1.5)
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Z (m)')
        ax2.grid(True)
        ax2.axis()
        ax2.set_title('XZ trajectory')


        ax3.plot(tempo, result['z(m)'], 'green', linewidth=1.5)
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Z (m)')
        ax3.grid(True)
        ax3.axis()
        ax3.set_title('Z trajectory')


        ax4.plot(result['z(m)'], result['By(T)'], 'teal', linewidth=1.5)
        ax4.set_xlabel('z(m)')
        ax4.set_ylabel('By(T)')
        ax4.grid(True)
        ax4.axis()
        ax4.set_title('By intensity along Z trajectory')


        plt.tight_layout()
        plt.show()


def plot_3d_trajectory(result ):
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=result['x(m)'],
        y=result['y(m)'],
        z=result['z(m)'],
        mode='markers'
    ))
    # set axis ranges properly using axis dicts and df_save columns
    fig.update_layout(
        title='3D Trajectory',
        scene=dict(
            xaxis=dict(title='x (m)'),
            yaxis=dict(title='y (m)'),
            zaxis=dict(title='z (m)'),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600,
        margin=dict(r=20, l=10, b=10, t=40)
    )
    fig.show()



def show_deviation_degree(result):

    x_list = result['x(m)']
    y_list = result['y(m)']
    z_list = result['z(m)']

    # Get initial and final positions (net displacement)
    x_initial, x_final = x_list.iloc[0], x_list.iloc[-1]
    y_initial, y_final = y_list.iloc[0], y_list.iloc[-1]
    z_initial, z_final = z_list.iloc[0], z_list.iloc[-1]

    # Calculate net displacement
    dx = x_final - x_initial
    dy = y_final - y_initial
    dz = z_final - z_initial

    angle01 = math.atan2(dz, dx) if abs(dx) > 1e-10 or abs(dz) > 1e-10 else 0.0
    angle02 = math.atan2(dy, dx) if abs(dx) > 1e-10 or abs(dy) > 1e-10 else 0.0

    degree_angle01 = math.degrees(angle01)
    degree_angle02 = math.degrees(angle02)

    print(f'The deviation degree (vertical) is approximately {degree_angle01:.2f}° ({degree_angle01})')
    print(f'The deviation degree (horizontal y-axis) is approximately {degree_angle02:.2f}° ({degree_angle02})')