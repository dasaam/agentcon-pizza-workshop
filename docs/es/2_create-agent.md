# Crea Tu Primer Agente  

En este capítulo, recorreremos el proceso de crear tu primer agente de IA utilizando el **Servicio de Agentes de Microsoft Foundry**.  
Al final, tendrás un agente simple ejecutándose localmente con el que podrás interactuar en tiempo real.  

Primero vuelve al entorno de Github codespace que creaste anteriormente. Asegúrate de que el panel de terminal todavía esté abierto en la carpeta **workshop**.


## Iniciar Sesión en Azure  

Antes de poder usar el Servicio de Agentes de Microsoft Foundry, necesitas iniciar sesión en tu suscripción de Azure.  

Ejecuta el siguiente comando y sigue las instrucciones en pantalla. Usa credenciales que tengan acceso a tu recurso de Microsoft Foundry:  

```shell
az login --use-device-code
```



## Instalar los Paquetes Requeridos  

A continuación, instala los paquetes de Python necesarios para trabajar con Microsoft Foundry y gestionar variables de entorno:  

```shell
pip install azure-identity
pip install azure-ai-projects
pip install azure-ai-agents==1.2.0b5
pip install jsonref
pip install python-dotenv
```


### Crear un Archivo `.env`  

Almacenaremos secretos (como la cadena de conexión de tu proyecto) en un archivo de entorno por seguridad y flexibilidad.  

1. **Crea un archivo llamado `.env` en la raíz del directorio de tu proyecto.**

2. **Agrega la siguiente línea al archivo:**

    ```env
    PROJECT_CONNECTION_STRING="https://<tu-recurso-foundry>.services.ai.azure.com/api/projects/<nombre-tu-proyecto>"
    ```

Reemplaza `https://<tu-recurso-foundry>.services.ai.azure.com/api/projects/<nombre-tu-proyecto>` con los valores reales de tu proyecto de Microsoft Foundry. 

![](/public/foundry/foundry-project-string.png)  


3. **Dónde encontrar tu cadena de conexión:**

   - Ve al **portal de Microsoft Foundry**
   - Navega a tu proyecto
   - Haz clic en **Descripción general**
   - La cadena de conexión se mostrará en la página de inicio de tu proyecto



### 📝 Notas

- Asegúrate de que **no haya espacios** alrededor del signo `=` en el archivo `.env`.



## Crear un Agente Básico  

Ahora crearemos un script básico de Python que define y ejecuta un agente.  

- Comienza creando un nuevo archivo llamado: **`agent.py`** en la carpeta **workshop**



### Agregar Importaciones a `agent.py`  

Estas importaciones traen el SDK de Azure, manejo de entorno y clases auxiliares:  

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from dotenv import load_dotenv
```

### Cargar el Archivo `.env`  

Carga las variables de entorno en tu script agregando esta línea a `agent.py`:  

```python
load_dotenv(override=True)
```



### Crear una Instancia de `AIProjectClient`  

Este cliente conecta tu script al servicio de Microsoft Foundry usando la cadena de conexión y tus credenciales de Azure.  

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```



### Crear el Agente  

Ahora, creemos el agente en sí. En este caso, usará el modelo **GPT-4o**.  

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent"
)
print(f"Created agent, ID: {agent.id}")
```



### Crear un Hilo  

Los agentes interactúan dentro de hilos. Un hilo es como un contenedor de conversación que almacena todos los mensajes intercambiados entre el usuario y el agente.  

```python
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")
```



### Agregar un Mensaje  

Este bucle te permite enviar mensajes al agente. Escribe en el terminal y el mensaje se agregará al hilo.  

```python
try:
    while True:

        # Obtener la entrada del usuario
        user_input = input("You: ")

        # Salir del bucle
        if user_input.lower() in ["exit", "quit"]:
            break

        # Agregar un mensaje al hilo
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER, 
            content=user_input
    )
```



### Crear y Procesar una Ejecución del Agente  

El agente procesa el hilo de conversación y genera una respuesta.  

```python
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=agent.id
        )
```



### Obtener Todos los Mensajes del Hilo  

Esto recupera todos los mensajes del hilo e imprime la respuesta más reciente del agente.  

```python
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None) 
        if first_message: 
            print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), "")) 
```



### Eliminar el Agente Cuando Termines  

Una vez que hayas terminado, limpia eliminando el agente:  

```python
finally:
    # Limpiar el agente cuando termines
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

Agrega este código para eliminar el agente fuera del bucle while True. De lo contrario, el agente se eliminará inmediatamente después de tu primera interacción.



## Ejecutar el Agente  

Finalmente, ejecuta el script de Python:  

```shell
python agent.py
```

Ahora puedes chatear con tu agente directamente en el terminal. Escribe `exit` o `quit` para detener la conversación.  

## Depuración 

Si obtienes un error (el principal `*****-****-***-****-*****`) **no tiene permiso** para crear asistentes en tu proyecto de Microsoft Foundry. Específicamente, le falta la acción de datos **`Microsoft.CognitiveServices/accounts/AIServices/agents/write`**.

Aquí está cómo solucionarlo:

1. **Ve al Portal de Azure**: [https://portal.azure.com](https://portal.azure.com)

2. **Navega a tu recurso de Microsoft Foundry**:
   - Puedes encontrarlo buscando el nombre de tu recurso de Foundry (por ejemplo, `mi-nombre-foundry`).

3. **Abre el panel "Control de acceso (IAM)"**:
   - En el menú de la izquierda del recurso, haz clic en **Control de acceso (IAM)**.

4. **Haz clic en "Agregar asignación de rol"**:
   - Elige **Agregar → Agregar asignación de rol**
   - Selecciona un rol que incluya la acción de datos requerida:
     - Recomendado: **Colaborador de Cognitive Services** o un **rol personalizado** que incluya `Microsoft.CognitiveServices/accounts/AIServices/agents/write`

5. **Asigna el rol a tu principal**:
   - Usa el ID de objeto o nombre del principal: `******-****-***-********`
   - Esto podría ser un principal de servicio, usuario o identidad administrada dependiendo de tu configuración.

6. **Guarda y confirma**:
   - Una vez asignado, espera unos minutos para que el permiso se propague.
   - Vuelve a intentar la operación para crear el asistente.



## Resumen  

En este capítulo, has:  

- Iniciado sesión en Azure  
- Recuperado una cadena de conexión  
- Separado secretos del código usando `.env`  
- Creado un agente básico con el Servicio de Agentes de Microsoft Foundry  
- Iniciado una conversación con un modelo **GPT-4o**  
- Limpiado eliminando el agente cuando terminaste  

*Traducido usando GitHub Copilot.*
