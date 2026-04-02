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

results = []
results.append(f"Question: {question}\n")

for label, model_id in models_from_code.items():
    try:
        llm = ChatGroq(model=model_id, temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))
        response = llm.invoke(question)
        content = response.content
        # Remove reasoning if present for clarity
        if "</think>" in content:
            content = content.split("</think>")[-1].strip()
        results.append(f"{label} Answer: {content}\n")
    except Exception as e:
        results.append(f"{label} Error: {str(e)}\n")

with open("results.txt", "w", encoding="utf-8") as f:
    f.writelines(results)
