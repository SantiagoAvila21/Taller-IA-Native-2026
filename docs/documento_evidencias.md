# Documento de Evidencias — Taller AI-Native Software Engineer

**Asignatura:** Ingeniería de Software I
**Estudiante:** Santiago Avila
**Repositorio:** https://github.com/SantiagoAvila21/Taller-IA-Native-2026
**Lenguaje:** Python 3
**Herramienta de IA utilizada:** Asistente de programación con IA (opencode) integrado en VS Code

---

## 1. Análisis inicial

El programa original (`task_manager_ai_native.py`) es una aplicación de escritorio con
`tkinter` para administrar tareas de empleados. Permite crear, consultar, completar y
eliminar tareas. Tras la lectura y ejecución del código se identificaron los siguientes
problemas:

| # | Problema | Tipo | Impacto | Posible solución |
|---|---|---|---|---|
| 1 | `list_tasks(user)` ignora el parámetro `user` y devuelve la lista global `tasks`; cualquier usuario ve las tareas de los demás. | Seguridad | Alto | Filtrar por propietario: `[t for t in tasks if t["user"] == user]` |
| 2 | `complete_task` y `delete_task` operan sobre la lista global. Un usuario puede completar o **eliminar tareas ajenas**. | Seguridad / Funcional | Alto | Resolver el índice sobre las tareas del usuario y validar la propiedad antes de operar |
| 3 | `get_index()` ejecuta `int(...)` sin validación. Con el campo vacío o no numérico el callback falla con `ValueError`. | Funcional | Medio | Validar la entrada y lanzar un error controlado con mensaje claro |
| 4 | No se valida el índice (fuera de rango, negativo). `IndexError` no controlado. | Funcional | Medio | Comprobar rango y tipo antes de acceder a la tarea |
| 5 | No se valida el título: se permiten tareas vacías, `None` o de longitud arbitraria. | Validación | Medio | `strip()`, rechazar vacío y limitar longitud |
| 6 | No se valida el usuario. Un usuario inexistente puede operar. | Seguridad / Validación | Medio | Lista blanca `VALID_USERS` |
| 7 | Los índices mostrados en la tabla son posiciones de la lista global, lo que impide un mapeo correcto al filtrar por usuario. | Funcional | Medio | Mapear el índice visible del usuario a la posición real en la lista global |

**Conclusión del análisis:** el defecto más grave es la **fuga de información y el control
de acceso**, porque el sistema no respeta la propiedad de las tareas. En segundo lugar, la
**falta de validación de entradas** provoca fallos no controlados en la interfaz.

---

## 2. Uso de Inteligencia Artificial

- **Herramienta utilizada:** asistente de programación con IA (opencode) dentro de VS Code.
- **Cómo se utilizó:** como apoyo dentro del ciclo de ingeniería
  `comprender → dar contexto → solicitar → verificar → probar → corregir → documentar`.
  La IA no se usó como generador ciego de código, sino para apoyar el análisis, proponer
  correcciones y generar pruebas que luego fueron ejecutadas y revisadas.
- **Tareas realizadas por la IA:**
  - Análisis del código original e identificación de problemas funcionales, de seguridad,
    calidad y testing.
  - Propuesta de refactorización de las funciones de lógica de negocio.
  - Generación de la batería de pruebas con `pytest`.
- **Decisiones tomadas por el estudiante:**
  - Rechazar explícitamente los índices `bool` y negativos (los `bool` son subclase de
    `int` en Python; un índice negativo permitiría accesos confusos). Marcado en el código
    con `# DECISIÓN DEL DESARROLLADOR`.
  - Mantener el nombre original del archivo `task_manager_ai_native.py` para conservar la
    estructura solicitada por el taller.
  - Mantener una única lista global y separar el acceso mediante funciones, **sin** añadir
    bases de datos ni frameworks (respetando las restricciones).
  - Hacer opcional el `import` de `tkinter` para poder importar y probar la lógica en un
    entorno sin interfaz gráfica.
  - Revisar manualmente la solución y ejecutar las pruebas.

---

## 3. Prompts utilizados

### 3.1 Prompt de análisis

```text
Actúa como un ingeniero de software senior especializado en Python.

Estamos desarrollando un pequeño sistema de gestión de tareas en un único archivo
(task_manager_ai_native.py) construido con tkinter. Su objetivo es permitir que
diferentes usuarios creen, consulten, completen y eliminen sus propias tareas.

Restricciones:
- Mantener Python y tkinter.
- No utilizar bases de datos externas.
- No agregar frameworks.
- Mantener una solución sencilla y evitar modificar innecesariamente la estructura.

Analiza primero el código que te adjunto.
No generes todavía la solución final.
Identifica problemas funcionales, de seguridad, de calidad y de testing,
indicando para cada uno: descripción, impacto y prioridad.
```

### 3.2 Prompt de generación / corrección

```text
Con base en el análisis anterior, entrega una nueva versión de
task_manager_ai_native.py que:
- Mantenga todas las funcionalidades existentes.
- Corrija los errores identificados.
- Respete el usuario propietario de cada tarea (listar, completar y eliminar
  solo las tareas propias).
- Maneje índices inválidos y entradas incorrectas sin que el programa falle.
- Incorpore mensajes de error apropiados en la interfaz.
- Evite cambios que no sean necesarios.
Mantén el estilo del código original y comenta las decisiones relevantes.
```

### 3.3 Prompt de testing

```text
Genera un archivo test_task_manager.py usando pytest que cubra como mínimo:
- Creación de una tarea.
- Listado de tareas.
- Restricción por usuario (aislamiento).
- Completar una tarea.
- Eliminar una tarea.
- Índice inválido.
- Usuario inexistente.
- Entrada incorrecta (título vacío / no texto).
- Intento de modificar o eliminar una tarea de otro usuario.
Las pruebas deben aislarse entre sí limpiando el estado global de tareas.
```

---

## 4. Evidencias

> Reemplazar cada marcador por el pantallazo correspondiente antes de exportar a PDF.

| Evidencia | Archivo / acción |
|---|---|
| Código original | `evidencias/codigo_original.png` |
| Prompt inicial | `evidencias/prompt_inicial.png` |
| Respuesta de la IA | `evidencias/respuesta_ia.png` |
| Código corregido | `evidencias/codigo_corregido.png` |
| Ejecución del programa | `evidencias/ejecucion_programa.png` |
| Ejecución de pruebas | `evidencias/ejecucion_pruebas.png` |
| Resultado final | `evidencias/resultado_final.png` |

### Comandos reproducibles

```bash
# Compilar / ejecutar la aplicación
python task_manager_ai_native.py

# Ejecutar las pruebas
pytest -q
```

### Resultado de la ejecución de pruebas

```text
................                                                         [100%]
16 passed in 0.04s
```

### Demostración del aislamiento por usuario

```text
ana ve: ['Informe']
jorge ve: ['Deploy']
ana completa su tarea 0: Tarea completada
jojo -> Índice fuera de rango: 0. El usuario jojo tiene 0 tarea(s).
registro global intacto: [('Informe', 'ana'), ('Deploy', 'jorge')]
```

---

## 5. Código final

- Repositorio: https://github.com/SantiagoAvila21/Taller-IA-Native-2026
- Archivos:
  - `task_manager_ai_native.py` — aplicación corregida.
  - `test_task_manager.py` — pruebas automáticas (16 casos).

---

## 6. Comparación entre la versión inicial y la final

**Resumen:** 140 líneas insertadas, 38 eliminadas en `task_manager_ai_native.py`.

| Aspecto | Versión inicial | Versión final |
|---|---|---|
| `list_tasks(user)` | Devuelve toda la lista global | Filtra por propietario |
| Completar / eliminar tarea ajena | Permitido (opera sobre lista global) | Bloqueado, valida propiedad |
| Índice inválido | `ValueError` / `IndexError` sin control | `TaskError` controlado con mensaje |
| Índice negativo / `bool` | Aceptado | Rechazado explícitamente |
| Título vacío o no texto | Aceptado | Rechazado con validación |
| Usuario inexistente | Sin validar | Lista blanca `VALID_USERS` |
| Manejo de errores en UI | `except Exception` genérico tardío | `TaskError` + mensajes `messagebox` |
| Import de `tkinter` | Obligatorio | Opcional (permite probar sin GUI) |
| Pruebas | No existían | 16 pruebas `pytest` |

### Cambio clave (extracto)

```diff
 def list_tasks(user):
-    return tasks
+    validate_user(user)
+    return [task for task in tasks if task["user"] == user]

 def complete_task(index, user):
-    user_tasks = list_tasks(user)
-    user_tasks[index]["completed"] = True
+    _, task = _resolve_task(index, user)
+    task["completed"] = True
     return "Tarea completada"

 def delete_task(index, user):
-    user_tasks = list_tasks(user)
-    user_tasks.pop(index)
+    position, _ = _resolve_task(index, user)
+    tasks.pop(position)
     return "Tarea eliminada"
```

---

## 7. Reflexión

1. **¿Qué parte fue realizada por el estudiante?**
   El análisis de los problemas, la definición de las restricciones y el contexto para la
   IA, la decisión sobre el rechazo de índices `bool`/negativos, la revisión manual de la
   solución, la ejecución de las pruebas y la verificación del aislamiento por usuario.

2. **¿La primera respuesta de la IA fue correcta?**
   Sirvió como punto de partida, pero no se aceptó automáticamente: fue necesario revisar
   que al filtrar las tareas el índice visible se tradujera correctamente a la posición
   global; de lo contrario, `pop(index)` habría eliminado la tarea equivocada. Esa
   verificación y el manejo de errores se ajustaron manualmente.

3. **¿Por qué es necesario validar el código producido por una IA?**
   Porque la IA puede producir código que "parece correcto" pero introduce fallos sutiles
   (por ejemplo, mezclar el índice de la lista filtrada con la global). Solo la ejecución
   real del programa y de las pruebas demuestra que la solución funciona.

4. **¿Qué ventaja tuvo proporcionar contexto detallado?**
   Permitió obtener una solución alineada con las restricciones (sin frameworks ni base de
   datos, manteniendo la estructura) y centrada en los problemas reales de seguridad, en
   lugar de una reescritura genérica.

5. **¿Qué diferencia encontró entre usar IA como generador de código y como parte de un
   proceso de ingeniería?**
   Usarla como generador produce código sin verificación; usarla dentro de un proceso
   implica analizar, proporcionar contexto, revisar, probar y corregir, lo que permite
   detectar y reparar errores que de otro modo llegarían a producción.
