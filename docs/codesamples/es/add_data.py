import os
from dotenv import load_dotenv

# Importaciones del SDK de Azure
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose

# Cargar variables de entorno (espera PROJECT_CONNECTION_STRING en .env)
load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

DOCS_DIR = "../documentos"

if not os.path.isdir(DOCS_DIR):
    raise FileNotFoundError(
        f"Carpeta de documentos no encontrada en {DOCS_DIR}. "
        "Créala y agrega tus archivos de Contoso Pizza (PDF, TXT, MD, etc.)."
    )

print(f"Subiendo archivos desde {DOCS_DIR} ...")
file_ids = []
for fname in os.listdir(DOCS_DIR):
    fpath = os.path.join(DOCS_DIR, fname)
    # omitir directorios y archivos ocultos como .DS_Store
    if not os.path.isfile(fpath) or fname.startswith('.'):
        continue
    uploaded = project_client.agents.files.upload_and_poll(
        file_path=fpath,
        purpose=FilePurpose.AGENTS
    )
    file_ids.append(uploaded.id)

print(f"Se subieron {len(file_ids)} archivos.")
if not file_ids:
    raise RuntimeError("No se subieron archivos. Coloca archivos en ../documentos y vuelve a ejecutar.")


vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="informacion-tiendas-contoso-pizza"
)
print(f"Vector store creado, ID: {vector_store.id}")

batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
print(f"Lote de archivos del vector store creado, ID: {batch.id}")