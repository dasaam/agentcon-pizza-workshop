# Llamado de Herramientas – Haciendo que Tu Agente Actúe

En los capítulos anteriores diste instrucciones a tu agente y lo fundamentaste en tus propios datos con Búsqueda de Archivos (RAG).  

Ahora, vamos a permitir que tu agente **tome acciones** llamando **herramientas** — funciones pequeñas y bien definidas que tu agente puede invocar para realizar tareas (por ejemplo, cálculos, búsquedas, llamadas API).

## ¿Qué Son las Herramientas (Llamado de Funciones)?

Las **herramientas** permiten que tu agente llame a *tu código* con entradas estructuradas.  
Cuando un usuario pregunta algo que coincide con el propósito de una herramienta, el agente seleccionará esa herramienta, pasará argumentos validados y usará el resultado de la herramienta para crear una respuesta final.

### Por qué esto importa
- **Acciones determinísticas:** delega trabajo preciso (matemáticas, búsquedas, llamadas API) a tu código.  
- **Seguridad y control:** tú defines qué puede hacer el agente.  
- **Mejor UX:** el agente puede proporcionar respuestas concretas y accionables.



## Agregar la herramienta de Calculadora de Tamaño de Pizza

Agregaremos una herramienta que, dado un **tamaño de grupo** y un **nivel de apetito**, recomienda cuántas pizzas y de qué tamaño ordenar.

### 1) Crear `tools.py` (nuevo archivo)

```python
<!--@include: ../codesamples/tools.py-->
```

::: info
Esta función no necesita importaciones; usa solo componentes integrados de Python.
:::


### 2) Importar la función en `agent.py`

Agrega la importación junto con tus otras importaciones:

```python
from tools import calculate_pizza_for_people
```

Tus importaciones deberían verse así:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```



### 3) Exponer la función como una herramienta

Crea un `FunctionTool` sembrado con la(s) función(es) de Python que el agente puede llamar:

```python
# Create a FunctionTool for the calculate_pizza_for_people function
function_tool = FunctionTool(functions={calculate_pizza_for_people})
```

Inserta este bloque **inmediatamente después** de tu configuración de Búsqueda de Archivos y creación del conjunto de herramientas, así:

**Existente**
```python
# Create the file_search tool
vector_store_id = "<INSERT COPIED VECTOR STORE ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
```

**Nuevo**
```python
# Create the file_search tool
vector_store_id = "<INSERT COPIED VECTOR STORE ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create the function tool
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
```


### 4) Habilitar el llamado automático de funciones (opcional, si es compatible)

Justo después de crear tu conjunto de herramientas, habilita el llamado automático de funciones para que el agente pueda invocar herramientas sin que enrutes las llamadas manualmente:

```python
toolset.add(function_tool)

# Enable automatic function calling for this toolset so the agent can call functions directly
project_client.agents.enable_auto_function_calls(toolset)
```

## Probándolo

Ejecuta tu agente y haz una pregunta que debería activar la herramienta:

```
Somos 7 personas con mucho apetito. ¿Qué pizzas deberíamos ordenar?
```

El agente debería llamar a `calculate_pizza_for_people` y responder con la recomendación que retorna.



## Consejos y Mejores Prácticas

- **Esquema primero:** si tu SDK admite esquemas de argumentos, define tipos/enumeraciones/campos requeridos claros.  
- **Valida entradas:** la herramienta debe manejar datos malos o faltantes con gracia.  
- **Herramientas de un solo propósito:** las herramientas pequeñas y enfocadas son más fáciles de elegir y combinar para el agente.  
- **Explicabilidad:** nombra/describe herramientas para que el agente sepa cuándo usarlas.



## Resumen

En este capítulo tú:
- Creaste una **calculadora de pizzas** en un `tools.py` separado.  
- La expusiste como una **herramienta de función** que el agente puede llamar.  
- La agregaste a tu **ToolSet** existente (junto con Búsqueda de Archivos).  
- (Opcionalmente) habilitaste el **llamado automático de funciones**.  
- Verificaste el llamado de herramientas consultando a tu agente.



## Muestra de código final

```python 
<!--@include: ../codesamples/agent_5_tools.py-->
```

*Traducido usando GitHub Copilot.*
