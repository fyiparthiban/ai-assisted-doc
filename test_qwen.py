import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=10
    )
    print("qwen/qwen3-32b works!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error with qwen/qwen3-32b: {e}")
