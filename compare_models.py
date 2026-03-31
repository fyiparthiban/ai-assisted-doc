import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

models_from_code = {
    "⚡ Fast (Llama 8B)": "llama-3.1-8b-instant",
    "🧠 Smart (Llama 70B)": "llama-3.3-70b-versatile",
    "🧬 Advanced (Qwen 32B)": "deepseek-r1-distill-qwen-32b"
}

question = "Explain what a RAG (Retrieval-Augmented Generation) system is in one concise sentence."

print(f"Question: {question}\n")

for label, model_id in models_from_code.items():
    print(f"Testing {label}...")
    try:
        llm = ChatGroq(model=model_id, temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))
        response = llm.invoke(question)
        print(f"Answer: {response.content}\n")
    except Exception as e:
        print(f"Error with {label}: {str(e)}\n")
