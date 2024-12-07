import numpy as np
from munkres import Munkres  # Se importa la librería Munkres, que implementa el algoritmo húngaro.

# Clase principal que gestiona la asignación de tareas
class AsignacionTareas:
    def __init__(self, matriz, optimizar_por):
        """
        Inicializa la clase con la matriz de costos/tiempos y el criterio de optimización.
        """
        self.matriz_original = np.array(matriz)  # Convierte la matriz ingresada a un array de NumPy.
        self.optimizar_por = optimizar_por  # Define si se optimiza por 'costo' o 'tiempo'.
        self.matriz = self.preparar_matriz(self.matriz_original)  # Prepara la matriz según el criterio.
        self.matriz = self.balancear_matriz(self.matriz)  # Balancea la matriz para que sea cuadrada.
        self.filas, self.columnas = self.matriz.shape  # Guarda las dimensiones de la matriz.

    def balancear_matriz(self, matriz):
        """
        Asegura que la matriz sea cuadrada agregando filas o columnas de ceros si es necesario.
        """
        filas, columnas = matriz.shape
        if filas < columnas:  # Si hay más tareas que programadores...
            # Se añaden filas de ceros.
            matriz_balanceada = np.vstack([matriz, np.zeros((columnas - filas, columnas))])
        elif filas > columnas:  # Si hay más programadores que tareas...
            # Se añaden columnas de ceros.
            matriz_balanceada = np.hstack([matriz, np.zeros((filas, filas - columnas))])
        else:
            matriz_balanceada = matriz  # Si ya es cuadrada, no se hace nada.
        return matriz_balanceada

    def preparar_matriz(self, matriz):
        """
        Ajusta la matriz según el criterio de optimización ('costo' o 'tiempo').
        """
        if self.optimizar_por == "costo":
            # No se transforma la matriz si se optimiza por costo.
            return matriz
        elif self.optimizar_por == "tiempo":
            # Para optimizar por tiempo, se invierten los valores.
            matriz_max = np.max(matriz)  # Encuentra el valor máximo en la matriz.
            return matriz_max - matriz  # Invierte los valores para minimizar tiempos.
        else:
            raise ValueError("Criterio de optimización no reconocido. Usa 'costo' o 'tiempo'.")

    def resolver_con_munkres(self):
        """
        Resuelve el problema de asignación usando el algoritmo húngaro implementado en la librería Munkres.
        """
        m = Munkres()  # Crea una instancia del algoritmo.
        indices = m.compute(self.matriz.tolist())  # Calcula las asignaciones óptimas.
        costo_total = sum(self.matriz[row][col] for row, col in indices)  # Suma los costos totales.
        return indices, costo_total

    def resolver_sin_librerias(self):
        """
        Resuelve el problema iterativamente usando una estrategia codiciosa.
        """
        matriz = self.matriz.copy()  # Crea una copia de la matriz para evitar modificar la original.
        filas, columnas = matriz.shape
        asignaciones = []

        while len(asignaciones) < min(filas, columnas):  # Itera hasta asignar todas las tareas.
            min_valor = np.min(matriz)  # Encuentra el valor mínimo en la matriz.
            indice = np.unravel_index(np.argmin(matriz), matriz.shape)  # Obtén las coordenadas del valor mínimo.
            asignaciones.append(indice)  # Registra la asignación.
            # Invalida la fila y la columna seleccionadas asignándoles un valor infinito.
            matriz[indice[0], :] = float('inf')
            matriz[:, indice[1]] = float('inf')

        # Calcula el costo total basado en las asignaciones.
        costo_total = sum(self.matriz[row][col] for row, col in asignaciones)
        return asignaciones, costo_total

    def mostrar_resultados(self, indices, costo_total):
        """
        Muestra los resultados de las asignaciones en un formato legible.
        """
        print(f"\nMatriz final utilizada para la asignación:\n{self.matriz}")
        print("\nAsignaciones:")
        for row, col in indices:
            print(f"Programador {row + 1} asignado a Tarea {col + 1}")  # Imprime las asignaciones en formato legible.
        print(f"\nCosto/tiempo total optimizado: {costo_total}")  # Muestra el costo total.

    def ejecutar(self, metodo_resolucion):
        """
        Ejecuta la solución según el método seleccionado ('munkres' o 'manual').
        """
        if metodo_resolucion == "munkres":
            print("\nResolviendo con Munkres...")
            indices, costo_total = self.resolver_con_munkres()
        elif metodo_resolucion == "manual":
            print("\nResolviendo sin librerías...")
            indices, costo_total = self.resolver_sin_librerias()
        else:
            print("\nMétodo de resolución no reconocido.")
            return

        self.mostrar_resultados(indices, costo_total)  # Muestra los resultados al usuario.


# Programa interactivo
if __name__ == "__main__":
    print("Bienvenido al sistema de asignación de tareas")
    filas = int(input("Ingresa el número de programadores: "))  # Solicita el número de programadores.
    columnas = int(input("Ingresa el número de tareas: "))  # Solicita el número de tareas.
    number = 1

    print("\nIntroduce los valores de la matriz de costos/tiempos:")
    matriz = [[None for j in range(columnas)] for i in range(filas)]  # Inicializa una matriz vacía.
    for i in range(filas):  # Solicita los valores fila por fila.
        for j in range(columnas):
            matriz[i][j] = int(input(f"Introduce el valor para el programador {i + 1}, tarea {j + 1} (valor número {number}): "))
            number += 1

    print("\nMatriz de costos/tiempos ingresada:")
    for fila in matriz:
        print(fila)  # Imprime la matriz ingresada.

    print("\n¿Deseas optimizar por costo o tiempo?")
    optimizar_por = input("Escribe 'costo' o 'tiempo': ").strip().lower()  # Solicita el criterio de optimización.

    print("\n¿Deseas resolver con o sin la librería munkres?")
    metodo_resolucion = input("Escribe 'munkres' o 'manual': ").strip().lower()  # Solicita el método de resolución.

    # Crea una instancia de la clase y ejecuta el método seleccionado.
    asignador = AsignacionTareas(matriz, optimizar_por)
    asignador.ejecutar(metodo_resolucion)
