# Trajectory of a particle
The main goal of this project is to calculate the trajectory of a particle under the action of a magnetic field.

## Table of Contents
- [Overview](#Overview)
- [Brief theoretical background](#brief_theoretical_background)
- [Using](#Using)
- [License](#license)

## Brief theoretical background

All the movement prediction is based on the Newton's movement law, as it describes the force on the particle, based on it's instant acceleration and mass.
```math
\vec{F} = m \cdot \vec{a} = m \cdot \frac{d\vec{v}}{dt} 
```

Newton's motion law can be associated with Lorentz force equation, as it also describes the force on the particle, but associating it with the incident magnetic and eletric fields.
```math
\vec{F} = q (\vec{E} + \vec{v} \times \vec{B}) = m \cdot \frac{d\vec{v}}{dt} 
```

An important observation is that, when working with accelerated particles, it's essential to consider the relativistic effects. The closer a particle gets to the speed of light, stronger are the relativistic effects, that can cause relevant change on it's trajectory. Lorentz factor is used to correct these changes, that happens on mass, velocity, acceleration and time.
```math
\gamma = \frac{1}{\sqrt{1 - \left(\frac{\vec{v}}{c} \right)^2}}
```

In this case, analytic solutions weren't enough to solve the trajectory equations, due to the varying magnetic field annalysed. The chosen method is called Fourth Order Runge-Kutta (or RK4) an is based on a seris of iterations  
```math
u^{n+1} = u^n + \Delta t \sum_{i=1}^{e}b_i k_i
```

where

```math
k_i = F(u^n + \Delta t \sum_{j-i}^{e}a_{ij}k_j;t_n+c_i \Delta t) i=1, ..., e
```

## Overview

## Installing and running