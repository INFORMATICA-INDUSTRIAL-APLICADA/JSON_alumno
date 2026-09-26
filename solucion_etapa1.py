# solucion_etapa1.py
# TU ARCHIVO DE TRABAJO — ETAPA 1: El mensaje de texto

import json
from autoevaluador_etapa1 import autoevaluador_etapa1
from generador_inversor import generar_datos_inversor


# =================================================================
# ETAPA 1 — OBJETIVO
# Construir un mensaje que represente el estado del inversor y que:
#   1. Sea un objeto JSON válido con exactamente 5 campos.
#   2. Incluya TODOS los tipos de datos del estándar JSON que se listan
#      en la especificación de abajo.
#   3. Pueda enviarse por la red (= debe ser una secuencia de bytes).
#   4. Sea recuperable en el receptor sin pérdida de información.
# =================================================================


# ── PASO 1: Adquisición de datos ─────────────────────────────────────────────
# Obtén los cuatro valores del inversor simulado.
(device_id, timestamp, status_code, lecturas) = generar_datos_inversor()


# ── PASO 2: Derivar el estado operativo ──────────────────────────────────────
# El inversor se considera "en operación" únicamente cuando su
# código de estado es 2. Calcula este campo como un valor lógico
# de verdadero/falso.
#
# TODO ▼

# operational = ...


# ── PASO 3: Construir la estructura del mensaje ───────────────────────────────
# Crea un diccionario Python con exactamente 5 campos que contengan:
#
#   Campo              Tipo JSON resultante    Descripción
#   ─────────────────  ─────────────────────   ────────────────────────────────
#   ID del dispositivo   cadena de texto       Identificador único del inversor
#   Timestamp            número entero         Instante de la medición (UNIX)
#   Código de estado     número entero         Código operativo del dispositivo
#   Estado operativo     booleano              true / false (del Paso 2)
#   Lecturas             array de números      Los 6 valores de los sensores
#
# ► Elige nombres de clave tan cortos como sea posible para minimizar el
#   tamaño del mensaje final; son tus identificadores propios.
# ► Las lecturas deben ser una lista Python de números (no texto).
#
# TODO ▼

# mensaje_dict = { ... }


# ── PASO 4: Serializar al formato de intercambio ─────────────────────────────
# Convierte el diccionario a una cadena de texto que siga el estándar JSON.
# ► El resultado debe ser un objeto 'str' de Python.
# ► El objetivo es que el mensaje sea lo más compacto posible;
#   consulta los parámetros disponibles en la documentación del módulo.
#
# Módulo que debes usar: json
#
# TODO ▼

# json_str = ...


# ── PASO 5: Codificar a bytes para la red ────────────────────────────────────
# Para poder "enviar" el mensaje, la cadena de texto debe transformarse en
# una secuencia de bytes. La codificación acordada entre emisor y receptor
# es UTF-8.
# ► El resultado debe ser un objeto 'bytes' de Python.
# ► Guarda el resultado en la variable 'mensaje_etapa1_bytes'.
#
# TODO ▼

# mensaje_etapa1_bytes = ...


# ── PASO 6 (RECEPTOR): Reconstruir los datos originales ──────────────────────
# Asume ahora el rol del servidor que acaba de recibir 'mensaje_etapa1_bytes'.
# Debes demostrar que los datos originales son recuperables aplicando
# las operaciones INVERSAS a las de los pasos 4 y 5, en orden inverso.
#
# a) Transforma los bytes recibidos de vuelta a una cadena de texto.
# b) Convierte esa cadena a una estructura de datos Python (diccionario).
# c) Imprime cada campo recuperado con una etiqueta descriptiva.
#
# TODO ▼

print("=== DATOS RECUPERADOS EN EL RECEPTOR ===")
# texto_recibido = ...
# datos_recuperados = ...
# print(f"ID:          {datos_recuperados[...]}")
# print(f"Timestamp:   {datos_recuperados[...]}")
# ...


# =================================================================
# AUTOEVALUACIÓN
# Cuando todos los pasos estén completos, descomenta la línea de abajo.
# =================================================================
# autoevaluador_etapa1(mensaje_etapa1_bytes, device_id, timestamp, status_code, lecturas)
