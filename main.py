from fastapi import FastAPI,UploadFile,File,HTTPException
from langchain_core.messages import HumanMessage,AIMessage
from fastapi.responses import JSONResponse
from typing import List
from embeddings.vectorstore import split_store_documents,namespace_deletion
from generation.response import response_generation
from embeddings.process_and_load import load_document
from schema.schema_models import ChatRequest
from generation.response import chat_history,response_generation
from pathlib import Path

app = FastAPI(title="Personal Knowledge Assistant API")

MODEL_VERSION="1.0.0"

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    return JSONResponse(status_code=200, content={"message": "Welcome to the Personal Knowledge Assistant!","version": MODEL_VERSION,})

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_status": "loaded",
        "vector_store_status": "connected",
        "version": MODEL_VERSION
    }
    
@app.post("/load_knowledge")
async def knowledge_assistant(files: List[UploadFile] = File(..., description="Knowledge that you want to give to assistant")):

    for file in files:
        
        MAX_SIZE= 1 * 1024 ** 3
        file_size = 0
        chunk_size = 5 * 1024 ** 2  # 5MB
        
        if (UPLOAD_DIR / file.filename).exists():
            raise HTTPException(status_code=400, detail=f"File {file.filename} already exists!")
        
        file_path = UPLOAD_DIR / file.filename

        while chunk := await file.read(chunk_size):
            file_size += len(chunk)
            
            if file_size > MAX_SIZE:
                    raise ValueError("File too large")
        await file.seek(0)
        
        async def process_file(file,file_path,chunk_size=None):
            with open (file_path,"wb") as out_file:
                
                if chunk_size:
                    while chunk:= await file.read(chunk_size):
                        out_file.write(chunk)
                        
                else:
                    out_file.write(await file.read())
                    
            loaded_docs = await load_document(file_path)
            await split_store_documents(loaded_docs)
            
        try:
            if file_size < 50 * 1024**2:
                await process_file(file,file_path)
                
            else:
                await process_file(file,file_path,chunk_size)
                
        finally:
                # Clean up temporary file
                if file_path and file_path.exists(): 
                    file_path.unlink()
    
    return JSONResponse(status_code=200, content={"message": "Files processed and stored successfully."})
    

@app.post('/chat_assistant')
async def chat_interface(request: ChatRequest):
    """
    Endpoint for chatting with the knowledge assistant.
    Takes a user query and returns a response based on the loaded documents.
    """
    query=request.query.strip()
    
    if not query:
        return JSONResponse(
            status_code=400,
            content={"error": "Query cannot be empty"}
        )
    
    try:
        
        if query.lower() in {"quit", "exit", "end"}:
            await namespace_deletion()
            if chat_history:
                chat_history.clear()
            return JSONResponse(status_code=200,content={"message":"Conversation ended. Session cleared."})
        
        chat_history.append(HumanMessage(content=query))
        
        # Generate response using the query
        response = await response_generation(query,chat_history)
        
        chat_history.append(AIMessage(content=response))
        
        print(chat_history)
        
        # Return the response in a structured format
        return JSONResponse(
            status_code=200,
            content={
                "query": query,
                "response": response
            }
        )
        
    except Exception as e:
        # Handle any errors that occur during response generation
        print(str(e))
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "query": query,
                "status": "Error",
                "message": "Failed to generate response. Please try again."
            }
        )
    