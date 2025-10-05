# Práctica: Empaquetado y Serialización de Datos

## Objetivo

Implementar el proceso de empaquetado y serialización de datos de un sensor, cumpliendo con una especificación de formato y una restricción de tamaño.

## Archivos del Proyecto

*   `generador_inversor.py`: **NO MODIFICAR**. Contiene la función `generar_datos_inversor()` que simula el hardware.
*   `autoevaluador.py`: **NO MODIFICAR**. Contiene la función `autoevaluador()` que permite la autoverificación del mensaje
*   `solucion_practica.py`: **TU ARCHIVO DE TRABAJO**. Completa el código en las secciones indicadas.

## Especificación del Mensaje

El script debe generar un mensaje final en formato `bytes` que cumpla las siguientes reglas:

**1. Estructura General:**
*   El mensaje debe ser un objeto JSON.
*   El objeto debe contener **4 pares clave-valor**. Los identificadores de las claves los eliges tú.
*   El objetivo es que el mensaje sea lo más compacto posible.

**2. Contenido de Datos:**
El JSON debe contener la siguiente información, obtenida de `generar_datos_inversor()`:
*   El ID del dispositivo (`string`).
*   El timestamp (`integer`).
*   El código de estado (`integer`).
*   Un payload con las 6 lecturas de sensores (`string`).

**3. Formato del Payload:**
El payload **no** es un JSON de texto. Debe generarse siguiendo estos pasos:
1.  **Empaquetado Binario:** Convertir la lista de 6 `float` a `bytes` usando el módulo `struct`.
*   **Orden de Bytes:** Big-Endian (orden de red).
*   **Tipo de Datos:** 6 flotantes de precisión simple (32-bit).

**5. Restricción Final:**
*   El tamaño total del mensaje final (`bytes`) debe ser **inferior a 300 bytes**.
