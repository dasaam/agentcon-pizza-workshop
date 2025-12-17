# Integración de MCP (Model Context Protocol)

En capítulos anteriores, tu agente aprendió a seguir instrucciones, fundamentarse en tus propios datos usando **Búsqueda de Archivos (RAG)**, y llamar **herramientas** personalizadas.  

En este capítulo final, conectaremos tu agente a un **servidor MCP** en vivo — dándole acceso a **capacidades externas** como menús en vivo, ingredientes y gestión de pedidos a través de un protocolo estándar y seguro.


## ¿Qué es MCP y Por Qué Usarlo?

**MCP (Model Context Protocol)** es un estándar abierto para conectar agentes de IA a herramientas externas, fuentes de datos y servicios a través de **servidores MCP** interoperables.  
En lugar de integrarte con APIs individuales, te conectas una vez a un servidor MCP y automáticamente obtienes acceso a todas las herramientas que ese servidor expone.

### Beneficios de MCP

- 🧩 **Interoperabilidad:** una forma universal de exponer herramientas de cualquier servicio a cualquier agente compatible con MCP.  
- 🔐 **Seguridad y gobernanza:** gestiona centralmente el acceso y los permisos de herramientas.  
- ⚙️ **Escalabilidad:** agrega o actualiza herramientas del servidor sin cambiar el código de tu agente.  
- 🧠 **Simplicidad:** mantén las integraciones y la lógica de negocio en el servidor; mantén tu agente enfocado en razonar.


## Instalar el SDK de Agentes de Azure AI (con soporte MCP)

Primero, asegúrate de tener la última versión del SDK que soporta la integración MCP.

```bash
pip install "azure-ai-agents>=1.2.0b5"
```

Luego, actualiza tus importaciones en `agent.py` para incluir clases y utilidades relacionadas con MCP:

```python
from azure.ai.agents.models import McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler
import time
from typing import Any
```

Tu sección de importaciones completa ahora debería verse así:

```python
import os
import time
from typing import Any
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet,
    McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler
)
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```


## El Servidor MCP de Contoso Pizza

Para Contoso Pizza, el servidor MCP expone APIs para:
- 🧀 **Pizzas:** elementos del menú disponibles y precios  
- 🍅 **Ingredientes:** categorías, disponibilidad y detalles  
- 📦 **Pedidos:** crear, ver y cancelar pedidos de clientes  

Conectarás tu agente a este servidor y le otorgarás **permiso explícito** para usar una lista curada de herramientas para estas operaciones.


## Crear y Agregar la Herramienta MCP

Definirás la **Herramienta MCP** justo después de crear tu `ToolSet`, junto con otras herramientas (como Búsqueda de Archivos o la Calculadora de Pizzas).

### Agregar la Herramienta MCP

```python
# Add MCP tool so the agent can call Contoso Pizza microservices
mcp_tool = McpTool(
    server_label="contoso_pizza",
    server_url="<!--@include: ./variables/mcp-url.md-->",
    allowed_tools=[
        "get_pizzas",
        "get_pizza_by_id",
        "get_toppings",
        "get_topping_by_id",
        "get_topping_categories",
        "get_orders",
        "get_order_by_id",
        "place_order",
        "delete_order_by_id",
    ],
)
mcp_tool.set_approval_mode("never")
```

Luego, agrégala al conjunto de herramientas:

```python
toolset.add(mcp_tool)
```

### Parámetros Explicados

| Parámetro | Descripción |
| -- | -- |
| **server_label** | Un nombre legible para registros y depuración. |
| **server_url** | El punto final del servidor MCP. |
| **allowed_tools** | Una lista blanca de herramientas MCP que tu agente puede llamar. |
| **approval_mode** | Define si las llamadas requieren aprobación manual (`"never"` desactiva las solicitudes). |

::: tip
💡 En producción, usa modos de aprobación más restrictivos y acceso a herramientas limitado.
::: 


## Manejo de Aprobaciones de Herramientas

Cuando el agente llama a una herramienta MCP, puedes interceptar y aprobar estas llamadas dinámicamente.  
Esto te da visibilidad y control fino sobre lo que se ejecuta.

Agrega un **manejador de ejecución personalizado**:

```python
# Custom RunHandler to approve MCP tool calls
class MyRunHandler(RunHandler):
    def submit_mcp_tool_approval(
        self, *, run: ThreadRun, tool_call: RequiredMcpToolCall, **kwargs: Any
    ) -> ToolApproval:
        print(f"[RunHandler] Approving MCP tool call: {tool_call.id} for tool: {tool_call.name}")
        return ToolApproval(
            tool_call_id=tool_call.id,
            approve=True,
            headers=mcp_tool.headers,
        )
```

Luego, pasa el manejador al ejecutar el agente:

```python
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
    run_handler=MyRunHandler()  # Enables controlled MCP approvals
)
```

::: tip
🧠 Piensa en esto como un middleware que intercepta todas las llamadas a herramientas remotas para registro, auditoría o reglas de seguridad dinámicas.
:::


## Agregar un ID de Usuario

Para realizar pedidos, el agente debe identificar al cliente.

1. **Obtén tu ID de Usuario**  
   Visita esta URL para registrar un cliente:  
   [<!--@include: ./variables/customer-registration.md-->](<!--@include: ./variables/customer-registration.md-->)  

2. **Actualiza tu `instructions.txt`** con los detalles de tu usuario o pasa el GUID en el chat.

```txt
## User details:
Name: <YOUR NAME>
UserId: <YOUR USER GUID>
```

3. (Opcional) Ve tu panel de pedidos:  
   [<!--@include: ./variables/pizza-dashboard.md-->](<!--@include: ./variables/pizza-dashboard.md-->)



## Probándolo

¡Ahora es el momento de probar tu agente conectado!  
Ejecuta el agente e intenta estos prompts:

```
Muéstrame las pizzas disponibles.
```

```
¿Cuál es el precio de una pizza hawaiana?
```

```
Realiza un pedido de 2 pizzas pepperoni grandes.
```

El agente llamará automáticamente a las herramientas MCP apropiadas, recuperará datos de la API en vivo de Contoso Pizza y responderá conversacionalmente — siguiendo las reglas de tu **instructions.txt** (por ejemplo, tono, moneda local y conversiones de zona horaria).



## Mejores Prácticas para la Integración de MCP

- 🔒 **Principio del mínimo privilegio:** solo permite las herramientas que el agente realmente necesita.  
- 📜 **Observabilidad:** registra todas las llamadas a herramientas para trazabilidad y depuración.  
- 🔁 **Resiliencia:** maneja errores de conexión con gracia y reintenta llamadas a herramientas fallidas.  
- 🧩 **Versionado:** ancla las versiones del servidor MCP para prevenir cambios que rompan la compatibilidad.  
- 👩‍💼 **Humano en el circuito:** usa modos de aprobación para acciones sensibles (como realización de pedidos).



## Resumen

En este capítulo, tú:  
- Aprendiste qué es **MCP** y por qué importa para el diseño escalable de agentes.  
- Instalaste el **SDK de Agentes de Azure AI** actualizado con soporte MCP.  
- Conectaste tu agente al **Servidor MCP de Contoso Pizza**.  
- Implementaste un **manejador de ejecución personalizado** para aprobaciones de herramientas.  
- Probaste la integración en tiempo real con herramientas de menú, ingredientes y pedidos.  



🎉 **¡Felicitaciones — has completado el taller!**  
Tu agente ahora puede:  
✅ Seguir instrucciones del sistema  
✅ Acceder y razonar sobre datos privados (RAG)  
✅ Llamar herramientas personalizadas  
✅ Interactuar con servicios en vivo a través de MCP  

Tu **Contoso PizzaBot** ahora es un asistente de IA totalmente operacional, inteligente y extensible.



## Muestra de código final

```python 
<!--@include: ../codesamples/agent_6_mcp.py-->
```

*Traducido usando GitHub Copilot.*
