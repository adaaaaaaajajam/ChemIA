def mol_a_gramos(moles, masa_molar):
    return moles * masa_molar


def litros_a_moles(litros, densidad, masa_molar):
    masa = litros * densidad
    return masa / masa_molar


def celsius_a_kelvin(celsius):
    return celsius + 273.15


def main():
    print("Convertidor de unidades químicas")
    print("1) mol a gramos")
    print("2) litros a moles")
    print("3) Celsius a Kelvin")

    opcion = input("Seleccione una opción (1-3): ")

    if opcion == "1":
        moles = float(input("Ingrese la cantidad de moles: "))
        masa_molar = float(input("Ingrese la masa molar (g/mol): "))
        resultado = mol_a_gramos(moles, masa_molar)
        print(f"{moles} mol(es) equivalen a {resultado:.4f} gramos con una masa molar de {masa_molar} g/mol.")
    elif opcion == "2":
        litros = float(input("Ingrese el volumen en litros: "))
        densidad = float(input("Ingrese la densidad en g/mL o g/cm^3: "))
        masa_molar = float(input("Ingrese la masa molar (g/mol): "))
        resultado = litros_a_moles(litros, densidad, masa_molar)
        print(f"{litros} litros equivalen a {resultado:.4f} moles con densidad {densidad} g/mL y masa molar {masa_molar} g/mol.")
    elif opcion == "3":
        celsius = float(input("Ingrese la temperatura en grados Celsius: "))
        resultado = celsius_a_kelvin(celsius)
        print(f"{celsius:.2f} °C equivalen a {resultado:.2f} K.")
    else:
        print("Opción no válida. Ejecute el programa de nuevo y seleccione 1, 2 o 3.")


if __name__ == "__main__":
    main()
