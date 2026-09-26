# autoevaluador_etapa1.py
# NO MODIFICAR

import json
import math
import sys

# Garantiza que los emojis (✅ ❌) se muestran correctamente en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NUM_LECTURAS = 6


def autoevaluador_etapa1(
    mensaje_bytes: bytes,
    device_id: str,
    timestamp: int,
    status_code: int,
    lecturas: list[float],
) -> None:
    """
    Verifica que el mensaje construido en la Etapa 1 cumple la especificación.

    Simula el comportamiento del servidor receptor: recibe una secuencia de
    bytes y comprueba que puede reconstruir todos los datos originales.
    """
    print("\n--- VERIFICANDO ETAPA 1 (SIMULACIÓN DEL SERVIDOR) ---")
    print(f"Mensaje recibido (primeros 80 bytes): {mensaje_bytes[:80]} ...")
    tamano = len(mensaje_bytes)
    print(f"Tamaño total del mensaje: {tamano} bytes")
    print()

    try:
        # ── Comprobación 0: tipo del argumento ───────────────────────────────
        assert isinstance(mensaje_bytes, bytes), (
            f"Se esperaba un objeto 'bytes', pero se recibió '{type(mensaje_bytes).__name__}'."
        )

        # ── Comprobación 1: decodificación UTF-8 ──────────────────────────────
        try:
            texto = mensaje_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise AssertionError(
                "Los bytes no son UTF-8 válido. ¿Usaste la codificación correcta?"
            )

        # ── Comprobación 2: es JSON válido ────────────────────────────────────
        try:
            datos: dict = json.loads(texto)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"El texto no es JSON válido: {exc}")

        assert isinstance(datos, dict), (
            "El JSON debe ser un objeto (entre llaves `{}`), no un array ni otro tipo."
        )

        # ── Comprobación 3: número de campos ─────────────────────────────────
        assert len(datos) == 5, (
            f"Se esperaban exactamente 5 campos; el mensaje tiene {len(datos)}."
        )

        # ── Comprobación 4: identificar cada campo por tipo ───────────────────
        valores = list(datos.values())

        # Separamos booleanos PRIMERO (en Python, bool es subclase de int)
        bools    = [v for v in valores if isinstance(v, bool)]
        enteros  = [v for v in valores if isinstance(v, int) and not isinstance(v, bool)]
        cadenas  = [v for v in valores if isinstance(v, str)]
        listas   = [v for v in valores if isinstance(v, list)]
        otros    = [v for v in valores
                    if not isinstance(v, (bool, int, str, list))]

        assert not otros, (
            f"El mensaje contiene valores de tipo inesperado: {otros}. "
            "Revisa que no uses null, objetos anidados ni flotantes en los metadatos."
        )

        # device_id
        assert device_id in cadenas, (
            f"El ID del dispositivo ('{device_id}') no se encontró como string en el mensaje."
        )

        # timestamp
        assert timestamp in enteros, (
            f"El timestamp ({timestamp}) no se encontró como entero en el mensaje."
        )

        # status_code
        assert status_code in enteros, (
            f"El código de estado ({status_code}) no se encontró como entero en el mensaje. "
            "Recuerda que debe ser un número entero JSON, no un string."
        )

        # operational (bool)
        esperado_op = status_code == 2
        assert len(bools) == 1, (
            f"Se esperaba exactamente 1 campo booleano (el estado operativo), "
            f"pero se encontraron {len(bools)}."
        )
        assert bools[0] == esperado_op, (
            f"El campo operativo debería ser {esperado_op} "
            f"(status_code={status_code}), pero es {bools[0]}."
        )

        # lecturas (list)
        assert len(listas) == 1, (
            "Se esperaba exactamente 1 campo de tipo lista (las lecturas de sensores), "
            f"pero se encontraron {len(listas)}."
        )
        lecturas_recv = listas[0]
        assert len(lecturas_recv) == NUM_LECTURAS, (
            f"La lista de lecturas debe tener {NUM_LECTURAS} elementos; "
            f"tiene {len(lecturas_recv)}."
        )
        assert all(isinstance(v, (int, float)) for v in lecturas_recv), (
            "Todos los elementos de la lista de lecturas deben ser números JSON."
        )

        # ── Comprobación 5: precisión de las lecturas ─────────────────────────
        for i, (orig, recv) in enumerate(zip(lecturas, lecturas_recv)):
            assert math.isclose(orig, recv, rel_tol=1e-9), (
                f"Lectura {i} incorrecta: original={orig}, recibido={recv}. "
                "En la Etapa 1 no debe haber pérdida de precisión."
            )

        # ── Resultado ─────────────────────────────────────────────────────────
        print("✅ OK — El mensaje es de tipo 'bytes'.")
        print("✅ OK — Los bytes se decodifican correctamente a texto UTF-8.")
        print("✅ OK — El texto es un objeto JSON válido con 5 campos.")
        print("✅ OK — Tipos correctos: str · int · int · bool · array.")
        print("✅ OK — Las 6 lecturas se recuperan con precisión completa (float64).")
        print(f"\nLecturas recuperadas: {[round(x, 4) for x in lecturas_recv]}")
        print(f"\n💡 Tamaño de este mensaje de texto: {tamano} bytes.")
        print(   "   En la Etapa 2 deberás reducirlo por debajo de 300 bytes.")

    except AssertionError as exc:
        print(f"❌ ERROR de verificación: {exc}")
    except Exception as exc:
        print(f"❌ ERROR inesperado al procesar el mensaje: {exc}")
