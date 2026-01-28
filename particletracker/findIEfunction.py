import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def find_function(chart):

    def linear(x, a, b):
        return a * x + b

    def polynomial2(x, a, b, c):
        return a * x**2 + b * x + c

    def exponential(x, a, b):
        return a * np.exp(b * x)

    def logarithmic(x, a, b):
        return a * np.log(x) + b

    def power_law(x, a, b):
        return a * np.power(x, b)

    models = {
        "Linear": (linear, [1, 1]),
        "Quadratic": (polynomial2, [1, 1, 1]),
        "Exponential": (exponential, [1, 0.1]),
        "Logarithmic": (logarithmic, [1, 1]),
        "Power Law": (power_law, [1, 1])
    }

    model01 = None
    model02 = None
    best_r2_01 = -np.inf
    best_r2_02 = -np.inf
    best_params01 = None
    best_params02 =None

    for name, (func, p0) in models.items():
        try:
            popt, _ = curve_fit(func, chart['Current(A)'], chart['Energy(MeV)'], p0=p0, maxfev=5000)
            y_pred = func(chart['Current(A)'], *popt)
            r2 = r2_score(chart['Energy(MeV)'], y_pred)
            
            if r2 > best_r2_01:
                best_r2_01 = r2
                model01 = (name, func)
                best_params01 = popt
        except Exception as e:
            print(f"{name} fitting failed: {e}")

    for name, (func, p0) in models.items():
        try:
            popt, _ = curve_fit(func, chart['Energy(MeV)'], chart['Current(A)'], p0=p0, maxfev=5000)
            y_pred = func(chart['Energy(MeV)'], *popt)
            r2 = r2_score(chart['Current(A)'], y_pred)
            
            if r2 > best_r2_02:
                best_r2_02 = r2
                model02 = (name, func)
                best_params02 = popt
        except Exception as e:
            print(f"{name} fitting failed: {e}")

    return model01, model02, best_params01, best_params02


def plot_function(model01, model02, best_params01, best_params02, chart):
    fig = plt.figure(figsize=(20, 8))
    ax1 = fig.add_subplot(121) 
    ax2 = fig.add_subplot(122)

    if model01:
        name, func = model01

        x_pred = np.linspace(max(chart['Current(A)']), min(chart['Energy(MeV)']), 200)
        y_pred_curve = func(x_pred, *best_params01)

    params01 = [float(best_params01[0]),
                float(best_params01[1]),
                float(best_params01[2])]

    ax1.scatter(chart['Current(A)'], chart['Energy(MeV)'], s=70, color='k')
    ax1.plot(x_pred, y_pred_curve, color='r', linestyle='--')
    ax1.set_xlabel('Current(A)')
    ax1.set_ylabel('Energy(MeV)')
    ax1.set_title('Current x Energy')
    ax1.grid(True)
    ax1.text(1.5, 1.5, f'E(i)={params01[0]:.4f}x²+{params01[1]:.4f}x+{params01[2]:.4f}', fontsize=9, color='black', bbox={'facecolor': 'white', 'pad': 10})



    if model02:
        name, func = model02

        x_pred = np.linspace(min(chart['Energy(MeV)']), min(chart['Current(A)']), 200)
        y_pred_curve = func(x_pred, *best_params02)

    params02 = [float(best_params02[0]),
                float(best_params02[1])]

    ax2.scatter(chart['Energy(MeV)'], chart['Current(A)'], s=70, color='k')
    ax2.plot(x_pred, y_pred_curve, color='g', linestyle='--')
    ax2.set_xlabel('Energy(MeV)')
    ax2.set_ylabel('Current(A)')
    ax2.set_title('Current x Energy')
    ax2.grid(True)

    plt.text(1.5, 4, f'i(E)={params02[0]:.4f}x^{params02[1]:.4f}', fontsize=9, color='black', bbox={'facecolor': 'white', 'pad': 10})

    plt.savefig('Energy_and_Current_functions_graph.png', dpi=300, bbox_inches='tight')
