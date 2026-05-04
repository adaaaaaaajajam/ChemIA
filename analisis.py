import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Temperatura (°C)": [0, 20, 40, 60, 80, 100],
    "Presión de vapor (kPa)": [0.61, 2.34, 7.38, 19.94, 47.39, 101.32],
    "Densidad (kg/m³)": [999.8, 998.2, 992.2, 983.2, 971.8, 958.4],
}

df = pd.DataFrame(data)

print("=== Primeras filas ===")
print(df.head())

print("\n=== Estadísticas descriptivas ===")
print(df.describe())

print("\n=== Media de cada columna ===")
print(df.mean())

plt.figure(figsize=(8, 5))
plt.plot(df["Temperatura (°C)"], df["Presión de vapor (kPa)"], marker="o", color="steelblue", linewidth=2)
plt.title("Temperatura vs Presión de vapor del agua")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Presión de vapor (kPa)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("grafica.png", dpi=150)
print("\nGráfica guardada como grafica.png")
