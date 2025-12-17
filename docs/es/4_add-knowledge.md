# Agregar Conocimiento con Búsqueda de Archivos  

En los capítulos anteriores, creaste un agente básico y le diste instrucciones a través de un prompt del sistema.  
Ahora es el momento de **hacer que tu agente sea más inteligente** al fundamentarlo en **tus propios datos**.  



## ¿Por Qué Agregar Conocimiento?  

Por defecto, el modelo solo sabe lo que fue entrenado para saber - no tiene acceso a la información privada o específica de dominio de tu organización.  
Para cerrar esta brecha, usaremos **Generación Aumentada por Recuperación (RAG)**.  

- **RAG** permite al agente obtener información relevante de tus propios datos antes de generar una respuesta.  
- Esto asegura que las respuestas de tu agente sean **precisas, actualizadas y fundamentadas** en información real.  
- En Microsoft Foundry, usaremos la función **Búsqueda de Archivos** para implementar esto.  

En este capítulo, usarás una carpeta llamada **`./documents`** que contiene información sobre **tiendas de Contoso Pizza** - como ubicaciones, horarios de apertura y menús.  

Subiremos estos archivos a **Microsoft Foundry**, crearemos un **almacén vectorial** y conectaremos ese almacén al agente usando una **herramienta de Búsqueda de Archivos**.  


## Paso 1 - Crear un Script de Almacén Vectorial  

Construiremos esto paso a paso para asegurarnos de que todo esté claro.  
Tu objetivo: crear un script que suba archivos, cree un almacén vectorial y vectorice tus datos para búsqueda.  

### Parte A - Preparar Tu Entorno  

**Objetivo:** Cargar secretos de `.env` e importar los SDKs necesarios.  

Crea un nuevo archivo llamado **`add_data.py`** y agrega:  

```python
import os
from dotenv import load_dotenv

# Azure SDK imports
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose

# Load environment variables (expects PROJECT_CONNECTION_STRING in .env)
load_dotenv(override=True)
```

**Por qué:**  
- `.env` mantiene tus credenciales separadas del código.  
- `AIProjectClient` te permite interactuar con tu proyecto de Microsoft Foundry.  
- `FilePurpose.AGENTS` le dice al servicio que estos archivos son para agentes.  

### Parte B - Conectar a Tu Proyecto de Microsoft Foundry  

**Objetivo:** Crear el cliente del proyecto usando tu cadena de conexión.  

Agrega esto a tu script:  

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```

**Por qué:**  
Esto conecta tu script a tu proyecto de Microsoft Foundry, permitiendo que las subidas de archivos y la creación de almacenes vectoriales ocurran en tu espacio de trabajo.  


### Parte C - Subir Tus Documentos  

**Objetivo:** Subir archivos desde `./documents` y recopilar sus IDs.  

Agrega esto:  

```python
DOCS_DIR = "./documents"

if not os.path.isdir(DOCS_DIR):
    raise FileNotFoundError(
        f"Documents folder not found at {DOCS_DIR}. "
        "Create it and add your Contoso Pizza files (PDF, TXT, MD, etc.)."
    )

print(f"Uploading files from {DOCS_DIR} ...")
file_ids = []
for fname in os.listdir(DOCS_DIR):
    fpath = os.path.join(DOCS_DIR, fname)
    # skip directories and hidden files like .DS_Store
    if not os.path.isfile(fpath) or fname.startswith('.'):
        continue
    uploaded = project_client.agents.files.upload_and_poll(
        file_path=fpath,
        purpose=FilePurpose.AGENTS
    )
    file_ids.append(uploaded.id)

print(f"Uploaded {len(file_ids)} files.")
if not file_ids:
    raise RuntimeError("No files uploaded. Put files in ./documents and re-run.")
```

**Por qué:**  
Tus documentos deben ser subidos antes de que puedan ser vectorizados y hacerse buscables.  

**Consejo:** Mantén los documentos cortos y relevantes (información de tiendas, horarios, menús). Divide documentos muy grandes cuando sea posible.  


### Parte D - Crear un Almacén Vectorial  

**Objetivo:** Crear un almacén vectorial vacío que almacenará e indexará las incrustaciones de tus documentos.  

Agrega:  

```python
vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Created vector store, ID: {vector_store.id}")
```

**Por qué:**  
Un almacén vectorial es lo que habilita la búsqueda semántica - encuentra texto que *significa* lo mismo que la consulta del usuario, incluso si las palabras difieren.  


### Parte E - Vectorizar Archivos en el Almacén  

**Objetivo:** Agregar tus archivos subidos al almacén vectorial y procesarlos para búsqueda.  

Agrega:  

```python
batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
print(f"Created vector store file batch, ID: {batch.id}")
```

**Por qué:**  
Esto crea incrustaciones vectoriales para tus archivos para que el agente pueda luego recuperar fragmentos relevantes a través de la herramienta de Búsqueda de Archivos.  


### Archivo final
```python
<!--@include: ../codesamples/add_data.py-->
```

### Ejecutar el Script  

Desde tu directorio **`workshop/`**, ejecuta:  

```bash
python add_data.py
```

Salida de ejemplo:  

```
Uploading files from ./documents ...
Uploaded 19 files.
Created vector store, ID: vs_ii6H96sVMeQcXICvj7e3DsrK
Created vector store file batch, ID: vsfb_47c68422adc24e0a915d0d14ca71a3cf
```

✅ **Copia el ID del almacén vectorial** - lo usarás en la siguiente sección.  



## Paso 2 - Agregar la Herramienta de Búsqueda de Archivos  

Ahora que has creado tu almacén vectorial, vamos a conectarlo a tu agente.  

En `agent.py`, justo después de crear tu `AIProjectClient`, agrega:  

```python
# Create the File Search tool
vector_store_id = "<INSERT YOUR VECTOR STORE ID HERE>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])
```

### Agregar la Herramienta a un Conjunto de Herramientas  

```python
# Create the toolset
toolset = ToolSet()
toolset.add(file_search)
```



### Crear el Agente con Conocimiento  

Encuentra el bloque donde creas tu agente y modifícalo para incluir el conjunto de herramientas:  

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Add the toolset to the agent
)
print(f"Created agent, ID: {agent.id}")
```



## Paso 3 - Ejecutar el Agente  

Pruébalo:  

```bash
python agent.py
```

Haz preguntas como:  
> "¿Qué tiendas de Contoso Pizza están abiertas después de las 8pm?"  
> "¿Dónde está la tienda de Contoso Pizza más cercana?"  

Escribe `exit` o `quit` para detener la conversación.  



## Resumen  

En este capítulo, tú:  
- Aprendiste cómo **RAG** fundamenta tu agente con tus propios datos  
- Subiste archivos desde el directorio `./documents`  
- Creaste y poblaste un **almacén vectorial**  
- Agregaste una **herramienta de Búsqueda de Archivos** a tu agente  
- Extendiste tu PizzaBot para responder preguntas sobre **tiendas de Contoso Pizza**  


## Muestra de código final

```python 
<!--@include: ../codesamples/agent_4_rag.py-->
```

*Traducido usando GitHub Copilot.*
