import json
import base64
import struct
import math

TAM_MAX_MENSAJE = 300  # bytes
NUM_FLOATS = 6
TAM_FLOAT = 4  # bytes (float32)
TAM_BYTES_PAYLOAD = NUM_FLOATS * TAM_FLOAT


def autoevaluador(mensaje_final_bytes: bytes, device_id: str, timestamp: int, status_code: int, lecturas: list[float]):

    print("\n--- VERIFICANDO LA SOLUCIÓN (MODELO SERVIDOR) ---")
    print(f"Mensaje final: {mensaje_final_bytes}")
    tamano_final = len(mensaje_final_bytes)
    print(f"Tamaño final del mensaje: {tamano_final} bytes")

    if tamano_final > TAM_MAX_MENSAJE:
        print(f"❌ ERROR: El mensaje supera el límite de {TAM_MAX_MENSAJE} bytes.")
    else:
        print("✅ OK: El mensaje cumple con la restricción de tamaño.")

    try:
        # 1. El servidor decodifica el mensaje y lo carga como JSON
        msg_decodificado = mensaje_final_bytes.decode('utf-8')
        datos_recibidos: dict[str, str | float | int] = json.loads(msg_decodificado)

        # 2. El servidor comprueba la estructura básica
        assert isinstance(datos_recibidos, dict), "El JSON no es un diccionario."
        assert len(datos_recibidos) == 4, f"Se esperaban 4 elementos, se recibieron {len(datos_recibidos)}."

        # 3. El servidor identifica el payload por eliminación.
        #    Extrae los metadatos conocidos y lo que queda DEBE ser el payload.
        valores = list(datos_recibidos.values())

        # Buscamos y removemos los metadatos que esperamos encontrar
        assert device_id in valores, "El ID del dispositivo no se encontró."
        valores.remove(device_id)

        assert timestamp in valores, "El timestamp no se encontró."
        valores.remove(timestamp)

        assert status_code in valores, "El código de estado no se encontró."
        valores.remove(status_code)

        # Lo que queda en la lista debe ser el payload
        assert len(valores) == 1, "No se pudo identificar un único payload."
        payload_str_recibido = valores[0]

        # 4. El servidor procesa el payload identificado
        assert isinstance(payload_str_recibido, str), "El payload identificado no es un string."

        # a) Decodifica de Base64. Esto fallará si el string no es Base64 válido.
        bytes_recuperados = base64.b64decode(payload_str_recibido)

        # b) Desempaqueta los bytes usando el formato de la especificación.
        assert len(
            bytes_recuperados) == TAM_BYTES_PAYLOAD, f"El payload binario debería tener {TAM_BYTES_PAYLOAD} bytes ({NUM_FLOATS} floats * {TAM_FLOAT} bytes/float), pero tiene {len(bytes_recuperados)}."
        lecturas_recuperadas_tupla = struct.unpack(f"!{NUM_FLOATS}f", bytes_recuperados)
        lecturas_recuperadas = list(lecturas_recuperadas_tupla)

        # 5. Comparación final de los datos numéricos (¡manejando la imprecisión!)
        #    No podemos hacer `assert lecturas == lecturas_recuperadas` por la pérdida
        #    de precisión de float64 a float32. Comparamos con una tolerancia.
        assert len(lecturas) == len(lecturas_recuperadas), "Número incorrecto de lecturas recuperadas."
        for original, recuperado in zip(lecturas, lecturas_recuperadas):
            assert math.isclose(original, recuperado, rel_tol=1e-6), \
                f"La lectura recuperada {recuperado} no es suficientemente cercana a la original {original}."

        print("✅ OK: El formato del mensaje es correcto y TODOS los datos se recuperaron con éxito.")
        print(f"Lecturas recuperadas: {[round(x, 2) for x in lecturas_recuperadas]}")

    except Exception as e:
        print(f"❌ ERROR: El mensaje no se pudo procesar correctamente. Causa: {e}")
