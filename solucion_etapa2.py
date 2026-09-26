# solucion_etapa2.py
# TU ARCHIVO DE TRABAJO — ETAPA 2: El mensaje compacto

import json
import struct
import base64
from autoevaluador_etapa2 import autoevaluador_etapa2
from generador_inversor import generar_datos_inversor


# =================================================================
# ETAPA 2 — CONTEXTO Y OBJETIVO
#
# En la Etapa 1 enviaste las lecturas como un array JSON de números.
# Ese formato es legible pero verboso: cada número ocupa varios
# caracteres de texto.
#
# En esta etapa reemplazarás ese array por un payload binario compacto,
# reduciendo el tamaño total del mensaje por debajo de 300 bytes.
#
# RESTRICCIÓN OBLIGATORIA: len(mensaje_etapa2_bytes) < 300
#
# ESPECIFICACIÓN DEL MENSAJE (4 campos):
#   Campo              Tipo JSON     Descripción
#   ─────────────────  ────────────  ─────────────────────────────────────────
#   ID del dispositivo   string      Identificador único del inversor
#   Timestamp            number      Instante de la medición (UNIX, entero)
#   Código de estado     number      Código operativo (entero)
#   Payload de lecturas  string      Las 6 lecturas en representación compacta
#
# El campo "Payload de lecturas" es el núcleo de esta etapa:
#   · Los 6 flotantes se empaquetan en binario (ver especificación abajo).
#   · Esos bytes se codifican para poder transportarlos en texto JSON.
#
# ESPECIFICACIÓN DEL PAYLOAD BINARIO:
#   · Tipo de dato de cada lectura : punto flotante de precisión simple (32 bits)
#   · Orden de bytes               : orden de red (big-endian)
#   · Resultado antes de codificar : exactamente 24 bytes
# =================================================================


# ── PASO 1: Adquisición de datos ─────────────────────────────────────────────
(device_id, timestamp, status_code, lecturas) = generar_datos_inversor()


# ── PASO 2: Empaquetar las lecturas en binario ────────────────────────────────
# Convierte la lista 'lecturas' a una secuencia compacta de bytes siguiendo
# la especificación del payload binario descrita arriba.
#
# ► El resultado de esta operación debe ser un objeto 'bytes'.
# ► Consulta la documentación del módulo 'struct': necesitas una función
#   que "empaquete" varios valores en binario dado un código de formato.
# ► El código de formato combina:
#     - Un carácter que indica el orden de bytes.
#     - Un número que indica cuántos valores hay.
#     - Una letra que indica el tipo de dato de cada valor.
#
# Módulo que debes usar: struct
#
# TODO ▼

# payload_bytes = ...


# ── PASO 3: Hacer el payload seguro para texto (JSON) ────────────────────────
# Los bytes del Paso 2 no pueden incluirse directamente en un string JSON:
# podrían contener valores inválidos en UTF-8.
#
# Solución estándar: codificar los bytes en Base64, que produce únicamente
# caracteres ASCII imprimibles.
#
# ► La función de codificación del módulo 'base64' devuelve un tipo concreto.
#   Reflexiona: ¿el módulo 'json' acepta ese tipo como valor de un campo?
#   Si no, ¿qué operación necesitas aplicar para obtener un 'str'?
#
# Módulo que debes usar: base64
#
# TODO ▼

# payload_b64_str = ...


# ── PASO 4: Construir el diccionario del mensaje ──────────────────────────────
# Crea un diccionario con exactamente 4 campos (ver especificación arriba).
# ► Usa las claves más cortas posibles.
#
# TODO ▼

# mensaje_dict = { ... }


# ── PASO 5: Serializar y codificar para la red ───────────────────────────────
# Repite el proceso de los Pasos 4 y 5 de la Etapa 1:
# diccionario → string JSON → bytes UTF-8.
# Guarda el resultado en 'mensaje_etapa2_bytes'.
#
# Módulos que debes usar: json  (y el método de codificación del str)
#
# TODO ▼

# mensaje_etapa2_bytes = ...


# ── PASO 6 (RECEPTOR): Reconstruir las lecturas originales ───────────────────
# Asume el rol del servidor. A partir de 'mensaje_etapa2_bytes' debes
# recuperar los 6 flotantes originales aplicando las operaciones inversas
# EN ORDEN INVERSO al del emisor.
#
# El proceso receptor tiene más pasos que en la Etapa 1:
#   a) bytes  →  string (decodificación UTF-8)
#   b) string →  dict   (deserialización JSON)
#   c) Extraer el campo payload (string Base64).
#   d) string Base64  →  bytes (decodificación Base64)
#   e) bytes binarios →  tupla de floats (desempaquetado)
#   f) Imprimir los valores recuperados con sus unidades.
#
# Módulos que debes usar: json · base64 · struct
#
# TODO ▼

print("=== DATOS RECUPERADOS EN EL RECEPTOR ===")
# ...


# =================================================================
# COMPARATIVA DE TAMAÑOS
# Imprime el tamaño de los mensajes de ambas etapas y calcula
# el porcentaje de reducción obtenido.
# =================================================================
# print(f"\nEtapa 1 (texto):   {len(mensaje_etapa1_bytes)} bytes")  # pega tu variable
# print(f"Etapa 2 (binario): {len(mensaje_etapa2_bytes)} bytes")
# reduccion = (1 - len(mensaje_etapa2_bytes) / len(mensaje_etapa1_bytes)) * 100
# print(f"Reducción:         {reduccion:.1f} %")


# =================================================================
# AUTOEVALUACIÓN
# =================================================================
# autoevaluador_etapa2(mensaje_etapa2_bytes, device_id, timestamp, status_code, lecturas)
