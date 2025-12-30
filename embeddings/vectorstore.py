from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pinecone import Pinecone
from dotenv import load_dotenv
from schema.schema_models import SplitDoc
import uuid
import os

load_dotenv()

def namespace_creation():
    return str(uuid.uuid4())

unique_namespace=namespace_creation()


index_name='pinecone-database-index'
pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index=pc.Index(index_name)

splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vectorstore(namespace : str):
    
    return PineconeVectorStore(
            embedding=embedding_model,
            index=index,
            namespace=namespace
        )


async def split_store_documents(loaded_docs : SplitDoc) :

    try:
        vectorstore = get_vectorstore(unique_namespace)
        
        vectorstore.add_documents(loaded_docs, show_progress=True)
        
        return JSONResponse(status_code=200, content={"message": "Documents processed and stored successfully."})
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error storing documents in Pinecone: {str(e)}")
        
        # Return error response
        raise HTTPException(
            status_code=500,
            detail=f"Failed to store documents in the database: {str(e)}"
        )
        
        
async def namespace_deletion():
    namespaces = index.list_namespaces()
    if unique_namespace in namespaces:
        await index.delete(delete_all=True, namespace=unique_namespace)
    else:
        print(f"Namespace {unique_namespace} doesn't exist, skipping")
