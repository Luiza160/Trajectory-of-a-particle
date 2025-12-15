# Trajectory of a particle
The main goal of this project is to calculate the trajectory of a particle under the action of a magnetic field.

## Table of Contents
- [Overview](#Overview)
- [Brief theoretical background](#brief_theoretical_background)
- [Using](#Using)


## Overview

This project is inspired by a proton accelerator system. Its purpose is to predict the trajectory of a proton as it passes through a magnetic dipole, which is used to alter its path. By adjusting particle and magnet parameters, this code can be applied to predict the motion of any particle in a magnetic field.

## Brief theoretical background

The motion prediction is based on Newton's second law of motion, which relates the force acting on a particle to its instantaneous acceleration and mass:
```math
\vec{F} = m \cdot \vec{a} = m \cdot \frac{d\vec{v}}{dt} 
```

Newton's law can be combined with the Lorentz force equation, which describes the force on a charged particle in the presence of electric and magnetic fields:
```math
\vec{F} = q (\vec{E} + \vec{v} \times \vec{B}) = m \cdot \frac{d\vec{v}}{dt} 
```

When dealing with accelerated particles, relativistic effects must be considered. As a particle approaches the speed of light, these effects become significant and can alter its trajectory. The Lorentz factor accounts for these changes in mass, velocity, acceleration, and time:
```math
\gamma = \frac{1}{\sqrt{1 - \left(\frac{\vec{v}}{c} \right)^2}}
```

Analytical solutions are insufficient for solving the trajectory equations due to the varying magnetic field analyzed. Therefore, the Fourth-Order Runge-Kutta method (RK4) was chosen. It is an iterative numerical method:
```math
u^{n+1} = u^n + \Delta t \sum_{i=1}^{e}b_i k_i
```

where:
```math
k_i = F(u^n + \Delta t \sum_{j-i}^{e}a_{ij}k_j;t_n+c_i \Delta t) i=1, ..., e
```

This method enables the prediction of all variables at every time step.

### Explaining the code
- **Parameter Input**: The user provides simulation parameters such as particle properties, initial conditions, and data files.
- **Field Functions**: Functions are defined to compute magnetic and electric fields at all coordinates. Since the magnetic field is not constant, interpolation is used to estimate values at unspecified points.
- **Main Functions**: Additional functions inside the main routine calculate instantaneous acceleration and implement the Runge-Kutta method. The RK4 algorithm updates variables at each time step.
- **Results**: All results are saved and displayed graphically for the user.

## Using
### Installing and running
Before executing the code, ensure that all required Python modules are installed. The dependencies are:
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [plotly](https://plotly.com/python/)
- [datetime](https://docs.python.org/3/library/datetime.html)

If any of these packages are missing, you can install them using *pip*. For example:

*pip install matplotlib numpy pandas plotly*

Once the dependencies are installed, download the main script (main.ipynb) from this repository. The code is provided as a Jupyter Notebook (.ipynb format), which means it was written for interactive execution.

To run the notebook:
- Open it in your preferred environment, such as Jupyter Notebook, JupyterLab, or VS Code with the Python extension.
- Execute the cells in order to perform the simulation.