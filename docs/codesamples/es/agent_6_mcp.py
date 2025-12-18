import os
import time
from typing import Any
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from azure.ai.agents.models import McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler 
from tools import calculate_pizza_for_people
from dotenv import load_dotenv

load_dotenv(override=True)

# Creando el AIProjectClient
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

# Crear la herramienta file_search
vector_store_id = "<INSERTA EL ID DEL VECTOR STORE COPIADO>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Crear la herramienta de función
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Agregar herramienta MCP para que el agente pueda llamar a microservicios de Contoso Pizza
mcp_tool = McpTool(
    server_label="contoso_pizza",
    server_url="https://ca-pizza-mcp-sc6u2typoxngc.graypond-9d6dd29c.eastus2.azurecontainerapps.io/sse",
    allowed_tools=[],
)
mcp_tool.set_approval_mode("never")

# Creando el toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
toolset.add(mcp_tool)

# Habilitar llamadas automáticas de funciones para este toolset para que el agente pueda llamar funciones directamente
project_client.agents.enable_auto_function_calls(toolset)

# RunHandler personalizado para aprobar llamadas a herramientas MCP
class MyRunHandler(RunHandler):
    def submit_mcp_tool_approval(
        self, *, run: ThreadRun, tool_call: RequiredMcpToolCall, **kwargs: Any
    ) -> ToolApproval:
        print(f"[RunHandler] Aprobando llamada a herramienta MCP: {tool_call.id} para la herramienta: {tool_call.name}")
        return ToolApproval(
            tool_call_id=tool_call.id,
            approve=True,
            headers=mcp_tool.headers,
        )

# Creando el agente
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instrucciones.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Agregar el toolset al agente
)
print(f"Agente creado, ID: {agent.id}")

# Creando el hilo
thread = project_client.agents.threads.create()
print(f"Hilo creado, ID: {thread.id}")
try:
    while True:
        # Obtener la entrada del usuario
        user_input = input("Tú: ")
        # Salir del loop
        if user_input.lower() in ["salir", "terminar"]:
            break

        # Agregar un mensaje al hilo
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=user_input
        )

        # Procesar la ejecución del agente
        run = project_client.agents.runs.create_and_process(  
            thread_id=thread.id, 
            agent_id=agent.id,
            run_handler=MyRunHandler() ## Run handler personalizado
        )

        # Listar mensajes e imprimir la primera respuesta de texto del agente
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)
        if first_message:
            print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), "")) 

finally:
    # Limpiar el agente al terminar
    project_client.agents.delete_agent(agent.id)
    print("Agente eliminado.")