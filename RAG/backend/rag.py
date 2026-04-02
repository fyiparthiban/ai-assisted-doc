import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Removed global llm instance to allow dynamic switching

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Global memory vectorstore
vectorstore = None
retriever = None

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
    return splitter.split_documents(documents)

def add_documents_to_db(file_path):
    global vectorstore, retriever
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        loader = PyMuPDFLoader(file_path)
    elif file_ext in ['.docx', '.doc']:
        loader = Docx2txtLoader(file_path)
    elif file_ext in ['.pptx', '.ppt']:
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding='utf-8')
        
    docs = loader.load()
    for doc in docs:
        doc.metadata = {key: str(value) for key, value in doc.metadata.items()}
        
    chunks = split_documents(docs)
    
    if vectorstore is None:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="rag_session"
        )
    else:
        vectorstore.add_documents(chunks)
        
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

def clear_db():
    global vectorstore, retriever
    vectorstore = None
    retriever = None

def corrective_rag(query, history_text, retrieved_docs, model_name):
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Instantiate LLM dynamically
    llm = ChatGroq(model=model_name, temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))
    
    relevance_prompt = ChatPromptTemplate.from_template(
        "Context: {context}\n\n"
        "Question: {query}\n\n"
        "Does the context above contain information relevant to answering the question? "
        "Answer strictly 'YES' or 'NO'."
    )
    
    relevance_response = llm.invoke(
        relevance_prompt.format(context=context, query=query)
    ).content.strip().upper()
    
    if "YES" in relevance_response:
        return retrieved_docs, context, query
        
    # 2. Query rewriting if NO
    rewrite_prompt = ChatPromptTemplate.from_template(
        "You are a search query optimizer. Rewrite the following query to be better for a vector database search, using history for context.\n\n"
        "STRICT RULES:\n"
        "1. Output ONLY the search query string.\n"
        "2. DO NOT answer the question.\n"
        "3. DO NOT add any conversational text (e.g. 'Here is your query').\n\n"
        "History:\n{history}\n\n"
        "Original Query: {query}\n\n"
        "Search Query:"
    )
    new_query = llm.invoke(rewrite_prompt.format(history=history_text, query=query)).content.strip()
    
    # Fetch again with rewritten query
    new_docs = retriever.invoke(new_query)
    new_context = "\n\n".join([doc.page_content for doc in new_docs])
    
    return new_docs, new_context, new_query

def get_answer(query, chat_history, model_name="llama-3.1-8b-instant"):
    global retriever
    # Skip RAG for simple greetings
    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if query.lower().strip().rstrip('?') in greetings:
        return "Hello! I'm ready to help you with your documents. What would you like to know?", []

    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        
    if retriever is None:
        # Fallback to general knowledge if no documents are uploaded
        final_docs = []
        context = "No documents uploaded. Answer using your internal knowledge."
        final_query = query
    else:
        retrieved_docs = retriever.invoke(query)
        # Corrective RAG
        final_docs, context, final_query = corrective_rag(query, history_text, retrieved_docs, model_name)
    
    # Generation
    llm = ChatGroq(model=model_name, temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant.
        
        Sourcing Rules:
        1. IF the answer can be found in the provided 'Context', answer using ONLY that context. 
        2. IF the answer is NOT in the context, use your general AI knowledge, but YOU MUST START your answer with the exact tag: [INTERNAL_KNOWLEDGE]
        3. Never cite a document source if the information came from your internal knowledge.

        Conversation History:
        {history}

        Context:
        {context}

        Question:
        {question}
        """
    )
    
    formatted_prompt = prompt.format(
        history=history_text,
        context=context,
        question=final_query
    )
    
    raw_response = llm.invoke(formatted_prompt).content
    
    if "[INTERNAL_KNOWLEDGE]" in raw_response:
        response = raw_response.replace("[INTERNAL_KNOWLEDGE]", "").strip()
        sources = ["Internet / General Knowledge"]
    else:
        response = raw_response
        sources = list(set([doc.metadata.get("source") for doc in final_docs]))
    
    return response, sources
