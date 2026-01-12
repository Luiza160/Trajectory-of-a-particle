import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import math


def flat_trajectory(df_save, total_t):
    
        fig = plt.figure(figsize=(15, 15))

        ax1 = fig.add_subplot(321) 
        ax2 = fig.add_subplot(322)
        ax3 = fig.add_subplot(323) 

        tempo = np.linspace(0, total_t, len(df_save))

        ax1.plot(df_save['x(m)'], df_save['y(m)'], 'palevioletred', linewidth=1.5)
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.grid(True)
        ax1.axis()
        ax1.set_title('XY trajectory')


        ax2.plot(tempo, df_save['z(m)'], 'green', linewidth=1.5)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Z (m)')
        ax2.grid(True)
        ax2.axis()
        ax2.set_title('Z trajectory')


        ax3.plot(df_save['z(m)'], df_save['By(T)'], 'teal', linewidth=1.5)
        ax3.set_xlabel('z(m)')
        ax3.set_ylabel('By(T)')
        ax3.grid(True)
        ax2.axis()
        ax3.set_title('By intensity along Z trajectory')


        plt.tight_layout()
        plt.show()


def three_dimensional_trajectory(df_save):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=df_save['x(m)'],
        y=df_save['y(m)'],
        z=df_save['z(m)'],
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



def deviation_degree(df_save):
    x_list = df_save['x(m)']
    y_list = df_save['y(m)']
    z_list = df_save['z(m)']
    x_range = x_list.max() - x_list.min()
    y_range = y_list.max() - y_list.min()
    z_range = z_list.max() - z_list.min()

    # calculte the deviation degree
    angle01 = math.atan(z_range/x_range)
    degree_angle01 = math.degrees(angle01)

    angle02 = math.atan(y_range/x_range)
    degree_angle02 = math.degrees(angle02)

    return degree_angle01, degree_angle02