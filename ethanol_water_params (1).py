"""
Parametros termodinamicos para el sistema binario etanol(1)-agua(2).
Fuente: valores estandar de literatura de ingenieria quimica (Smith, Van Ness,
Abbott - Introduction to Chemical Engineering Thermodynamics).

Estos son un punto de partida razonable, pero para un modelo mas riguroso
deberias validarlos/afinarlos contra datos del NIST WebBook o el Dortmund
Data Bank (DDB) para tu rango de presion/temperatura de interes.
"""

# Constantes de Antoine: log10(Psat [mmHg]) = A - B / (T[C] + C)
# Validas aproximadamente entre 20-100 C
ANTOINE = {
    "ethanol": {"A": 8.20417, "B": 1642.89, "C": 230.300},
    "water":   {"A": 8.07131, "B": 1730.63, "C": 233.426},
}

# Parametros del modelo de van Laar para el par etanol(1)-agua(2) a 1 atm
# ln(gamma1) = A12 * (A21*x2 / (A12*x1 + A21*x2))^2
# ln(gamma2) = A21 * (A12*x1 / (A12*x1 + A21*x2))^2
VAN_LAAR = {
    "A12": 1.6798,  # etanol en agua
    "A21": 0.9227,  # agua en etanol
}
