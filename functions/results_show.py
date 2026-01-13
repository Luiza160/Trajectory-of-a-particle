import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

from functions.fieldparser import create_interpolators


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

    return degree_angle01, degree_angle02


def field_plot(df, I):


    def plot_comparison_2d(interp_func, df, component='Bx', res=(500, 600), y_fixed=None):
        
        # Convert to numeric and ensure consistent units
        df = df.copy()
        for col in ['x_mm', 'y_mm', 'z_mm', 'Bx_T', 'By_T', 'Bz_T']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna()
        
        # Get unique coordinate values
        x_vals = np.sort(df["x_mm"].unique())
        y_vals = np.sort(df["y_mm"].unique())
        z_vals = np.sort(df["z_mm"].unique())
        
        # Set y coordinate if not provided
        if y_fixed is None:
            y_fixed = y_vals[0]
        
        # Filter original data for this y-plane
        df_plane = df[np.isclose(df['y_mm'], y_fixed, atol=1e-6)]
        
        if len(df_plane) == 0:
            raise ValueError(f"No data found at y={y_fixed} mm")
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Original data (scatter plot)
        if component == 'Bx':
            field_vals = df_plane['Bx_T'].values
        elif component == 'By':
            field_vals = df_plane['By_T'].values
        elif component == 'Bz':
            field_vals = df_plane['Bz_T'].values
        elif component == 'Bmag':
            field_vals = np.sqrt(df_plane['Bx_T']**2 + df_plane['By_T']**2 + df_plane['Bz_T']**2).values
        else:
            raise ValueError("component must be 'Bx', 'By', 'Bz', or 'Bmag'")
        
        sc1 = ax1.scatter(df_plane['x_mm'], df_plane['z_mm'], c=field_vals, 
                        s=20, cmap='viridis', alpha=0.8)
        ax1.set_xlabel('x [mm]')
        ax1.set_ylabel('z [mm]')
        ax1.set_title(f'Original Data ({component}) at y={y_fixed:.3f} mm')
        plt.colorbar(sc1, ax=ax1, label=f'{component} [T]')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Interpolated data (heatmap) - VECTORIZED APPROACH
        nx, nz = res
        Xg = np.linspace(x_vals.min(), x_vals.max(), nx)
        Zg = np.linspace(z_vals.min(), z_vals.max(), nz)
        X, Z = np.meshgrid(Xg, Zg, indexing='ij')
        
        # Create all points at once
        points = np.column_stack([
            X.ravel(),
            np.full(X.size, y_fixed),
            Z.ravel()
        ])
        
        # Evaluate interpolator at all points
        results = np.array([interp_func(p) for p in points])
        Bx_grid = results[:, 0].reshape(X.shape)
        By_grid = results[:, 1].reshape(X.shape)
        Bz_grid = results[:, 2].reshape(X.shape)
        
        # Select the appropriate component for display
        if component == 'Bx':
            Img = Bx_grid
            cbar_label = 'Bx [T]'
        elif component == 'By':
            Img = By_grid
            cbar_label = 'By [T]'
        elif component == 'Bz':
            Img = Bz_grid
            cbar_label = 'Bz [T]'
        elif component == 'Bmag':
            Img = np.sqrt(Bx_grid**2 + By_grid**2 + Bz_grid**2)
            cbar_label = '|B| [T]'
        
        # Plot the interpolated field
        extent = [Xg.min(), Xg.max(), Zg.min(), Zg.max()]
        im = ax2.imshow(Img.T, origin='lower', aspect='auto', 
                    extent=extent, cmap='viridis')
        ax2.set_xlabel('x [mm]')
        ax2.set_ylabel('z [mm]')
        ax2.set_title(f'Interpolated Field ({component}) at y={y_fixed:.3f} mm')
        plt.colorbar(im, ax=ax2, label=cbar_label)
        
        plt.tight_layout()
        plt.show()
        
        return fig, (ax1, ax2)
        
    # Create interpolator
    interp_func = create_interpolators(df, I)
            
    # Plot comparisons - use the vectorized version for better performance
    plot_comparison_2d(interp_func, df, component='Bx', res=(500, 600))
    plot_comparison_2d(interp_func, df, component='By', res=(500, 600))
    plot_comparison_2d(interp_func, df, component='Bz', res=(500, 600))
    plot_comparison_2d(interp_func, df, component='Bmag', res=(500, 600))