# solucion_practica.py

import json
import struct
import base64

from autoevaluador import autoevaluador
from generador_inversor import generar_datos_inversor

# =================================================================
# SOLUCIÓN DEL EJERCICIO
# =================================================================

# 1. Obtén los datos del inversor
(device_id, timestamp, status_code, lecturas) = generar_datos_inversor()

# TODO: Serializa los datos en formato JSON

# Descomenta la siguiente línea para autoevaluar tu solución
# Cambia mensaje_final_bytes por el identificador que hayas usado
# autoevaluador(mensaje_final_bytes, device_id, timestamp, status_code, lecturas)
