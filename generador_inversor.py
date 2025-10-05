# generador_inversor.py

import random
import time


def generar_datos_inversor():
    """
    Simula la lectura de sensores de un inversor fotovoltaico.

    Esta función actúa como un "hardware simulado", proporcionando
    los datos crudos que el alumno debe procesar.

    Devuelve:
        tuple: Una tupla con los siguientes datos de estado:
            - device_id (str): Identificador único del dispositivo.
            - timestamp (int): Timestamp actual en formato UNIX (entero).
            - status_code (int): 0=OFF, 1=STANDBY, 2=OPERANDO, 3=FALLO.
            - lecturas (list of float): Lista con 6 mediciones de sensores.
    """
    # Identificador único del dispositivo
    device_id = "INV-2024-A7B4"

    # Timestamp actual en formato UNIX (entero), ideal para sistemas embebidos
    timestamp = int(time.time())

    # Estado operativo: 0=OFF, 1=STANDBY, 2=OPERANDO, 3=FALLO
    status_code = random.choice([1, 2, 2, 2, 2, 2, 3])  # Hacemos que "OPERANDO" sea más probable

    # Lecturas de sensores (6 valores flotantes)
    dc_voltage = round(random.uniform(380.0, 450.0), 2)
    dc_current = round(random.uniform(8.0, 10.5), 2)
    # Potencia AC simulada con una eficiencia del 95%
    ac_power = dc_voltage * dc_current * 0.95
    ac_frequency = round(random.uniform(49.9, 50.1), 2)
    temperature = round(random.uniform(45.0, 65.0), 2)
    efficiency = round(random.uniform(0.94, 0.96), 2)

    lecturas = [dc_voltage, dc_current, ac_power, ac_frequency, temperature, efficiency]

    return (device_id, timestamp, status_code, lecturas)


# Este bloque permite ejecutar el fichero directamente para ver un ejemplo
if __name__ == "__main__":
    datos_crudos = generar_datos_inversor()
    print("--- Ejemplo de datos generados por el sensor ---")
    print(f"ID Dispositivo: {datos_crudos[0]}")
    print(f"Timestamp UNIX: {datos_crudos[1]}")
    print(f"Código de Estado: {datos_crudos[2]}")
    print(f"Lecturas (V, A, W, Hz, °C, %): {[round(v, 2) for v in datos_crudos[3]]}")
