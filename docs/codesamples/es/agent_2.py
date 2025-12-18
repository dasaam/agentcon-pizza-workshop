import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from dotenv import load_dotenv

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="mi-agente"
)
print(f"Agente creado, ID: {agent.id}")

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
            agent_id=agent.id
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