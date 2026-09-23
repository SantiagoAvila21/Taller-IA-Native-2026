# Taller Práctico: AI-Native Software Engineer

## Descripción

En este taller se debe utilizar un asistente o agente de Inteligencia Artificial como parte del proceso de desarrollo de software.

La actividad no consiste simplemente en pedirle a una IA que “haga el programa”. El objetivo es aplicar un flujo de trabajo **AI-Native**, donde el desarrollador:

```text
comprende → proporciona contexto → solicita → verifica → prueba → corrige → documenta
```

El estudiante recibirá un código con errores y deberá utilizar IA para analizarlo, corregirlo, mejorar su calidad y comprobar que la solución funciona.

- **Lenguaje:** Python
- **Herramientas sugeridas:** Visual Studio Code, Git y un asistente de programación con IA como GitHub Copilot, ChatGPT, Claude, Gemini, Cursor u otro equivalente.

---

## 1. Propósito del taller

Aplicar los principios de un **AI-Native Software Engineer** mediante el análisis, corrección, refactorización y validación de un programa utilizando herramientas de Inteligencia Artificial.

El estudiante asumirá el papel de AI-Native Software Engineer y deberá demostrar que la IA fue utilizada como apoyo dentro de un proceso de ingeniería, no como simple generador de código.

---

## 2. Objetivos

### Objetivo general

Aplicar los principios de un AI-Native Software Engineer mediante el análisis, corrección, refactorización y validación de un programa utilizando herramientas de Inteligencia Artificial.

### Objetivos específicos

- Utilizar IA como herramienta de apoyo dentro del ciclo de desarrollo de software.
- Aplicar técnicas de **context engineering** para proporcionar información relevante al modelo.
- Diseñar prompts claros, estructurados y orientados a tareas de ingeniería.
- Identificar errores funcionales, de calidad y de seguridad en código existente.
- Crear o mejorar pruebas para validar el comportamiento del programa.

---

## 3. Situación planteada

Una pequeña empresa utiliza un programa en Python para administrar tareas de sus empleados. El programa permite:

- Crear tareas.
- Consultar tareas.
- Marcar tareas como completadas.
- Eliminar tareas.

Sin embargo, el código presenta varios problemas. El equipo de desarrollo solicita realizar una revisión utilizando herramientas de IA y entregar una versión corregida y validada.

El estudiante asumirá el papel de **AI-Native Software Engineer**.

---

## 4. Problemas a investigar

El estudiante deberá analizar el código y descubrir qué aspectos deben mejorarse.

Como mínimo deberán investigarse las siguientes categorías:

### A. Errores funcionales

Determine si las funciones realmente hacen lo que deberían hacer.

Preguntas guía:

- ¿Un usuario puede visualizar tareas de otro usuario?
- ¿Qué ocurre si se introduce un índice inexistente?
- ¿Se puede eliminar una tarea que no pertenece al usuario?

### B. Seguridad

Determine si existen problemas relacionados con:

- Control de acceso.
- Validación de entradas.
- Acceso a información de otros usuarios.
- Operaciones no autorizadas.

### C. Testing

Determine qué comportamientos deberían ser comprobados mediante pruebas automáticas.

---

## 5. Actividad 1 — Análisis inicial

Antes de pedirle a la IA que modifique el código, el estudiante deberá realizar un análisis propio.

Elabore una tabla como la siguiente:

| Problema | Tipo | Impacto | Posible solución |
|---|---|---|---|
| El usuario puede ver tareas ajenas | Seguridad | Alto | Filtrar por usuario |
| Índice inexistente genera error | Funcional | Medio | Validar índice |
| ... | ... | ... | ... |

Se deben identificar mínimo **3 problemas**.

---

## 6. Actividad 2 — Aplicación de Context Engineering

No se debe comenzar simplemente con un prompt como:

```text
Corrige este código.
```

En su lugar, el estudiante deberá construir un contexto para la IA.

El contexto deberá contener, como mínimo:

- Objetivo del sistema.
- Código original.
- Requisitos funcionales.
- Restricciones.
- Problemas encontrados.
- Lenguaje utilizado.
- Comportamiento esperado.
- Criterios de calidad.

### Ejemplo de prompt

```text
Actúa como un ingeniero de software senior especializado en Python.

Estamos desarrollando un pequeño sistema de gestión de tareas.

Objetivo:
Permitir que diferentes usuarios creen, consulten, completen y eliminen sus propias tareas.

Restricciones:
- Mantener Python.
- No utilizar bases de datos externas.
- No agregar frameworks.
- Mantener una solución sencilla.
- Evitar modificar innecesariamente la estructura.

Requisitos:
1. Cada tarea pertenece a un usuario.
2. Un usuario solo puede consultar sus tareas.
3. Un usuario solo puede modificar sus tareas.
4. Deben manejarse índices inválidos.
5. Las entradas del usuario deben validarse.
6. El programa no debe finalizar inesperadamente ante entradas incorrectas.

Analiza primero el código.
No generes todavía la solución final.
Primero identifica problemas funcionales, de seguridad, calidad y testing.
```

El estudiante deberá adaptar y mejorar este prompt.

La respuesta deberá contener:

- Problemas encontrados.
- Explicación de cada problema.
- Nivel de prioridad.
- Recomendación de solución.

### Evidencia requerida

Incluya en el documento:

- **Pantallazo 1:** Prompt utilizado.
- **Pantallazo 2:** Respuesta de la IA.

---

## 7. Actividad 3 — Generación de la solución

Después del análisis, solicite a la IA una propuesta de código corregido.

El prompt deberá exigir:

- Mantener las funcionalidades existentes.
- Corregir los errores identificados.
- Respetar el usuario propietario de cada tarea.
- Mejorar la estructura del código.
- Incorporar mensajes de error apropiados.
- Evitar cambios que no sean necesarios.

La IA deberá entregar una nueva versión de:

```text
task_manager_ai_native.py
```

---

## 8. Actividad 4 — Revisión humana

El código generado por la IA no debe aceptarse automáticamente.

El estudiante deberá revisar manualmente la solución y responder:

1. ¿La IA corrigió todos los problemas identificados?
2. ¿Introdujo algún problema nuevo?
3. ¿La solución es entendible?
4. ¿Se mantienen las funcionalidades originales?
5. ¿Existen problemas de seguridad?
6. ¿Qué parte de la solución fue modificada por el estudiante?

El estudiante deberá marcar en el código al menos una decisión realizada personalmente.

Ejemplo:

```python
# DECISIÓN DEL DESARROLLADOR:
# Se utiliza una función independiente para validar el índice
```

---

## 9. Actividad 5 — Testing con IA

Solicite a la IA crear pruebas para verificar el programa.

Como mínimo deberán probarse:

- Creación de una tarea.
- Listado de tareas.
- Restricción por usuario.
- Completar una tarea.
- Eliminar una tarea.
- Índice inválido.
- Usuario inexistente.
- Entrada incorrecta.
- Intento de modificar una tarea de otro usuario.

El estudiante deberá crear un archivo:

```text
test_task_manager.py
```

Puede utilizar `pytest` o cualquier otro mecanismo sencillo de pruebas.

---

## 10. Actividad 6 — Ejecución y verificación

Ejecute el programa y las pruebas.

El objetivo es demostrar que la solución funciona realmente, no solamente que la IA afirmó que funciona.

El estudiante deberá obtener evidencia de:

- Ejecución correcta.
- Pruebas realizadas.
- Resultados.
- Corrección de errores encontrados.

---

## 11. Producto final solicitado

La entrega deberá contener dos elementos principales.

### A. Código

Entregar:

```text
task_manager.py
test_task_manager.py
```

En caso de utilizar otros archivos, deberán incluirse también.

El código debe:

- Ejecutarse correctamente.
- Mantener una estructura clara.
- Contener las correcciones realizadas.
- Incluir las pruebas desarrolladas.

### B. Documento de evidencias

Entregar un documento en PDF o Word con la siguiente estructura:

1. **Análisis inicial**  
   Presentar los problemas encontrados en el código original.

2. **Uso de Inteligencia Artificial**  
   Indicar:
   - Herramienta utilizada.
   - Cómo se utilizó.
   - Qué tareas realizó la IA.
   - Qué decisiones fueron tomadas por el estudiante.

3. **Prompts utilizados**  
   Presentar los principales prompts utilizados durante el proceso. Como mínimo:
   - Prompt de análisis.
   - Prompt de generación/corrección.
   - Prompt de testing.

4. **Evidencias**  
   Incluir pantallazos de:
   - Código original.
   - Prompt inicial.
   - Respuesta de la IA.
   - Código corregido.
   - Ejecución del programa.
   - Ejecución de pruebas.
   - Resultado final.

5. **Código final**  
   Incluir el enlace al repositorio.

6. **Comparación**  
   Mostrar las diferencias principales entre la versión inicial y final.

7. **Reflexión**  
   Responder las siguientes preguntas:
   1. ¿Qué parte fue realizada por el estudiante?
   2. ¿La primera respuesta de la IA fue correcta?
   3. ¿Por qué es necesario validar el código producido por una IA?
   4. ¿Qué ventaja tuvo proporcionar contexto detallado?
   5. ¿Qué diferencia encontró entre utilizar IA como generador de código y utilizarla como parte de un proceso de ingeniería?

---

## 12. Reglas del taller

Para que la actividad realmente evalúe el enfoque AI-Native, deben cumplirse las siguientes condiciones:

### Regla 1 — La IA está permitida

Se permite utilizar cualquier asistente de programación con IA.

### Regla 2 — No se acepta únicamente el resultado final

La evaluación tendrá en cuenta el proceso. Por esta razón, deben presentarse los prompts y las evidencias de las iteraciones.

### Regla 3 — La solución debe ser verificada

No es suficiente indicar:

```text
La IA confirmó que el código funciona.
```

El estudiante debe ejecutar el programa y las pruebas.

### Regla 5 — Debe existir intervención humana

La entrega deberá indicar claramente al menos una decisión realizada por el estudiante después de recibir recomendaciones de la IA.

---

## 13. Nivel de exigencia adicional — Opcional

Para estudiantes que quieran profundizar, se puede agregar una de las siguientes extensiones:

### Opción A — Git

Crear un repositorio Git y registrar:

```text
commit 1 → código original
commit 2 → primera corrección
commit 3 → pruebas
commit 4 → corrección final
```

### Opción B — Mejora arquitectónica

Transformar el programa de un único archivo en una estructura como:

```text
task_manager_ai_native/
│
├── main.py
├── models.py
├── services.py
├── validators.py
└── tests/
```

La IA puede utilizarse para proponer la arquitectura, pero el estudiante debe justificar la decisión.

---

## Estructura sugerida del repositorio

```text
task_manager_ai_native/
│
├── task_manager_ai_native.py
├── test_task_manager.py
├── README.md
├── evidencias/
│   ├── codigo_original.png
│   ├── prompt_inicial.png
│   ├── respuesta_ia.png
│   ├── codigo_corregido.png
│   ├── ejecucion_programa.png
│   └── ejecucion_pruebas.png
└── docs/
    └── documento_evidencias.pdf
```

---

## Cómo ejecutar

Ejecutar la aplicación:

```bash
python task_manager_ai_native.py
```

Ejecutar las pruebas:

```bash
pytest -q
```

o, si se usa `unittest`:

```bash
python -m unittest test_task_manager.py
```

---

## Evidencias requeridas

Incluir en el repositorio o en el documento de evidencias:

- Código original.
- Prompt inicial.
- Respuesta de la IA.
- Código corregido.
- Ejecución del programa.
- Ejecución de pruebas.
- Resultado final.
- Enlace al repositorio.

---

## Reflexión

1. ¿Qué parte fue realizada por el estudiante?
2. ¿La primera respuesta de la IA fue correcta?
3. ¿Por qué es necesario validar el código producido por una IA?
4. ¿Qué ventaja tuvo proporcionar contexto detallado?
5. ¿Qué diferencia encontró entre utilizar IA como generador de código y utilizarla como parte de un proceso de ingeniería?

---

## Enlaces

- Repositorio base del taller: https://github.com/AndUm423/Taller-AI-Native
