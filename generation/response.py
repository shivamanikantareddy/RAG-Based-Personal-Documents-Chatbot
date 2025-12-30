from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from typing import List,Tuple,Dict
from schema.schema_models import ChatHist,ChatRequest
from embeddings.vectorstore import get_vectorstore,unique_namespace

async def response_generation(query : ChatRequest,chat_history : ChatHist) -> str:
    
    vectorstore = get_vectorstore(unique_namespace)
        
    retriever=vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k":7,"lambda_mult":0.4}
    )

    context_chain = retriever | RunnableLambda(lambda docs: "\n\n".join(doc.page_content for doc in docs))
    
    context = context_chain.invoke(query)

    final_template = PromptTemplate(
    template="""
    You are a reliable and precise AI assistant.

    ### CRITICAL RULES (Must Follow Strictly)
    - Use **ONLY** the information provided in the Context section.
    - Do **NOT** use prior knowledge or assumptions.
    - Do **NOT** make up or infer missing details.
    - If the answer is not clearly present in the context, say:
    **"I cannot find the answer in the provided context."**

    ### TASK
    - First understand the user query and respond to it like a human with the relevant data.
    - Answer the user's question accurately using only the provided context.
    - If the context partially answers the question, clearly state what is available and what is missing.
    - If the question is unclear, ask a clarification question **without adding new information**.

    ### CONTEXT
    {context}

    ### CHAT HISTORY (For reference only, do not add new facts)
    {chat_history}

    ### RESPONSE GUIDELINES
    - **Maintain a helpful and conversational tone** while staying factual.
    - Be concise, clear, and factual.
    - Do not repeat the context verbatim unless necessary.
    - If relevant, summarize the information in simple terms.

    ### FINAL ANSWER
    """,
        input_variables=["context", "chat_history"]
    )

    
    llm=HuggingFaceEndpoint(
        model="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation"
    )
    
    model=ChatHuggingFace(llm=llm)
    
    parser=StrOutputParser()
    
    final_chain = final_template | model | parser
    
    response= await final_chain.ainvoke({"context":context,"chat_history":chat_history})
    
    return response


chat_history : ChatHist =[]