from langchain_core.documents import Document
from schema.schema_models import FilePath
from typing import List,Dict,Any
from langchain_unstructured import UnstructuredLoader
from dotenv import load_dotenv
import os

load_dotenv()

async def load_document(file_path : FilePath) -> List[Document]:
    
    
    
    try:
        
        def clean_metadata_for_pinecone(metadata: Dict[str, Any]) -> Dict[str, Any]:
            """Clean metadata to be Pinecone compatible."""
            
            cleaned = {}
            
            for key, value in metadata.items():
                # Skip coordinates field entirely as it's problematic for Pinecone
                if key == "coordinates":
                    continue
                    
                # Pinecone accepts: str, int, float, bool, list of strings
                if isinstance(value, (str, int, float, bool, dict, list)):
                    cleaned[key] = value
                elif value is None:
                    cleaned[key] = ""
                else:
                    # Convert any other type to string
                    cleaned[key] = str(value)
            
            return cleaned

        loader = UnstructuredLoader(
            file_path=file_path,
            mode="elements",
            chunking_strategy="by_title",
            max_characters=4000
            )

        loaded = loader.lazy_load()
        loaded_docs=[]
        
        for doc in loaded:
            loaded_docs.append(doc)
        
        for doc in loaded_docs:
            doc.metadata = clean_metadata_for_pinecone(doc.metadata)

        return loaded_docs


    except Exception as e:
        print(f"Error loading document {file_path}: {str(e)}")
        raise
    
    finally:
            
        if file_path and os.path.exists(file_path):
            
            try:
                os.remove(file_path)
            except PermissionError:
                print(f"Warning: Could not delete {file_path}")
