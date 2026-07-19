"""
Motor de calculo VLE (equilibrio liquido-vapor) para un sistema binario,
usando la ley de Raoult modificada:

    P * y_i = x_i * gamma_i * Psat_i(T)

Este es el "modelo clasico" que sirve de linea base (paso 3 del plan).
Mas adelante, este mismo modulo se puede sustituir/combinar con un modelo
de datos (paso 4) y con la API de Claude para razonar sobre sistemas nuevos
(paso 5).
"""

import math
import numpy as np
import pandas as pd


def antoine_psat(T_celsius: float, A: float, B: float, C: float) -> float:
    """Presion de vapor (mmHg) a partir de la ecuacion de Antoine."""
    return 10 ** (A - B / (T_celsius + C))


def van_laar_gammas(x1: float, A12: float, A21: float) -> tuple[float, float]:
    """Coeficientes de actividad (gamma1, gamma2) segun el modelo de van Laar."""
    x2 = 1 - x1
    if x1 == 0:
        return math.exp(A12), 1.0
    if x2 == 0:
        return 1.0, math.exp(A21)
    term = (A12 * x1) / (A21 * x2 + A12 * x1)
    ln_g1 = A12 * (A21 * x2 / (A12 * x1 + A21 * x2)) ** 2
    ln_g2 = A21 * (A12 * x1 / (A12 * x1 + A21 * x2)) ** 2
    return math.exp(ln_g1), math.exp(ln_g2)


def bubble_point_T(x1: float, P_total_mmHg: float, antoine1, antoine2, van_laar,
                    T_guess=80.0, tol=1e-4, max_iter=100):
    """
    Calcula la temperatura de burbuja (punto de ebullicion de la mezcla)
    para una composicion x1 dada, por iteracion simple.
    Devuelve (T_celsius, y1).
    """
    T = T_guess
    x2 = 1 - x1
    for _ in range(max_iter):
        gamma1, gamma2 = van_laar_gammas(x1, van_laar["A12"], van_laar["A21"])
        Psat1 = antoine_psat(T, **antoine1)
        Psat2 = antoine_psat(T, **antoine2)
        P_calc = x1 * gamma1 * Psat1 + x2 * gamma2 * Psat2

        # Ajuste de T: si P_calc > P_total, la mezcla hierve a menor T, y viceversa
        error = P_calc - P_total_mmHg
        if abs(error) < tol:
            y1 = x1 * gamma1 * Psat1 / P_total_mmHg
            return T, y1
        # paso simple tipo Newton numerico (derivada aproximada)
        dT = 0.01
        Psat1_dT = antoine_psat(T + dT, **antoine1)
        Psat2_dT = antoine_psat(T + dT, **antoine2)
        P_calc_dT = x1 * gamma1 * Psat1_dT + x2 * gamma2 * Psat2_dT
        dPdT = (P_calc_dT - P_calc) / dT
        T = T - error / dPdT

    raise RuntimeError("No convergio la temperatura de burbuja")


def generate_txy_diagram(antoine1, antoine2, van_laar, P_total_mmHg=760.0, n_points=21):
    """Genera el diagrama T-x-y completo para el sistema binario."""
    rows = []
    for x1 in np.linspace(0.001, 0.999, n_points):
        T, y1 = bubble_point_T(x1, P_total_mmHg, antoine1, antoine2, van_laar)
        rows.append({"x1": x1, "y1": y1, "T_celsius": T})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from ethanol_water_params import ANTOINE, VAN_LAAR

    df = generate_txy_diagram(ANTOINE["ethanol"], ANTOINE["water"], VAN_LAAR)
    print(df)
    print("\nPunto de ebullicion del etanol puro (x1=0.999):",
          round(df.iloc[-1]["T_celsius"], 2), "C (referencia real: 78.37 C)")
    print("Punto de ebullicion del agua pura (x1=0.001):",
          round(df.iloc[0]["T_celsius"], 2), "C (referencia real: 100.00 C)")
