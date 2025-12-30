from pydantic import BaseModel,Field
from langchain_core.documents import Document
from typing import Annotated,List
from langchain_core.messages import BaseMessage
from pathlib import Path

class ChatRequest(BaseModel):
    query: Annotated[ str , Field(...,description="query of the user")]
    
class SplitDoc(BaseModel):
    doc : Annotated[ List[Document] , Field(...,description="The list of loaded documents")]
    
class FilePath(BaseModel):
    path : Annotated[ Path , Field(...,description="Path of the file that is stored")]
    
class ChatHist(BaseModel):
    chat_history : Annotated[ List[BaseMessage] , Field(...,description="Chat history of the user per session")]