# Agregar Instrucciones al Agente  

En el capítulo anterior, creaste tu primer agente básico e iniciaste una conversación con él.  
Ahora, daremos un paso más al aprender sobre **prompts del sistema** y por qué son esenciales para dar forma al comportamiento de tu agente.  


## ¿Qué es un Prompt del Sistema?  

Un prompt del sistema es un conjunto de **instrucciones** que proporcionas al modelo al crear un agente.  
Piensa en él como la **personalidad y el libro de reglas** para tu agente: define cómo debe responder el agente, qué tono debe usar y qué limitaciones debe seguir.  

Sin un prompt del sistema, tu agente puede responder de manera genérica. Al agregar instrucciones claras, puedes adaptarlo a tus necesidades.  

### Los prompts del sistema:  

- Aseguran que el agente se mantenga **consistente** a través de las conversaciones  
- Ayudan a guiar el **tono y rol** del agente (por ejemplo, maestro amigable, revisor de código estricto, bot de soporte técnico)  
- Reducen el riesgo de que el agente dé **respuestas irrelevantes o fuera de tema**  
- Te permiten **codificar reglas** que el agente debe seguir (por ejemplo, "siempre responde en JSON")  


## Agregar Instrucciones a Tu Agente  

Al crear un agente, puedes pasar el parámetro `instructions`.  
Aquí hay un ejemplo:  

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="You are a helpful support assistant for Microsoft Foundry. Always provide concise, step-by-step answers."
)
print(f"Created agent with system prompt, ID: {agent.id}")
```

Ahora, cada vez que el agente procese una conversación, intentará seguir tus **instrucciones del sistema**.  


## Usar un Archivo de Instrucciones Externo  

En lugar de codificar las instrucciones en tu script de Python, a menudo es mejor almacenarlas en un **archivo de texto separado**.  
Esto hace que sean más fáciles de editar y mantener.  

Primero, crea un archivo llamado **`instructions.txt`** en la carpeta workshop con el siguiente contenido:  

```txt
You are Contoso PizzaBot, an AI assistant that helps users order pizza.

Your primary role is to assist users in ordering pizza, checking menus, and tracking order status.

## guidelines
When interacting with users, follow these guidelines:
1. Be friendly, helpful, and concise in your responses.
1. When users want to order pizza, make sure to gather all necessary information (pizza type, options).
1. Contoso Pizza has stores in multiple locations. Before making an order, check to see if the user has specified the store to order from. 
   If they have not, assume they are ordering from the San Francisco, USA store.
1. Your tools will provide prices in USD. 
   When providing prices to the user, convert to the currency appropriate to the store the user is ordering from.
1. Your tools will provide pickup times in UTC. 
   When providing pickup times to the user, convert to the time zone appropriate to the store the user is ordering from.
1. When users ask about the menu, provide the available options clearly. List at most 5 menu entries at a time, and ask the user if they'd like to hear more.
1. If users ask about order status, help them check using their order ID.
1. If you're uncertain about any information, ask clarifying questions.
1. Always confirm orders before placing them to ensure accuracy.
1. Do not talk about anything else then Pizza
1. If you do not have a UserId and Name, always start with requesting that.

## Tools & Data Access
- Use the **Contoso Pizza Store Information Vector Store** to search get information about stores, like address and opening times.
    - **Tool:** `file_search`
    - Only return information found in the vector store or uploaded files.
    - If the information is ambiguous or not found, ask the user for clarification.

## Response
You will interact with users primarily through voice, so your responses should be natural, short and conversational. 
1. **Only use plain text**
2. No emoticons, No markup, No markdown, No html, only plain text.
3. Use short and conversational language.

When customers ask about how much pizza they need for a group, use the pizza calculator function to provide helpful recommendations based on the number of people and their appetite level.
```


## Modificar el Código del Agente  

Ahora, actualiza tu `agent.py` para cargar estas instrucciones y establecer parámetros de generación (`top_p` y `temperature`):  

Encuentra el código 

```
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent"
)
print(f"Created agent, ID: {agent.id}")
```

Reemplaza este código con 

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
)
print(f"Created agent with system prompt, ID: {agent.id}")
```

Al hacer esto:  
- El agente **seguirá las instrucciones de PizzaBot** de tu `instructions.txt`.  
- Los parámetros `top_p` y `temperature` te dan control sobre la **creatividad y aleatoriedad** en las respuestas.  


## Ejecutar el Agente  

Prueba el Agente:  

```shell
python agent.py
```

Intenta modificar tu `instructions.txt` y vuelve a ejecutar el agente. Verás cómo las instrucciones del sistema influyen directamente en la personalidad y el comportamiento del agente.  

Ahora puedes chatear con tu agente directamente en el terminal. Escribe `exit` o `quit` para detener la conversación.  


## Resumen  

En este capítulo, has:  

- Aprendido qué es un **prompt del sistema**  
- Comprendido por qué agregar **instrucciones** es importante  
- Creado un agente con un **prompt del sistema personalizado**  
- Usado un **archivo de instrucciones externo (`instructions.txt`)**  
- Experimentado con **configuraciones de generación** (`top_p` y `temperature`)  




## Muestra de código final

```python 
<!--@include: ../codesamples/agent_3_instructions.py-->
```

*Traducido usando GitHub Copilot.*
