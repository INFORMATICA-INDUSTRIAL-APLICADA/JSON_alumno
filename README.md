# Práctica: Serialización de Datos Industriales

## Contexto

Un inversor fotovoltaico debe enviar periódicamente su estado a un servidor central.
La información incluye un identificador de dispositivo, una marca de tiempo, un código
de estado y seis lecturas de sensores (tensión CC, corriente CC, potencia CA,
frecuencia, temperatura y eficiencia).

Para que este mensaje pueda viajar por la red, debe seguir un formato estándar y
convertirse en una secuencia de bytes. Esta práctica recorre ese proceso en dos etapas
de dificultad creciente.

---

## Archivos del proyecto

| Archivo | Rol |
|---|---|
| `generador_inversor.py` | **NO MODIFICAR.** Simula el hardware; devuelve los datos crudos del inversor. |
| `autoevaluador_etapa1.py` | **NO MODIFICAR.** Verifica automáticamente la solución de la Etapa 1. |
| `autoevaluador_etapa2.py` | **NO MODIFICAR.** Verifica automáticamente la solución de la Etapa 2. |
| `solucion_etapa1.py` | ✏️ **Tu archivo de trabajo** para la Etapa 1. |
| `solucion_etapa2.py` | ✏️ **Tu archivo de trabajo** para la Etapa 2. |

---

## Etapa 1 — El mensaje de texto

### Objetivo

Construir un mensaje JSON completo que represente el estado del inversor y demostrar
que puede ser recuperado sin pérdida de información en el lado receptor.

### Especificación del mensaje

El mensaje debe ser un **objeto JSON** con exactamente **5 campos**:

| Campo | Tipo JSON | Origen |
|---|---|---|
| Identificador del dispositivo | cadena de texto | `generar_datos_inversor()` |
| Marca de tiempo | número entero | `generar_datos_inversor()` |
| Código de estado | número entero | `generar_datos_inversor()` |
| Estado operativo | **booleano** | Derivado: `true` si código == 2, `false` en otro caso |
| Lecturas de sensores | **array** de 6 números | `generar_datos_inversor()` |

> **Sobre los nombres de clave:** son de libre elección. Cuanto más cortos,
> más compacto será el mensaje.

### Lo que debes implementar

El archivo `solucion_etapa1.py` te guía paso a paso con comentarios. En resumen:

1. **Emisor:** construye el diccionario, conviértelo al formato de intercambio de datos
   estándar y después transfórmalo en la secuencia de bytes que viajaría por la red.
   El resultado final debe ser de tipo `bytes`.

2. **Receptor:** a partir de esos bytes, recupera el diccionario original e imprime
   todos los campos. Este paso es tan importante como el primero: demuestra que el
   proceso es reversible.

### Autoevaluación

Cuando hayas completado ambos lados (emisor y receptor), descomenta la llamada al
autoevaluador al final del archivo. Comprueba que todos los indicadores aparecen
con ✅.

Al terminar, fíjate en el tamaño que reporta el autoevaluador: lo necesitarás
como referencia en la Etapa 2.

---

## Etapa 2 — El mensaje compacto

### Objetivo

Reducir el tamaño del mensaje reemplazando el array de lecturas por una
representación binaria compacta. El mensaje final **debe ocupar menos de 300 bytes**.

### ¿Por qué el array de texto es ineficiente?

Cada número de coma flotante ocupa en texto entre 4 y 10 caracteres (por ejemplo,
`412.75` son 6 bytes de texto). En cambio, en su representación binaria nativa,
un flotante de precisión simple ocupa siempre exactamente **4 bytes**,
independientemente de su valor.

### Especificación del mensaje

El mensaje sigue siendo un **objeto JSON**, pero ahora con **4 campos**:

| Campo | Tipo JSON | Descripción |
|---|---|---|
| Identificador del dispositivo | cadena de texto | Sin cambios respecto a la Etapa 1 |
| Marca de tiempo | número entero | Sin cambios |
| Código de estado | número entero | Sin cambios |
| Payload de lecturas | **cadena de texto** | Las lecturas empaquetadas en binario y convertidas a texto seguro |

### Especificación del payload

El campo de payload se construye en dos fases:

**Fase A — Empaquetado binario:**
Convierte las 6 lecturas a una secuencia de bytes siguiendo estas reglas:
- Tipo de dato por lectura: punto flotante de **precisión simple** (32 bits).
- Orden de bytes: **orden de red** (*big-endian*).
- Resultado esperado: exactamente **24 bytes**.

**Fase B — Adaptación al texto:**
Los bytes del Paso A no pueden incluirse directamente en un JSON porque podrían
contener valores que rompen la codificación de texto. Debes convertirlos a una
cadena de texto mediante un esquema de codificación binario-a-texto estándar.
Esta codificación introduce un sobrecoste de aproximadamente un 33 % respecto
al tamaño binario, pero garantiza que el resultado es texto ASCII puro.

### Lo que debes implementar

El archivo `solucion_etapa2.py` te guía paso a paso. Los módulos Python que
necesitarás son: `json`, `struct` y `base64`. Consulta su documentación oficial.

Al implementar el lado receptor, presta especial atención al orden de las
operaciones: el proceso de reconstrucción es el inverso exacto del de construcción.

### Autoevaluación y comparativa

Descomenta la llamada al autoevaluador al final del archivo. Una vez superada,
calcula el porcentaje de reducción de tamaño respecto al mensaje de la Etapa 1.

---

## Restricciones generales

- No modifiques los archivos marcados como **NO MODIFICAR**.
- No importes bibliotecas externas (solo las de la biblioteca estándar de Python).
- El resultado final de cada etapa debe ser de tipo `bytes`.
