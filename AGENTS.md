# AGENTS.md

## Propósito del proyecto

Este repositorio contiene un programa con interfaz CLI cuyo objetivo es reunir varias herramientas de uso común entre el equipo de desarrollo de un software CAD para el calzado.

Objetivo principal:
- Mantener en ejecución este software mientras los desarrolladores del equipo CAD trabajan para tener acceso rápido a las funcionalidades que ofrece.

El agente debe priorizar:
1. Código correcto y mantenible.
2. Cambios pequeños que sean fáciles de revisar.
3. Respetar la arquitectura existente.
4. Alertar al desarrollador si va a introducir dependencias nuevas y justificar su implementación.

---

## Entorno de trabajo

Editor principal: Visual Studio Code.

Sistema operativo esperado:
- Windows

Lenguaje y stack:
- Lenguaje principal: Python.
- Framework: prompt_toolkit
- Gestor de paquetes: pip

Versiones:
- Python 3.10
- prompt_toolkit 3

## Comandos frecuentes

```bash
[Comando para instalar dependencias]
pip install -r requirements.txt
```

```bash
[Comando para compilar]
create_exe.bat
```

```bash
[Comando para ejecutar el programa]
python main.py
```

## Formato

Mantén el formato de los archivos ya existentes. A destacar las siguientes directrices:
- Debes de usar el formato snake_case para variables y funciones.
- Debes utilizar el formato PascalCase para nombres de clases.
- Utiliza SCREAMING_SNAKE_CASE para constantes.

## Estructura

- assets/: Carpeta que contiene todas las herramientas que habían sido desarrolladas previamente al desarrollo de este programa. Para evitar tener que implementarlas de nuevo.
- build/: Carpeta que contiene archivos de compilación. A destacar que el exe resultante se guarda en la raíz del proyecto, no en esta carpeta.
- src/: Código fuente principal.
- src/dev_toolkit/cli_menu: Código relacionado con el manejo de la interfaz CLI.
- src/dev_toolkit/config: Código relacionado con la configuración de la aplicación.
- src/dev_toolkit/misc: Código con funciones auxiliares y genéricas.
- src/dev_toolkit/modules: Código de las distintas herramientas que incluye el programa.
- AGENTS.md: Instrucciones para agentes.
- create_exe.bat: Archivo por lotes para facilitar la creación del exe resultante.
- main.py: Punto de entrada al programa.
- main.exe: Resultado de la compilación. Este es el archivo que se compartirá a los usuarios.
- requirements.txt: Documento con un listado de dependencias de python.

Reglas de estructura:
- Deberás consultar siempre si el desarrollador está de acuerdo con la creación de un nuevo archivo o carpeta. No lo hagas de forma autónoma, prioriza la utilización de las carpetas existentes si se ajusta a dicha funcionalidad.
- Mantén la separación lógica entre la interfaz CLI y las herramientas.

## Convenciones de código

Normas generales:
- Usar siempre nombres descriptivos.
- Utiliza comillas simples siempre que sea posible.
- Separa los operadores con un espacio antes y después.
- Todo el código debe de estar en inglés, incluidos los comentarios.

## Reglas para el agente

Antes de modificar código:
- Revisa los archivos relacionados con la tarea.
- Entiende los patrones ya existentes antes de proporcionar cambios.
- Trata de modificar lo mínimo posible la arquitectura ya existente.

Durante la modificación:
- Haz cambios mínimos, enfocados y refactorizados.
- No reescribas archivos completos si no es necesario.
- Si has añadido dependencias, añádelas también a la lista de requirements.txt.
  
Después de modificar el código:
- Ejecutar build.

## Estilo de respuesta del agente

Responder en español.

En cada respuesta técnica:
- Explicar brevemente el cambio.
- Listar archivos modificados.
- Indicar comandos ejecutados.
- Avisar si algo no pudo verificarse.

Evitar:
- Respuestas demasiado largas si no es necesario.
- Cambios no solicitados.

## Criterios de finalización

Una tarea se considera terminada cuando:
- El código compila.
- El agente entrega un resumen claro de las modificaciones llevadas a cabo.