import os
from RAG.backend.rag import get_answer, add_documents_to_db, clear_db
from dotenv import load_dotenv

load_dotenv()

# Setup: Add a sample document
with open("test_doc.txt", "w") as f:
    f.write("The secret code for the vault is 998877. This is a highly confidential document.")

clear_db()
add_documents_to_db("test_doc.txt")

tests = [
    {
        "name": "Context Question",
        "query": "What is the secret code for the vault?",
        "expected_source": "test_doc.txt"
    },
    {
        "name": "General Knowledge Question",
        "query": "Which is heavier: a pound of gold or a pound of feathers?",
        "expected_source": "Internet / General Knowledge"
    }
]

print("Starting RAG Verification...\n")

for test in tests:
    print(f"Testing: {test['name']}")
    print(f"Query: {test['query']}")
    answer, sources = get_answer(test['query'], [])
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
    
    found = any(test['expected_source'] in s for s in sources)
    if found:
        print("✅ Result: Correct Sourcing\n")
    else:
        print(f"❌ Result: Incorrect Sourcing (Expected {test['expected_source']})\n")

# Cleanup
if os.path.exists("test_doc.txt"):
    os.remove("test_doc.txt")
