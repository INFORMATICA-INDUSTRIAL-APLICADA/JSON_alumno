# autoevaluador_etapa2.py
# NO MODIFICAR

import json
import base64
import struct
import math
import sys

# Garantiza que los emojis (✅ ❌) se muestran correctamente en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TAM_MAX_MENSAJE = 300   # bytes
NUM_FLOATS      = 6
TAM_FLOAT       = 4     # bytes  (float32 / precisión simple)
TAM_PAYLOAD_BIN = NUM_FLOATS * TAM_FLOAT


def autoevaluador_etapa2(
    mensaje_bytes: bytes,
    device_id: str,
    timestamp: int,
    status_code: int,
    lecturas: list[float],
) -> None:
    """
    Verifica que el mensaje construido en la Etapa 2 cumple la especificación.

    Simula el comportamiento del servidor receptor: recibe una secuencia de
    bytes y comprueba que puede reconstruir todos los datos originales a partir
    de un payload binario empaquetado y codificado en Base64.
    """
    print("\n--- VERIFICANDO ETAPA 2 (SIMULACIÓN DEL SERVIDOR) ---")
    print(f"Mensaje recibido: {mensaje_bytes}")
    tamano = len(mensaje_bytes)
    print(f"Tamaño total del mensaje: {tamano} bytes")

    if tamano > TAM_MAX_MENSAJE:
        print(f"❌ RESTRICCIÓN DE TAMAÑO: el mensaje supera el límite de {TAM_MAX_MENSAJE} bytes.")
    else:
        print(f"✅ OK — Tamaño {tamano} B ≤ {TAM_MAX_MENSAJE} B.")

    try:
        # ── Comprobación 0: tipo del argumento ───────────────────────────────
        assert isinstance(mensaje_bytes, bytes), (
            f"Se esperaba 'bytes', se recibió '{type(mensaje_bytes).__name__}'."
        )

        # ── Comprobación 1: decodificación UTF-8 ─────────────────────────────
        try:
            texto = mensaje_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise AssertionError(
                "Los bytes no son UTF-8 válido. ¿Usaste la codificación correcta?"
            )

        # ── Comprobación 2: JSON válido ───────────────────────────────────────
        try:
            datos: dict = json.loads(texto)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"El texto no es JSON válido: {exc}")

        assert isinstance(datos, dict), "El JSON debe ser un objeto `{}`."
        assert len(datos) == 4, (
            f"Se esperaban exactamente 4 campos; el mensaje tiene {len(datos)}."
        )

        # ── Comprobación 3: localizar cada campo por eliminación ──────────────
        valores = list(datos.values())

        assert device_id in valores, (
            f"El ID del dispositivo ('{device_id}') no se encontró en el mensaje."
        )
        valores.remove(device_id)

        assert timestamp in valores, (
            f"El timestamp ({timestamp}) no se encontró en el mensaje."
        )
        valores.remove(timestamp)

        assert status_code in valores, (
            f"El código de estado ({status_code}) no se encontró en el mensaje."
        )
        valores.remove(status_code)

        assert len(valores) == 1, "No se pudo aislar un único campo de payload."
        payload_str = valores[0]

        # ── Comprobación 4: el payload es un string Base64 válido ─────────────
        assert isinstance(payload_str, str), (
            f"El payload debe ser un string (str), pero es {type(payload_str).__name__}."
        )

        try:
            payload_bytes = base64.b64decode(payload_str)
        except Exception:
            raise AssertionError(
                "El payload no es una cadena Base64 válida. "
                "¿Aplicaste la codificación Base64 correctamente?"
            )

        # ── Comprobación 5: tamaño del payload binario ────────────────────────
        assert len(payload_bytes) == TAM_PAYLOAD_BIN, (
            f"El payload binario debería tener {TAM_PAYLOAD_BIN} bytes "
            f"({NUM_FLOATS} floats × {TAM_FLOAT} bytes/float), "
            f"pero tiene {len(payload_bytes)}. "
            "Comprueba el tipo de dato usado en el empaquetado (¿float32?)."
        )

        # ── Comprobación 6: desempaquetado y precisión ────────────────────────
        lecturas_recv = list(struct.unpack(f"!{NUM_FLOATS}f", payload_bytes))

        assert len(lecturas_recv) == NUM_FLOATS, (
            f"Se esperaban {NUM_FLOATS} valores; se obtuvieron {len(lecturas_recv)}."
        )

        for i, (orig, recv) in enumerate(zip(lecturas, lecturas_recv)):
            assert math.isclose(orig, recv, rel_tol=1e-6), (
                f"Lectura {i}: original={orig:.4f}, recuperado={recv:.4f}. "
                "La diferencia supera la tolerancia permitida para float32."
            )

        # ── Resultado ─────────────────────────────────────────────────────────
        print("✅ OK — El mensaje es de tipo 'bytes'.")
        print("✅ OK — Los bytes se decodifican correctamente a texto UTF-8.")
        print("✅ OK — El texto es un objeto JSON válido con 4 campos.")
        print("✅ OK — El payload es una cadena Base64 válida.")
        print(f"✅ OK — El payload binario tiene {TAM_PAYLOAD_BIN} bytes "
              f"({NUM_FLOATS} × float32).")
        print("✅ OK — Las 6 lecturas se recuperan dentro de la tolerancia float32.")
        print(f"\nLecturas recuperadas: {[round(x, 4) for x in lecturas_recv]}")

    except AssertionError as exc:
        print(f"❌ ERROR de verificación: {exc}")
    except Exception as exc:
        print(f"❌ ERROR inesperado al procesar el mensaje: {exc}")
