import numpy as np
import scipy.optimize as opt
from typing import Tuple
from .medicoes import Me
import matplotlib.pyplot as plt

def weighted_linear_regression(x: np.ndarray, y: np.ndarray, y_err: np.ndarray) -> Tuple[Me, Me, float|int]:
    """
    Realiza uma regressão linear ponderada considerando as incertezas em y.

    Parâmetros:
    x (numpy.ndarray): Array de valores independentes.
    y (numpy.ndarray): Array de valores dependentes.
    y_err (numpy.ndarray): Array de incertezas em y.

    Retorna:
    Tuple[float, float, float, float]: intercepto, inclinação, incerteza no intercepto, incerteza na inclinação
    """
    
    # Definindo a função do modelo linear
    def model(params: Tuple[float, float], x: np.ndarray) -> np.ndarray:
        return params[0] + params[1] * x
    
    # Função objetivo que calcula os resíduos ponderados
    def objective(params: Tuple[float, float], x: np.ndarray, y: np.ndarray, y_err: np.ndarray) -> np.ndarray:
        residuals = (y - model(params, x)) / y_err
        return residuals
    
    # Estimativas iniciais para intercepto e inclinação
    initial_params = [0.0, 1.0]
    
    # Ajuste utilizando a função least_squares do scipy.optimize
    result = opt.least_squares(objective, initial_params, args=(x, y, y_err))
    
    # Extraindo os parâmetros ajustados
    intercept, slope = result.x
    
    # Calculando a matriz de covariância para estimar as incertezas dos parâmetros
    _, s, VT = np.linalg.svd(result.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(result.jac.shape) * s[0]
    s = s[s > threshold]
    VT = VT[:s.size]
    cov = np.dot(VT.T / s**2, VT)
    
    intercept_err, slope_err = np.sqrt(np.diag(cov))

    # Calculando o R²
    y_fit = model(result.x, x)
    ss_res = np.sum(((y - y_fit) / y_err) ** 2)
    ss_tot = np.sum(((y - np.average(y, weights=1/y_err)) / y_err) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    return Me(intercept, intercept_err), Me(slope, slope_err), r_squared

def plot_linear_regression(ax:any, limits:list[float], intercept:Me, slope:Me, r_squared:float, color:str = "blue"):
    x_arr = np.linspace(limits[0], limits[1], 1000)
    y_arr = intercept.m + slope.m*x_arr
    yu_arr = intercept.u + slope.u*x_arr

    ax.plot(
        limits, 
        np.array([
            intercept.m + limits[0]*slope.m, 
            intercept.m + limits[1]*slope.m
        ]),
        label = "Reta linearizada $Y = Ax + B$ | $R^{2} ="+f" {r_squared:.3f}$\n"
         + rf"$A = {slope.repr_latex()}$, $B = {intercept.repr_latex()}$",
        color = color,
    )
    ax.fill_between(
        x = x_arr,
        y1 = y_arr-yu_arr,
        y2 = y_arr+yu_arr,
        color=color, 
        alpha=0.2
    )

    return