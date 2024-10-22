from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import load_index_from_storage
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

load_dotenv()
# Create a local Qdrant vector store

q_url=os.getenv('QDRANT_URL')
q_api=os.getenv('QDRANT_API_KEY')

client =QdrantClient( 
    url=q_url, 
    api_key=q_api,)

    # path="dataanalyst_agent/qdrant_store") 
image_dir='dataanalyst_agent/data_store/images_data'
# initialize collections
text_store = QdrantVectorStore(
    client=client, collection_name="text_collection"
)
image_store = QdrantVectorStore(
    client=client, collection_name="image_collection"
)

def data_ingestion():

    storage_context = StorageContext.from_defaults(
    vector_store=text_store,
    image_store=image_store
                    )
    # Create the MultiModal index
    documents = SimpleDirectoryReader(image_dir).load_data()
    index = MultiModalVectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        # embed_model=embedding_model,
        # image_embed_model=embedding_model,
    )
    index.storage_context.persist(persist_dir="dataanalyst_agent/qdrant_index")
    
    return index

def query_engine(query_str):

    openai_mm_llm = OpenAIMultiModal(
    model="gpt-4o-mini",
    )
    storage_context = StorageContext.from_defaults(
        vector_store=text_store, image_store=image_store, persist_dir="dataanalyst_agent/qdrant_index"
    )
  
    loaded_index = load_index_from_storage(storage_context)

    query_engine = loaded_index.as_query_engine(
        llm=openai_mm_llm,
        similarity_top_k=20, 
        image_similarity_top_k=5
    )

    response = query_engine.query(query_str)
    print(response)
  
    return response

# data_ingestion()
# query_engine("give me an overview of the points where we're doing worse than in the last reporting period")